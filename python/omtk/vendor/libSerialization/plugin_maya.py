import pymel.core as pymel
from maya import OpenMaya
import sys
import logging
import core

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def is_valid_PyNode(val):
    return val and hasattr(val, 'exists') and val.exists()

__all__ = (
    'export_network',
    'import_network',
    'iter_connected_networks',
    'get_connected_networks',
    'iter_networks_from_class',
    'get_networks_from_class',
    'is_network_from_class'
)

# Pymel compatibility implementation
core.types_dag.append(pymel.PyNode)
core.types_dag.append(pymel.Attribute)
core.types_dag.append(pymel.datatypes.Matrix)
core.types_dag.append(pymel.datatypes.Vector)


#
# Maya Metanetwork Serialization
#

def _create_attr(name, data):
    """
    Factory method that create an OpenMaya.MFnAttribute object from an arbitrary instance.
    :param name: The name of the OpenMaya.MFnAttribute to create.
    :param data: The value used to determine the type of OpenMaya.MFnAttribute to create.
    :return: An OpenMaya.MFnAttribute subclass instance.
    """
    # (str, unicode) -> MFnTypedAttribute(kString)
    if isinstance(data, basestring):
        fn = OpenMaya.MFnTypedAttribute()
        fn.create(name, name, OpenMaya.MFnData.kString)
        return fn
    data_type = type(data)
    # (bool,) -> MFnNumericAttribute(kBoolean)
    if issubclass(data_type, bool):
        fn = OpenMaya.MFnNumericAttribute()
        fn.create(name, name, OpenMaya.MFnNumericData.kBoolean)
        return fn
    # (int,) -> MFnNumericData(kInt)
    if issubclass(data_type, int):
        fn = OpenMaya.MFnNumericAttribute()
        fn.create(name, name, OpenMaya.MFnNumericData.kInt)
        return fn
    # (float,) -> MFnNumericData(kFloat)
    if issubclass(data_type, float):
        fn = OpenMaya.MFnNumericAttribute()
        fn.create(name, name, OpenMaya.MFnNumericData.kFloat)
        return fn
    # (dict,) -> MFnMessageAttribute
    if isinstance(data, dict):
        fn = OpenMaya.MFnMessageAttribute()
        fn.create(name, name)
        return fn
    # (list, tuple,) -> arbitrary type depending on the list content.
    # Note contrary to python list, Maya lists are typed.
    # This will crash if the list contain multiple types at the same time.
    # However, the None value is supported.
    if isinstance(data, (list, tuple)):
        if len(data) < 1:
            pymel.warning("Can't create attribute {0}, empty array are unsuported".format(name))
            return None

        # Resolve the type
        # todo:raise an Exception if we find multiple types.
        iter_valid_values = (d for d in data if d is not None)
        ref_val = next(iter(iter_valid_values), None)

        # If the list only contain None values, don't create anything.
        if ref_val is None:
            return

        # todo: raise an exception if multiples types are in the same list. check performance impact.

        fn = _create_attr(name, ref_val)
        fn.setArray(True)
        return fn
    # (pymel.datatypes.Matrix,) -> MFnMatrixAttribute
    if issubclass(data_type, pymel.datatypes.Matrix):  # HACK
        fn = OpenMaya.MFnMatrixAttribute()
        fn.create(name, name)
        return fn
    # (pymel.datatypes.Vector,) -> MFnNumericAttribute(kDouble)
    if issubclass(data_type, pymel.datatypes.Vector):
        name_x = '{0}X'.format(name)
        name_y = '{0}Y'.format(name)
        name_z = '{0}Z'.format(name)
        fn = OpenMaya.MFnNumericAttribute()
        mo_x = fn.create(name_x, name_x, OpenMaya.MFnNumericData.kDouble)
        mo_y = fn.create(name_y, name_y, OpenMaya.MFnNumericData.kDouble)
        mo_z = fn.create(name_z, name_z, OpenMaya.MFnNumericData.kDouble)
        fn.create(name, name, mo_x, mo_y, mo_z)
        return fn
    # (pymel.general.Attribute,) -> arbitrary type depending on the attribute type itself.
    if issubclass(data_type, pymel.Attribute):
        if not is_valid_PyNode(data):
            log.warning("Can't serialize {0} attribute because of non-existent pymel Attribute!".format(name))
            return None
        elif data.type() == 'doubleAngle':
            fn = OpenMaya.MFnUnitAttribute()
            fn.create(name, name, OpenMaya.MFnUnitAttribute.kAngle)
            return fn
        elif data.type() == 'time':
            fn = OpenMaya.MFnUnitAttribute()
            fn.create(name, name, OpenMaya.MFnUnitAttribute.kTime)
            return fn
        # If the attribute doesn't represent anything special,
        # we'll check it's value to know what attribute type to create.
        else:
            return _create_attr(name, data.get())
    # (pymel.general.PyNode,) -> MFnMessageAttribute
    # The order is important here as if we hit this, we don't deal with a pymel.general.Attribute.
    # Note that by using duct-typing we support any 'pymel-like' behavior.
    if hasattr(data, '__melobject__'):  # TODO: Really usefull?
        fn = OpenMaya.MFnMessageAttribute()
        fn.create(name, name)
        return fn
    # (object,) -> MFnMessageAttribute
    if hasattr(data, '__dict__'):
        fn = OpenMaya.MFnMessageAttribute()
        fn.create(name, name)
        return fn

    pymel.error("Can't create MFnAttribute for {0} {1} {2}".format(name, data, data_type))

