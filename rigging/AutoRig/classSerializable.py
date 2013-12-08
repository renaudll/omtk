import pymel.core as pymel
import logging

def CreateSerializableClass():
	aSerializableClasses = [cls for cls in object.__subclasses__() if cls.__name__ == 'Serializable']
	if len(aSerializableClasses) > 0:
		return aSerializableClasses[-1]
	return None

def CreateClassInstanceByName(_name, _baseclass=None):
	if _baseclass is None: 
		_baseclass = CreateSerializableClass()

	if _baseclass is None:
		logging.error("[CreateClassInstanceByName] Can't find Serializable class"); return None

	for cls in _baseclass.__subclasses__():
		if cls.__name__ == _name:
			return cls()
		else:
			t = CreateClassInstanceByName(cls, _name)
			if t is not None:
				return t()
	return None

'''
This class handle the serialization of it's subclasses in multiples formats (ex: json, xml, maya nodes, etc)
'''
class Serializable(object):
	gClassToken = '_class'
	def SetAttrPublic(self, _sAttrName, _pAttrValue=None, _pAttrType=None):
		setattr(self, _sAttrName, _pAttrValue)

	def SetAttrPrivate(self, _sAttrName, _pAttrValue=None):
		setattr(self, _sAttrName, _pAttrValue)

	# Serialize self to a dictionary of basic values
	def __serialize__(self, _recursive=True):
		dicReturn = {}
		dicReturn[self.gClassToken] = self.__class__.__name__
		for key, val in self.__dict__.items():
			if hasattr(val, '__serialize__'): # Monkey patching
				subval = val.__serialize__() # Recursive call
				dicReturn[key] = subval
			elif key != self.gClassToken:
				dicReturn[key] = val
		return dicReturn

	# Serialize a dictionary of basic values to a dictionary
	def __deserialize__(self, _dic, _recursive=True):
		for key, val in _dic.items():
			if isinstance(val, dict) and self.gClassToken in val:
				pInstance = CreateClassInstanceByName(_dic[self.gClassToken])
				if pInstance is not None:
					pInstance = pInstance.__deserialize__(val)
					self.__dict__[key] = pInstance
			else: 
				self.__dict__[key] =  val
		return self

	def __createMayaNetwork__(self):
		return pymel.createNode('network', name=self.__class__.__name__)

	def ExportToMayaNetwork(self):
		oNetwork = self.__createMayaNetwork__()
		pymel.addAttr(oNetwork, longName=self.gClassToken, niceName=self.gClassToken, dt='string')
		oNetwork.attr(self.gClassToken).set(self.__class__.__name__)
		for key, val in self.__repr__(_recursive=False).items():
			if isinstance(val, Serializable):
				oSubNetwork = val.ExportToMayaNetwork()
				pymel.addAttr(oNetwork, longName=key, at='message')
				pymel.connectAttr(oSubNetwork.message, oNetwork.attr(key))
			else:
				dicArgsByType = {
					"<type 'int'>" : {'at':'short'},
					"<type 'float'>": { 'at':'float'},
					"<type 'string'>" : {'dt':'string'},
					"<type 'unicode'>" : {'dt':'string'}
				}
				valtype = str(type(val))
				if valtype in dicArgsByType:
					kwargs = dicArgsByType[valtype]
					pymel.addAttr(oNetwork, longName=key, niceName=key, k=False, **kwargs)
					oNetwork.attr(key).set(val)
				else:
					logging.info("Can't serialize {0} : {1}".format(key, val))
		return oNetwork

	def ImportFromMayaNetwork(self, oNetwork):
		raise NotImplemented
		'''
		attNames = oNetwork.listAttr(userDefined=True)
		for attName in attNames:
			if attName in self.__dict__(self):
		'''

	'''
	# Return a filtered version of self.__dict__ that contain only basic values
	def __repr__(self, _recursive=True):
		return self.__serialize(_recursive=_recursive)

	def __str__(self):
		return '<{0} serializable object>'.format(self.__class__.__name__)
	'''

'''
TODO: Find a solution for seamless pymel integration
def PymelSerialize(self, *args, **kwargs):

def PymelDeserialize(self, _pData, *args, **kwargs):
	return pymel.PyNode(_pData)

pymel.PyNode.__serialize__ = PymelSerialize
pymel.PyNode.__deserialize__ = PymelDeserialize
'''
