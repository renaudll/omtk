import pymel.core as pymel
import logging
from classSerializable import Serializable
from classRigPart import RigPart
from classRigCtrl import RigCtrl
from classRigNode import RigNode

class CtrlRoot(RigCtrl):
	def __init__(self, *args, **kwargs):
		super(CtrlRoot, self).__init__(_bOffset=False, *args, **kwargs)

	def __createNode__(self, *args, **kwargs):
		uNode = pymel.circle(*args, **kwargs)[0]
		oMake = uNode.getShape().create.inputs()[0]
		oMake.radius.set(10)
		oMake.normal.set((0,1,0))

		# Add a globalScale attribute to replace the sx, sy and sz.
		pymel.addAttr(uNode, longName='globalScale', k=True, defaultValue=1.0)
		pymel.connectAttr(uNode.globalScale, uNode.sx)
		pymel.connectAttr(uNode.globalScale, uNode.sy)
		pymel.connectAttr(uNode.globalScale, uNode.sz)
		uNode.s.set(lock=True, channelBox=False)

		return uNode

class RigRoot(Serializable):
	def __init__(self):
		self.SetAttrPublic('aChildrens', [])

	def AddPart(self, _part):
		if not isinstance(_part, RigPart):
			logging.error("[RigRoot:AddPart] Invalid RigPart '{0}' provided".format(_part))
		self.aChildrens.append(_part)

	def Build(self, *args, **kwargs):
		self.PreBuild()
		for children in self.aChildrens:
			children.Build(*args, **kwargs)
		self.PostBuild()

	def PreBuild(self):
		pass

	def PostBuild(self):
		# Group everything
		aAllCtrls = filter(lambda x: x.getParent() is None, iter(pymel.ls('anm*')))
		oGrpAnms = CtrlRoot(name='anm_root')
		for oCtrl in aAllCtrls: 
			oCtrl.setParent(oGrpAnms)

		aAllRigs = filter(lambda x: x.getParent() is None, iter(pymel.ls('rig*')))
		oGrpRigs = RigNode(name='rigs')
		for oRig in aAllRigs:
			oRig.setParent(oGrpRigs)

		aAllJnts = filter(lambda x: x.getParent() is None, iter(pymel.ls('jnt*')))
		oGrpJnts = RigNode(name='jnts')
		oGrpJnts.setParent(oGrpRigs)
		for oJnt in aAllJnts:
			oJnt.setParent(oGrpJnts)

		aAllGeos = filter(lambda x: x.getParent() is None, iter(pymel.ls('geo*')))
		oGrpGeos = RigNode(name='geos')
		for oGeo in aAllGeos:
			oGeo.setParent(oGrpGeos)

		# Setup displayLayers
		oLayerAnm = pymel.createDisplayLayer(name='layer_anm', number=1, empty=True)
		pymel.editDisplayLayerMembers(oLayerAnm, oGrpAnms)
		oLayerAnm.color.set(17) # Yellow

		oLayerRig = pymel.createDisplayLayer(name='layer_rig', number=1, empty=True)
		pymel.editDisplayLayerMembers(oLayerRig, oGrpRigs)
		oLayerRig.color.set(13) # Red
		oLayerRig.visibility.set(0) # Hidden
		oLayerRig.displayType.set(2) # Frozen

		oLayerGeo = pymel.createDisplayLayer(name='layer_geo', number=1, empty=True)
		pymel.editDisplayLayerMembers(oLayerGeo, oGrpGeos)
		oLayerGeo.color.set(12) # Green?
		oLayerGeo.displayType.set(2) # Frozen
