import logging
import sys

from maya import OpenMaya
import pymel.core as pymel
from .decorators import memoized

__all__ = (
    "_get_class_module_root",
    "_get_class_namespace",
    "_create_instance",
    "export_dict",
    "import_dict",
    "register_alias",
    "export_network",
    "import_network",
)

_LOG = logging.getLogger(__name__)

# constants
TYPE_BASIC, TYPE_LIST, TYPE_DAGNODE, TYPE_COMPLEX, TYPE_NONE = range(5)

_REGISTRY_TYPES_BASIC = (int, float, bool)
_REGISTRY_TYPES_LIST = (list, tuple)
_REGISTRY_TYPES_COMPLEX = (dict,)
_REGISTRY_TYPES_DAG = (
    pymel.PyNode,
    pymel.Attribute,
    pymel.datatypes.Matrix,
    pymel.datatypes.Vector,
)

_REGISTRY_ALIASES = {}

# Python3 support
try:
    _REGISTRY_TYPES_BASIC += (basestring,)
except NameError:
    _REGISTRY_TYPES_BASIC += (str,)


def _get_class_module_root(cls):
    """
    Resolve the top namespace of a class associated module.

    >>> from omtk.core.classCtrl import BaseCtrl
    >>> BaseCtrl.__module__
    'omtk.core.ctrl'
    >>> _get_class_module_root(BaseCtrl)
    'omtk'

    :param cls: A class definition to inspect.
    :return: A str instance representing the root module.
    """
    return cls.__module__.split(".")[0]


def _get_class_namespace(cls):
    """
    Resolve the full qualified namespace of a class.
    This support multiple inheritance using Python's method resolution order.

    >>> from omtk.rigs.rigArm import Arm
    >>> _get_class_namespace(Arm)
    'Module.Limb.Arm'

    :param cls: A class definition to inspect.
    :return: A str instance representing the full qualified class namespace.
    """
    if not hasattr(cls, "__mro__"):
        raise NotImplementedError(
            "Class {0} is a Python old-style class and is unsupported.".format(cls)
        )

    return ".".join(
        reversed([subcls.__name__ for subcls in cls.__mro__ if subcls != object])
    )


def _create_instance(cls):
    """
    Create a class instance.
    This will ensure that even if the provided class definition is outdated
    (because of a reload) the latest definition (available from sys.modules)
    will be used.

    :param cls: A class definition to inspect.
    :return: A class instance.
    """
    class_def = getattr(sys.modules[cls.__module__], cls.__name__)
    assert class_def is not None

    try:
        return class_def()
    except Exception as e:
        _LOG.error("Fatal error creating '{0}' instance: {1}".format(cls, str(e)))
        return None


def _get_data_type(data):
    if data is None:
        return TYPE_NONE

    if isinstance(data, _REGISTRY_TYPES_BASIC):
        return TYPE_BASIC

    if isinstance(data, _REGISTRY_TYPES_LIST):
        return TYPE_LIST

    # It is important to check pymel data before complex data since basically,
    # pymel.PyNode and pymel.PyNode are complex data types themselves.
    if isinstance(data, _REGISTRY_TYPES_DAG):
        return TYPE_DAGNODE

    if isinstance(data, _REGISTRY_TYPES_COMPLEX) or hasattr(data, "__dict__"):
        return TYPE_COMPLEX

    raise NotImplementedError(
        "Unsupported object type {0} ({1})".format(data, type(data))
    )


