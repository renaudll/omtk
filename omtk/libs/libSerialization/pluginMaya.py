import pymel.core as pymel
from maya import OpenMaya
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

import core

# Pymel compatibility implementation
core._basic_types.append(pymel.datatypes.Matrix)
core._dag_types.append(pymel.general.PyNode)

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
    if isinstance(kType, pymel.datatypes.Matrix): # HACK
        print '!!!!!'
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
    sType = core.getDataType(_pValue)

    # Skip empty list
    bIsMulti = sType == core.TYPE_LIST
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
    sType = core.getDataType(_val)
    if sType == core.TYPE_LIST:
        iNumElements = len(_val)

        _plug.setNumElements(iNumElements) # TODO: MAKE IT WORK # TODO: NECESSARY???

        for i in range(iNumElements):
            _setAttr(_plug.elementByLogicalIndex(i), _val[i])

    elif sType == core.TYPE_BASIC:
        # Basic types
        if isinstance(_val, bool):
            _plug.setBool(_val)
        elif isinstance(_val, int):
            _plug.setInt(_val)
        elif isinstance(_val, float):
            _plug.setFloat(_val)
        elif isinstance(_val, basestring):
            _plug.setString(_val)
        elif isinstance(_val, pymel.datatypes.Matrix):
            fn = OpenMaya.MFnMatrixData()
            mo = fn.create(_val.apicls(_val))
            _plug.setMObject(mo)

    elif sType == core.TYPE_COMPLEX:
        network = exportToNetwork(_val)
        plugMessage = network.__apimfn__().findPlug('message')

        # Use a dag modifier to connect the attribute. TODO: Is this really the best way?
        dagM = OpenMaya.MDagModifier()
        dagM.connect(plugMessage, _plug)
        dagM.doIt()

    elif sType == core.TYPE_DAGNODE:
        plug = None
        if isinstance(_val, pymel.Attribute): # pymel.Attribute
            # Hack: Don't crash with non-existent pymel.Attribute
            if not _val.exists():
                log.warning("Can't setAttr, Attribute {0} don't exist".format(_val))
                return
            plug = _val.__apimfn__()
        elif hasattr(_val, 'exists'): # pymel.PyNode
            # Hack: Don't crash with non-existent pymel.Attribute
            if not pymel.objExists(_val.__melobject__()):
                log.warning("Can't setAttr, PyNode {0} don't exist".format(_val))
                return
            plug = _val.__apimfn__().findPlug('message')

        if plug is not None:
            dagM = OpenMaya.MDagModifier()
            #if pymel.attributeQuery(pymel.Attribute(_val), writable=True):
            dagM.connect(plug, _plug)
            '''
            else:
                dagM.connect(_plug, plug)
            '''
            dagM.connect(plug, _plug)
            dagM.doIt()
        else:
            raise Exception("Unknow TYPE_DAGNODE {0}".format(_val))

    else:
        print _val, sType
        raise NotImplementedError

def _getNetworkAttr(_att):
    # Recursive
    if _att.isMulti():
        return [_getNetworkAttr(_att.elementByPhysicalIndex(i)) for i in range(_att.numElements())]

    if _att.type() == 'message':
        if not _att.isConnected():
            log.warning('[_getNetworkAttr] Un-connected message attribute, skipping {0}'.format(_att))
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

def exportToNetwork(_data, **kwargs):
    log.debug('CreateNetwork {0}'.format(_data))

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
    dicData = core.exportToBasicData(_data, _bRecursive=False, **kwargs)
    assert(isinstance(dicData, dict))

    fnNet = network.__apimfn__()
    for key, val in dicData.items():
        if val is not None:
            if key == '_class' or key[0] != '_': # Attributes starting with '_' are protected or private
                _addAttr(fnNet, key, val)

    return network

def importFromNetwork(_network):
    if not _network.hasAttr('_class'):
        log.error('[importFromNetwork] Network dont have mandatory attribute _class')
        raise AttributeError

    cls = _network.getAttr('_class').split('.')[-1]
    obj = core._createClassInstance(cls)
    if obj is None:
        return None
    obj._network = _network

    for key in pymel.listAttr(_network, userDefined=True):
        if '_' != key[0]: # Variables starting with '_' are private
            #logging.debug('Importing attribute {0} from {1}'.format(key, _network.name()))
            val = _getNetworkAttr(_network.attr(key))
            #if hasattr(obj, key):
            setattr(obj, key, val)
            #else:
            #    #logging.debug("Can't set attribute {0} to {1}, attribute does not exists".format(key, obj))

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
