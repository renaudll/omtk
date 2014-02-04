import pymel.core as pymel
from classRigCtrl import RigCtrl
from classRigPart import RigPart
from omtk.libs import libRigging


class CtrlIk(RigCtrl):
    kAttrName_State = 'ikFk'

    def __createNode__(self, *args, **kwargs):
        super(CtrlIk, self).__createNode__(*args, **kwargs)
        assert(self.node is not None)
        pymel.addAttr(self.node, longName=self.kAttrName_State)
        self.m_attState = getattr(self.node, self.kAttrName_State)


class CtrlIkSwivel(RigCtrl):
    def __createNode__(self, _oLineTarget=False, *args, **kwargs):
        super(CtrlIkSwivel, self).__createNode__(*args, **kwargs)
        assert(self.node is not None)
        oMake = self.node.getShape().create.inputs()[0]
        oMake.radius.set(oMake.radius.get() * 0.5)
        oMake.degree.set(1)
        oMake.sections.set(4)

        # Create line
        if _oLineTarget is True:
            oCtrlShape = self.node.getShape()
            oLineShape = pymel.createNode('annotationShape')
            oLineTransform = oLineShape.getParent()
            pymel.connectAttr(oCtrlShape.worldMatrix, oLineShape.dagObjectMatrix[0], force=True)
            oLineTransform.setParent(self.offset)
            pymel.pointConstraint(_oLineTarget, oLineTransform)

# Todo: Support more complex IK limbs (ex: 2 knees)
class IK(RigPart):
    def __init__(self, *args, **kwargs):
        super(IK, self).__init__(*args, **kwargs)
        self.bStretch = True
        self.iCtrlIndex = 2

    def Build(self, _bOrientIkCtrl=True, *args, **kwargs):
        super(IK, self).Build(*args, **kwargs)
        oChainS = self.aInput[0]
        oChainE = self.aInput[self.iCtrlIndex]

        # Compute chainLength
        fChainLength = 0
        for oInput in self.aInput[1:self.iCtrlIndex + 1]:
            fChainLength += oInput.t.get().length()

        # Compute swivel position
        p3ChainS = oChainS.getTranslation(space='world')
        p3ChainE = oChainE.getTranslation(space='world')
        fRatio = self.aInput[1].t.get().length() / fChainLength
        p3SwivelBase = (p3ChainE - p3ChainS) * fRatio + p3ChainS
        p3SwivelDir = (self.aInput[1].getTranslation(space='world') - p3SwivelBase).normal()
        p3SwivelPos = p3SwivelBase + p3SwivelDir * fChainLength

        # Create ikChain
        oChainRoot = pymel.createNode('transform', name=self._pNameMapRig.Serialize('ikChain'), parent=self.oGrpRig)
        oChainRoot.setMatrix(oChainS.getMatrix(worldSpace=True), worldSpace=True)
        oChainS.setParent(oChainRoot)

        self._oIkHandle, oIkEffector = pymel.ikHandle(startJoint=oChainS, endEffector=oChainE, solver='ikRPsolver')
        self._oIkHandle.rename(self._pNameMapRig.Serialize('ikHandle'))
        self._oIkHandle.setParent(oChainRoot)
        oIkEffector.rename(self._pNameMapRig.Serialize('ikEffector'))

        # Create ctrls
        self.ctrlIK = CtrlIk(_create=True)
        self.ctrlIK.setParent(self.oGrpAnm)
        self.ctrlIK.rename(self._pNameMapAnm.Serialize('ik'))
        self.ctrlIK.offset.setTranslation(oChainE.getTranslation(space='world'), space='world')
        if _bOrientIkCtrl is True:
            self.ctrlIK.offset.setRotation(oChainE.getRotation(space='world'), space='world')

        self.ctrlSwivel = CtrlIkSwivel(_oLineTarget=self.aInput[1], _create=True)
        self.ctrlSwivel.setParent(self.oGrpAnm)
        self.ctrlSwivel.rename(self._pNameMapAnm.Serialize('ikSwivel'))
        self.ctrlSwivel.offset.setTranslation(p3SwivelPos, space='world')
        self.ctrlSwivel.offset.setRotation(self.aInput[self.iCtrlIndex - 1].getRotation(space='world'), space='world')
        self.swivelDistance = fChainLength # Used in ik/fk switch

        # Connect rig -> anm
        pymel.pointConstraint(self.ctrlIK, self._oIkHandle)
        pymel.orientConstraint(self.ctrlIK, oChainE, maintainOffset=True)
        pymel.poleVectorConstraint(self.ctrlSwivel, self._oIkHandle)

        # Connect stretch
        if self.bStretch is True:
            attChainDistance = libRigging.CreateUtilityNode('distanceBetween', inMatrix1=oChainRoot.worldMatrix,
                                                       inMatrix2=self.ctrlIK.worldMatrix).distance
            attStretch = libRigging.CreateUtilityNode('multiplyDivide', operation=2, input1X=attChainDistance,
                                                 input2X=fChainLength).outputX
            attStretch = libRigging.CreateUtilityNode('condition', operation=2, firstTerm=attStretch, secondTerm=1.0,
                                                 colorIfTrueR=attStretch, colorIfFalseR=1.0).outColorR # GreaterThan
            for oInput in self.aInput[1:self.iCtrlIndex + 1]:
                attNewPos = libRigging.CreateUtilityNode('multiplyDivide', input1=oInput.t.get(), input2X=attStretch,
                                                    input2Y=attStretch, input2Z=attStretch).output
                pymel.connectAttr(attNewPos, oInput.t)

        # Connect to parent
        if self._oParent is not None:
            pymel.parentConstraint(self._oParent, oChainRoot, maintainOffset=True)

    def Unbuild(self, *args, **kwargs):
        super(IK, self).Unbuild(*args, **kwargs)

        self.ctrlIk = None
        self.ctrlSwivel = None
