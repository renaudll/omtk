import pymel.core as pymel
import collections
from omtk.core.classModule import Module
from omtk.core.classCtrl import BaseCtrl
from omtk.core import constants
from omtk.core.utils import decorator_uiexpose
from omtk.modules import rigIK
from omtk.modules import rigFK
from omtk.modules import rigTwistbone
from omtk.libs import libRigging
from omtk.libs import libCtrlShapes
from omtk.libs import libAttr


class BaseAttHolder(BaseCtrl):
    def __createNode__(self, size=None, refs=None, **kwargs):
        # Resolve size automatically if refs are provided.
        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs
        if size is None and ref is not None:
            size = libRigging.get_recommended_ctrl_size(ref)
        else:
            size = 1.0

        node = libCtrlShapes.create_shape_attrholder(size=size, **kwargs)

        # Hide default keyable attributes
        node.t.set(channelBox=False)
        node.r.set(channelBox=False)
        node.s.set(channelBox=False)

        return node


class CtrlElbow(BaseCtrl):
    def __createNode__(self, size=None, refs=None, *args, **kwargs):
        # Resolve size automatically if refs are provided
        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs
        if size is None and ref is not None:
            size = libRigging.get_recommended_ctrl_size(ref) * 1.25
        else:
            size = 1.0

        return libCtrlShapes.create_shape_cross(size=size, **kwargs)


