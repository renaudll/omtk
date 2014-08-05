import pymel.core as pymel
from classNameMap import NameMap
from classRigCtrl import RigCtrl
from classRigPart import RigPart

class CtrlFk(RigCtrl):
	def build(self, *args, **kwargs):
		super(CtrlFk, self).build(*args, **kwargs)
		oMake = self.node.getShape().create.inputs()[0]
		oMake.radius.set(5)
		oMake.degree.set(1)
		oMake.sections.set(6)
		return self.node

class FK(RigPart):
	def build(self, _bConstraint=True, *args, **kwargs):
		super(FK, self).build(_bCreateGrpRig=False, *args, **kwargs)

		# Create ctrl chain
		self.aCtrls = []
		for oInput in self.input:
			#sCtrlName = self._pNameMapAnm.Serialize('fk')
			sCtrlName = NameMap(oInput).Serialize('fk', _sType='anm')
			oCtrl = CtrlFk(name=sCtrlName, _create=True)
			oCtrl.offset.setMatrix(oInput.getMatrix(worldSpace=True))
			self.aCtrls.append(oCtrl)

		self.aCtrls[0].setParent(self.grp_anm)
		for i in range(1, len(self.aCtrls)):
			self.aCtrls[i].setParent(self.aCtrls[i-1])

		# Connect jnt -> anm
		if _bConstraint is True:
			for oInput, oCtrl in zip(self.input, self.aCtrls):
				pymel.parentConstraint(oCtrl, oInput)
				pymel.connectAttr(oCtrl.s, oInput.s)

		# Connect to parent
		if self._oParent is not None:
			pymel.parentConstraint(self._oParent, self.grp_anm, maintainOffset=True)

	def unbuild(self, *args, **kwargs):
		super(FK, self).unbuild(*args, **kwargs)

		self.aCtrls = None
