import pymel.core as pymel
from className import Name
from classModule import Module
from classCtrl import BaseCtrl
from rigIK import IK
from rigFK import FK
from libs import libRigging, libCtrlShapes


class BaseAttHolder(BaseCtrl):
    def __createNode__(self, name=None, **kwargs):
        node = libCtrlShapes.create_shape_attrholder(**kwargs)
        if isinstance(name, basestring):
            node.rename(name)
        # Hide default keyable attributes
        node.t.set(channelBox=False)
        node.r.set(channelBox=False)
        node.s.set(channelBox=False)
        return node


class CtrlElbow(BaseCtrl):
    def __createNode__(self, size=1, *args, **kwargs):
        return libCtrlShapes.create_shape_cross(size=size, **kwargs)


class Arm(Module):
    kAttrName_State = 'fkIk'  # The name of the IK/FK attribute

    def __init__(self, *args, **kwargs):
        super(Arm, self).__init__(*args, **kwargs)
        self.sysIK = None
        self.sysFK = None
        self.ctrl_elbow = None
        self.attState = None
        self.offset_ctrl_ik = None

    def _create_sys_ik(self, **kwargs):
        if not isinstance(self.sysIK, IK):
            self.sysIK = IK(self.input)
        self.sysIK.build(constraint=False, **kwargs)

    def _create_sys_fk(self, **kwargs):
        if not isinstance(self.sysFK, FK):
            self.sysFK = FK(self.input)
        self.sysFK.build(constraint=False, **kwargs)

    def build(self, *args, **kwargs):
        super(Arm, self).build(*args, **kwargs)

        # Rig ikChain and fkChain
        self._create_sys_ik()
        self._create_sys_fk()

        # Store the offset between the ik ctrl and it's joint equivalent.
        # Usefull when they don't match for example on a leg setup.
        self.offset_ctrl_ik = self.sysIK.ctrl_ik.getMatrix(worldSpace=True) * self.input[self.iCtrlIndex].getMatrix(worldSpace=True).inverse()

        # Create attribute holder (this is where the IK/FK attribute will be stored)
        jnt_hand = self.input[self.sysIK.iCtrlIndex]
        obj_attr = BaseAttHolder(name=self.name_anm.resolve('atts'), create=True)
        obj_attr.build()
        obj_attr.setParent(self.grp_anm)
        pymel.parentConstraint(jnt_hand, obj_attr.offset)
        pymel.addAttr(obj_attr, longName=self.kAttrName_State, hasMinValue=True, hasMaxValue=True, minValue=0,
                      maxValue=1, defaultValue=1, k=True)
        attr_ik_weight = obj_attr.attr(self.kAttrName_State)
        attr_fk_weight = libRigging.create_utility_node('reverse', inputX=attr_ik_weight).outputX

        # Create a chain for blending ikChain and fkChain
        chain_blend = pymel.duplicate(self.input, renameChildren=True, parentOnly=True)
        for input_, node in zip(self.input, chain_blend):
            node.rename(self.name_rig.resolve('blend'))

        # Blend ikChain with fkChain
        for blend, oIk, oFk in zip(chain_blend, self.sysIK._chain_ik, self.sysFK.ctrls):
            constraint = pymel.parentConstraint(oIk, oFk, blend)
            attr_weight_ik, attr_weight_fk = constraint.getWeightAliasList()
            pymel.connectAttr(attr_ik_weight, attr_weight_ik)
            pymel.connectAttr(attr_fk_weight, attr_weight_fk)
        chain_blend[0].setParent(self.grp_rig)

        #
        # Create elbow chain
        # This provide the elbow ctrl, an animator friendly way of cheating the elbow on top of the blend chain.
        #

        # Create a chain that provide the elbow controller and override the blend chain
        # (witch should only be nodes already)
        chain_elbow = pymel.duplicate(self.input[:self.sysIK.iCtrlIndex], renameChildren=True, parentOnly=True)
        for input_, node in zip(self.input, chain_elbow):
            node.rename(self.name_rig.resolve('elbow'))  # todo: find a better name???
        chain_elbow[0].setParent(self.grp_rig)

        # Create elbow ctrl
        # Note that this only affect the chain until @iCtrlIndex
        index_elbow = 1
        ctrl_elbow_name = self.name_anm.resolve('elbow')
        ctrl_elbow_parent = chain_blend[index_elbow]
        if not isinstance(self.ctrl_elbow, CtrlElbow):
            self.ctrl_elbow = CtrlElbow(create_offset=True)
        ctrl_elbow_size = libRigging.get_recommended_ctrl_size(self.input[self.iCtrlIndex - 1]) * 1.25
        self.ctrl_elbow.build(size=ctrl_elbow_size)
        self.ctrl_elbow.rename(ctrl_elbow_name)
        self.ctrl_elbow.setParent(self.grp_anm)
        pymel.parentConstraint(ctrl_elbow_parent, self.ctrl_elbow.offset, maintainOffset=False)

        pymel.pointConstraint(chain_blend[0], chain_elbow[0], maintainOffset=False)
        pymel.aimConstraint(self.ctrl_elbow, chain_elbow[0], worldUpType=2,
                            worldUpObject=chain_blend[0])  # Object Rotation Up
        pymel.aimConstraint(chain_blend[self.sysIK.iCtrlIndex], chain_elbow[index_elbow], worldUpType=2,
                            worldUpObject=chain_blend[index_elbow])  # Object Rotation Up
        pymel.pointConstraint(self.ctrl_elbow, chain_elbow[index_elbow], maintainOffset=False)

        # Constraint input chain
        # Note that we only constraint to the elbow chain until @iCtrlIndex.
        # Afterward we constraint to the blend chain.
        for i in range(self.sysIK.iCtrlIndex):
            inn = self.input[i]
            ref = chain_elbow[i]
            pymel.parentConstraint(ref, inn, maintainOffset=True)  # todo: set to maintainOffset=False?
        for i in range(self.sysIK.iCtrlIndex, len(self.input)):
            inn = self.input[i]
            ref = chain_blend[i]
            pymel.parentConstraint(ref, inn, maintainOffset=True)  # todo: set to maintainOffset=False?

        # Connect visibility
        pymel.connectAttr(attr_ik_weight, self.sysIK.grp_anm.visibility)
        pymel.connectAttr(attr_fk_weight, self.sysFK.grp_anm.visibility)

        # Connect globalScale
        pymel.connectAttr(self.grp_rig.globalScale, self.sysIK.grp_rig.globalScale, force=True)

        # Parent sub-modules so they are affected by displayLayer assignment and such.
        self.sysIK.grp_anm.setParent(self.grp_anm)
        self.sysIK.grp_rig.setParent(self.grp_rig)
        self.sysFK.grp_anm.setParent(self.grp_anm)

        self.attState = attr_ik_weight  # Expose state

    def unbuild(self):
        if self.sysIK.is_built():
            self.sysIK.unbuild()
        if self.sysFK.is_built():
            self.sysFK.unbuild()

        super(Arm, self).unbuild()

        self.attState = None

    #
    # Functions called for IK/FK switch (animation tools)
    #

    def snap_ik_to_fk(self):
        # Position ikCtrl
        ctrl_ik_tm = self.input[self.sysIK.iCtrlIndex].getMatrix(worldSpace=True)
        self.sysIK.ctrl_ik.node.setMatrix(self.offset_ctrl_ik * ctrl_ik_tm, worldSpace=True)

        # Position swivel
        pos_ref = self.sysFK.ctrls[self.sysIK.iCtrlIndex - 1].getTranslation(space='world')
        pos_s = self.sysFK.ctrls[0].getTranslation(space='world')
        pos_m = self.sysFK.ctrls[self.sysIK.iCtrlIndex - 1].getTranslation(space='world')
        pos_e = self.sysFK.ctrls[self.sysIK.iCtrlIndex].getTranslation(space='world')
        length_start = pos_m.distanceTo(pos_s)
        length_end = pos_m.distanceTo(pos_e)
        length_ratio = length_start / (length_start + length_end)

        pos_middle = (pos_e - pos_s) * length_ratio + pos_s
        dir_swivel = pos_m - pos_middle
        dir_swivel.normalize()
        pos_swivel = dir_swivel * self.sysIK.swivelDistance + pos_ref
        self.sysIK.ctrl_swivel.setTranslation(pos_swivel, space='world')

    def snap_fk_to_ik(self):
        for ctrl, jnt in zip(self.sysFK.ctrls, self.input):
            ctrl.node.setMatrix(jnt.getMatrix(worldSpace=True), worldSpace=True)

    def switch_to_ik(self):
        self.snap_ik_to_fk()
        self.attState.set(1.0)

    def switch_to_fk(self):
        self.snap_fk_to_ik()
        self.attState.set(0.0)
