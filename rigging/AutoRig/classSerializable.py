import pymel.core as pymel
import logging

'''
This class handle the serialization of it's subclasses in multiples formats (ex: json, xml, maya nodes, etc)
'''
class Serializable(object):
	gClassToken = '_class'
	def SetAttrPublic(self, _sAttrName, _pAttrValue=None, _pAttrType=None):
		setattr(self, _sAttrName, _pAttrValue)

	def SetAttrPrivate(self, _sAttrName, _pAttrValue=None):
		setattr(self, _sAttrName, _pAttrValue)

	def Serialize(self):
		pass

	def Deserialize(self):
		pass

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

	# Return a filtered version of self.__dict__ that contain only basic values
	def __repr__(self, _recursive=True):
		dicReturn = {}
		for key, val in self.__dict__.items():
			if isinstance(val, Serializable):
				subval = val.__repr__() # Recursive call
				subval[self.gClassToken, self.__class__.__name__]
				dicReturn[key] = subval
			else:
				dicReturn[key] = val
		return dicReturn

	def __str__(self):
		return '<{0} serializable object>'.format(self.__class__.__name__)