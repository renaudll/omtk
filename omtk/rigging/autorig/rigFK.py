import pymel.core as pymel
from classNameMap import NameMap
from classRigCtrl import RigCtrl
from classRigPart import RigPart

class CtrlFk(RigCtrl):
	def __createNode__(self, *args, **kwargs):
		super(CtrlFk, self).__createNode__(*args, **kwargs)
		oMake = self.node.getShape().create.inputs()[0]
		oMake.radius.set(5)
		oMake.degree.set(1)
		oMake.sections.set(6)
		return self.node

class FK(RigPart):
	def Build(self, _bConstraint=True, *args, **kwargs):
		super(FK, self).Build(_bCreateGrpRig=False, *args, **kwargs)

		# Create ctrl chain
		self.aCtrls = []
		for oInput in self.aInput:
			#sCtrlName = self._pNameMapAnm.Serialize('fk')
			sCtrlName = NameMap(oInput).Serialize('fk', _sType='anm')
			oCtrl = CtrlFk(name=sCtrlName, _create=True)
			oCtrl.setMatrix(oInput.getMatrix(worldSpace=True))
			self.aCtrls.append(oCtrl)

		self.aCtrls[0].setParent(self.oGrpAnm)
		for i in range(1, len(self.aCtrls)):
			self.aCtrls[i].setParent(self.aCtrls[i-1])

		# Connect jnt -> anm
		if _bConstraint is True:
			for oInput, oCtrl in zip(self.aInput, self.aCtrls):
				pymel.parentConstraint(oCtrl, oInput)
				pymel.connectAttr(oCtrl.s, oInput.s)

		# Connect to parent
		if self._oParent is not None:
			pymel.parentConstraint(self._oParent, self.oGrpAnm, maintainOffset=True)

	def Unbuild(self, *args, **kwargs):
		super(FK, self).Unbuild(*args, **kwargs)

		self.aCtrls = None
