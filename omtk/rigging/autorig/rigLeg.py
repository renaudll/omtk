import pymel.core as pymel
from classRigNode import RigNode
from rigArm import Arm
from omtk.libs import libRigging

class Leg(Arm):
	def build(self, *args, **kwargs):
		super(Leg, self).build(_bOrientIkCtrl=False, *args, **kwargs)

		# Hack: Ensure the ctrlIK is looking in the right direction
		oMake = self.sysIK.ctrlIK.getShape().create.inputs()[0]
		oMake.normal.set((0,1,0))

		self.create_footroll()

	# TODO: Support foot that is not aligned to world plane
	def create_footroll(self):
		oFoot = self.sysIK._chain_ik[self.iCtrlIndex]
		oToes = self.sysIK._chain_ik[self.iCtrlIndex+1]
		oTips = self.sysIK._chain_ik[self.iCtrlIndex+2]

		# Create FootRoll
		p3Foot = oFoot.getTranslation(space='world')
		#tmFoot = pymel.datatypes.Matrix(1,0,0,0,0,1,0,0,0,0,1,0, p3Foot[0], 0, p3Foot[2], 1)
		p3Toes = oToes.getTranslation(space='world')
		#tmToes = pymel.datatypes.Matrix(1,0,0,0,0,1,0,0,0,0,1,0, p3Toes[0], p3Toes[1], p3Toes[2], 1)

		fOffsetF = 5
		fOffsetB = fOffsetF * 0.25

		# Create pivots; TODO: Create side pivots
		oPivotM = RigNode(name=self._pNameMapRig.Serialize('pivotM'))
		oPivotM.build()
		oPivotM.t.set(p3Toes) # Optimisation: t.set is faster than setMatrix
		#oPivotM.setMatrix(tmToes)
		#oPivotM.r.set((0,0,0))

		oPivotF = RigNode(name=self._pNameMapRig.Serialize('pivotF'))
		oPivotF.build()
		oPivotF.t.set(p3Foot + [0,0,fOffsetF]) # Optimisation: t.set is faster than setMatrix
		#oPivotF.setMatrix(pymel.datatypes.Matrix(1,0,0,0,0,1,0,0,0,0,1,0, 0,0,fOffsetF, 1) * tmFoot)
		#oPivotF.r.set((0,0,0))

		oPivotB = RigNode(name=self._pNameMapRig.Serialize('pivotB'))
		oPivotB.build()
		oPivotB.t.set(p3Foot + [0,0,-fOffsetB]) # Optimisation: t.set is faster than setMatrix
		#oPivotB.setMatrix(pymel.datatypes.Matrix(1,0,0,0,0,1,0,0,0,0,1,0, 0,0,-fOffsetB, 1) * tmFoot)
		#oPivotB.r.set((0,0,0))

		oFootRollRoot = RigNode(name=self._pNameMapRig.Serialize('footroll'))
		oFootRollRoot.build()

		# Create hyerarchy
		oPivotM.set_parent(oPivotF)
		oPivotF.set_parent(oPivotB)
		oPivotB.set_parent(oFootRollRoot)
		oFootRollRoot.set_parent(self.grp_rig)
		pymel.parentConstraint(self.sysIK.ctrlIK, oFootRollRoot, maintainOffset=True)
		
		# Create attributes
		oAttHolder = self.sysIK.ctrlIK
		pymel.addAttr(oAttHolder, longName='footRoll', k=True)
		pymel.addAttr(oAttHolder, longName='footRollThreshold', k=True, defaultValue=45)
		attFootRoll = oAttHolder.attr('footRoll')
		attFootRollThreshold = oAttHolder.attr('footRollThreshold')

		attRollF = libRigging.CreateUtilityNode('condition', operation=2, 
			firstTerm=attFootRoll, secondTerm=attFootRollThreshold, colorIfFalseR=0,
			colorIfTrueR=(libRigging.CreateUtilityNode('plusMinusAverage', operation=2, input1D=[attFootRoll, attFootRollThreshold]).output1D)).outColorR # Substract
		attRollM = libRigging.CreateUtilityNode('condition', operation=2, firstTerm=attFootRoll, secondTerm=attFootRollThreshold, colorIfTrueR=attFootRollThreshold, colorIfFalseR=attFootRoll).outColorR # Less
		attRollB = libRigging.CreateUtilityNode('condition', operation=2, firstTerm=attFootRoll, secondTerm=0.0, colorIfTrueR=0, colorIfFalseR=attFootRoll).outColorR # Greater
		pymel.connectAttr(attRollM, oPivotM.rotateX)
		pymel.connectAttr(attRollF, oPivotF.rotateX)
		pymel.connectAttr(attRollB, oPivotB.rotateX)

		pymel.parentConstraint(self.sysIK.ctrlIK, self.sysIK.ctrl_swivel, maintainOffset=True) # TODO: Implement SpaceSwitch

		# Create ikHandles
		oIkHandleFoot, oIkEffectorFoot = pymel.ikHandle(startJoint=oFoot, endEffector=oToes, solver='ikSCsolver')
		oIkHandleFoot.rename(self._pNameMapRig.Serialize('ikHandle', 'foot'))
		oIkHandleFoot.set_parent(oFootRollRoot)
		oIkHandleToes, oIkEffectorToes = pymel.ikHandle(startJoint=oToes, endEffector=oTips, solver='ikSCsolver')
		oIkHandleToes.rename(self._pNameMapRig.Serialize('ikHandle', 'ties'))
		oIkHandleToes.set_parent(oFootRollRoot)

		# Connect ikHandles
		pymel.delete([o for o in self.sysIK._oIkHandle.getChildren() if isinstance(o, pymel.nodetypes.Constraint) and not isinstance(o, pymel.nodetypes.PoleVectorConstraint)])
		pymel.parentConstraint(oPivotM, self.sysIK._oIkHandle, maintainOffset=True)
		pymel.parentConstraint(oPivotF, oIkHandleFoot, maintainOffset=True)
		pymel.parentConstraint(oPivotB, oIkHandleToes, maintainOffset=True)
