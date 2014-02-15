import pymel.core as pymel
import logging

'''
This method facilitate the creation of utility nodes by connecting/settings automaticly attributes.
'''
__aBasicTypes = [int, float, bool, pymel.datatypes.Matrix, pymel.datatypes.Vector]
def _isBasicType(_val):
	global __aBasicTypes
	return type(_val) in __aBasicTypes

def ConnectOrSetAttr(_attr, _val):
	if isinstance(_val, list) or isinstance(_val, tuple):
		for i, pSubValue in enumerate(_val):
			ConnectOrSetAttr(_attr[i], pSubValue)
	else:
		if isinstance(_val, pymel.Attribute):
			pymel.connectAttr(_val, _attr, force=True)
		elif _isBasicType(_val):
			_attr.set(_val)
		else:
			logging.error('[ConnectOrSetAttr] Invalid argument {0} of type {1} and value {2}'.format(_attr.name(), type(_val), _val))
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

# TODO: Fix bug when two objects have the same name.
def RestoreCtrlShapes():
    aSources = [o.getParent() for o in pymel.ls('_anm_*', type='nurbsCurve')]

    for oSource in aSources:
    	sTargetName = oSource.name()[1:]
    	if pymel.objExists(sTargetName):
    		oTarget = pymel.PyNode(str(sTargetName))

    		pymel.delete(filter(lambda x: isinstance(x, pymel.nodetypes.CurveShape), oTarget.getShapes()))
	    	for oShape in oSource.getShapes():
	    		oShape.setParent(oTarget, r=True, s=True)
	    		oShape.rename(oTarget.name() + 'Shape')

	    	# TODO: Restore AnnotationShapes
	    	pymel.delete(oSource)
