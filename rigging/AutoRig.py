import logging
import pymel.core as pymel

'''
This method facilitate the creation of utility nodes by connecting/settings automaticly attributes.
'''
def CreateUtilityNode(_sClass, *args, **kwargs):
	aBasicTypes = [int, float, bool, pymel.datatypes.Matrix, pymel.datatypes.Vector]
	uNode = pymel.shadingNode(_sClass, asUtility=True)
	for sAttrName, pAttrValue in kwargs.items():
		if not uNode.hasAttr(sAttrName):
			logging.warning('[CreateUtilityNode] UtilityNode {0} doesn\'t have an {1} attribute. Skipping it.'.format(_sClass, sAttrName))
		else:
			if isinstance(pAttrValue, pymel.Attribute):
				pymel.connectAttr(pAttrValue, uNode.attr(sAttrName), force=True)
			elif any(kType for kType in aBasicTypes if isinstance(pAttrValue, kType)):
				uNode.attr(sAttrName).set(pAttrValue)
			else:
				logging.error('[CreateUtilityNode] Invalid argument {0} of type {1} and value {2}'.format(sAttrName, type(pAttrValue), pAttrValue))
				raise TypeError
	return uNode

'''
This class handle the naming of object.
'''
# Tokens: Type, Name, Side, Iterator
class NameMap(object):
	m_sSeparator = '_'
	def __init__(self, *args, **kwargs):
		self.name = None
		self.type = None
		self.side = None
		self.iter = None
		self.aOthers = []
		self.Deserialize(*args, **kwargs)

	def Deserialize(self, _pData, _sName=None, _sType=None, _sSide=None, _iIter=None, _aOthers=[]):
		if isinstance(_pData, pymel.PyNode):
			_pData = _pData.nodeName()
		if isinstance(_pData, basestring):
			aTokens = _pData.split(self.m_sSeparator)
			iNumTokens = len(aTokens)
			if iNumTokens > 0:
				if iNumTokens == 1:
					self.name = aTokens[0]
				else:
					self.type = aTokens[0]
					if iNumTokens > 1 and self.name is None:
						self.name = aTokens[1]
					if iNumTokens > 2:
						pass # TODO: Implement

	def Serialize(self, *args, **kwargs):
		sType = self.type if '_sType' not in kwargs else kwargs['_sType']
		sName = self.name if '_sName' not in kwargs else kwargs['_sName']
		sSide = self.side if '_sSide' not in kwargs else kwargs['_sSide']
		sIter = self.iter if '_iIter' not in kwargs else kwargs['_iIter']
		if sIter is not None: sIter = str(sIter)
		return self.m_sSeparator.join(filter(None, [sType, sName, sSide, sIter] + self.aOthers + list(args)))

'''
This class handle the serialization of it's subclasses in multiples formats (ex: json, xml, maya nodes, etc)
'''
class Serializable(object):
	def SetAttrPublic(self, _sAttrName, _pAttrValue=None, _pAttrType=None):
		setattr(self, _sAttrName, _pAttrValue)

	def SetAttrPrivate(self, _sAttrName, _pAttrValue=None):
		setattr(self, _sAttrName, _pAttrValue)

	def Serialize(self):
		pass

	def Deserialize(self):
		pass

'''
This class is a pymel.PyNode wrapper that extent it's functionnality.
Note: We can't directly inherit from pymel.PyNode.
'''
class RigNode(object):
	def __init__(self):
		pass
	def __melobject__(self): # Mirror PyNode behavior
		pass

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

	def Build(self, *args, **kwargs):
		self.oGrpAnm = pymel.createNode('transform', name=self.pNameMapAnm.Serialize(_sType='anm'))
		self.oGrpRig = pymel.createNode('transform', name=self.pNameMapRig.Serialize(_sType='rig'))

	def Unbuild(self):
		if self.oGrpAnm is not None:
			pymel.delete(self.oGrpAnm)
		if self.oGrpRig is not None:
			pymel.delete(self.oGrpRig)