def export_dict(data, skip_none=True, recursive=True, cache=None):
    """
    Export an object instance into a dictionary of basic data types.

    :param data: An instance of the build-in python class object.
    :param skip_none: Don't store an attribute if is value is None.
    :param recursive: Export recursively embedded instances of object in (excluding protected and private properties).
    :return: A dict instance containing only basic data types.
    """
    cache = cache or Cache()

    # Check if we already exported this data.
    # This allow us to support cyclic references.
    data_id = id(data)
    result = cache.get_import_value_by_id(data_id)
    if result is not None:
        _LOG.debug("Using cache for %s", data)
        return result

    data_type = _get_data_type(data)
    # object instance
    if data_type == TYPE_COMPLEX:
        data_cls = data.__class__
        result = {
            "_class": data_cls.__name__,
            "_class_namespace": _get_class_namespace(data_cls),
            "_class_module": _get_class_module_root(data_cls),
            "_uid": id(data),
        }

        # Cache it as soon as possible since we might use recursion.
        cache.set_import_value_by_id(data_id, result)

        for key, val in (data if isinstance(data, dict) else data.__dict__).iteritems():
            # Ignore private keys (starting with an underscore)
            if key.startswith("_"):
                continue

            if not skip_none or val is not None:
                if (data_type == TYPE_COMPLEX and recursive) or data_type == TYPE_LIST:
                    val = export_dict(
                        val, skip_none=skip_none, recursive=recursive, cache=cache,
                    )
                if not skip_none or val is not None:
                    result[key] = val
    else:

        # Handle other types of data
        if data_type == TYPE_BASIC:
            result = data

        # Handle iterable
        elif data_type == TYPE_LIST:
            result = [
                export_dict(v, skip_none=skip_none, cache=cache)
                for v in data
                if not skip_none or v is not None
            ]

        elif data_type == TYPE_DAGNODE:
            result = data

        else:
            _LOG.warning(
                "[exportToBasicData] Unsupported type {0} ({1}) for {2}".format(
                    type(data), data_type, data
                )
            )
            result = None

        cache.set_import_value_by_id(data_id, result)

    return result


def import_dict(data, cache=None):
    """
    Rebuild any instance of a python object instance that have been serialized using export_dict.

    :param data: A dict instance containing only basic data types.
    """
    cache = cache or Cache()

    # assert (data is not None)
    if isinstance(data, dict) and "_class" in data:
        # Handle Serializable object
        cls_path = data.pop("_class", "")
        cls_name = cls_path.split(".")[-1]
        cls_module = data.pop("_class_module", None)
        data.pop("_uid", None)
        data.pop("_class_namespace", None)

        # HACK: Previously we were storing the complete class namespace.
        # However this was not very flexible when we played with the class hierarchy.
        # If we find a '_class_module' attribute, it mean we are doing thing the new way.
        # Otherwise we'll let it slip for now.
        if cls_module and cls_path:
            try:
                cls_path = _REGISTRY_ALIASES[(cls_module, cls_path)]
            except KeyError:
                pass
            else:
                cls_name = cls_path.split(".")[-1]

        if cls_module:
            cls_def = cache.get_class_by_name(cls_name, module_name=cls_module)
        else:
            cls_def = cache.get_class_by_namespace(cls_name)

        if cls_def is None:
            _LOG.error(
                "Can't create class instance for {0}, did you import to module?".format(
                    cls_path
                )
            )
            return None

        instance = _create_instance(cls_def)

        for key, val in data.iteritems():
            if key != "_class":
                instance.__dict__[key] = import_dict(val, cache=cache)
        return instance

    # Handle array
    if _get_data_type(data) == TYPE_LIST:
        return [import_dict(v, cache=cache) for v in data]

    # Handle other types of data
    return data


def register_alias(module, src, dst):
    """
    Register an alias for a deprecated class that should be replaced by another.

    :param str module: The class module name
    :param str src: The class namespace
    :param str dst: The class new namespace
    """
    _REGISTRY_ALIASES[(module, src)] = dst


