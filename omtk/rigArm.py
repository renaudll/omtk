import pymel.core as pymel
from className import Name
from classModule import Module
from classCtrl import BaseCtrl
from rigIK import IK
from rigFK import FK
from libs import libRigging

class BaseAttHolder(BaseCtrl):
    def __createNode__(self, name=None, *args, **kwargs):
        s1 = 1.0
        s2 = s1 * 0.7
        node = pymel.curve(d=1, p=[(0,0,s1),(0,s2,s2),(0,s1,0),(0,s2,-s2),(0,0,-s1),(0,-s2,-s2),(0,-s1,0),(0,-s2,s2),(0,0,s1),(-s2,0,s2),(-s1,0,0),(-s2,s2,0),(0,s1,0),(s2,s2,0),(s1,0,0),(s2,0,-s2),(0,0,-s1),(-s2,0,-s2),(-s1,0,0),(-s2,-s2,0),(0,-s1,0),(s2,-s2,0),(s1,0,0),(s2,0,s2),(0,0,s1),(-s2,0,s2)], k=range(26), *kwargs)
        if isinstance(name, basestring): node.rename(name)
        node.t.set(channelBox=False)
        node.r.set(channelBox=False)
        node.s.set(channelBox=False)
        return node

class Arm(Module):
    kAttrName_State = 'fkIk' # The name of the IK/FK attribute

    def __init__(self, *args, **kwargs):
        super(Arm, self).__init__(*args, **kwargs)
        self.sysIK = None
        self.sysFK = None
        self.ctrl_elbow = None

    def build(self, *args, **kwargs):
        super(Arm, self).build(*args, **kwargs)

        '''
        # Create ikChain and fkChain
        self._aIkChain = pymel.duplicate(self.input, renameChildren=True, parentOnly=True)
        for oInput, oIk, in zip(self.input, self._aIkChain):
            namemap = Name(oInput, _sType='rig')
            oIk.rename(namemap('ik'))
        self._aIkChain[0].setParent(self._oParent) # Trick the IK system (temporary solution)
        '''

        # Rig ikChain and fkChain
        if not isinstance(self.sysIK, IK):
            self.sysIK = IK(self.input)
        self.sysIK.build(**kwargs)

        if not isinstance(self.sysFK, FK):
            self.sysFK = FK(self.input)
        self.sysFK.build(constraint=False, **kwargs)

        self.sysIK.grp_anm.setParent(self.grp_anm)
        self.sysIK.grp_rig.setParent(self.grp_rig)
        self.sysFK.grp_anm.setParent(self.grp_anm)

        # Create attribute holder (this is where the IK/FK attribute will be stored)
        oAttHolder = BaseAttHolder(name=self._name_anm.resolve('atts'), create=True)
        oAttHolder.setParent(self.grp_anm)
        pymel.parentConstraint(self.input[self.sysIK.iCtrlIndex], oAttHolder.offset)
        pymel.addAttr(oAttHolder, longName=self.kAttrName_State, hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=1, k=True)
        attIkWeight = oAttHolder.attr(self.kAttrName_State)
        attFkWeight = libRigging.create_utility_node('reverse', inputX=attIkWeight).outputX

        # Create a chain for blending ikChain and fkChain
        _chain_blend = pymel.duplicate(self.input, renameChildren=True, parentOnly=True)
        for input_, node in zip(self.input, _chain_blend):
            node.rename(self._name_rig.resolve('blend'))

        # Blend ikChain with fkChain
        for blend, oIk, oFk in zip(_chain_blend, self.sysIK._chain_ik, self.sysFK.ctrls):
            oConstraint = pymel.parentConstraint(oIk, oFk, blend)
            attr_weight_ik, attr_weight_fk = oConstraint.getWeightAliasList()
            pymel.connectAttr(attIkWeight, attr_weight_ik)
            pymel.connectAttr(attFkWeight, attr_weight_fk)
        _chain_blend[0].setParent(self.grp_rig)

        # Connect visibility
        pymel.connectAttr(attIkWeight, self.sysIK.grp_anm.visibility)
        pymel.connectAttr(attFkWeight, self.sysFK.grp_anm.visibility)

        # Create a chain that provide the elbow controller and override the blend chain (wich should only be nodes already)
        _chain_elbow = pymel.duplicate(self.input, renameChildren=True, parentOnly=True)
        for input_, node in zip(self.input, _chain_elbow):
            node.rename(self._name_rig.resolve('elbow')) # todo: find a better name???
        _chain_elbow[0].setParent(self.grp_rig)

        # Create elbow ctrl
        index_elbow = 1
        ctrl_elbow_name = self._name_anm.resolve('elbow')
        ctrl_elbow_parent = _chain_blend[index_elbow]
        if not isinstance(self.ctrl_elbow, BaseCtrl):
            self.ctrl_elbow = BaseCtrl(create_offset=True) # todo: custom RigCtrl implementation?
        self.ctrl_elbow.build()
        self.ctrl_elbow.rename(ctrl_elbow_name)
        self.ctrl_elbow.setParent(self.grp_anm)
        pymel.parentConstraint(ctrl_elbow_parent, self.ctrl_elbow.offset, maintainOffset=False)

        pymel.aimConstraint(self.ctrl_elbow, _chain_elbow[0])
        pymel.aimConstraint(self.sysIK.ctrlIK, _chain_elbow[index_elbow])
        pymel.pointConstraint(self.ctrl_elbow, _chain_elbow[index_elbow], maintainOffset=False)
        pymel.pointConstraint(_chain_blend[-1], _chain_elbow[-1], maintainOffset=False)

        # Constraint elbow setup to input
        for innJnt, ref in zip(self.input, _chain_elbow):
            pymel.parentConstraint(ref, innJnt, maintainOffset=True)

        #self.ctrlIkOffset = self.sysIK.ctrlIK.getMatrix(worldSpace=True) * \
        #                    self.sysFK.ctrls[self.iCtrlIndex].getMatrix(worldSpace=True).inverse()

        self.attState = attIkWeight # Expose state

    def unbuild(self, *args, **kwargs):
        if self.sysIK.is_built():
            self.sysIK.unbuild()
        if self.sysFK.is_built():
            self.sysFK.unbuild()
        #self.sysIK = None # hack
        #self.sysFK = None # hack
        self.attState = None
        super(Arm, self).unbuild(*args, **kwargs)

    #
    # Functions called for IK/FK switch (animation tools)
    #

    def snapIkToFk(self):
        # Position ikCtrl
        ctrl_ik_tm = self.input[self.sysIK.iCtrlIndex].getMatrix(worldSpace=True)
        self.sysIK.ctrlIK.setMatrix(self.ctrlIkOffset * ctrl_ik_tm, worldSpace=True)

        # Position swivel
        pos_ref = self.sysFK.ctrls[self.sysIK.iCtrlIndex - 1].getTranslation(space='world')
        pos_s = self.sysFK.ctrls[0].getTranslation(space='world')
        pos_m = self.sysFK.ctrls[self.sysIK.iCtrlIndex - 1].getTranslation(space='world')
        pos_e = self.sysFK.ctrls[self.sysIK.iCtrlIndex].getTranslation(space='world')
        length_start = pos_m.distanceTo(pos_s)
        length_end = pos_m.distanceTo(pos_e)
        length_ratio = length_start / (length_start+length_end)

        pos_middle = (pos_e-pos_s)*length_ratio + pos_s
        dir_swivel = pos_m - pos_middle
        dir_swivel.normalize()
        pos_swivel = dir_swivel * self.sysIK.swivelDistance + pos_ref
        self.sysIK.ctrlSwivel.setTranslation(pos_swivel, space='world')

    def snapFkToIk(self):
        for ctrl, jnt in zip(self.sysFK.ctrls, self.input):
            ctrl.setMatrix(jnt.getMatrix(worldSpace=True), worldSpace=True)

    def switchToIk(self):
        self.snapIkToFk()
        self.attState.set(1.0)

    def switchToFk(self):
        self.snapFkToIk()
        self.attState.set(0.0)


