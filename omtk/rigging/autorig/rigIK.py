import pymel.core as pymel
from classRigCtrl import RigCtrl
from classRigPart import RigPart
from omtk.libs import libRigging, libAttr, libFormula

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

    def __debug(self, attr, scale=1.0, name=None):
        parent = pymel.createNode('transform')
        #if name: parent.rename(name + '_parent')
        loc = pymel.spaceLocator()
        if name: loc.rename(name)
        loc.setParent(parent)
        #if name: loc.rename(name)
        pymel.connectAttr(attr, loc.ty)
        parent.scale.set(scale, scale, scale)

    def build(self, _bOrientIkCtrl=True, softik=True, *args, **kwargs):
        super(IK, self).build(*args, **kwargs)
        oChainS = self.input[0]
        oChainE = self.input[self.iCtrlIndex]

        # Compute chain length
        self._chain_length = self._chain.getLength()

        # Compute swivel position
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
            fnParse = functools.partial(libFormula.parse, **vars)

            #vars['inStretchAmount'] = fnAddAttr(oAttHolder, longName='StretchAmount', niceName='Stretch', minValue=0, maxValue=1)

            # Constants
            vars['inRatio'] = fnAddAttr(oAttHolder, longName='SoftIkRatio', niceName='SoftIK', defaultValue=0.125, minValue=0.001, maxValue=.5, k=True)
            vars['inStretch'] = fnAddAttr(oAttHolder, longName='Stretch', niceName='Stretch', defaultValue=0, minValue=0, maxValue=1.0, k=True)
            vars['distanceMax'] = fnAddAttr(oAttHolder, longName='chainBaseLength', defaultValue=self._chain_length)

            vars['identity'] = oChainRoot.worldMatrix
            vars['pos'] = self.oSoftIKCtrlRef.worldMatrix

            # Variables (input)
            libFormula.parseToVar("inDistance", "identity~pos", vars)

            # Variables (logic)
            libFormula.parseToVar("distanceSoft", "distanceMax*inRatio", vars)

            # distanceSafe: the maximum length where the soft ik isnt active
            # The maximum distane where the soft ik is not activated
            libFormula.parseToVar("distanceSafe", "distanceMax-distanceSoft", vars)


            vars['inDistanceFloor'] = libRigging.CreateUtilityNode('condition',
                operation=2,
                firstTerm=vars['inDistance'],
                secondTerm=vars['distanceSafe'],
                colorIfTrueR=vars['inDistance'],
                colorIfFalseR=vars['distanceSafe']
            ).outColorR

            # This represent the soft-ik state
            # When the soft-ik kick in, the value is 0.0.
            # When the stretch kick in, the value is 1.0.
            # |-----------|-----------|----------|
            # -1          0.0         1.0         +++
            # -dBase      dSafe       dMax
            libFormula.parseToVar("deltaSafeSoft", "(inDistanceFloor-distanceSafe)/distanceSoft", vars)
            #self.__debug(vars['deltaSafeSoft'], scale=1.0, name='deltaSafeSoft')

            # soft_ik formula
            # src: http://www.softimageblog.com/userContent/anicholas/softik/Equation.gif
            libFormula.parseToVar("outDistanceSoft", "(distanceSoft*(1-(e^(deltaSafeSoft*-1))))+distanceSafe", vars)
            vars['outDistanceNoStretch'] = libRigging.CreateUtilityNode('condition',
                operation=2,
                firstTerm=vars['deltaSafeSoft'],
                secondTerm=0.0,
                colorIfTrueR=vars['outDistanceSoft'],
                colorIfFalseR=vars['distanceSafe']
            ).outColorR
            #self.__debug(vars['outDistanceNoStretch'], scale=1.0, name='outDistanceNoStretch')

            print 'softik is accessible via utility node: ' + str(vars['outDistanceNoStretch'])

            vars['outRatioNoStretch'] = libFormula.parse("outDistanceNoStretch/distanceSafe", **vars)
            #self.__debug(vars['outRatioNoStretch'], scale=10.0, name='outRatioNoStretch')

            libFormula.parseToVar("outRatioWithStretch", "inDistanceFloor/outDistanceNoStretch", vars)
            self.__debug(vars['outRatioWithStretch'], scale=10.0, name='outRatioWithStretch')


            vars['out'] = libRigging.CreateUtilityNode('blendTwoAttr',
                input=[vars['outRatioNoStretch'], vars['outRatioWithStretch']],
                attributesBlender=vars['inStretch']).output

            #libFormula.parseToVar("outRatioStretch", "inDistance/outDistance", vars)

            num_jnts = len(self._chain)
            for i in range(1, num_jnts):
                obj = self._chain[i]
                pymel.connectAttr(
                    libRigging.CreateUtilityNode('multiplyDivide',
                        input1X=vars['out'],
                        input1Y=vars['out'],
                        input1Z=vars['out'],
                        input2=obj.t.get()).output,
                    obj.t, force=True)


            # Debug: create gizmos
            gsafe, gsafes = pymel.circle(name="safe")
            gsoft, gsofts = pymel.circle(name="soft")
            gbase, gbases = pymel.circle(name="base")
            pymel.connectAttr(vars['distanceMax'], gbases.radius)
            pymel.connectAttr(vars['distanceSoft'], gsofts.radius)
            pymel.connectAttr(vars['distanceSafe'], gsafes.radius)

            # Debug locators


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