def _create_attr(name, data):
    """
    Factory method that create the appropriate OpenMaya.MFnAttribute instance
    for a provided object.

    :param str name: The name of the OpenMaya.MFnAttribute to create.
    :param object data: The value to represent as an attribute.
    :return: An OpenMaya.MFnAttribute subclass instance.
    :rtype: OpenMaya.MFnAttribute
    :raises ValueError: If we don't support the provided data type.
    """
    # (str, unicode) -> MFnTypedAttribute(kString)
    if isinstance(data, basestring):
        mfn = OpenMaya.MFnTypedAttribute()
        mfn.create(name, name, OpenMaya.MFnData.kString)
        return mfn

    data_type = type(data)
    # (bool,) -> MFnNumericAttribute(kBoolean)
    if issubclass(data_type, bool):
        mfn = OpenMaya.MFnNumericAttribute()
        mfn.create(name, name, OpenMaya.MFnNumericData.kBoolean)
        return mfn

    # (int,) -> MFnNumericData(kInt)
    if issubclass(data_type, int):
        mfn = OpenMaya.MFnNumericAttribute()
        mfn.create(name, name, OpenMaya.MFnNumericData.kInt)
        return mfn

    # (float,) -> MFnNumericData(kFloat)
    if issubclass(data_type, float):
        mfn = OpenMaya.MFnNumericAttribute()
        mfn.create(name, name, OpenMaya.MFnNumericData.kFloat)
        return mfn

    # (dict,) -> MFnMessageAttribute
    if isinstance(data, dict):
        mfn = OpenMaya.MFnMessageAttribute()
        mfn.create(name, name)
        return mfn

    # (list, tuple,) -> arbitrary type depending on the list content.
    # Note contrary to python list, Maya lists are typed.
    # This will crash if the list contain multiple types at the same time.
    # However, the None value is supported.
    # TODO: Raise an exception if multiples types are in the same list.
    if isinstance(data, (list, tuple)):
        if len(data) < 1:
            _LOG.warning("Can't create attribute %s, empty array are unsupported", name)
            return None

        # Resolve the type
        iter_valid_values = (d for d in data if d is not None)
        ref_val = next(iter(iter_valid_values), None)

        # If the list only contain None values, don't create anything.
        if ref_val is None:
            return

        mfn = _create_attr(name, ref_val)
        mfn.setArray(True)
        return mfn

    # (pymel.datatypes.Matrix,) -> MFnMatrixAttribute
    if issubclass(data_type, pymel.datatypes.Matrix):  # HACK
        mfn = OpenMaya.MFnMatrixAttribute()
        mfn.create(name, name)
        return mfn

    # (pymel.datatypes.Vector,) -> MFnNumericAttribute(kDouble)
    if issubclass(data_type, pymel.datatypes.Vector):
        name_x = "{0}X".format(name)
        name_y = "{0}Y".format(name)
        name_z = "{0}Z".format(name)
        mfn = OpenMaya.MFnNumericAttribute()
        mo_x = mfn.create(name_x, name_x, OpenMaya.MFnNumericData.kDouble)
        mo_y = mfn.create(name_y, name_y, OpenMaya.MFnNumericData.kDouble)
        mo_z = mfn.create(name_z, name_z, OpenMaya.MFnNumericData.kDouble)
        mfn.create(name, name, mo_x, mo_y, mo_z)
        return mfn

    # (pymel.general.Attribute,) -> type depending on the attribute type itself.
    if issubclass(data_type, pymel.Attribute):
        if not data.exists():
            _LOG.warning(
                "Can't serialize non-existent pymel.Attribute %s", name,
            )
            return None

        if data.type() == "doubleAngle":
            mfn = OpenMaya.MFnUnitAttribute()
            mfn.create(name, name, OpenMaya.MFnUnitAttribute.kAngle)
            return mfn

        if data.type() == "time":
            mfn = OpenMaya.MFnUnitAttribute()
            mfn.create(name, name, OpenMaya.MFnUnitAttribute.kTime)
            return mfn

        # If the attribute doesn't represent anything special,
        # we'll check it's value to know what attribute type to create.
        return _create_attr(name, data.get())

    # (pymel.general.PyNode,) -> MFnMessageAttribute
    # The order is important here as if we hit this,
    # we don't deal with a pymel.general.Attribute.
    # Using duct-typing we support any 'pymel-like' objects.
    if hasattr(data, "__melobject__"):
        mfn = OpenMaya.MFnMessageAttribute()
        mfn.create(name, name)
        return mfn

    # (object,) -> MFnMessageAttribute
    if hasattr(data, "__dict__"):
        mfn = OpenMaya.MFnMessageAttribute()
        mfn.create(name, name)
        return mfn

    raise ValueError("Can't create MFnAttribute for %s %s %s" % (name, data, data_type))


