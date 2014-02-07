import pymel.core as pymel

'''
This class is a pymel.PyNode wrapper that extent it's functionnality.
Note: We can't directly inherit from pymel.PyNode.
'''

class RigNode(object):
	def __init__(self, _pData=None, _create=False, *args, **kwargs):
		self.__dict__['node'] = _pData
		if _create is True:
			self.node = self.__createNode__(*args, **kwargs)
		#self.__dict__['node'] = self.__createNode__(*args, **kwargs) if _pData is None else pymel.PyNode(_pData, *args, **kwargs) # Prevent call to __setattr__

	#def __melobject__(self): # Mirror PyNode behavior
	#	return self.node.__melobject__()
	# Allow the programmer to manipulate a RigNode instance like a pymel.PyNode instance.

	def __getattr__(self, _sAttrName):
		if hasattr(self.__dict__['node'], _sAttrName):
			return getattr(self.__dict__['node'], _sAttrName)

	def __createNode__(self, *args, **kwargs):
		self.node = pymel.createNode('transform', *args, **kwargs)
		#self.fetchAttrs()

	def __deleteNode__(self, *args, **kwargs):
		self.holdAttrs()
		pymel.delete(self.node)
		self.node = None

	def holdAttrs(self):
		self.tx = self.node.tx if isinstance(self.node.tx, pymel.Attribute) else self.node.tx.get()
		self.ty = self.node.ty if isinstance(self.node.ty, pymel.Attribute) else self.node.ty.get()
		self.tz = self.node.tz if isinstance(self.node.tz, pymel.Attribute) else self.node.tz.get()
		self.rx = self.node.rx if isinstance(self.node.rx, pymel.Attribute) else self.node.rx.get()
		self.ry = self.node.ry if isinstance(self.node.ry, pymel.Attribute) else self.node.ry.get()
		self.rz = self.node.rz if isinstance(self.node.rz, pymel.Attribute) else self.node.rz.get()
		self.sx = self.node.sx if isinstance(self.node.sx, pymel.Attribute) else self.node.sx.get()
		self.sy = self.node.sy if isinstance(self.node.sy, pymel.Attribute) else self.node.sy.get()
		self.sz = self.node.sz if isinstance(self.node.sz, pymel.Attribute) else self.node.sz.get()

	def fetchAttrs(self):
		if isinstance(self.node.tx, pymel.Attribute): pymel.connectAttr(self.tx, self.node.tx)
		if isinstance(self.node.ty, pymel.Attribute): pymel.connectAttr(self.ty, self.node.ty)
		if isinstance(self.node.tz, pymel.Attribute): pymel.connectAttr(self.tz, self.node.tz)
		if isinstance(self.node.rx, pymel.Attribute): pymel.connectAttr(self.rx, self.node.rx)
		if isinstance(self.node.ry, pymel.Attribute): pymel.connectAttr(self.ry, self.node.ry)
		if isinstance(self.node.rz, pymel.Attribute): pymel.connectAttr(self.tr, self.node.rz)
		if isinstance(self.node.sx, pymel.Attribute): pymel.connectAttr(self.sx, self.node.sx)
		if isinstance(self.node.sy, pymel.Attribute): pymel.connectAttr(self.sy, self.node.sy)
		if isinstance(self.node.sz, pymel.Attribute): pymel.connectAttr(self.sr, self.node.sz)
