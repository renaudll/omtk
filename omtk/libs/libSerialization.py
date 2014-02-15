import pymel.core as pymel
from maya import OpenMaya, mel
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

def _createAttribute(_name, _val):
    if isinstance(_val, basestring):
        fn = OpenMaya.MFnTypedAttribute()
        fn.create(_name, _name, OpenMaya. MFnData.kString)
        return fn
    kType = type(_val)
    if issubclass(kType, bool):
        fn = OpenMaya.MFnNumericAttribute()
        fn.create(_name, _name, OpenMaya.MFnNumericData.kBoolean)
        return fn
    if issubclass(kType, int):
        fn = OpenMaya.MFnNumericAttribute()
        fn.create(_name, _name, OpenMaya.MFnNumericData.kInt)
        return fn
    if issubclass(kType, float):
        fn = OpenMaya.MFnNumericAttribute()
        fn.create(_name, _name, OpenMaya.MFnNumericData.kFloat)
        return fn
    if isinstance(_val, dict):
        fn = OpenMaya.MFnMessageAttribute()
        fn.create(_name, _name)
        return fn
    if isinstance(_val, list) or isinstance(type, tuple):
        if len(_val) < 1:
            pymel.warning("Can't create attribute {0}, empty array are unsuported".format(_name))
            return None
        # TODO: Throw error when the array have multiple types
        fn = _createAttribute(_name, _val[0])
        fn.setArray(True)
        return fn
    if isinstance(kType, pymel.datatypes.Matrix):
        fn = OpenMaya.MFnMatrixAttribute()
        fn.create(_name, _name)
        return fn
    if issubclass(kType, pymel.Attribute):
        return _createAttribute(_name, _val.get())
    if hasattr(_val, '__melobject__'): # TODO: Really usefull?
        fn = OpenMaya.MFnMessageAttribute()
        fn.create(_name, _name)
        return fn
    if hasattr(_val, '__dict__'):
        fn = OpenMaya.MFnMessageAttribute()
        fn.create(_name, _name)
        return fn

    pymel.error("Can't create MFnAttribute for {0} {1} {2}".format(_name, _val, kType))

def _addAttr(_fnDependNode, _sName, _pValue):
    logging.debug('AddNetworkAttribute {0} {1}'.format(_sName, _pValue))

    sType = getDataType(_pValue)

    # Skip empty list
    bIsMulti = sType == 'list'
    if bIsMulti and len(_pValue) == 0:
        return

    plug = None
    # Get attribute arguments
    try: # TODO: Is a try/catch really the best way to know if the plug exists?
        plug = _fnDependNode.findPlug(_sName)
    except:
        pass

    if plug is None:
        fnAtt = _createAttribute(_sName, _pValue)
        fnAtt.setNiceNameOverride(_sName)
        moAtt = fnAtt.object()
        if moAtt is not None:
            _fnDependNode.addAttribute(moAtt)
            plug = OpenMaya.MPlug(_fnDependNode.object(), moAtt)

    if plug is not None:
        _setAttr(plug, _pValue)

def _setAttr(_plug, _val):
    sType = getDataType(_val)
    if sType == 'list':
        iNumElements = len(_val)

        _plug.setNumElements(iNumElements) # TODO: MAKE IT WORK # TODO: NECESSARY???

        for i in range(iNumElements):
            _setAttr(_plug.elementByLogicalIndex(i), _val[i])

    elif sType == 'basic':
        # Basic types
        if isinstance(_val, bool):
            _plug.setBool(_val)
        elif isinstance(_val, int):
            _plug.setInt(_val)
        elif isinstance(_val, float):
            _plug.setFloat(_val)
        elif isinstance(_val, basestring):
            _plug.setString(_val)

    elif sType == 'complex':
        network = exportToNetwork(_val)
        plugMessage = network.__apimfn__().findPlug('message')

        # Use a dag modifier to connect the attribute. TODO: Is this really the best way?
        dagM = OpenMaya.MDagModifier()
        dagM.connect(plugMessage, _plug)
        dagM.doIt()

    elif sType == 'dagNode':
        plug = None
        if isinstance(_val, pymel.Attribute): # pymel.Attribute
            plug = _val.__apimfn__()
        elif hasattr(_val, 'exists'): # pymel.PyNode
            plug = _val.__apimfn__().findPlug('message')

        if plug is not None:
            dagM = OpenMaya.MDagModifier()
            dagM.connect(plug, _plug)
            dagM.doIt()
        else:
            pymel.error("Unknow 'dagNode' {0}".format(_val))

    else:
        print _val, sType
        raise NotImplementedError

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

def exportToNetwork(_data, **kwargs):
    logging.debug('CreateNetwork {0}'.format(_data))

    if hasattr(_data, '_network') and isinstance(_data._network, pymel.PyNode) and _data._network.exists():
        network = _data._network
    else:
        # Automaticly name network whenever possible
        if hasattr(_data, '__getNetworkName__') and _data.__getNetworkName__ is None: 
            networkName = _data.__class__.__name__
        else:
            networkName = _data.__getNetworkName__() if hasattr(_data, '__getNetworkName__') else _data.__class__.__name__
            _data._network = networkName
        
        network = pymel.createNode('network', name=networkName)

    # Convert _pData to basic data dictionary (recursive for now)
    dicData = exportToBasicData(_data, _bRecursive=False, **kwargs)
    assert(isinstance(dicData, dict))

    fnNet = network.__apimfn__()
    for key, val in dicData.items():
        if val is not None:
            if key == '_class' or key[0] != '_': # Attributes starting with '_' are protected or private
                _addAttr(fnNet, key, val)

    '''
    # If we're exporting part of an already-exported, connect it to the already-exported network
    if hasattr(_data, '_parent'):
        if hasattr(_data._parent, '_network'):     
            if hasattr(_data._parent, 'aChildrens'):
                plugMessage = fnNet.findPlug('message')
                plugSource = _data._parent._network.findPlug('aChildrens') # TODO: DON'T HARDCODE
                print plugMessage
                print plugSource
                pymel.warning("TODO: Connect {0} to parent {1}".format(_data, _data._parent))
            else:
                pymel.warning("{0} parent {1} doesnt support parenting", _data, _data._parent)
        else:
            pymel.warning("Can't connect to parent, {0} have to network, maybe re-export?".format(_data._parent))
    '''

    return network

def importFromNetwork(_network):
    if not _network.hasAttr('_class'):
        logging.error('[importFromNetwork] Network dont have mandatory attribute _class')
        raise AttributeError

    cls = _network.getAttr('_class').split('.')[-1]
    obj = _createClassInstance(cls)
    if obj is None:
        return None
    obj._network = _network

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