class IK(RigPart):
	def __init__(self, *args, **kwargs):
		super(IK, self).__init__(*args, **kwargs)
		self.SetAttrPublic('bStretch', True)

	def Build(self, *args, **kwargs):
		super(IK, self).Build(*args, **kwargs)

		# Create ikChain
		oChainS = self.aInput[0]
		oChainE = self.aInput[self.iCtrlIndex]
		oChainRoot = pymel.createNode('transform', name=self.pNameMapRig.Serialize('ikChain'), parent=self.oGrpRig)
		oChainRoot.setMatrix(oChainS.getMatrix(worldSpace=True), worldSpace=True)
		oChainS.setParent(oChainRoot)
		
		oIkHandle, oIkEffector = pymel.ikHandle(startJoint=oChainS, endEffector=oChainE, solver='ikRPsolver')
		oIkHandle.rename(self.pNameMapRig.Serialize('ikHandle'))
		oIkHandle.setParent(oChainRoot)
		oIkEffector.rename(self.pNameMapRig.Serialize('ikEffector'))

		# Create ctrls
		oCtrlIK = pymel.circle()[0]
		oCtrlIK.setParent(self.oGrpAnm)
		oCtrlIK.rename(self.pNameMapAnm.Serialize('ik'))
		oCtrlIK.setMatrix(oChainE.getMatrix(worldSpace=True), worldSpace=True)

		oCtrlSwivel = pymel.circle()[0]
		oCtrlSwivel.setParent(self.oGrpAnm)
		oCtrlSwivel.rename(self.pNameMapAnm.Serialize('ikSwivel'))
		oCtrlSwivel.setMatrix(self.aInput[self.iCtrlIndex-1].getMatrix(worldSpace=True), worldSpace=True)

		# Connect rig -> anm
		pymel.pointConstraint(oCtrlIK, oIkHandle)
		pymel.orientConstraint(oCtrlIK, oChainE)
		pymel.poleVectorConstraint(oCtrlSwivel, oIkHandle)

		# Connect stretch
		if self.bStretch is True:
			# Compute safeDistance (maximum chain length without stretch)
			fSafeDistance = 0
			for oInput in self.aInput[1:self.iCtrlIndex+1]:
				fSafeDistance += oInput.t.get().length()

			attChainDistance = CreateUtilityNode('distanceBetween', inMatrix1=oChainRoot.worldMatrix, inMatrix2=oCtrlIK.worldMatrix).distance
			attStretch = CreateUtilityNode('multiplyDivide', operation=2, input1X=attChainDistance, input2X=fSafeDistance).outputX
			attStretch = CreateUtilityNode('condition', operation=2, firstTerm=attStretch, secondTerm=1.0, colorIfTrueR=attStretch, colorIfFalseR=1.0).outColorR # GreaterThan
			for oInput in self.aInput[1:self.iCtrlIndex+1]:
				attNewPos = CreateUtilityNode('multiplyDivide', input1=oInput.t.get(), input2X=attStretch, input2Y=attStretch, input2Z=attStretch).output
				pymel.connectAttr(attNewPos, oInput.t)

class FK(RigPart):
	def Build(self, *args, **kwargs):
		super(FK, self).Build(*args, **kwargs)

		# Create ctrl chain
		aCtrls = []
		for oInput in self.aInput:
			oCtrl = pymel.circle(name=NameMap(oInput).Serialize('fk', _sType='anm'))[0]
			oCtrl.setMatrix(oInput.getMatrix(worldSpace=True), worldSpace=True)
			aCtrls.append(oCtrl)

		aCtrls[0].setParent(self.oGrpAnm)
		for i in range(1, len(aCtrls)):
			aCtrls[i].setParent(aCtrls[i-1])

		# Connect jnt -> anm
		for oInput, oCtrl in zip(self.aInput, aCtrls):
			pymel.parentConstraint(oCtrl, oInput)
			pymel.connectAttr(oCtrl.s, oInput.s)

class Arm(RigPart):
	kAttrName_State = 'fkIk' # The name of the IK/FK attribute

	def Build(self, *args, **kwargs):
		super(Arm, self).Build(*args, **kwargs)

		# Create attribute holder (this is where the IK/FK attribute will be stored)
		oAttHolder = pymel.circle(name=self.pNameMapAnm.Serialize('atts'))[0]
		oAttHolder.setParent(self.oGrpAnm)
		pymel.addAttr(oAttHolder, longName=self.kAttrName_State, hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=1, k=True)
		attState = oAttHolder.attr(self.kAttrName_State)

		# Create ikChain and fkChain
		aIkChain = pymel.duplicate(self.aInput, renameChildren=True)
		aFkChain = pymel.duplicate(self.aInput, renameChildren=True)
		for oInput, oIk, oFk, in zip(self.aInput, aIkChain, aFkChain):
			pNameMap = NameMap(oInput, _sType='rig')
			oIk.rename(pNameMap.Serialize('ik'))
			oFk.rename(pNameMap.Serialize('fk'))
		aIkChain[0].setParent(self.oGrpRig)
		aFkChain[0].setParent(self.oGrpRig)

		# Rig ikChain and fkChain
		self.sysIK = IK(aIkChain); self.sysIK.Build()
		self.sysFK = FK(aFkChain); self.sysFK.Build()
		self.sysIK.oGrpAnm.setParent(self.oGrpAnm)
		self.sysIK.oGrpRig.setParent(self.oGrpRig)
		self.sysFK.oGrpAnm.setParent(self.oGrpAnm)
		self.sysFK.oGrpRig.setParent(self.oGrpRig)

		# Blend ikChain with fkChain
		for oInput, oIk, oFk in zip(self.aInput, aIkChain, aFkChain):
			oConstraint = pymel.parentConstraint(oIk, oFk, oInput)
			attIkWeight, attFkWeight = oConstraint.getWeightAliasList()
			pymel.connectAttr(attState, attIkWeight)
			pymel.connectAttr(CreateUtilityNode('reverse', inputX=attIkWeight).outputX, attFkWeight)
