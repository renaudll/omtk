import logging
import pymel.core as pymel

'''
Usage example:
#import sys
from rigging import AutoRig
from pymel import core as pymel

AutoRig.Arm(pymel.ls('jnt_arm_l_*')).Build()
AutoRig.Arm(pymel.ls('jnt_arm_r_*')).Build()
AutoRig.FK(pymel.ls('jnt_spine')).Build()
AutoRig.FK(pymel.ls('jnt_chest')).Build()
AutoRig.FK(pymel.ls('jnt_neck')).Build()
AutoRig.FK(pymel.ls('jnt_head')).Build()
'''

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

	def Deserialize(self, _pData, _sName=None, _sType=None, _sSide=None, _iIter=None):
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
						self.side = aTokens[2] # TODO: Make it bulletproof
					pass # TODO: Implement
		if _sName is not None: self.name = _sName
		if _sType is not None: self.type = _sType
		if _sSide is not None: self.side = _sSide
		if _iIter is not None: self.iter = _iIter

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

class RigCtrl(RigNode):
	def __init__(self, _bOffset=True, *args, **kwargs):
		super(RigCtrl, self).__init__(*args, **kwargs)

		# Create offset node to ensure that the transforma attributes starts at zero
		if _bOffset is True:
			self.offset = pymel.createNode('transform', name=(self.node.name() + '_offset'))
			self.offset.setMatrix(self.node.getMatrix(worldSpace=True), worldSpace=True)
			self.node.setParent(self.offset)

	def __createNode__(self, *args, **kwargs):
		return pymel.circle(*args, **kwargs)[0]

	def rename(self, _sName, *args, **kwargs):
		self.node.rename(_sName, *args, **kwargs)
		self.offset.rename(_sName + '_offset')

	def setParent(self, *args, **kwargs):
		return self.offset.setParent(*args, **kwargs)

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
		self.oParent = oRef.getParent()

	def Build(self, _bCreateGrpAnm=True, _bCreateGrpRig=True, *args, **kwargs):
		if _bCreateGrpAnm:
			self.oGrpAnm = pymel.createNode('transform', name=self.pNameMapAnm.Serialize(self.__class__.__name__.lower(), _sType='anm'))
		if _bCreateGrpRig:
			self.oGrpRig = pymel.createNode('transform', name=self.pNameMapRig.Serialize(self.__class__.__name__.lower(), _sType='rig'))

	def Unbuild(self):
		if self.oGrpAnm is not None:
			pymel.delete(self.oGrpAnm)
		if self.oGrpRig is not None:
			pymel.delete(self.oGrpRig)

#
# IK system
#
class CtrlIk(RigCtrl):
	kAttrName_State = 'ikFk'
	def __init__(self, *args, **kwargs):
		super(CtrlIk, self).__init__(*args, **kwargs)

		pymel.addAttr(self.node, longName=self.kAttrName_State)
		self.m_attState = getattr(self.node, self.kAttrName_State)

class CtrlIkSwivel(RigCtrl):
	pass # Todo: Implement custom shape

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
		
		self.oIkHandle, oIkEffector = pymel.ikHandle(startJoint=oChainS, endEffector=oChainE, solver='ikRPsolver')
		self.oIkHandle.rename(self.pNameMapRig.Serialize('ikHandle'))
		self.oIkHandle.setParent(oChainRoot)
		oIkEffector.rename(self.pNameMapRig.Serialize('ikEffector'))

		# Create ctrls
		self.oCtrlIK = CtrlIk()
		self.oCtrlIK.setParent(self.oGrpAnm)
		self.oCtrlIK.rename(self.pNameMapAnm.Serialize('ik'))
		self.oCtrlIK.setMatrix(oChainE.getMatrix(worldSpace=True), worldSpace=True)

		self.oCtrlSwivel = CtrlIkSwivel()
		self.oCtrlSwivel.setParent(self.oGrpAnm)
		self.oCtrlSwivel.rename(self.pNameMapAnm.Serialize('ikSwivel'))
		self.oCtrlSwivel.setMatrix(self.aInput[self.iCtrlIndex-1].getMatrix(worldSpace=True), worldSpace=True)

		# Connect rig -> anm
		pymel.pointConstraint(self.oCtrlIK, self.oIkHandle)
		pymel.orientConstraint(self.oCtrlIK, oChainE)
		pymel.poleVectorConstraint(self.oCtrlSwivel, self.oIkHandle)

		# Connect stretch
		if self.bStretch is True:
			# Compute safeDistance (maximum chain length without stretch)
			fSafeDistance = 0
			for oInput in self.aInput[1:self.iCtrlIndex+1]:
				fSafeDistance += oInput.t.get().length()

			attChainDistance = CreateUtilityNode('distanceBetween', inMatrix1=oChainRoot.worldMatrix, inMatrix2=self.oCtrlIK.worldMatrix).distance
			attStretch = CreateUtilityNode('multiplyDivide', operation=2, input1X=attChainDistance, input2X=fSafeDistance).outputX
			attStretch = CreateUtilityNode('condition', operation=2, firstTerm=attStretch, secondTerm=1.0, colorIfTrueR=attStretch, colorIfFalseR=1.0).outColorR # GreaterThan
			for oInput in self.aInput[1:self.iCtrlIndex+1]:
				attNewPos = CreateUtilityNode('multiplyDivide', input1=oInput.t.get(), input2X=attStretch, input2Y=attStretch, input2Z=attStretch).output
				pymel.connectAttr(attNewPos, oInput.t)

		# Connect to parent
		if self.oParent is not None:
			pymel.parentConstraint(self.oParent, oChainRoot, maintainOffset=True)

