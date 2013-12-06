import pymel.core as pymel
import logging

'''
This method facilitate the creation of utility nodes by connecting/settings automaticly attributes.
'''
def ConnectOrSetAttr(_pAttr, _pValue):
	aBasicTypes = [int, float, bool, pymel.datatypes.Matrix, pymel.datatypes.Vector]
	if isinstance(_pValue, list) or isinstance(_pValue, tuple):
		print '{0} is iterable! {0}'.format(_pAttr)
		for i, pSubValue in enumerate(_pValue):
			ConnectOrSetAttr(_pAttr[i], pSubValue)
	else:
		if isinstance(_pValue, pymel.Attribute):
			pymel.connectAttr(_pValue, _pAttr, force=True)
		elif any(kType for kType in aBasicTypes if isinstance(_pValue, kType)):
			_pAttr.set(_pValue)
		else:
			logging.error('[ConnectOrSetAttr] Invalid argument {0} of type {1} and value {2}'.format(_pAttr.name(), type(_pValue), _pValue))
			raise TypeError

def CreateUtilityNode(_sClass, *args, **kwargs):
	uNode = pymel.shadingNode(_sClass, asUtility=True)
	for sAttrName, pAttrValue in kwargs.items():
		if not uNode.hasAttr(sAttrName):
			logging.warning('[CreateUtilityNode] UtilityNode {0} doesn\'t have an {1} attribute. Skipping it.'.format(_sClass, sAttrName))
		else:
			ConnectOrSetAttr(uNode.attr(sAttrName), pAttrValue)	
	return uNode
