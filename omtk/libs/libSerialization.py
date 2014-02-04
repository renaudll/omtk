import pymel.core as pymel
import logging as _logging
logging = _logging.getLogger()
logging.setLevel(_logging.WARNING)
import sys

def _getClassDef(_clsName, _baseclass=object):
    try:
        for cls in _baseclass.__subclasses__():
            if cls.__name__ == _clsName:
                return cls
            else:
                t = _getClassDef(_clsName, _baseclass=cls)
                if t is not None:
                    return t
    except Exception, e:
        logging.info(str(e)) # TODO: FIX
    return None

def _createClassInstance(_clsName):
    cls = _getClassDef(_clsName)

    if cls is None:
        logging.warning("Can't find class definition '{0}'".format(_clsName));
        return None

    try:
        return getattr(sys.modules[cls.__module__], cls.__name__)()
    except Exception, e:
        logging.error("Fatal error creating '{0}' instance: {1}".format(_clsName, str(e)))
        return None

def _getClassNamespace(_cls):
    if not isinstance(_cls, object):
        return None # Todo: throw exception
    tokens = []
    while (not _cls is object):
        tokens.append(_cls.__name__)
        _cls = _cls.__bases__[0]
    return '.'.join(reversed(tokens))

# We consider a data complex if it's a class instance.
# Note: We check for __dict__ because isinstance(_data, object) return True for basic types.
def _isDataComplex(_data):
    return hasattr(_data, '__dict__') or isinstance(_data, dict)

def _isDataBasic(_data):
    aTypes = [int, float, basestring, bool]#, pymel.datatypes.Matrix]
    return any(filter(lambda x: isinstance(_data, x), (iter(aTypes))))

def _isDataList(_data):
    aTypes = [list, tuple]
    return any(filter(lambda x: isinstance(_data, x), (iter(aTypes))))

def _isDataDagNode(_data):
    return isinstance(_data, pymel.general.PyNode)
    #return hasattr(_data, '__melobject__')

def getDataType(_data, *args, **kwargs):
    if _isDataList(_data, *args, **kwargs):
        logging.debug('{0} is a list'.format(_data))
        return 'list'
    elif _isDataDagNode(_data, *args, **kwargs):
        logging.debug('{0} is a dagNode'.format(_data))
        return 'dagNode'
    elif _isDataComplex(_data, *args, **kwargs):
        logging.debug('{0} is complex'.format(_data))
        return 'complex'
    elif _isDataBasic(_data, *args, **kwargs):
        logging.debug('{0} is basic'.format(_data))
        return 'basic'
    else:
        logging.warning('{0} is unknow type'.format(_data))
        return None
#
# Maya Metanetwork Serialization
#

def _getAttArgs(_val):
    if isinstance(_val, basestring):
        return {'dt':'string'}
    kType = type(_val)
    if issubclass(kType, bool):
        return {'at':'bool'}
    if issubclass(kType, int):
        return {'at':'long'}
    if issubclass(kType, float):
        return {'at':'double'}
    if isinstance(_val, dict):
        return {'at':'message'}
    if isinstance(kType, list) or isinstance(type, tuple):
        return {'at':'message'}
    if isinstance(kType, pymel.datatypes.Matrix):
        return {'dt':'matrix'}
    if issubclass(kType, pymel.Attribute):
        return _getAttArgs(_val.get())
    if hasattr(_val, '__melobject__'): # TODO: Really usefull?
        return {'at':'message'}    
    if hasattr(_val, '__dict__'):
        return {'at':'message'}
    return None

def _addNetworkAttr(_oNode, _sName, _pValue):
    logging.debug('AddNetworkAttribute {0} {1}'.format(_sName, _pValue))

    sType = getDataType(_pValue)

    # Skip empty list
    bIsMulti = sType == 'list'
    if bIsMulti and len(_pValue) == 0:
        return

    # Get attribute arguments
    _sType = _getAttArgs(_pValue) if not bIsMulti else _getAttArgs(_pValue[0])
    if _sType is None:
        logging.error("Can't add attribute {0} '{1}', unreconised attr type {3} for value {2}".format(_oNode, _sName, _pValue, type(_pValue)))
        return

    # Add attribute
    pymel.addAttr(_oNode, longName=_sName, niceName=_sName, multi=bIsMulti, keyable=True, **_sType)
    pAttribute = _oNode.attr(_sName)
    _setNetworkAttribute(pAttribute, _pValue)

    return pAttribute

def _setNetworkAttribute(_att, _val):
    logging.debug('setNetworkAttribute', _att, _val)
    sType = getDataType(_val)
    if sType == 'list':
        for i in range(len(_val)):
            if _val[i] is not None:
                _setNetworkAttribute(_att[i], _val[i])

    elif sType == 'dagNode':
        # pymel.Attribute
        if isinstance(_val, pymel.Attribute):
            pymel.connectAttr(_val, _att)
        # pymel.PyNode
        elif hasattr(_val, 'exists'):
            if _val.exists():
                pymel.connectAttr(_val.message, _att)
        # other pymel types, matrix and shitz
        else:
            _att.set(_val)

    elif sType == 'complex':
        uSubNode = exportToNetwork(_val)
        pymel.connectAttr(uSubNode.message, _att)

    elif sType == 'basic':
        _att.set(_val)

    else:
        pass
        #logging.exception('Unreconised data type {0} {1}'.format(sType, _val))
        #raise AttributeError