#
# FK system
#
class CtrlFk(RigCtrl):
	def __createNode__(self, *args, **kwargs):
		n = pymel.circle(*args, **kwargs)[0]
		oMake = n.getShape().create.inputs()[0]
		oMake.degree.set(1)
		oMake.sections.set(4)
		oMake.normalX.set(1); oMake.normalY.set(0); oMake.normalZ.set(0)
		return n

class FK(RigPart):
	def Build(self, _bConstraint=True, *args, **kwargs):
		super(FK, self).Build(_bCreateGrpRig=False, *args, **kwargs)

		# Create ctrl chain
		self.aCtrls = []
		for oInput in self.aInput:
			oCtrl = CtrlFk(name=NameMap(oInput).Serialize('fk', _sType='anm'))
			oCtrl.setMatrix(oInput.getMatrix(worldSpace=True), worldSpace=True)
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
		if self.oParent is not None:
			pymel.parentConstraint(self.oParent, self.oGrpAnm, maintainOffset=True)

#
# Arm system
#
class Arm(RigPart):
	kAttrName_State = 'fkIk' # The name of the IK/FK attribute

	def Build(self, *args, **kwargs):
		super(Arm, self).Build(*args, **kwargs)

		# Create attribute holder (this is where the IK/FK attribute will be stored)
		oAttHolder = RigCtrl(name=self.pNameMapAnm.Serialize('atts'))
		oAttHolder.setParent(self.oGrpAnm)
		pymel.addAttr(oAttHolder, longName=self.kAttrName_State, hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=1, k=True)
		attState = oAttHolder.attr(self.kAttrName_State)

		# Create ikChain and fkChain
		aIkChain = pymel.duplicate(self.aInput, renameChildren=True)
		for oInput, oIk, in enumerate(aIkChain):
			pNameMap = NameMap(oInput, _sType='rig')
			oIk.rename(pNameMap.Serialize('ik'))
		aIkChain[0].setParent(self.oParent) # Trick the IK system (temporary solution)

		# Rig ikChain and fkChain
		self.sysIK = IK(aIkChain); self.sysIK.Build()
		self.sysFK = FK(self.aInput); self.sysFK.Build(_bConstraint=False)
		self.sysIK.oGrpAnm.setParent(self.oGrpAnm)
		self.sysIK.oGrpRig.setParent(self.oGrpRig)
		self.sysFK.oGrpAnm.setParent(self.oGrpAnm)
		#self.sysFK.oGrpRig.setParent(self.oGrpRig)

		# Blend ikChain with fkChain
		for oInput, oIk, oFk in zip(self.aInput, aIkChain, self.sysFK.aCtrls):
			oConstraint = pymel.parentConstraint(oIk, oFk, oInput)
			attIkWeight, attFkWeight = oConstraint.getWeightAliasList()
			pymel.connectAttr(attState, attIkWeight)
			pymel.connectAttr(CreateUtilityNode('reverse', inputX=attIkWeight).outputX, attFkWeight)

		# Create ikFkNetwork
		self.CreateIkFkNetwork()

	def CreateIkFkNetwork(self):
		# Create ikFkNetwork (used for the ikFkSwitch script)
		oIkFkNetwork = pymel.createNode('network')
		pymel.addAttr(oIkFkNetwork, longName='ctrlIk', at='message')
		pymel.addAttr(oIkFkNetwork, longName='ctrlSwivel', at='message')
		pymel.addAttr(oIkFkNetwork, longName='ctrlsFk', multi=True, at='message')
		pymel.addAttr(oIkFkNetwork, longName='state')
		pymel.addAttr(oIkFkNetwork, longName='ctrlsOthers', multi=True, at='message')
		pymel.addAttr(oIkFkNetwork, longName='jnts', multi=True, at='message')

		pymel.connectAttr(self.sysIK.oCtrlIK.message, oIkFkNetwork.ctrlIk)
		pymel.connectAttr(self.sysIK.oCtrlSwivel.message, oIkFkNetwork.ctrlSwivel)
		for oCtrlFk, attNetwork in zip(self.sysFK.aCtrls, oIkFkNetwork.ctrlsOthers): 
			pymel.connectAttr(oCtrlFk.message, attNetwork)
		pymel.connectAttr(self.sysIK.oCtrlIK.m_attState, oIkFkNetwork.state)
		for oJnt, attNetwork in zip(self.aInput, oIkFkNetwork.ctrlsOthers):
			pymel.connectAttr(oJnt.message, )