def _add_attr(fnDependNode, name, data, cache=None):
    data_type = core.get_data_type(data)

    # Skip empty list
    is_multi = data_type == core.TYPE_LIST
    if is_multi and len(filter(None, data)) == 0:
        return

    plug = None
    # Get attribute arguments
    try:  # TODO: Is a try/catch really the best way to know if the plug exists?
        plug = fnDependNode.findPlug(name)
    except:
        pass

    if plug is None:
        fnAtt = _create_attr(name, data)
        if fnAtt is None:
            return  # In case of invalid value like missing pymel PyNode & Attributes
        fnAtt.setNiceNameOverride(name)
        moAtt = fnAtt.object()
        if moAtt is not None:
            try:
                fnDependNode.addAttribute(moAtt)
                plug = OpenMaya.MPlug(fnDependNode.object(), moAtt)
            except Exception as e:
                log.warning('Error adding attribute {0}: {1}'.format(name, e))

    if plug is not None:
        _set_attr(plug, data, cache=cache)


def _set_attr(_plug, data, cache=None):
    data_type = core.get_data_type(data)
    if data_type == core.TYPE_LIST:
        num_elements = len(data)

        _plug.setNumElements(num_elements)  # TODO: MAKE IT WORK # TODO: NECESSARY???

        for i in range(num_elements):
            _set_attr(_plug.elementByLogicalIndex(i), data[i], cache=cache)

    elif data_type == core.TYPE_BASIC:
        # Basic types
        if isinstance(data, bool):
            _plug.setBool(data)
        elif isinstance(data, int):
            _plug.setInt(data)
        elif isinstance(data, float):
            _plug.setFloat(data)
        elif isinstance(data, basestring):
            _plug.setString(data)
            # pymel.Attribute(_plug).set(_val)

    elif data_type == core.TYPE_COMPLEX:
        network = export_network(data, cache=cache)
        plug = network.__apimfn__().findPlug('message')

        # Use a dag modifier to connect the attribute. TODO: Is this really the best way?
        dagM = OpenMaya.MDagModifier()
        dagM.connect(plug, _plug)
        dagM.doIt()

    elif data_type == core.TYPE_DAGNODE:
        plug = None
        if isinstance(data, pymel.Attribute):  # pymel.Attribute
            # Hack: Don't crash with non-existent pymel.Attribute
            if not data.exists():
                log.warning("Can't setAttr, Attribute {0} don't exist".format(data))
                return
            plug = data.__apimfn__()
        elif isinstance(data, pymel.datatypes.Matrix):
            fn = OpenMaya.MFnMatrixData()
            mo = fn.create(data.apicls(data))
            _plug.setMObject(mo)
            return True
        elif isinstance(data, pymel.datatypes.Vector):
            _plug.child(0).setFloat(data.x)
            _plug.child(1).setFloat(data.y)
            _plug.child(2).setFloat(data.z)
            return True
        elif hasattr(data, 'exists'):  # pymel.PyNode
            # Hack: Don't crash with non-existent pymel.Attribute
            if not pymel.objExists(data.__melobject__()):
                log.warning("Can't setAttr, PyNode {0} don't exist".format(data))
                return
            plug = data.__apimfn__().findPlug('message')

        if plug is not None:
            dagM = OpenMaya.MDagModifier()
            # if pymel.attributeQuery(pymel.Attribute(_val), writable=True):
            dagM.connect(plug, _plug)
            dagM.connect(plug, _plug)  # is connecting two times necessary?
            dagM.doIt()
        else:
            raise Exception("Unknow TYPE {0}, {1}".format(type(data), data))
    elif data_type == core.TYPE_NONE:
        return

    else:
        print data, data_type
        raise NotImplementedError