def _add_attr(fnDependNode, name, data, cache=None):
    data_type = _get_data_type(data)

    # Skip empty list
    is_multi = data_type == TYPE_LIST
    if is_multi and len(filter(None, data)) == 0:
        return

    plug = None
    # Get attribute arguments
    try:  # TODO: Is a try/catch really the best way to know if the plug exists?
        plug = fnDependNode.findPlug(name)
    except:
        pass

    # Create attribute if missing
    if not plug:
        fn_attr = _create_attr(name, data)
        if fn_attr is None:
            return  # In case of invalid value like missing pymel PyNode & Attributes

        fn_attr.setNiceNameOverride(name)
        mobject = fn_attr.object()
        if mobject:
            try:
                fnDependNode.addAttribute(mobject)
                plug = OpenMaya.MPlug(fnDependNode.object(), mobject)
            except Exception as e:
                _LOG.warning("Error adding attribute %s: %s", name, e)

    # Set attribute value
    if plug:
        _set_attr(plug, data, cache=cache)


def _set_attr(_plug, data, cache=None):
    data_type = _get_data_type(data)
    if data_type == TYPE_LIST:
        num_elements = len(data)

        _plug.setNumElements(num_elements)  # TODO: MAKE IT WORK # TODO: NECESSARY???

        for i in range(num_elements):
            _set_attr(_plug.elementByLogicalIndex(i), data[i], cache=cache)

    elif data_type == TYPE_BASIC:
        # Basic types
        if isinstance(data, bool):
            _plug.setBool(data)
        elif isinstance(data, int):
            _plug.setInt(data)
        elif isinstance(data, float):
            _plug.setFloat(data)
        elif isinstance(data, basestring):
            _plug.setString(data)

    elif data_type == TYPE_COMPLEX:
        network = export_network(data, cache=cache)
        plug = network.__apimfn__().findPlug("message")

        # TODO: Is this really the best way?
        dag_modifier = OpenMaya.MDagModifier()
        dag_modifier.connect(plug, _plug)
        dag_modifier.doIt()

    elif data_type == TYPE_DAGNODE:
        plug = None
        if isinstance(data, pymel.Attribute):  # pymel.Attribute
            # Hack: Don't crash with non-existent pymel.Attribute
            if not data.exists():
                _LOG.warning("Can't setAttr, Attribute %s don't exist", data)
                return
            plug = data.__apimfn__()
        elif isinstance(data, pymel.datatypes.Matrix):
            mfn = OpenMaya.MFnMatrixData()
            mobject = mfn.create(data.apicls(data))
            _plug.setMObject(mobject)
            return True
        elif isinstance(data, pymel.datatypes.Vector):
            _plug.child(0).setFloat(data.x)
            _plug.child(1).setFloat(data.y)
            _plug.child(2).setFloat(data.z)
            return True
        elif hasattr(data, "exists"):  # pymel.PyNode
            # Hack: Don't crash with non-existent pymel.Attribute
            if not pymel.objExists(data.__melobject__()):
                _LOG.warning("Can't setAttr, PyNode %s don't exist", data)
                return
            plug = data.__apimfn__().findPlug("message")

        if plug:
            dag_modifier = OpenMaya.MDagModifier()
            dag_modifier.connect(plug, _plug)
            dag_modifier.connect(plug, _plug)  # is connecting two times necessary?
            dag_modifier.doIt()
        else:
            raise Exception("Unknow TYPE %s, %s", type(data), data)
    elif data_type == TYPE_NONE:
        return

    else:
        raise NotImplementedError


def _get_network_attr(attr, fn_skip=None, cache=None):
    # Recursive
    if attr.isMulti():
        attr_indices = attr.getArrayIndices()
        # Empty array
        if not attr_indices:
            return []
        num_logical_elements = max(attr_indices) + 1
        return [
            _get_network_attr(
                attr.elementByLogicalIndex(i), fn_skip=fn_skip, cache=cache
            )
            for i in range(num_logical_elements)
        ]

    if attr.type() == "message":
        if not attr.isConnected():
            return None
        attr_input = attr.inputs()[0]

        # Network
        if hasattr(attr_input, "_class"):
            return import_network(attr_input, fn_skip=fn_skip, cache=cache)

        # Node
        return attr_input

    # pymel.Attribute
    if attr.isConnected():
        return attr.inputs(plugs=True)[0]

    # Basic type
    return attr.get()


