import logging as _logging
import sys

__all__ = (
    'get_class_module_root',
    'get_class_namespace',
    'create_class_instance',
    'export_dict',
    'import_dict'
)

logging = _logging.getLogger()
logging.setLevel(_logging.WARNING)

# constants
TYPE_BASIC, TYPE_LIST, TYPE_DAGNODE, TYPE_COMPLEX, TYPE_NONE = range(5)


def get_class_module_root(cls):
    """
    Resolve the top namespace of a class associated module.

    >>> from omtk.core.classCtrl import BaseCtrl
    >>> BaseCtrl.__module__
    'omtk.core.classCtrl'
    >>> get_class_module_root(BaseCtrl)
    'omtk'

    :param cls: A class definition to inspect.
    :return: A str instance representing the root module.
    """
    return next(iter(cls.__module__.split('.')), None)

def get_class_namespace(cls):
    """
    Resolve the full qualified namespace of a class.
    This support multiple inheritance using Python's method resolution order.

    >>> from omtk.rigs.rigArm import Arm
    >>> get_class_namespace(Arm)
    'Module.Limb.Arm'

    :param cls: A class definition to inspect.
    :return: A str instance representing the full qualified class namespace.
    """
    if not hasattr(cls, '__mro__'):
        raise NotImplementedError("Class {0} is a Python old-style class and is unsupported.".format(cls))

    return '.'.join(
        reversed([subcls.__name__ for subcls in cls.__mro__ if subcls != object])
    )


def create_class_instance(cls):
    """
    Create a class instance.
    This will ensure that even if the provided class definition is outdated (because of a reload)
    the latest definition (available from sys.modules) will be used.
    :param cls: A class definition to inspect.
    :return: A class instance.
    """
    class_def = getattr(sys.modules[cls.__module__], cls.__name__)
    assert (class_def is not None)

    try:
        return class_def()
    except Exception as e:
        logging.error("Fatal error creating '{0}' instance: {1}".format(cls, str(e)))
        return None

#
# Types definitions
# Type affect how the data is read & writen.
# By using global variables, we allow any script to hook itself in the module.
#

# We consider a data complex if it's a class instance.
# Note: We check for __dict__ because isinstance(_data, object) return True for basic types.
types_complex = [dict]


def is_data_complex(_data):
    return any(filter(lambda x: isinstance(_data, x), (iter(types_complex)))) or hasattr(_data, '__dict__')


types_basic = [int, float, bool]

# Python3 support
try:
    types_basic.append(basestring)
except NameError:
    pass
    types_basic.append(str)


def is_data_basic(_data):
    global types_basic
    return any(filter(lambda x: isinstance(_data, x), (iter(types_basic))))


types_list = [list, tuple]


def is_data_list(_data):
    global types_list
    return any(filter(lambda x: isinstance(_data, x), (iter(types_list))))


types_dag = []


def is_data_pymel(data):
    """
    Add pymel support.
    """
    global types_dag
    return any(filter(lambda x: isinstance(data, x), iter(types_dag)))


def get_data_type(data):
    if data is None:
        return TYPE_NONE
    if is_data_basic(data):
        return TYPE_BASIC
    if is_data_list(data):
        return TYPE_LIST
    # It is important to check pymel data before complex data since basically,
    # pymel.PyNode and pymel.PyNode are complex datatypes themselfs.
    if is_data_pymel(data):
        return TYPE_DAGNODE
    if is_data_complex(data):
        return TYPE_COMPLEX

    raise NotImplementedError("Unsupported object type {0} ({1})".format(data, type(data)))


def export_dict(data, skip_None=True, recursive=True, cache=None, **args):
    """
    Export an object instance (data) into a dictionary of basic data types (including pymel.Pynode and pymel.Attribute).

    Args:
        data: An instance of the build-in python class object.
        skip_None: Don't store an attribute if is value is None.
        recursive: Export recursively embedded instances of object in (excluding protected and private properties).
        **args:

    Returns: A dict instance containing only basic data types.
    """
    if cache is None:
        from cache import Cache
        cache = Cache()

    # Check if we already exported this data.
    # This allow us to support cyclic references.
    data_id = id(data)
    result = cache.get_import_value_by_id(data_id)
    if result is not None:
        print("Using cache for {0}".format(data))
        return result

    data_type = get_data_type(data)
    # object instance
    if data_type == TYPE_COMPLEX:
        data_cls = data.__class__
        result = {
            '_class': data_cls.__name__,
            '_class_namespace': get_class_namespace(data_cls),
            '_class_module': get_class_module_root(data_cls),
            '_uid': id(data)
        }

        # Cache it as soon as possible since we might use recursivity.
        cache.set_import_value_by_id(data_id, result)

        for key, val in (data.items() if isinstance(data, dict) else data.__dict__.items()):  # TODO: Clean
            # Ignore private keys (starting with an underscore)
            if key[0] == '_':
                continue

            if not skip_None or val is not None:
                if (data_type == TYPE_COMPLEX and recursive is True) or data_type == TYPE_LIST:
                    val = export_dict(val, skip_None=skip_None, recursive=recursive, cache=cache, **args)
                if not skip_None or val is not None:
                    result[key] = val
    else:

        # Handle other types of data
        if data_type == TYPE_BASIC:
            result = data

        # Handle iterable
        elif data_type == TYPE_LIST:
            result = [export_dict(v, skip_None=skip_None, cache=cache, **args) for v in data if not skip_None or v is not None]

        elif data_type == TYPE_DAGNODE:
            result = data

        else:
            logging.warning("[exportToBasicData] Unsupported type {0} ({1}) for {2}".format(type(data), data_type, data))
            result = None

        cache.set_import_value_by_id(data_id, result)

    return result



def import_dict(data, cache=None, **kwargs):
    """
    Rebuild any instance of a python object instance that have been serialized using export_dict.

    Args:
        _data: A dict instance containing only basic data types.
        **kwargs:

    Returns:

    """

    if cache is None:
        from cache import Cache
        cache = Cache()

    #assert (data is not None)
    if isinstance(data, dict) and '_class' in data:
        # Handle Serializable object
        cls_path = data['_class']
        cls_name = cls_path.split('.')[-1]
        cls_module = data.get('_class_module', None)
        #cls_namespace = data.get('_class_namespace')

        # HACK: Previously we were storing the complete class namespace.
        # However this was not very flexible when we played with the class hierarchy.
        # If we find a '_class_module' attribute, it mean we are doing thing the new way.
        # Otherwise we'll let it slip for now.

        if cls_module:
            cls_def = cache.get_class_by_name(cls_name, module_name=cls_module)
        else:
            cls_def = cache.get_class_by_namespace(cls_name)

        if cls_def is None:
            logging.error("Can't create class instance for {0}, did you import to module?".format(cls_path))
            return None

        instance = create_class_instance(cls_def)

        for key, val in data.items():
            if key != '_class':
                instance.__dict__[key] = import_dict(val, cache=cache)
        return instance

    # Handle array
    elif is_data_list(data):
        return [import_dict(v, cache=cache) for v in data]

    # Handle other types of data
    else:
        return data