def _get_network_attr(attr, fn_skip=None, cache=None):
    # Recursive
    if attr.isMulti():
        attr_indices = attr.getArrayIndices()
        # Empty array
        if not attr_indices:
            return []
        num_logical_elements = max(attr_indices)+1
        return [_get_network_attr(attr.elementByLogicalIndex(i), fn_skip=fn_skip, cache=cache) for i in range(num_logical_elements)]

    if attr.type() == 'message':
        if not attr.isConnected():
            #log.warning('[_getNetworkAttr] Un-connected message attribute, skipping {0}'.format(attr))
            return None
        attr_input = attr.inputs()[0]
        # Network
        if hasattr(attr_input, '_class'):
            return import_network(attr_input, fn_skip=fn_skip, cache=cache)
        # Node
        else:
            return attr_input

    # pymel.Attribute
    if attr.isConnected():
        return attr.inputs(plugs=True)[0]

    # Basic type
    return attr.get()

_export_network_key_whitelist = ['_class', '_class_module', '_class_namespace']
def _can_export_attr_by_name(name):
    """
    Determine what attribute can be exported to a network.
    All key that start with an underscore are considered private and won't be exported.
    The reserved keyword and automatically excempted from this rule.
    """
    if name in _export_network_key_whitelist:
        return True

    if name[0] == '_':
        return False

    return True

def export_network(data, cache=None, **kwargs):
    if cache is None:
        from cache import Cache
        cache = Cache()
    #log.debug('CreateNetwork {0}'.format(data))

    # We'll deal with two additional attributes, '_network' and '_uid'.
    # Thoses two attributes allow us to find the network from the value and vice-versa.
    # Note that since the '_uid' refer to the current python context,
    # it's value could be erroned when calling import_network.
    # However the change of collisions are extremely improbable so checking the type of the python variable
    # is sufficient.
    # Please feel free to provide a better design if any if possible.

    # todo: after refactoring, the network cache will be merged with the import cache
    data_id = id(data)
    result = cache.get_network_by_id(data_id)
    if result is not None:
        return result

    # Create network
    # Optimisation: Use existing network if already present in scene
    #if hasattr(data, '_network') and is_valid_PyNode(data._network):
    #    network = data._network
    #else:
    # Automaticly name network whenever possible
    try:
        network_name = data.__getNetworkName__()
    except (AttributeError, TypeError):
        network_name = data.__class__.__name__

    network = pymel.createNode('network', name=network_name)

    # Monkey patch the network in a _network attribute if supported.
    if isinstance(data, object) and not isinstance(data, dict):
        data._network = network

    # Ensure the network have the current python id stored
    if not network.hasAttr('_uid'):
        pymel.addAttr(network, longName='_uid', niceName='_uid', at='long')  # todo: validate attributeType
    # network._uid.set(id(_data))

    # Cache as soon as possible since we'll use recursivity soon.
    cache.set_network_by_id(data_id, network)

    # Convert _pData to basic data dictionary (recursive for now)
    data_dict = core.export_dict(data, recursive=False, cache=cache, **kwargs)
    assert (isinstance(data_dict, dict))

    fnNet = network.__apimfn__()
    for key, val in data_dict.items():
        if _can_export_attr_by_name(key):
            _add_attr(fnNet, key, val, cache=cache)

    return network


