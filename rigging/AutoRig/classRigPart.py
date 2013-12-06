import pymel.core as pymel
import logging
from classSerializable import Serializable
from classNameMap import NameMap

'''
This is the baseclass for anything that can be Build/Unbuild
'''
class RigPart(Serializable):
	def __init__(self, _aInput=[], *args, **kwargs):
		super(RigPart, self).__init__(*args, **kwargs)
		self.SetAttrPublic('aInput', _aInput)
		self.SetAttrPublic('iCtrlIndex', 2)
		self.SetAttrPublic('oGrpAnm')
		self.SetAttrPublic('oGrpRig')

		oRef = next(iter(_aInput), None)
		self.SetAttrPublic('pNameMapAnm', NameMap(oRef, _sType='anm'))
		self.SetAttrPublic('pNameMapRig', NameMap(oRef, _sType='rig'))
		self.oParent = oRef.getParent() if oRef is not None else None

	def Build(self, _bCreateGrpAnm=True, _bCreateGrpRig=True, *args, **kwargs):
		logging.info('Building {0}'.format(self.pNameMapRig.Serialize()))

		if len(self.aInput) == 0:
			logging.error("[RigPart:Build] Can't build, aInput is empty"); return False

		if _bCreateGrpAnm:
			self.oGrpAnm = pymel.createNode('transform', name=self.pNameMapAnm.Serialize(self.__class__.__name__.lower(), _sType='anms'))
		if _bCreateGrpRig:
			self.oGrpRig = pymel.createNode('transform', name=self.pNameMapRig.Serialize(self.__class__.__name__.lower(), _sType='rigs'))

	def Unbuild(self):
		if self.oGrpAnm is not None:
			pymel.delete(self.oGrpAnm)
		if self.oGrpRig is not None:
			pymel.delete(self.oGrpRig)

	# Overwritten from Serializable
	def __createMayaNetwork__(self):
		return pymel.createNode('network', name=self.pNameMapAnm.Serialize(_sType='net'))
