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
        # Handle softIk
        #
        oAttHolder = self.ctrlIK

        '''
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
        '''

        fnAddAttr = functools.partial(libAttr.addAttr, hasMinValue=True, hasMaxValue=True)
        formula = libFormula.Formula()
        formula.inRatio = fnAddAttr(oAttHolder, longName='SoftIkRatio', niceName='SoftIK', defaultValue=0, minValue=0, maxValue=.5, k=True)
        formula.inStretch = fnAddAttr(oAttHolder, longName='Stretch', niceName='Stretch', defaultValue=0, minValue=0, maxValue=1.0, k=True)
        # distanceMax is the length of the chain. If inStretch is activated, this is where streching without softIK occur.
        formula.distanceMax = fnAddAttr(oAttHolder, longName='chainBaseLength', defaultValue=self._chain_length)
        # inDistance is the distance between the start of the chain and the ikCtrl
        formula.inDistance = libFormula.parse("identity~pos", identity=grp_ikChain.worldMatrix, pos=self.ctrlIK.worldMatrix)
        # distanceSoft is the distance before distanceMax where the softIK kick in.
        # ex: For a chain of length 10.0 with a ratio of 0.1, the distanceSoft will be 1.0.
        formula.distanceSoft = "distanceMax*inRatio"
        # distanceSafe is the distance where there's no softIK.
        # ex: For a chain of length 10.0 with a ratio of 0.1, the distanceSafe will be 9.0.
        formula.distanceSafe = "distanceMax-distanceSoft"
        # This represent the soft-ik state
        # When the soft-ik kick in, the value is 0.0.
        # When the stretch kick in, the value is 1.0.
        # |-----------|-----------|----------|
        # -1          0.0         1.0         +++
        # -dBase      dSafe       dMax
        formula.deltaSafeSoft = "(inDistance-distanceSafe)/distanceSoft"
        # Hack: Prevent potential division by zero when soft-ik is desactivated
        formula.deltaSafeSoft = libRigging.CreateUtilityNode('condition',
            firstTerm=formula.distanceSoft,
            secondTerm=0.0,
            colorIfTrueR=0.0,
            colorIfFalseR=formula.deltaSafeSoft
        ).outColorR

        # outDistanceSoft is the desired ikEffector distance from the chain start after aplying the soft-ik
        # If there's no stretch, this will be directly applied to the ikEffector.
        # If there's stretch, this will be used to compute the amount of stretch needed to reach the ikCtrl while preserving the shape.
        formula.outDistanceSoft = "(distanceSoft*(1-(e^(deltaSafeSoft*-1))))+distanceSafe"

        # Affect ikEffector distance only where inDistance if bigger than distanceSafe.
        formula.outDistance = libRigging.CreateUtilityNode('condition',
            operation=2,
            firstTerm=formula.deltaSafeSoft,
            secondTerm=0.0,
            colorIfTrueR=formula.outDistanceSoft,
            colorIfFalseR=formula.inDistance
        ).outColorR
        # Affect ikEffector when we're not using stretching
        formula.outDistance = libRigging.CreateUtilityNode('blendTwoAttr',
            input=[formula.outDistance,formula.inDistance],
            attributesBlender=formula.inStretch).output

        # Connect ikEffector position
        # todo: don't use multiple nodes
        #pymel.connectAttr(formula.outDistance, self.oSoftIKEffector.tx)

        # WIP WIP
        '''
        # todo: make it work in older versions of maya
        formula.spos = libRigging.CreateUtilityNode('decomposeMatrix',
            inputMatrix=grp_ikChain.worldMatrix
        ).outputTranslate
        formula.epos = libRigging.CreateUtilityNode('decomposeMatrix',
            inputMatrix=self.ctrlIK.worldMatrix
        ).outputTranslate
        '''

        formula.outRatio = "outDistance/inDistance"
        formula.outRatioInv = "1.0-outRatio"
        pymel.select(clear=True)
        pymel.select(self.ctrlIK, grp_ikChain, self._oIkHandle)
        constraint = pymel.pointConstraint()
        constraint.rename(constraint.name().replace('pointConstraint', 'softIkConstraint'))
        pymel.select(constraint)
        weight_inn, weight_out = constraint.getWeightAliasList()
        pymel.connectAttr(formula.outRatio, weight_inn)
        pymel.connectAttr(formula.outRatioInv, weight_out)


        # WIP END



        #
        # Handle Stretching
        #

        # If we're using softIk AND stretchIk, we'll use the outRatioSoft to stretch the joints enough so that the ikEffector reach the ikCtrl.
        formula.outStretch = "inDistance/outDistanceSoft"

        # Apply the softIK only AFTER the distanceSafe
        formula.outStretch = libRigging.CreateUtilityNode('condition',
            operation=2,
            firstTerm=formula.inDistance,
            secondTerm=formula.distanceSafe,
            colorIfTrueR=formula.outStretch,
            colorIfFalseR=1.0
        ).outColorR

        # Apply stretching only if inStretch is ON
        formula.outStretch = libRigging.CreateUtilityNode('blendTwoAttr',
            input=[1.0, formula.outStretch],
            attributesBlender=formula.inStretch).output

        # Apply joints stretching
        num_jnts = len(self._chain_ik)
        for i in range(1, num_jnts):
            obj = self._chain_ik[i]
            pymel.connectAttr(
                libRigging.CreateUtilityNode('multiplyDivide',
                    input1X=formula.outStretch,
                    input1Y=formula.outStretch,
                    input1Z=formula.outStretch,
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