def import_network(network, fn_skip=None, cache=None, **kwargs):
    """
    Recursively create class instances from provided network.
    :param network: The network to read from.
    :param fn_skip: A function taken a pymel.nodetypes.Network as argument that return True if we need to ignore a specific network.
    :param cache: Used internally.
    :return: An object instance corresponding to the provided network.
    """
    if cache is None:
        from cache import Cache
        cache = Cache()

    # Duck-type the network, if the '_class' attribute exist, it is a class instance representation.
    # Otherwise it is a simple pymel.PyNode datatypes.
    if not network.hasAttr('_class'):
        return network

    network_id = hash(network)

    # Check if the object related to the network already exist in the cache and return it if found
    cached_obj = cache.get_import_value_by_id(network_id)
    if cached_obj is not None:
        return cached_obj

    # Check if the object is blacklisted. If it is, we'll still add it to the cache in case we encounter it again.
    if fn_skip and fn_skip(network):
        cache.set_import_value_by_id(network_id, None)
        return None

    cls_name = network.getAttr('_class')

    # HACK: Previously we were storing the complete class namespace.
    # However this was not very flexible when we played with the class hierarchy.
    # If we find a '_class_module' attribute, it mean we are doing thing the new way.
    # Otherwise we'll let it slip for now.
    cls_module = network.getAttr('_class_module') if network.hasAttr('_class_module') else None
    if cls_module:
        cls_def = cache.get_class_by_name(cls_name, module_name=cls_module)
    else:
        cls_def = cache.get_class_by_namespace(cls_name)

    if cls_def is None:
        log.warning("Can't find class definiton for {0}. Returning None".format(cls_name))
        return None

    # HACK: Get latest definition
    cls_def = getattr(sys.modules[cls_def.__module__], cls_def.__name__)
    obj = cls_def()

    # Monkey patch the network if supported
    if isinstance(obj, object) and not isinstance(obj, dict):
        obj._network = network

    # Fill the import cache to make sure that self reference doesn't try to infinitly loop in it's import
    cache.set_import_value_by_id(network_id, obj)

    # Resolve wich attribute we'll want to import
    attrs_by_longname = {}
    for attr_name in pymel.listAttr(network, userDefined=True):
        if '_' != attr_name[0]:  # Attribute longName starting with '_' are considered private
            attrs_by_longname[attr_name] = network.attr(attr_name)

    # Filter compound children as we are only interested the compound value itself.
    # ex: import translate and skip translateX, translateY, translateZ
    for attr in attrs_by_longname.values():
        if attr.isCompound():
            for child in attr.getChildren():
                child_longname = child.longName()
                try:
                    attrs_by_longname.pop(child_longname)
                except KeyError:
                    pass

    for attr_name, attr in attrs_by_longname.iteritems():
        # logging.debug('Importing attribute {0} from {1}'.format(key, _network.name()))
        val = _get_network_attr(attr, fn_skip=fn_skip, cache=cache)
        # if hasattr(obj, key):
        if isinstance(obj, dict):
            obj[attr_name.longName()] = val
        else:
            setattr(obj, attr_name, val)
        # else:
        #    #logging.debug("Can't set attribute {0} to {1}, attribute does not exists".format(key, obj))

        # Update network _uid to the current python variable context
        #    if _network.hasAttr('_uid'):
        #        _network._uid.set(id(obj))

    # Hack: Find implemented class via duck-typing
    # Implement a __callbackNetworkPostBuild__ method in your class instances as a callback.
    try:
        obj.__callbackNetworkPostBuild__()
    except (AttributeError, TypeError):
        pass

    return obj


