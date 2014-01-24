import pymel.core as pymel
import logging

'''
This method facilitate the creation of utility nodes by connecting/settings automaticly attributes.
'''
def ConnectOrSetAttr(_pAttr, _pValue):
	aBasicTypes = [int, float, bool, pymel.datatypes.Matrix, pymel.datatypes.Vector]
	if isinstance(_pValue, list) or isinstance(_pValue, tuple):
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

#
# CtrlShapes Backup
#
def BackupCtrlShape(_oCtrl):
    aShapes = filter(lambda x: isinstance(x, pymel.nodetypes.CurveShape), _oCtrl.getShapes())
    oSnapshot = pymel.duplicate(_oCtrl, parentOnly=True, returnRootsOnly=True)[0]
    for oShape in aShapes:
        oShape.setParent(oSnapshot, s=True, r=True)
    oSnapshot.setParent(world=True)
    oSnapshot.rename('_{0}'.format(_oCtrl.name()))
    return oSnapshot

def BackupCtrlShapes():
    aCtrls = [o.getParent() for o in pymel.ls('anm_*', type='nurbsCurve')]
    return [BackupCtrlShape(oCtrl) for oCtrl in aCtrls]

def RestoreCtrlShapes():
    aSources = [o.getParent() for o in pymel.ls('_anm_*', type='nurbsCurve')]

    for oSource in aSources:
    	sTargetName = oSource.name()[1:]
    	if pymel.objExists(sTargetName):
    		oTarget = pymel.PyNode(sTargetName)

    		pymel.delete(filter(lambda x: isinstance(x, pymel.nodetypes.CurveShape), oTarget.getShapes()))
	    	for oShape in oSource.getShapes():
	    		oShape.setParent(oTarget, r=True, s=True)

	    	# TODO: Restore AnnotationShapes

	    	pymel.delete(oSource)