import pymel.core as pymel
from classRigCtrl import RigCtrl
from classRigPart import RigPart
from omtk.libs import libRigging, libAttr, libPymel
from omtk.rigging import formulaParser


class CtrlIk(RigCtrl):
    kAttrName_State = 'ikFk'

    def build(self, *args, **kwargs):
        super(CtrlIk, self).build(*args, **kwargs)
        assert(self.node is not None)
        pymel.addAttr(self.node, longName=self.kAttrName_State)
        self.m_attState = getattr(self.node, self.kAttrName_State)
        return self.node


class CtrlIkSwivel(RigCtrl):
    def build(self, _oLineTarget=False, *args, **kwargs):
        super(CtrlIkSwivel, self).build(*args, **kwargs)
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

    def calc_swivel_pos(self):
        p3ChainS = self.input[0].getTranslation(space='world')
        p3ChainE = self.input[self.iCtrlIndex].getTranslation(space='world')
        fRatio = self.input[1].t.get().length() / self._chain_length
        p3SwivelBase = (p3ChainE - p3ChainS) * fRatio + p3ChainS
        p3SwivelDir = (self.input[1].getTranslation(space='world') - p3SwivelBase).normal()
        return p3SwivelBase + p3SwivelDir * self._chain_length

    def build(self, _bOrientIkCtrl=True, softik=True, *args, **kwargs):
        super(IK, self).build(*args, **kwargs)
        oChainS = self.input[0]
        oChainE = self.input[self.iCtrlIndex]

        # fChainLength = 0
        # for oInput in self.input[1:self.iCtrlIndex + 1]:
        #     fChainLength += oInput.t.get().length()
        #
        self._chain_length = self._chain.getLength()

        # Compute swivel position
        # p3ChainS = oChainS.getTranslation(space='world')
        # p3ChainE = oChainE.getTranslation(space='world')
        # fRatio = self.input[1].t.get().length() / self.fChainLength
        # p3SwivelBase = (p3ChainE - p3ChainS) * fRatio + p3ChainS
        # p3SwivelDir = (self.input[1].getTranslation(space='world') - p3SwivelBase).normal()
        # p3SwivelPos = p3SwivelBase + p3SwivelDir * self.fChainLength
        p3SwivelPos = self.calc_swivel_pos()

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

        self.ctrl_swivel = CtrlIkSwivel(_oLineTarget=self.input[1], _create=True)
        self.ctrl_swivel.setParent(self.grp_anm)
        self.ctrl_swivel.rename(self._pNameMapAnm.Serialize('ikSwivel'))
        self.ctrl_swivel.offset.setTranslation(p3SwivelPos, space='world')
        self.ctrl_swivel.offset.setRotation(self.input[self.iCtrlIndex - 1].getRotation(space='world'), space='world')
        self.swivelDistance = self._chain_length # Used in ik/fk switch

        # Create softIk
        if softik:
            oAttHolder = self.ctrlIK

            # Create an obj exposing the oCtrlIk translate relative to the start of the ikChain
            self.oSoftIKCtrlRef = pymel.createNode('transform')
            self.oSoftIKCtrlRef.rename(self._pNameMapRig.Serialize('ikHandleRef'))
            self.oSoftIKCtrlRef.setTranslation(self._oIkHandle.getTranslation(space='world'), space='world') # Todo: match unit scale?
            pymel.pointConstraint(self.ctrlIK, self.oSoftIKCtrlRef, maintainOffset=True)

            # Create the attributes that will be accessible by the end-user
            import functools

            vars = {}
            fnAddAttr = functools.partial(libAttr.addAttr, hasMinValue=True, hasMaxValue=True)
            fnParse = functools.partial(formulaParser.parse, **vars)

            #vars['inStretchAmount'] = fnAddAttr(oAttHolder, longName='StretchAmount', niceName='Stretch', minValue=0, maxValue=1)

            # Constants
            vars['inRatio'] = fnAddAttr(oAttHolder, longName='SoftIkRatio', niceName='SoftIK', defaultValue=0.25, minValue=0, maxValue=.5, k=True)
            vars['distanceBase'] = fnAddAttr(oAttHolder, longName='chainBaseLength', defaultValue=self._chain_length)

            vars['identity'] = oChainRoot.worldMatrix
            vars['pos'] = self.oSoftIKCtrlRef.worldMatrix

            # Variables (input)
            formulaParser.parse2("inDistance", "identity~pos", vars)

            # Variables (logic)
            formulaParser.parse2("distanceSoft", "distanceBase*inRatio", vars)

            # distanceSafe: the maximum length where the soft ik isnt active
            formulaParser.parse2("distanceSafe", "distanceBase-distanceSoft", vars)


            # soft_ik formula
            # src: http://www.softimageblog.com/userContent/anicholas/softik/Equation.gif
            formulaParser.parse2("outDistance", "distanceSoft*(1-(e^(((inDistance-distanceSafe)*-1)/distanceSoft)))+distanceSafe)", vars)
            # Apply soft-ik on ik chain

            # Variables (output)

            vars['outDistance'] = libRigging.CreateUtilityNode('condition', operation=2, firstTerm=vars['inDistance'], secondTerm=vars['distanceSafe'], colorIfTrueR=vars['outDistance'], colorIfFalseR=vars['distanceSafe']).outColorR

            print 'softik is accessible via utility node: ' + str(vars['outDistance'])

            vars['outRatio'] = formulaParser.parse("outDistance/distanceSafe", **vars)

            vars['outMultiplier'] = libRigging.CreateUtilityNode('condition', operation=2,
                firstTerm=vars['inDistance'],
                secondTerm=vars['distanceSafe'],
                colorIfTrueR=vars['outRatio'],
                colorIfFalseR=(vars['distanceSafe'])
            ).outColorR

            num_jnts = len(self._chain)
            for i in range(1, num_jnts):
                obj = self._chain[i]
                pymel.connectAttr(
                    libRigging.CreateUtilityNode('multiplyDivide',
                        input1X=vars['outRatio'],
                        input1Y=vars['outRatio'],
                        input1Z=vars['outRatio'],
                        input2=obj.t.get()).output,
                    obj.t, force=True)

            '''
            # Debug: create gizmos
            gsafe, gsafes = pymel.circle(name="safe")
            gsoft, gsofts = pymel.circle(name="soft")
            gbase, gbases = pymel.circle(name="base")
            pymel.connectAttr(vars['distanceBase'], gbases.radius)
            pymel.connectAttr(vars['distanceSoft'], gsofts.radius)
            pymel.connectAttr(vars['distanceSafe'], gsafes.radius)

            # Debug locators
            loc = pymel.spaceLocator()
            pymel.connectAttr(vars['outDistance'], loc.tx)

            grp = pymel.createNode('transform')
            grp.s.set(10, 10, 10)
            loc = pymel.spaceLocator()
            loc.setParent(grp)
            pymel.connectAttr(vars['outRatio'], loc.ty)
            '''

        # Connect rig -> anm
        pymel.pointConstraint(self.ctrlIK, self._oIkHandle)
        pymel.orientConstraint(self.ctrlIK, oChainE, maintainOffset=True)
        pymel.poleVectorConstraint(self.ctrl_swivel, self._oIkHandle)

        # Connect stretch
        '''
        if self.bStretch is True:
            attChainDistance = libRigging.CreateUtilityNode('distanceBetween', inMatrix1=oChainRoot.worldMatrix,
                                                            inMatrix2=self.ctrlIK.worldMatrix).distance
            attStretch = libRigging.CreateUtilityNode('multiplyDivide', operation=2, input1X=attChainDistance,
                                                      input2X=self._chain_length).outputX
            attStretch = libRigging.CreateUtilityNode('condition', operation=2, firstTerm=attStretch, secondTerm=1.0,
                                                      colorIfTrueR=attStretch,
                                                      colorIfFalseR=1.0).outColorR  # GreaterThan
            for oInput in self.input[1:self.iCtrlIndex + 1]:
                attNewPos = libRigging.CreateUtilityNode('multiplyDivide', input1=oInput.t.get(), input2X=attStretch,
                                                         input2Y=attStretch, input2Z=attStretch).output
                pymel.connectAttr(attNewPos, oInput.t)
        '''

        # Connect to parent
        if self._oParent is not None:
            pymel.parentConstraint(self._oParent, oChainRoot, maintainOffset=True)

    def unbuild(self, *args, **kwargs):
        super(IK, self).unbuild(*args, **kwargs)

        self.ctrlIk = None
        self.ctrl_swivel = None
