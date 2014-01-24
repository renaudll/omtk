import pymel.core as pymel
import logging

'''
This class is a pymel.PyNode wrapper that extent it's functionnality.
Note: We can't directly inherit from pymel.PyNode.
'''
class RigNode(object):
	def __init__(self, _pData=None, *args, **kwargs):
		self.__dict__['node'] = self.__createNode__(*args, **kwargs) if _pData is None else pymel.PyNode(_pData, *args, **kwargs) # Prevent call to __setattr__

	def __melobject__(self): # Mirror PyNode behavior
		return self.node.__melobject__()
	# Allow the programmer to manipulate a RigNode instance like a pymel.PyNode instance.

	def __getattr__(self, _sAttrName):
		if hasattr(self.node, _sAttrName):
			return getattr(self.node, _sAttrName)
		logging.error('{0} don\'t have an {1} attribute'.format(self, _sAttrName))
		return AttributeError

	def __createNode__(self, *args, **kwargs):
		return pymel.createNode('transform', *args, **kwargs)
