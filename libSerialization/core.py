import logging as _logging
import sys
logging = _logging.getLogger()
logging.setLevel(_logging.WARNING)

# constants
TYPE_BASIC, TYPE_LIST, TYPE_DAGNODE, TYPE_COMPLEX = range(4)


def get_class_def(class_name, base_class=object):
    try:
        for cls in base_class.__subclasses__():
            if cls.__name__ == class_name:
                return cls
            else:
                t = get_class_def(class_name, base_class=cls)
                if t is not None:
                    return t
    except Exception as e:
        pass  # logging.info(str(e)) # TODO: FIX
    return None


def create_class_instance(class_name):
    cls = get_class_def(class_name)

    if cls is None:
        logging.warning("Can't find class definition '{0}'".format(class_name));
        return None

    clsDef = getattr(sys.modules[cls.__module__], cls.__name__)
    assert (clsDef is not None)

    try:
        return clsDef()
    except Exception as e:
        logging.error("Fatal error creating '{0}' instance: {1}".format(class_name, str(e)))
        return None


def get_class_namespace(classe):
    if not isinstance(classe, object):
        return None  # Todo: throw exception
    tokens = []
    while not classe is object:
        tokens.append(classe.__name__)
        classe = classe.__bases__[0]
    return '.'.join(reversed(tokens))

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

def get_data_type(data, *args, **kwargs):
    if is_data_basic(data):
        return TYPE_BASIC
    if is_data_list(data):
        return TYPE_LIST
    if is_data_pymel(data): # It is important to check pymel data before complex data since basically, pymel.PyNode and pymel.PyNode are complex datatypes themselfs.
        return TYPE_DAGNODE
    if is_data_complex(data):
        return TYPE_COMPLEX


    raise NotImplementedError("Unsupported object type {0} ({1})".format(data, type(data)))

def export_dict(data, skip_None=True, recursive=True, **args):
    """
    Export an object instance (data) into a dictionary of basic data types (including pymel.Pynode and pymel.Attribute).

    Args:
        data: An instance of the build-in python class object.
        skip_None: Don't store an attribute if is value is None.
        recursive: Export recursively embedded instances of object in (excluding protected and private properties).
        **args:

    Returns: A dict instance containing only basic data types.

    """
    ##logging.debug('[exportToBasicData]', _data)

    sType = get_data_type(data)
    # object instance
    if sType == TYPE_COMPLEX:
        dicReturn = {}
        dicReturn['_class'] = get_class_namespace(data.__class__)
        dicReturn['_uid'] = id(data)
        for key, val in (data.items() if isinstance(data, dict) else data.__dict__.items()):  # TODO: Clean
            if '_' not in key[0]:
                if not skip_None or val is not None:
                    if (sType == TYPE_COMPLEX and recursive is True) or sType == TYPE_LIST:
                        val = export_dict(val, skip_None=skip_None, recursive=recursive, **args)
                    if not skip_None or val is not None:
                        dicReturn[key] = val

        return dicReturn

    # Handle other types of data
    elif sType == TYPE_BASIC:
        return data

    # Handle iterable
    elif sType == TYPE_LIST:
        return [export_dict(v, skip_None=skip_None, **args) for v in data if not skip_None or v is not None]

    elif sType == TYPE_DAGNODE:
        return data

    logging.warning("[exportToBasicData] Unsupported type {0} ({1}) for {2}".format(type(data), sType, data))
    return None


def import_dict(data, **args):
    """
    Rebuild any instance of a python object instance that have been serialized using export_dict.

    Args:
        _data: A dict instance containing only basic data types.
        **args:

    Returns:

    """
    assert (data is not None)
    if isinstance(data, dict) and '_class' in data:
        # Handle Serializable object
        class_path = data['_class']
        class_name = class_path.split('.')[-1]
        instance = create_class_instance(class_name)
        if instance is None or not isinstance(instance, object):
            logging.error("Can't create class instance for {0}, did you import to module?".format(class_path))
            # TODO: Log error
            return None
        for key, val in data.items():
            if key != '_class':
                instance.__dict__[key] = import_dict(val, **args)
        return instance
    # Handle array
    elif is_data_list(data):
        return [import_dict(v, **args) for v in data]
    # Handle other types of data
    else:
        return data