class Limb(Module):
    """
    Generic IK/FK setup. Twistbones are included.
    """
    kAttrName_State = 'fkIk'  # The name of the IK/FK attribute
    _CLASS_SYS_IK = rigIK.IK
    _CLASS_SYS_FK = rigFK.FK
    _CLASS_CTRL_ATTR = BaseAttHolder
    _CLASS_CTRL_ELBOW = CtrlElbow
    _CLASS_SYS_TWIST = rigTwistbone.Twistbone

    def __init__(self, *args, **kwargs):
        super(Limb, self).__init__(*args, **kwargs)
        self.sysIK = None
        self.sysFK = None
        self.sys_twist = []
        self.create_twist = True
        self.ctrl_elbow = None
        self.attState = None
        self.offset_ctrl_ik = None
        self.ctrl_attrs = None
        self.STATE_IK = 1.0
        self.STATE_FK = 0.0

    def build(self, *args, **kwargs):
        super(Limb, self).build(*args, **kwargs)

        nomenclature_anm = self.get_nomenclature_anm()
        nomenclature_rig = self.get_nomenclature_rig()

        # Create IK system
        if not isinstance(self.sysIK, self._CLASS_SYS_IK):
            self.sysIK = self._CLASS_SYS_IK(self.chain_jnt, rig=self.rig)
        self.sysIK.name = '{0}_Ik'.format(self.name) # Hack
        self.sysIK.build(constraint=False, **kwargs)

        # Create FK system
        if not isinstance(self.sysFK, self._CLASS_SYS_FK):
            self.sysFK = self._CLASS_SYS_FK(self.chain_jnt, rig=self.rig)
        self.sysFK.name = '{0}_Fk'.format(self.name) # Hack
        self.sysFK.build(constraint=False, **kwargs)

        # Create twistbone system if needed
        if self.create_twist:
            num_twist_sys = self.sysIK.iCtrlIndex
            # If the IK system is a quad, we need to have two twist system
            for i in range(0, num_twist_sys):
                cur_sys_twist = self.sys_twist[i] if i < len(self.sys_twist) else None
                if not isinstance(cur_sys_twist, self._CLASS_SYS_TWIST):
                    cur_sys_twist = self._CLASS_SYS_TWIST(self.chain_jnt[i:(i+2)], rig=self.rig)
                    self.sys_twist.append(cur_sys_twist)
                # Hack
                twist_sys_name = self.chain_jnt[i].name().replace('_' + nomenclature_rig.type_jnt, "")
                cur_sys_twist.name = '{0}'.format(twist_sys_name)
                cur_sys_twist.build(num_twist=3, create_bend=True, **kwargs)

        # Lock X and Y axis on the elbow/knee ctrl
        if self.rig._up_axis == constants.Axis.y:
            libAttr.lock_hide_rotation(self.sysFK.ctrls[1], z=False)
        elif self.rig._up_axis == constants.Axis.z:
            libAttr.lock_hide_rotation(self.sysFK.ctrls[1], y=False)

        # Store the offset between the ik ctrl and it's joint equivalent.
        # Useful when they don't match for example on a leg setup.
        self.offset_ctrl_ik = self.sysIK.ctrl_ik.getMatrix(worldSpace=True) * self.chain_jnt[self.iCtrlIndex].getMatrix(worldSpace=True).inverse()

        # Add attributes to the attribute holder.
        # Add ikFk state attribute on the grp_rig.
        # This is currently controlled by self.ctrl_attrs.
        pymel.addAttr(self.grp_rig, longName=self.kAttrName_State, hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=1, k=True)
        attr_ik_weight = self.grp_rig.attr(self.kAttrName_State)
        attr_fk_weight = libRigging.create_utility_node('reverse', inputX=attr_ik_weight).outputX

        # Create attribute holder (this is where the IK/FK attribute will be stored)
        # Note that this is production specific and should be defined in a sub-class implementation.
        jnt_hand = self.chain_jnt[self.sysIK.iCtrlIndex]
        ctrl_attrs_name = nomenclature_anm.resolve('atts')
        if not isinstance(self.ctrl_attrs, self._CLASS_CTRL_ATTR):
            self.ctrl_attrs = self._CLASS_CTRL_ATTR()
        self.ctrl_attrs.build(name=ctrl_attrs_name, refs=jnt_hand)
        self.ctrl_attrs.setParent(self.grp_anm)
        pymel.parentConstraint(jnt_hand, self.ctrl_attrs.offset)

        pymel.addAttr(self.ctrl_attrs, longName=self.kAttrName_State, hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=1, k=True)
        pymel.connectAttr(self.ctrl_attrs.attr(self.kAttrName_State), self.grp_rig.attr(self.kAttrName_State))

        # Create a chain for blending ikChain and fkChain
        chain_blend = pymel.duplicate(list(self.chain_jnt), renameChildren=True, parentOnly=True)
        for input_, node in zip(self.chain_jnt, chain_blend):
            blend_nomenclature = nomenclature_rig.rebuild(input_.name())
            node.rename(blend_nomenclature.resolve('blend'))

        # Blend ikChain with fkChain
        constraint_ik_chain = self.sysIK._chain_ik
        if getattr(self.sysIK, '_chain_quad_ik', None):
            constraint_ik_chain = self.sysIK._chain_quad_ik
        for blend, oIk, oFk in zip(chain_blend, constraint_ik_chain, self.sysFK.ctrls):
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
        chain_elbow = pymel.duplicate(self.chain_jnt[:self.sysIK.iCtrlIndex + 1], renameChildren=True, parentOnly=True)
        for input_, node in zip(self.chain_jnt, chain_elbow):
            nomenclature_elbow = nomenclature_rig.rebuild(input_.name())
            node.rename(nomenclature_elbow.resolve('elbow'))  # todo: find a better name???
        chain_elbow[0].setParent(self.grp_rig)

        # Create elbow ctrl
        # Note that this only affect the chain until @iCtrlIndex
        for i in range(1, self.sysIK.iCtrlIndex):
            ctrl_elbow_name = nomenclature_anm.resolve('elbow{:02}'.format(i))
            ctrl_elbow_parent = chain_blend[i]
            if not isinstance(self.ctrl_elbow, self._CLASS_CTRL_ELBOW):
                self.ctrl_elbow = self._CLASS_CTRL_ELBOW(create_offset=True)
            ctrl_elbow_ref = self.chain_jnt[i]  # jnt_elbow
            self.ctrl_elbow.build(refs=ctrl_elbow_ref)
            self.ctrl_elbow.rename(ctrl_elbow_name)
            self.ctrl_elbow.setParent(self.grp_anm)
            pymel.parentConstraint(ctrl_elbow_parent, self.ctrl_elbow.offset, maintainOffset=False)
            pymel.pointConstraint(chain_blend[0], chain_elbow[0], maintainOffset=False)
            pymel.aimConstraint(self.ctrl_elbow, chain_elbow[i-1], worldUpType=2,
                                worldUpObject=chain_blend[i-1])  # Object Rotation Up
            pymel.aimConstraint(chain_blend[i+1], chain_elbow[i], worldUpType=2,
                                worldUpObject=chain_blend[i])  # Object Rotation Up
            pymel.pointConstraint(self.ctrl_elbow, chain_elbow[i], maintainOffset=False)
        # Constraint the last elbow joint on the blend joint at the ctrl index
        pymel.parentConstraint(chain_blend[self.sysIK.iCtrlIndex], chain_elbow[self.sysIK.iCtrlIndex])

        # Constraint input chain
        # Note that we only constraint to the elbow chain until @iCtrlIndex.
        # Afterward we constraint to the blend chain.
        for i in range(self.sysIK.iCtrlIndex):
            inn = self.chain_jnt[i]
            ref = chain_elbow[i]
            pymel.parentConstraint(ref, inn, maintainOffset=True)  # todo: set to maintainOffset=False?
        for i in range(self.sysIK.iCtrlIndex, len(self.chain_jnt)):
            inn = self.chain_jnt[i]
            ref = chain_blend[i]
            pymel.parentConstraint(ref, inn, maintainOffset=True)  # todo: set to maintainOffset=False?

        # Connect visibility
        pymel.connectAttr(attr_ik_weight, self.sysIK.grp_anm.visibility)
        pymel.connectAttr(attr_fk_weight, self.sysFK.grp_anm.visibility)

        # Connect globalScale
        pymel.connectAttr(self.grp_rig.globalScale, self.sysIK.grp_rig.globalScale, force=True)
        self.globalScale = self.grp_rig.globalScale  # Expose the attribute, the rig will reconise it.

        # Parent sub-modules so they are affected by displayLayer assignment and such.
        self.sysIK.grp_anm.setParent(self.grp_anm)
        self.sysIK.grp_rig.setParent(self.grp_rig)
        self.sysFK.grp_anm.setParent(self.grp_anm)
        for sys_twist in self.sys_twist:
            if sys_twist.create_bend:
                sys_twist.grp_anm.setParent(self.grp_anm)
            sys_twist.grp_rig.setParent(self.grp_rig)

        self.attState = attr_ik_weight  # Expose state

    def unbuild(self):
        for twist_sys in self.sys_twist:
            twist_sys.unbuild()
        if self.sysIK and self.sysIK.is_built():
            self.sysIK.unbuild()
        if self.sysFK and self.sysFK.is_built():
            self.sysFK.unbuild()

        super(Limb, self).unbuild()

        self.attState = None

    def parent_to(self, parent):
        # Do nothing as everything is handled by the sysIK and sysFK modules.
        pass

    #
    # Functions called for IK/FK switch (animation tools)
    #

    def snap_ik_to_fk(self):
        # Position ikCtrl
        ctrl_ik_tm = self.chain_jnt[self.sysIK.iCtrlIndex].getMatrix(worldSpace=True)
        self.sysIK.ctrl_ik.node.setMatrix(self.offset_ctrl_ik * ctrl_ik_tm, worldSpace=True)

        # Position swivel
        #pos_ref = self.sysFK.ctrls[self.sysIK.iCtrlIndex - 1].getTranslation(space='world')
        pos_s = self.sysFK.ctrls[0].getTranslation(space='world')
        pos_m = self.sysFK.ctrls[self.sysIK.iCtrlIndex - 1].getTranslation(space='world')
        pos_e = self.sysFK.ctrls[self.sysIK.iCtrlIndex].getTranslation(space='world')

        length_start = pos_m.distanceTo(pos_s)
        length_end = pos_m.distanceTo(pos_e)
        length_ratio = length_start / (length_start + length_end)

        pos_middle = (pos_e - pos_s) * length_ratio + pos_s
        dir_swivel = pos_m - pos_middle
        dir_swivel.normalize()
        pos_swivel = (dir_swivel * self.sysIK.swivelDistance) + pos_middle
        self.sysIK.ctrl_swivel.node.setTranslation(pos_swivel, space='world')

    def snap_fk_to_ik(self):
        for ctrl, jnt in zip(self.sysFK.ctrls, self.chain_jnt):
            ctrl.node.setMatrix(jnt.getMatrix(worldSpace=True), worldSpace=True)

    def switch_to_ik(self):
        self.snap_ik_to_fk()
        attr_state = libAttr.get_settable_attr(self.attState)
        if attr_state:
            attr_state.set(self.STATE_IK)

    def switch_to_fk(self):
        self.snap_fk_to_ik()
        attr_state = libAttr.get_settable_attr(self.attState)
        if attr_state:
            attr_state.set(self.STATE_FK)

    def iter_ctrls(self):
        for ctrl in super(Limb, self).iter_ctrls():
            yield ctrl
        if self.sysIK:
            for ctrl in self.sysIK.iter_ctrls():
                yield ctrl
        if self.sysFK:
            for ctrl in self.sysFK.iter_ctrls():
                yield ctrl
        yield self.ctrl_attrs
        yield self.ctrl_elbow

    @decorator_uiexpose()
    def assign_twist_weights(self):
        for module in self.sys_twist:
            if isinstance(module, rigTwistbone.Twistbone) and module.is_built():
                module.assign_twist_weights()

    @decorator_uiexpose()
    def unassign_twist_weights(self):
        for module in self.sys_twist:
            if isinstance(module, rigTwistbone.Twistbone) and module.is_built():
                module.unassign_twist_weights()

def register_plugin():
    return Limb