_export_network_key_whitelist = ["_class", "_class_module", "_class_namespace"]


def _can_export_attr_by_name(name):
    """
    Determine what attribute can be exported to a network.
    All key that start with an underscore are considered private and won't be exported.
    The reserved keyword and automatically excempted from this rule.
    """
    if name in _export_network_key_whitelist:
        return True

    if name[0] == "_":
        return False

    return True


def export_network(data, cache=None, **kwargs):
    cache = cache or Cache()
    # _LOG.debug('CreateNetwork {0}'.format(data))

    # We'll deal with two additional attributes, '_network' and '_uid'.
    # Those two attributes allow us to find the network from the value and vice-versa.
    # Note that since the '_uid' refer to the current python context,
    # it's value could be incorrect when calling import_network.
    # However the change of collisions are extremely improbable so
    # checking the type of the python variable is sufficient.
    # Please feel free to provide a better design if any if possible.

    data_id = id(data)
    result = cache.get_network_by_id(data_id)
    if result is not None:
        return result

    # Create network, re-use existing network if already present in scene
    # Automatically name network whenever possible
    try:
        network_name = data.__getNetworkName__()
    except (AttributeError, TypeError):
        network_name = data.__class__.__name__

    network = pymel.createNode("network", name=network_name)

    # Monkey patch the network in a _network attribute if supported.
    if isinstance(data, object) and not isinstance(data, dict):
        data._network = network

    # Ensure the network have the current python id stored
    if not network.hasAttr("_uid"):
        pymel.addAttr(
            network, longName="_uid", niceName="_uid", at="long"
        )  # todo: validate attributeType

    # Cache as soon as possible since we'll use recursion soon.
    cache.set_network_by_id(data_id, network)

    # Convert _pData to basic data dictionary (recursive for now)
    data_dict = export_dict(data, recursive=False, cache=cache, **kwargs)
    assert isinstance(data_dict, dict)

    mfn = network.__apimfn__()
    for key, val in sorted(data_dict.items()):
        if _can_export_attr_by_name(key):
            _add_attr(mfn, key, val, cache=cache)

    return network


