import pymel.core as pymel
from classRigNode import RigNode
from omtk.libs import libRigging

class RigCtrl(RigNode):
	def __init__(self, _bOffset=True, *args, **kwargs):
		super(RigCtrl, self).__init__(*args, **kwargs)

		# Create offset node to ensure that the transforma attributes starts at zero
		if _bOffset is True:
			self.offset = pymel.createNode('transform', name=(self.node.name() + '_offset'))
			self.setMatrix(self.node.getMatrix(worldSpace=True), worldSpace=True)
			self.node.setParent(self.offset)

	def __createNode__(self, *args, **kwargs):
		n = pymel.circle(*args, **kwargs)[0]
		oMake = n.getShape().create.inputs()[0]
		oMake.radius.set(5) # HARDCODED
		oMake.normal.set((1,0,0))
		return n

	def rename(self, _sName, *args, **kwargs):
		self.node.rename(_sName, *args, **kwargs)
		self.offset.rename(_sName + '_offset')

	# Overwrite common pymel methods
	def setMatrix(self, *args, **kwargs): self.offset.setMatrix(*args, **kwargs)
	def setTranslation(self, *args, **kwargs): self.offset.setTranslation(*args, **kwargs)
	def setRotation(self, *args, **kwargs): self.offset.setRotation(*args, **kwargs)
	def setParent(self, *args, **kwargs): return self.offset.setParent(*args, **kwargs)

	# TODO: Make sure it work
	def CreateSpaceSwitch(self, _aSpaces, _aLabels, _bUseDefault=True):
		oConstraint = pymel.parentConstraint(_aSpaces, self.offset, maintainOffset=True)
		pymel.addAttr(self.offset, longName='space', at='enum', enumName=_aLabels)
		attSpace = self.offset.getAttr('space')
		aWeightAtts = oConstraint.getWeightAliasList()
		for i, attWeight in enumerate(aWeightAtts):
			iIndexToMatch = i if not _bUseDefault else i + 1
			attSpaceIsActive = libRigging.CreateUtilityNode('condition', firstTerm=attSpace, secondTerm=iIndexToMatch, colorIfTrueR=1, colorIfFalseR=0).outColorR #Equal
			pymel.connectAttr(attSpaceIsActive, attWeight)
