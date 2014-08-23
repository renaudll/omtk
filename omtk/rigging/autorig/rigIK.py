import pymel.core as pymel
from classRigCtrl import RigCtrl
from classRigPart import RigPart
from omtk.libs import libRigging, libAttr, libFormula, libPymel
from classNameMap import NameMap
import functools

class CtrlIk(RigCtrl):
    kAttrName_State = 'ikFk'

    def build(self, *args, **kwargs):
        super(CtrlIk, self).build(*args, **kwargs)
        assert(self.node is not None)
        pymel.addAttr(self.node, longName=self.kAttrName_State)
        self.m_attState = getattr(self.node, self.kAttrName_State)
        return self.node

    def unbuild(self, *args, **kwargs):
        super(CtrlIk, self).unbuild(*args, **kwargs)
        self.m_attState = None


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
        self.ctrlIK = None
        self.ctrl_swivel = None


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

    def build(self, _bOrientIkCtrl=True, *args, **kwargs):
        super(IK, self).build(*args, **kwargs)

        # Duplicate input chain (we don't want to move the hierarchy)
        # Todo: implement a duplicate method in omtk.libs.libPymel.PyNodeChain
        # Create ikChain and fkChain
        self._chain_ik = pymel.duplicate(self.input, renameChildren=True, parentOnly=True)
        for oInput, oIk, in zip(self.input, self._chain_ik):
            pNameMap = NameMap(oInput, _sType='rig')
            oIk.rename(pNameMap.Serialize('ik'))
        self._chain_ik[0].setParent(self._oParent) # Trick the IK system (temporary solution)

        oChainS = self._chain_ik[0]
        oChainE = self._chain_ik[self.iCtrlIndex]

        # Compute chain length
        self._chain_length = self._chain.getLength()

        # Compute swivel position
        p3SwivelPos = self.calc_swivel_pos()

        # Create ikChain
        grp_ikChain = pymel.createNode('transform', name=self._pNameMapRig.Serialize('ikChain'), parent=self.grp_rig)
        grp_ikChain.setMatrix(oChainS.getMatrix(worldSpace=True), worldSpace=True)
        oChainS.setParent(grp_ikChain)

        # Create ikEffector
        self._oIkHandle, oIkEffector = pymel.ikHandle(startJoint=oChainS, endEffector=oChainE, solver='ikRPsolver')
        self._oIkHandle.rename(self._pNameMapRig.Serialize('ikHandle'))
        self._oIkHandle.setParent(grp_ikChain)
        oIkEffector.rename(self._pNameMapRig.Serialize('ikEffector'))

        # Create ctrls
        if not isinstance(self.ctrlIK, CtrlIk): self.ctrlIK = CtrlIk()
        self.ctrlIK.build()
        #self.ctrlIK = CtrlIk(_create=True)
        self.ctrlIK.setParent(self.grp_anm)
        self.ctrlIK.rename(self._pNameMapAnm.Serialize('ik'))
        self.ctrlIK.offset.setTranslation(oChainE.getTranslation(space='world'), space='world')
        if _bOrientIkCtrl is True:
            self.ctrlIK.offset.setRotation(oChainE.getRotation(space='world'), space='world')

        if not isinstance(self.ctrl_swivel, CtrlIkSwivel): self.ctrl_swivel = CtrlIkSwivel()
        self.ctrl_swivel.build()
        #self.ctrl_swivel = CtrlIkSwivel(_oLineTarget=self.input[1], _create=True)
        self.ctrl_swivel.setParent(self.grp_anm)
        self.ctrl_swivel.rename(self._pNameMapAnm.Serialize('ikSwivel'))
        self.ctrl_swivel.offset.setTranslation(p3SwivelPos, space='world')
        self.ctrl_swivel.offset.setRotation(self.input[self.iCtrlIndex - 1].getRotation(space='world'), space='world')
        self.swivelDistance = self._chain_length # Used in ik/fk switch

        #
        # Create softIk
        #
        oAttHolder = self.ctrlIK

        # Create a null that always point to the ikCtrl so we only need to control one axis on the softIK effector
        self.oSoftIKEffectorParent = pymel.createNode('transform')
        self.oSoftIKEffectorParent.rename(self._pNameMapRig.Serialize('softIkEffectorAim'))
        self.oSoftIKEffectorParent.setParent(grp_ikChain)

        # Create a null that will control the ikEffector (necessary for softIK without stretching)
        self.oSoftIKEffector = pymel.createNode('transform')
        self.oSoftIKEffector.rename(self._pNameMapRig.Serialize('softIkEffector'))
        self.oSoftIKEffector.setParent(self.oSoftIKEffectorParent)

        self.oSoftIKEffectorParent.t.set(0,0,0)
        pymel.aimConstraint(self.ctrlIK, self.oSoftIKEffectorParent)
        pymel.pointConstraint(self.oSoftIKEffector, self._oIkHandle)

        vars = {}
        fnAddAttr = functools.partial(libAttr.addAttr, hasMinValue=True, hasMaxValue=True)
        fnParse = functools.partial(libFormula.parse, **vars)

        # Constants
        vars['inRatio'] = fnAddAttr(oAttHolder, longName='SoftIkRatio', niceName='SoftIK', defaultValue=0, minValue=0, maxValue=.5, k=True)
        vars['inStretch'] = fnAddAttr(oAttHolder, longName='Stretch', niceName='Stretch', defaultValue=0, minValue=0, maxValue=1.0, k=True)
        vars['distanceMax'] = fnAddAttr(oAttHolder, longName='chainBaseLength', defaultValue=self._chain_length)

        vars['identity'] = grp_ikChain.worldMatrix
        vars['pos'] = self.ctrlIK.worldMatrix

        # Variables (input)
        libFormula.parseToVar("inDistance", "identity~pos", vars)

        # Variables (logic)
        libFormula.parseToVar("distanceSoft", "distanceMax*inRatio", vars)

        # distanceSafe: the maximum length where the soft ik isnt active
        # The maximum distane where the soft ik is not activated
        libFormula.parseToVar("distanceSafe", "distanceMax-distanceSoft", vars)


        # This represent the soft-ik state
        # When the soft-ik kick in, the value is 0.0.
        # When the stretch kick in, the value is 1.0.
        # |-----------|-----------|----------|
        # -1          0.0         1.0         +++
        # -dBase      dSafe       dMax
        libFormula.parseToVar("deltaSafeSoft", "(inDistance-distanceSafe)/distanceSoft", vars)
        # Hack: Precent potential division by zero
        vars['deltaSafeSoft'] = libRigging.CreateUtilityNode('condition',
            firstTerm=vars['distanceSoft'],
            secondTerm=0.0,
            colorIfTrueR=0.0,
            colorIfFalseR=vars['deltaSafeSoft']
        ).outColorR


        # soft_ik formula
        # src: http://www.softimageblog.com/userContent/anicholas/softik/Equation.gif
        libFormula.parseToVar("outDistanceSoft", "(distanceSoft*(1-(e^(deltaSafeSoft*-1))))+distanceSafe", vars)
        vars['outDistanceNoStretch'] = vars['outDistanceSoft']

        print 'softik is accessible via utility node: ' + str(vars['outDistanceNoStretch'])
        vars['outRatioNoStretch'] = libFormula.parse("outDistanceNoStretch/distanceSafe", **vars)
        libFormula.parseToVar("outRatioWithStretch", "inDistance/outDistanceNoStretch", vars)
        vars['outStretch'] = libRigging.CreateUtilityNode('blendTwoAttr',
            input=[1.0, vars['outRatioWithStretch']],
            attributesBlender=vars['inStretch']).output

        # Limit stretch AFTER the safe distance
        vars['outStretch'] = libRigging.CreateUtilityNode('condition',
            operation=2,
            firstTerm=vars['inDistance'],
            secondTerm=vars['distanceSafe'],
            colorIfTrueR=vars['outStretch'],
            colorIfFalseR=1.0
        ).outColorR

        # We only want stretching if stretching is ON
        vars['outStretch'] = libRigging.CreateUtilityNode('blendTwoAttr',
            input=[1.0, vars['outStretch']],
            attributesBlender=vars['inStretch']).output

        vars['outDistanceNoStretchFloor'] = libRigging.CreateUtilityNode('condition',
            operation=2,
            firstTerm=vars['deltaSafeSoft'],
            secondTerm=0.0,
            colorIfTrueR=vars['outDistanceSoft'],
            colorIfFalseR=vars['inDistance']
        ).outColorR
        vars['outDistanceNoStretchFloor'] = libRigging.CreateUtilityNode('blendTwoAttr',
            input=[vars['outDistanceNoStretchFloor'],vars['inDistance']],
            attributesBlender=vars['inStretch']).output
        pymel.connectAttr(vars['outDistanceNoStretchFloor'], self.oSoftIKEffector.tx)

        # Connect stretch
        num_jnts = len(self._chain_ik)
        for i in range(1, num_jnts):
            obj = self._chain_ik[i]
            pymel.connectAttr(
                libRigging.CreateUtilityNode('multiplyDivide',
                    input1X=vars['outStretch'],
                    input1Y=vars['outStretch'],
                    input1Z=vars['outStretch'],
                    input2=obj.t.get()).output,
                obj.t, force=True)

        # Connect rig -> anm
        #pymel.pointConstraint(self.ctrlIK, self._oIkHandle)
        pymel.orientConstraint(self.ctrlIK, oChainE, maintainOffset=True)
        pymel.poleVectorConstraint(self.ctrl_swivel, self._oIkHandle)

        # Connect to parent

        print self.parent
        if libPymel.is_valid_PyNode(self.parent):
            pymel.parentConstraint(self.parent, grp_ikChain, maintainOffset=True)

        for source, target in zip(self._chain_ik, self._chain):
            pymel.parentConstraint(source, target)


    def unbuild(self):
        pass