def import_network(network, fn_skip=None, cache=None):
    """
    Recursively create class instances from provided network.
    :param network: The network to read from.
    :param fn_skip: A function taken a pymel.nodetypes.Network as argument
                    that return True if we need to ignore a specific network.
    :param cache: Used internally.
    :return: An object instance corresponding to the provided network.
    """
    cache = cache or Cache()

    # Duck-type the network, if the '_class' attribute exist,
    # it is a class instance representation.
    # Otherwise it is a simple pymel.PyNode datatypes.
    if not network.hasAttr("_class"):
        return network

    network_id = hash(network)

    # Check if the object related to the network already exist
    # in the cache and return it if found
    cached_obj = cache.get_import_value_by_id(network_id)
    if cached_obj is not None:
        return cached_obj

    # Check if the object is blacklisted. If it is,
    # we'll still add it to the cache in case we encounter it again.
    if fn_skip and fn_skip(network):
        cache.set_import_value_by_id(network_id, None)
        return None

    cls_name = network.getAttr("_class")

    # HACK: Previously we were storing the complete class namespace.
    # However this was not very flexible when we played with the class hierarchy.
    # If we find a '_class_module' attribute, it mean we are doing thing the new way.
    # Otherwise we'll let it slip for now.
    cls_module = (
        network.getAttr("_class_module") if network.hasAttr("_class_module") else None
    )
    if cls_module:
        cls_def = cache.get_class_by_name(cls_name, module_name=cls_module)
    else:
        cls_def = cache.get_class_by_namespace(cls_name)

    if cls_def is None:
        _LOG.warning("Can't find class definiton for %s. Returning None", cls_name)
        return None

    # HACK: Get latest definition
    cls_def = getattr(sys.modules[cls_def.__module__], cls_def.__name__)
    obj = cls_def()

    # Monkey patch the network if supported
    if isinstance(obj, object) and not isinstance(obj, dict):
        obj._network = network

    # Fill the import cache to make sure that self reference
    # doesn't try to infinitly loop in it's import
    cache.set_import_value_by_id(network_id, obj)

    # Resolve wich attribute we'll want to import
    attr_map = {}
    for attr_name in pymel.listAttr(network, userDefined=True):
        # Attribute longName starting with '_' are considered private
        if not attr_name.startswith("_"):
            attr_map[attr_name] = network.attr(attr_name)

    # Filter compound children as we are only interested the compound value itself.
    # ex: import translate and skip translateX, translateY, translateZ
    for attr in attr_map.values():
        if attr.isCompound():
            for child in attr.getChildren():
                child_longname = child.longName()
                try:
                    attr_map.pop(child_longname)
                except KeyError:
                    pass

    try:
        obj.__callbackNetworkPreBuild__(attr_map)
    except AttributeError:  # Hook don't exist.
        pass
    except Exception as error:
        _LOG.warning(
            "Call to __callbackNetworkPreBuild__ failed for %s: %s", obj, error
        )

    for attr_name, attr in attr_map.iteritems():
        # _LOG.debug('Importing attribute {0} from {1}'.format(key, _network.name()))
        val = _get_network_attr(attr, fn_skip=fn_skip, cache=cache)
        if isinstance(obj, dict):
            obj[attr_name.longName()] = val
        else:
            try:
                setattr(obj, attr_name, val)
            except AttributeError as error:
                print(obj, attr_name, val, error)

    # Execute the __callbackNetworkPostBuild__ hook.
    # This can be used to act immediately after import.
    try:
        obj.__callbackNetworkPostBuild__()
    except AttributeError:  # Hook don't exist
        pass
    except Exception as error:
        _LOG.warning(
            "Call to __callbackNetworkPostBuild__ failed for %s: %s", obj, error
        )

    return obj


def _iter_subclasses_recursive(cls):
    yield cls

    try:
        for sub_cls in cls.__subclasses__():
            for yielded in _iter_subclasses_recursive(sub_cls):
                yield yielded
    except TypeError:  # This will fail when encountering the 'type' datatype.
        pass


def _iter_module_subclasses_recursive(module_root, cls):
    for sub_cls in _iter_subclasses_recursive(cls):
        cur_module_root = _get_class_module_root(sub_cls)
        if module_root == cur_module_root:
            yield sub_cls


class Cache(object):
    def __init__(self):
        self.classes = None
        self._cache_import_by_id = {}
        self._cache_networks_by_id = {}  # todo: merge with _cache_import_by_id

    @memoized
    def _get_cls_cache_by_module(self, module_name, base_class=object):
        i = _iter_module_subclasses_recursive(module_name, base_class)
        result = {}
        for cls in i:
            result[cls.__name__] = cls
        return result

    @memoized
    def _get_cls_cache(self, base_class=object):
        i = _iter_subclasses_recursive(base_class)
        result = {}
        for cls in i:
            result[cls.__name__] = cls
        return result

    def get_class_by_name(self, cls_name, module_name=None, base_class=object):
        if module_name:
            cache = self._get_cls_cache_by_module(
                module_name=module_name, base_class=base_class
            )
        else:
            cache = self._get_cls_cache(base_class=base_class)

        return cache.get(cls_name, None)

    def get_class_by_namespace(
        self, cls_namespace, module_name=None, base_class=object
    ):
        if module_name is None:
            cache = self._get_cls_cache(base_class=base_class)
        else:
            cache = self._get_cls_cache_by_module(base_class=base_class)
        for cls in cache.values():
            cur_namespace = _get_class_namespace(cls)
            if cls_namespace == cur_namespace:
                return cls

    def get_import_value_by_id(self, id, default=None):
        return self._cache_import_by_id.get(id, default)

    def set_import_value_by_id(self, id_, val):
        self._cache_import_by_id[id_] = val

    def get_network_by_id(self, id_):
        return self._cache_networks_by_id.get(id_)

    def set_network_by_id(self, id_, net):
        self._cache_networks_by_id[id_] = net
