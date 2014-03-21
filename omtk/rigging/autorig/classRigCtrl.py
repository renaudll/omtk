import pymel.core as pymel
from omtk.rigging.autorig.classRigNode import RigNode
from omtk.libs import libRigging

class RigCtrl(RigNode):
	def __init__(self, _create=False, _bOffset=True, *args, **kwargs):
		super(RigCtrl, self).__init__(_create=_create, *args, **kwargs)
		if _create is True and _bOffset is True:
			self.__createOffset__()

	def __createOffset__(self):
		self.offset = pymel.group(self.node, absolute=True, name=(self.node.name() + '_offset')) # faster
		#self.offset = pymel.createNode('transform', name=(self.node.name() + '_offset'))
		#self.setMatrix(self.node.getMatrix(worldSpace=True), worldSpace=True)
		#self.node.setParent(self.offset)
		return self.offset

	def __createNode__(self, *args, **kwargs):
		self.node = pymel.circle(*args, **kwargs)[0]
		oMake = self.node.getShape().create.inputs()[0]
		oMake.radius.set(5) # HARDCODED
		oMake.normal.set((1,0,0))
		return self.node

	def rename(self, _sName, *args, **kwargs):
		if self.node is not None:
			self.node.rename(_sName, *args, **kwargs)
		if self.offset is not None:
			self.offset.rename(_sName + '_offset')

	# Overwrite common pymel methods
	def setParent(self, *args, **kwargs): 
		if not isinstance(self.offset, pymel.PyNode):
			print "[setParent] {0} don't have an offset attribute".format(self)
		return self.offset.setParent(*args, **kwargs)

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
