import pymel.core as pymel
from classRigNode import RigNode
from rigArm import Arm
import libUtils as Utils


class Leg(Arm):
	def __init__(self, *args, **kwargs):
		super(Leg, self).__init__(*args, **kwargs)

	def Build(self, *args, **kwargs):
		super(Leg, self).Build(_bOrientIkCtrl=False, *args, **kwargs)

		# Hack: Ensure the ctrlIK is looking in the right direction
		oMake = self.sysIK.oCtrlIK.getShape().create.inputs()[0]
		oMake.normal.set((0,1,0))

		self.CreateFootRoll()

	# TODO: Support foot that is not aligned to world plane
	def CreateFootRoll(self):
		oFoot = self.aIkChain[self.iCtrlIndex]
		oToes = self.aIkChain[self.iCtrlIndex+1]
		oTips = self.aIkChain[self.iCtrlIndex+2]

		# Create FootRoll
		p3Foot = oFoot.getTranslation(space='world')
		tmFoot = pymel.datatypes.Matrix(1,0,0,0,0,1,0,0,0,0,1,0, p3Foot[0], 0, p3Foot[2], 1)
		p3Toes = oToes.getTranslation(space='world')
		tmToes = pymel.datatypes.Matrix(1,0,0,0,0,1,0,0,0,0,1,0, p3Toes[0], p3Toes[1], p3Toes[2], 1)

		fOffsetF = 5
		fOffsetB = fOffsetF * 0.25

		# Create pivots; TODO: Create side pivots
		oPivotM = RigNode(name=self.pNameMapRig.Serialize('pivotM'))
		oPivotM.setMatrix(tmToes)
		oPivotM.r.set((0,0,0))

		oPivotF = RigNode(name=self.pNameMapRig.Serialize('pivotF'))
		oPivotF.setMatrix(pymel.datatypes.Matrix(1,0,0,0,0,1,0,0,0,0,1,0, 0,0,fOffsetF, 1) * tmFoot)
		oPivotF.r.set((0,0,0))

		oPivotB = RigNode(name=self.pNameMapRig.Serialize('pivotB'))
		oPivotB.setMatrix(pymel.datatypes.Matrix(1,0,0,0,0,1,0,0,0,0,1,0, 0,0,-fOffsetB, 1) * tmFoot)
		oPivotB.r.set((0,0,0))

		oFootRollRoot = RigNode(name=self.pNameMapRig.Serialize('footroll'))

		# Create hyerarchy
		oPivotM.setParent(oPivotF)
		oPivotF.setParent(oPivotB)
		oPivotB.setParent(oFootRollRoot)
		oFootRollRoot.setParent(self.oGrpRig)
		pymel.parentConstraint(self.sysIK.oCtrlIK, oFootRollRoot, maintainOffset=True)
		
		# Create attributes
		oAttHolder = self.sysIK.oCtrlIK
		pymel.addAttr(oAttHolder, longName='footRoll', k=True)
		pymel.addAttr(oAttHolder, longName='footRollThreshold', k=True, defaultValue=45)
		attFootRoll = oAttHolder.attr('footRoll')
		attFootRollThreshold = oAttHolder.attr('footRollThreshold')

		attRollF = Utils.CreateUtilityNode('condition', operation=2, 
			firstTerm=attFootRoll, secondTerm=attFootRollThreshold, colorIfFalseR=0,
			colorIfTrueR=(Utils.CreateUtilityNode('plusMinusAverage', operation=2, input1D=[attFootRoll, attFootRollThreshold]).output1D)).outColorR # Substract
		attRollM = Utils.CreateUtilityNode('condition', operation=2, firstTerm=attFootRoll, secondTerm=attFootRollThreshold, colorIfTrueR=attFootRollThreshold, colorIfFalseR=attFootRoll).outColorR # Less
		attRollB = Utils.CreateUtilityNode('condition', operation=2, firstTerm=attFootRoll, secondTerm=0.0, colorIfTrueR=0, colorIfFalseR=attFootRoll).outColorR # Greater
		pymel.connectAttr(attRollM, oPivotM.rotateX)
		pymel.connectAttr(attRollF, oPivotF.rotateX)
		pymel.connectAttr(attRollB, oPivotB.rotateX)

		pymel.parentConstraint(self.sysIK.oCtrlIK, self.sysIK.oCtrlSwivel, maintainOffset=True) # TODO: Implement SpaceSwitch

		# Create ikHandles
		oIkHandleFoot, oIkEffectorFoot = pymel.ikHandle(startJoint=oFoot, endEffector=oToes, solver='ikSCsolver')
		oIkHandleFoot.rename(self.pNameMapRig.Serialize('ikHandle', 'foot'))
		oIkHandleFoot.setParent(oFootRollRoot)
		oIkHandleToes, oIkEffectorToes = pymel.ikHandle(startJoint=oToes, endEffector=oTips, solver='ikSCsolver')
		oIkHandleToes.rename(self.pNameMapRig.Serialize('ikHandle', 'ties'))
		oIkHandleToes.setParent(oFootRollRoot)

		# Connect ikHandles
		pymel.delete([o for o in self.sysIK.oIkHandle.getChildren() if isinstance(o, pymel.nodetypes.Constraint) and not isinstance(o, pymel.nodetypes.PoleVectorConstraint)])
		pymel.parentConstraint(oPivotM, self.sysIK.oIkHandle, maintainOffset=True)
		pymel.parentConstraint(oPivotF, oIkHandleFoot, maintainOffset=True)
		pymel.parentConstraint(oPivotB, oIkHandleToes, maintainOffset=True)