#
# Leg system
#

class Leg(Arm):
	def __init__(self, *args, **kwargs):
		super(Leg, self).__init__(*args, **kwargs)

	def Build(self, *args, **kwargs):
		super(Leg, self).Build(*args, **kwargs)
		self.CreateFootRoll()

	def CreateFootRoll(self):
		# Create FootRoll
		tmFoot = self.aInput[self.iCtrlIndex].getMatrix(worldSpace=True)
		tmToes = self.aInput[self.iCtrlIndex+1].getMatrix(worldSpace=True)

		fOffsetF = 10
		fOffsetB = 2.5

		# Create pivots; TODO: Create side pivots
		oPivotM = RigNode(name=self.pNameMapRig.Serialize('pivotM'))
		oPivotM.setMatrix(tmToes)

		oPivotT = RigNode(name=self.pNameMapRig.Serialize('pivotF'))
		oPivotT.setMatrix(pymel.datatypes.Matrix(1,0,0,0,0,1,0,0,0,0,1,0, fOffsetF,0,0, 1) * tmFoot)

		oPivotB = RigNode(name=self.pNameMapRig.Serialize('pivotB'))
		oPivotB.setMatrix(pymel.datatypes.Matrix(1,0,0,0,0,1,0,0,0,0,1,0, -fOffsetB,0,0, 1) * tmFoot)

		# Create hyerarchy
		oPivotM.setParent(oPivotT)
		oPivotT.setParent(oPivotB)
		oPivotB.setParent(self.oGrpRig)
		pymel.parentConstraint(self.sysIK.oCtrlIK, oPivotB, maintainOffset=True)
		pymel.delete([o for o in self.sysIK.oIkHandle.getChildren() if isinstance(o, pymel.nodetypes.Constraint)])
		pymel.pointConstraint(oPivotM, self.sysIK.oIkHandle, maintainOffset=True)
		
		# Create attributes
		pymel.addAttr(self.sysIK.oCtrlIK, longName='footRoll')
		pymel.connectAttr(self.sysIK.oCtrlIK.footRoll, oPivotM.rotateX)

#
# Pre/Post Rigging
#

def PreRigging():
	pass

class CtrlRoot(RigCtrl):
	def __init__(self, *args, **kwargs):
		super(CtrlRoot, self).__init__(_bOffset=False, *args, **kwargs)

	def __createNode__(self, *args, **kwargs):
		uNode = pymel.circle(*args, **kwargs)[0]

		# Add a globalScale attribute to replace the sx, sy and sz.
		pymel.addAttr(uNode, longName='globalScale')
		pymel.connectAttr(uNode.globalScale, uNode.sx)
		pymel.connectAttr(uNode.globalScale, uNode.sy)
		pymel.connectAttr(uNode.globalScale, uNode.sz)
		uNode.s.set(channelBox=False)

		return uNode

def PostRigging():
	aAllCtrls = filter(lambda x: x.getParent() is None, iter(pymel.ls('anm_*')))
	oGrpCtrls = CtrlRoot(name='anm_root')
	for oCtrl in aAllCtrls: 
		oCtrl.setParent(oGrpCtrls)

	aAllJnts = filter(lambda x: x.getParent() is None, iter(pymel.ls('jnt_*')))
	oGrpJnts = RigNode(name='jnt_ALL')
	for oJnt in aAllJnts:
		oJnt.setParent(oGrpJnts)

	aAllRigs = filter(lambda x: x.getParent() is None, iter(pymel.ls('rig_*')))
	oGrpRigs = RigNode(name='rig_ALL')
	for oRig in aAllRigs:
		oRig.setParent(oGrpRigs)
	
	#oGrpCtrls.setParent(oCtrlRoot)
	#oGrpJnts.setParent(oCtrlRoot)
