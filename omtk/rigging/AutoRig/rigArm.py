import pymel.core as pymel
from classNameMap import NameMap
from classRigPart import RigPart
from classRigNode import RigNode
from rigIK import IK
from rigFK import FK
from omtk.libs import libRigging

class RigAttHolder(RigNode):
    def __init__(self, *args, **kwargs):
        super(RigAttHolder, self).__init__(*args, **kwargs)
        self.node.t.set(channelBox=False)
        self.node.r.set(channelBox=False)
        self.node.s.set(channelBox=False)
    def __createNode__(self, name=None, *args, **kwargs):
        s1 = 1.0
        s2 = s1 * 0.7
        n =  pymel.curve(d=1, p=[(0,0,s1),(0,s2,s2),(0,s1,0),(0,s2,-s2),(0,0,-s1),(0,-s2,-s2),(0,-s1,0),(0,-s2,s2),(0,0,s1),(-s2,0,s2),(-s1,0,0),(-s2,s2,0),(0,s1,0),(s2,s2,0),(s1,0,0),(s2,0,-s2),(0,0,-s1),(-s2,0,-s2),(-s1,0,0),(-s2,-s2,0),(0,-s1,0),(s2,-s2,0),(s1,0,0),(s2,0,s2),(0,0,s1),(-s2,0,s2)], k=range(26), *kwargs)
        if isinstance(name, basestring): n.rename(name)
        return n

class Arm(RigPart):
    kAttrName_State = 'fkIk' # The name of the IK/FK attribute

    def Build(self, *args, **kwargs):
        super(Arm, self).Build(*args, **kwargs)

        # Create ikChain and fkChain
        self._aIkChain = pymel.duplicate(self.aInput, renameChildren=True, parentOnly=True)
        for oInput, oIk, in zip(self.aInput, self._aIkChain):
            pNameMap = NameMap(oInput, _sType='rig')
            oIk.rename(pNameMap.Serialize('ik'))
        self._aIkChain[0].setParent(self._oParent) # Trick the IK system (temporary solution)

        # Rig ikChain and fkChain
        self.sysIK = IK(self._aIkChain); self.sysIK.Build(**kwargs)
        self.sysFK = FK(self.aInput); self.sysFK.Build(_bConstraint=False, **kwargs)
        self.sysIK.oGrpAnm.setParent(self.oGrpAnm)
        self.sysIK.oGrpRig.setParent(self.oGrpRig)
        self.sysFK.oGrpAnm.setParent(self.oGrpAnm)
        #self.sysFK.oGrpRig.setParent(self.oGrpRig)

        # Create attribute holder (this is where the IK/FK attribute will be stored)
        oAttHolder = RigAttHolder(name=self._pNameMapAnm.Serialize('atts'))
        oAttHolder.setParent(self.oGrpAnm)
        pymel.parentConstraint(self.aInput[self.sysIK.iCtrlIndex], oAttHolder)
        pymel.addAttr(oAttHolder, longName=self.kAttrName_State, hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=1, k=True)
        attIkWeight = oAttHolder.attr(self.kAttrName_State)
        attFkWeight = libRigging.CreateUtilityNode('reverse', inputX=attIkWeight).outputX

        # Blend ikChain with fkChain
        for oInput, oIk, oFk in zip(self.aInput, self._aIkChain, self.sysFK.aCtrls):
            oConstraint = pymel.parentConstraint(oIk, oFk, oInput)
            attCurIkWeight, attCurFkWeight = oConstraint.getWeightAliasList()
            pymel.connectAttr(attIkWeight, attCurIkWeight)
            pymel.connectAttr(attFkWeight, attCurFkWeight)

        # Connect visibility
        pymel.connectAttr(attIkWeight, self.sysIK.oGrpAnm.visibility)
        pymel.connectAttr(attFkWeight, self.sysFK.oGrpAnm.visibility)

        self.attState = attIkWeight # Expose state
    #
    # Functions called for IK/FK switch (animation tools)
    #

    def snapIkToFk(self):
        ctrlIndex = 2 # TODO: Implement
        self.sysIK.ctrlIK.setMatrix(self.aInput[ctrlIndex].getMatrix(worldSpace=True), worldSpace=True)
        self.sysIK.ctrlSwivel.setMatrix(self.aInput[ctrlIndex-1].getMatrix(worldSpace=True), worldSpace=True)

    def snapFkToIk(self):
        for ctrl, jnt in zip(self.sysFK.aCtrls, self.aInput):
            ctrl.setMatrix(jnt.getMatrix(worldSpace=True), worldSpace=True)

    def switchToIk(self):
        self.snapIkToFk()
        self.attState.set(1.0)

    def switchToFk(self):
        self.snapFkToIk()
        self.attState.set(0.0)