def is_network_from_class(net, cls_name):
    """
    Inspect a potentially serialized pymel.nodetypes.Network and check if
    if was created from a specific class instance.
    :param net: A pymel.nodetypes.Network to inspect.
    :param cls_name: A string representing a class name.
    :return:
    """
    # HACK: Backward compatibility with the old system.
    # Previously the full namespace was stored in the '_class' attribute.
    if hasattr(net, '_class_namespace'):
        return cls_name in net._class_namespace.get().split('.')
    elif hasattr(net, '_class'):
        return cls_name in net._class.get().split('.')
    return None

def iter_networks_from_class(cls_name):
    for network in pymel.ls(type='network'):
        if is_network_from_class(network, cls_name):
            yield network

def get_networks_from_class(cls_name):
    """
    Return all networks serialized from a specified base class.
    Note that this don't check if the network itself is deserializable.

    For example, if we are looking for the Rig class and the network class is RigElement.Rig
    but RigElement is not defined, this will still return the network, however
    calling libSerialization.import_network will return None.
    # todo: add an option to pre-validate

    :param cls_name: A string representing the name of a class.
    :return: A list of pymel.nodetypes.Network.
    """
    return list(iter_networks_from_class(cls_name))

def iter_connected_networks(objs, key=None, key_skip=None, recursive=True, cache=None):
    """
    Inspect provided pymel.nodetypes.DagNode connections in search of serialized networks.
    By providing a function pointer, specific networks can be targeted.
    :param objs: A list of pymel.nodetypes.DagNode to inspect.
    :param key: A function to filter specific networks.
    :param key_skip: A function that receive a pymel.nodetypes.Network as input and return True if
    the network is blacklisted. If the network is blacklisted, it will not be iterated through.
    :param recursive: If true, will inspect recursively.
    :param cache: Used internally, do not overwrite.
    :yield: pymel.nodetypes.Networks
    """
    # Initialise the array the first time, we don't want to do it in the function argument as it will keep old values...
    if cache is None:
        cache = []

    # Ensure objects are provided as a list.
    if not hasattr(objs, '__iter__'):
        objs = [objs]

    for obj in objs:
        # Ignore known objects
        if obj in cache:
            continue

        # Remember this object in the cache
        cache.append(obj)

        # Ignore this object if it is blacklisted.
        # However still keep it in the cache in case we encounter it again.
        if key_skip and key_skip(obj):
            continue

        # Ignore any object that don't have a message attribute.
        # This is equivalent to searching for dagnodes only.
        if not obj.hasAttr('message'):
            continue

        for output_obj in obj.message.outputs():
            # Only check pymel.nodetypes.Network
            if not isinstance(output_obj, pymel.nodetypes.Network):
                continue

            # Prevent cyclic dependencies
            if output_obj in cache:
                continue

            # Prevent self referencing
            if output_obj is obj:
                continue

            if key is None or key(output_obj):
                yield output_obj

            if recursive:
                for result in iter_connected_networks(output_obj, key=key, key_skip=key_skip, recursive=recursive, cache=cache):
                    yield result

def get_connected_networks(objs, key=None, key_skip=None, recursive=True):
    """
    Inspect provided pymel.nodetypes.DagNode connections in search of serialized networks.
    By providing a function pointer, specific networks can be targeted.
    :param objs: A list of pymel.nodetypes.DagNode to inspect.
    :param key: A function to filter specific networks
    :param key_skip: A function that receive a pymel.nodetypes.Network as input and return True if
    the network is blacklisted. If the network is blacklisted, it will not be iterated through.
    :param recursive: If true, will inspect recursively.
    :return: A list of pymel.nodetypes.Network
    """
    return list(iter_connected_networks(objs, key=key, key_skip=key_skip, recursive=recursive))