def _getNetworkAttr(_att):
    # Recursive
    if _att.isMulti():
        return [_getNetworkAttr(_att.elementByPhysicalIndex(i)) for i in range(_att.numElements())]

    if _att.type() == 'message':
        if not _att.isConnected():
            logging.warning('[_getNetworkAttr] Un-connected message attribute, skipping {0}'.format(_att))
            return None
        oInput = _att.inputs()[0]
        # Network
        if hasattr(oInput, '_class'):
            return importFromNetwork(oInput)
        # Node
        else:
            return oInput

    # pymel.Attribute
    if _att.isConnected():
        return _att.inputs(plugs=True)[0]

    # Basic type
    return _att.get()
#
# Pubic methods
#

def exportToBasicData(_data, _bSkipNone=True, _bRecursive=True, **args):
    #logging.debug('[exportToBasicData]', _data)

    sType = getDataType(_data)
    # object instance
    if sType == 'complex':
        dicReturn = {}
        dicReturn['_class'] = _getClassNamespace(_data.__class__)
        dicReturn['_uid'] = id(_data)
        for key, val in (_data.items() if isinstance(_data, dict) else _data.__dict__.items()): # TODO: Clean
            if '_' not in key[0]:
                if not _bSkipNone or val is not None:
                    if (sType == 'complex' and _bRecursive is True) or sType == 'list':
                        val = exportToBasicData(val, _bSkipNone=_bSkipNone, _bRecursive=_bRecursive, **args)
                    if not _bSkipNone or val is not None:
                        dicReturn[key] = val

        return dicReturn

    # Handle other types of data
    elif sType == 'basic':
        return _data

    # Handle iterable
    elif sType == 'list':
        return [exportToBasicData(v, _bSkipNone=_bSkipNone, **args) for v in _data if not _bSkipNone or v is not None]

    elif sType == 'dagNode':
        return _data

    logging.warning("[exportToBasicData] Unsupported type {0} for {1}".format(sType, _data))
    return None

def importToBasicData(_data, **args):
    if isinstance(_data, dict) and '_class' in _data:
        # Handle Serializable object
        clsName = _data['_class'].split('.')[-1]
        instance = _createClassInstance(clsName)
        if not isinstance(instance, object):
            # TODO: Log error
            return None
        for key, val in _data.items():
            if key != '_class':
                instance.__dict__[key] = importToBasicData(val, **args)
        return instance
    # Handle array
    elif _isDataList(_data):
        return [importToBasicData(v, **args) for v in _data]
    # Handle other types of data
    else:
        return _data

def exportToNetwork(_data, _network=None, **kwargs):
    logging.debug('CreateNetwork {0}'.format(_data))
    # Convert _pData to basic data dictionary (recursive for now)
    dicData = exportToBasicData(_data, _bRecursive=False, **kwargs)

    if not isinstance(dicData, dict):
        logging.error("[createNetwork] Invalid data, excepted dict, got {0}".format(type(_data))); return False

    # Automaticly name network whenever possible
    if hasattr(_data, '__getNetworkName__') and _data.__getNetworkName__ is None: 
        networkName = _data.__class__.__name__
    else:
        networkName = _data.__getNetworkName__() if hasattr(_data, '__getNetworkName__') else _data.__class__.__name__
    
    network = pymel.createNode('network', name=networkName)
    for key, val in dicData.items():
        if val is not None:
            if key == '_class' or key[0] != '_': # Attributes starting with '_' are protected or private
                _addNetworkAttr(network, key, val)

    return network

def importFromNetwork(_network):
    if not _network.hasAttr('_class'):
        logging.error('[importFromNetwork] Network dont have mandatory attribute _class')
        raise AttributeError

    cls = _network.getAttr('_class').split('.')[-1]
    obj = _createClassInstance(cls)
    if obj is None:
        return None

    for key in pymel.listAttr(_network, userDefined=True):
        if '_' != key[0]: # Variables starting with '_' are private
            logging.debug('Importing attribute {0} from {1}'.format(key, _network.name()))
            val = _getNetworkAttr(_network.attr(key))
            #if hasattr(obj, key):
            setattr(obj, key, val)
            #else:
            #    logging.debug("Can't set attribute {0} to {1}, attribute does not exists".format(key, obj))

    return obj


def isNetworkInstanceOfClass(_network, _clsName):
    return hasattr(_network, '_class') and _clsName in _network._class.get().split('.')

def getNetworksByClass(_clsName):
    return [network for network in pymel.ls(type='network') if isNetworkInstanceOfClass(network, _clsName)]

# TODO: benchmark with sets
def getConnectedNetworks(_objs, key=None, recursive=True, inArray=[]):
    if not hasattr(_objs, '__iter__'):
        _objs = [_objs]

    for obj in _objs:
        if hasattr(obj, 'message'):
            for output in obj.message.outputs():
                if isinstance(output, pymel.nodetypes.Network):
                    if output not in inArray:
                        if key is None or key(output):
                            inArray.append(output)
                        if recursive:
                            getConnectedNetworks(output, key=key, recursive=recursive, inArray=inArray)
    return inArray
