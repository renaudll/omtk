import pymel.core as pymel
from classRigCtrl import RigCtrl
from classRigPart import RigPart
from omtk.libs import libRigging, libAttr
from omtk.rigging import formulaParser


class CtrlIk(RigCtrl):
    kAttrName_State = 'ikFk'

    def __createNode__(self, *args, **kwargs):
        super(CtrlIk, self).__createNode__(*args, **kwargs)
        assert(self.node is not None)
        pymel.addAttr(self.node, longName=self.kAttrName_State)
        self.m_attState = getattr(self.node, self.kAttrName_State)
        return self.node


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

        return self.node

# Todo: Support more complex IK limbs (ex: 2 knees)
class IK(RigPart):
    def __init__(self, *args, **kwargs):
        super(IK, self).__init__(*args, **kwargs)
        self.bStretch = True
        self.iCtrlIndex = 2

    def build(self, _bOrientIkCtrl=True, softik=True, *args, **kwargs):
        super(IK, self).build(*args, **kwargs)
        oChainS = self.input[0]
        oChainE = self.input[self.iCtrlIndex]

        # Compute chainLength
        fChainLength = 0
        for oInput in self.input[1:self.iCtrlIndex + 1]:
            fChainLength += oInput.t.get().length()

        # Compute swivel position
        p3ChainS = oChainS.getTranslation(space='world')
        p3ChainE = oChainE.getTranslation(space='world')
        fRatio = self.input[1].t.get().length() / fChainLength
        p3SwivelBase = (p3ChainE - p3ChainS) * fRatio + p3ChainS
        p3SwivelDir = (self.input[1].getTranslation(space='world') - p3SwivelBase).normal()
        p3SwivelPos = p3SwivelBase + p3SwivelDir * fChainLength

        # Create ikChain
        oChainRoot = pymel.createNode('transform', name=self._pNameMapRig.Serialize('ikChain'), parent=self.grp_rig)
        oChainRoot.setMatrix(oChainS.getMatrix(worldSpace=True), worldSpace=True)
        oChainS.setParent(oChainRoot)

        # Create ikEffector
        self._oIkHandle, oIkEffector = pymel.ikHandle(startJoint=oChainS, endEffector=oChainE, solver='ikRPsolver')
        self._oIkHandle.rename(self._pNameMapRig.Serialize('ikHandle'))
        self._oIkHandle.setParent(oChainRoot)
        oIkEffector.rename(self._pNameMapRig.Serialize('ikEffector'))

        # Create ctrls
        self.ctrlIK = CtrlIk(_create=True)
        self.ctrlIK.setParent(self.grp_anm)
        self.ctrlIK.rename(self._pNameMapAnm.Serialize('ik'))
        self.ctrlIK.offset.setTranslation(oChainE.getTranslation(space='world'), space='world')
        if _bOrientIkCtrl is True:
            self.ctrlIK.offset.setRotation(oChainE.getRotation(space='world'), space='world')

        self.ctrlSwivel = CtrlIkSwivel(_oLineTarget=self.input[1], _create=True)
        self.ctrlSwivel.setParent(self.grp_anm)
        self.ctrlSwivel.rename(self._pNameMapAnm.Serialize('ikSwivel'))
        self.ctrlSwivel.offset.setTranslation(p3SwivelPos, space='world')
        self.ctrlSwivel.offset.setRotation(self.input[self.iCtrlIndex - 1].getRotation(space='world'), space='world')
        self.swivelDistance = fChainLength # Used in ik/fk switch

        # Create softIk
        '''
        if softik:
            oAttHolder = self.ctrlIK

            # Create an obj exposing the oCtrlIk translate relative to the start of the ikChain
            self.oSoftIKCtrlRef = pymel.createNode('transform')
            self.oSoftIKCtrlRef.rename(self._pNameMapRig.Serialize('ikHandleRef'))
            self.oSoftIKCtrlRef.setTranslation(self._oIkHandle.getTranslation(space='world'), space='world') # Todo: match unit scale?
            pymel.pointConstraint(self.oIkHandleParent, self.oSoftIKCtrlRef, maintainOffset=True)

            # Create the attributes that will be accessible by the end-user
            import functools

            vars = {}
            fnAddAttr = functools.partial(libAttr.addAttr, hasMinValue=True, hasMaxValue=True, defaultValue=0, k=True)
            fnParse = functools.partial(formulaParser.parse, **vars)
            vars['inBaseDistance'] = self.GetBaseLength()
            vars['inDistance'] = fnParse("0~pos", pos=self.oSoftIKCtrlRef.t) #pos length
            vars['inStretchAmount'] = fnAddAttr(oAttHolder, longName='StretchAmount', niceName='Stretch', minValue=0, maxValue=1)
            vars['inRatio'] = fnAddAttr(oAttHolder, longName='SoftIkRatio', niceName='SoftIK', k=True, minValue=0, maxValue=.5)
            vars['distanceSoft'] = formulaParser.parse("inBaseDistance*inRatio", **vars)
            vars['distanceSafe'] = formulaParser.parse("inBaseDistance-distanceSoft", **vars)
            outMultiplier=0#???
            outStretchJnt=0#???
            # soft_ik formula
            # src: http://www.softimageblog.com/userContent/anicholas/softik/Equation.gif
            botL = formulaParser.parse("distanceSoft*(1-(e^(inDistance-distanceSafe)*-1/distanceSoft))+distanceSafe", *vars)

            util8 = formulaParser.parse("if(inDistance>distanceSafe)then(if_true)else(inDistance)")
            vars['outDistance'] = formulaParser.parse("if(inRatio)>(0)then(util8)else(inDistance)")
            vars['attEffectorStretch_WithSoftIK'] = formulaParser.parse("outDistance/inDistance")
            vars['attEffectorStretch_WithoutSoftIK'] = formulaParser.parse("if(inDistance>inBaseDistance)then(inBaseDistance/inDistance)else(1.0)")
            vars['attEffectorStretch'] = formulaParser.parse("if(inRatio>0.0)then(attEffectorStretch_WithSoftIK)else(attEffectorStretch_WithoutSoftIK)")

            """
            # Soft-IK
            utility14 = libShadingNode.BlendTwoAttr(
                _aInputs=[attEffectorStretch, 1.0],
                _attAttributesBlender=self.oSoftIK.inStretchAmount,
                _attOutput=self.oSoftIK.outMultiplier,
                _attParent=self.oGrpRig.aUtilityNodes)

            # Compute 'joints' stretch
            utility15 = libShadingNode.Divide(
                _attInput1X=self.oSoftIK.inDistance,
                _attInput2X=self.oSoftIK.outDistance,
                _attParent=self.oGrpRig.aUtilityNodes)
            utility16 = libShadingNode.GreaterThan(
                _attFirstTerm=self.oSoftIK.inDistance,
                _attSecondTerm=self.oSoftIK.distanceSafe,
                _attColorIfTrueR=utility15.outputX,
                _attColorIfFalseR=1.0,
                _attParent=self.oGrpRig.aUtilityNodes)
            attJointStretch_WithSoftIK = utility16.outColorR
            # HACK: When soft-ik is inactive, we can't use the outDistance, we have to go back to an older method (distance/basedistance)
            utility17 = libShadingNode.GreaterThan(
                _attFirstTerm=self.oSoftIK.inRatio,
                _attSecondTerm=0.0,
                _attColorIfTrueR=attJointStretch_WithSoftIK,
                _attColorIfFalseR=attEffectorStretch_WithoutSoftIK,
                _attParent=self.oGrpRig.aUtilityNodes)
            attJointStretch = utility17.outColorR
            utility18 = libShadingNode.BlendTwoAttr(
                _aInputs=[1.0, attJointStretch],
                _attAttributesBlender=self.oSoftIK.inStretchAmount,
                _attOutput=self.oSoftIK.outStretchJnt,
                _attParent=self.oGrpRig.aUtilityNodes)

            # Apply effector stretch
            self.oIkHandle.setParent(self.oGrpIkChain)
            utility19 = libShadingNode.Multiply(
                _attInput1X=self.oSoftIKCtrlRef.tx,
                _attInput1Y=self.oSoftIKCtrlRef.ty,
                _attInput1Z=self.oSoftIKCtrlRef.tz,
                _attInput2X=self.oSoftIK.outMultiplier,
                _attInput2Y=self.oSoftIK.outMultiplier,
                _attInput2Z=self.oSoftIK.outMultiplier,
                _attOutputX=self.oIkHandle.tx,
                _attOutputY=self.oIkHandle.ty,
                _attOutputZ=self.oIkHandle.tz,
                _attParent=self.oGrpRig.aUtilityNodes)

            # Apply joint stretch
            StretchAndSquash.ConnectStretch(self.aOutput, self.oSoftIK.outStretchJnt, _p3Axis=self._pOrientData.p3LookAxis, _iMaxIndex=self.iCtrlIndex)
            if self.bConstraint:
                StretchAndSquash.ConnectStretch(self.aInput, self.oSoftIK.outStretchJnt, _p3Axis=self._pOrientData.p3LookAxis,_iMaxIndex=self.iCtrlIndex)
            """
        '''

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
                                                      colorIfTrueR=attStretch,
                                                      colorIfFalseR=1.0).outColorR  # GreaterThan
            for oInput in self.input[1:self.iCtrlIndex + 1]:
                attNewPos = libRigging.CreateUtilityNode('multiplyDivide', input1=oInput.t.get(), input2X=attStretch,
                                                         input2Y=attStretch, input2Z=attStretch).output
                pymel.connectAttr(attNewPos, oInput.t)

        # Connect to parent
        if self._oParent is not None:
            pymel.parentConstraint(self._oParent, oChainRoot, maintainOffset=True)

    def unbuild(self, *args, **kwargs):
        super(IK, self).unbuild(*args, **kwargs)

        self.ctrlIk = None
        self.ctrlSwivel = None
