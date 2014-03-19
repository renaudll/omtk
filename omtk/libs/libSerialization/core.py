import logging as _logging
logging = _logging.getLogger()
logging.setLevel(_logging.WARNING)
import sys
import core

# constants
TYPE_BASIC, TYPE_LIST, TYPE_DAGNODE, TYPE_COMPLEX = range(4)

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

#
# Types definitions
# Type affect how the data is read & writen.
# By using global variables, we allow any script to hook itself in the module.
#

# We consider a data complex if it's a class instance.
# Note: We check for __dict__ because isinstance(_data, object) return True for basic types.
_complex_types = [dict]
def _isDataComplex(_data):
    return any(filter(lambda x: isinstance(_data, x), (iter(_basic_types)))) or hasattr(_data, '__dict__')

_basic_types = [int, float, basestring, bool]
def _isDataBasic(_data):
    global _basic_types
    return any(filter(lambda x: isinstance(_data, x), (iter(_basic_types))))

_list_types = [list, tuple]
def _isDataList(_data):
    global _list_types
    return any(filter(lambda x: isinstance(_data, x), (iter(_list_types))))

_dag_types = []
def _isDataDagNode(_data):
    global _dag_types
    return any(filter(lambda x: isinstance(_data, x), iter(_dag_types)))

def getDataType(_data, *args, **kwargs):
    if _isDataList(_data, *args, **kwargs):
        return TYPE_LIST
    elif _isDataBasic(_data, *args, **kwargs):
        return TYPE_BASIC
    elif _isDataDagNode(_data, *args, **kwargs):
        return TYPE_DAGNODE
    elif _isDataComplex(_data, *args, **kwargs):
        return TYPE_COMPLEX
    else:
        logging.warning('{0} is unknow type'.format(_data))

def exportToBasicData(_data, _bSkipNone=True, _bRecursive=True, **args):
    ##logging.debug('[exportToBasicData]', _data)

    sType = getDataType(_data)
    # object instance
    if sType == TYPE_COMPLEX:
        dicReturn = {}
        dicReturn['_class'] = _getClassNamespace(_data.__class__)
        dicReturn['_uid'] = id(_data)
        for key, val in (_data.items() if isinstance(_data, dict) else _data.__dict__.items()): # TODO: Clean
            if '_' not in key[0]:
                if not _bSkipNone or val is not None:
                    if (sType == TYPE_COMPLEX and _bRecursive is True) or sType == TYPE_LIST:
                        val = exportToBasicData(val, _bSkipNone=_bSkipNone, _bRecursive=_bRecursive, **args)
                    if not _bSkipNone or val is not None:
                        dicReturn[key] = val

        return dicReturn

    # Handle other types of data
    elif sType == TYPE_BASIC:
        return _data

    # Handle iterable
    elif sType == TYPE_LIST:
        return [exportToBasicData(v, _bSkipNone=_bSkipNone, **args) for v in _data if not _bSkipNone or v is not None]

    elif sType == TYPE_DAGNODE:
        return _data

    logging.warning("[exportToBasicData] Unsupported type {0} for {1}".format(sType, _data))
    return None


def importToBasicData(_data, **args):
    if isinstance(_data, dict) and '_class' in _data:
        # Handle Serializable object
        clsName = _data['_class'].split('.')[-1]
        instance = core._createClassInstance(clsName)
        if not isinstance(instance, object):
            # TODO: Log error
            return None
        for key, val in _data.items():
            if key != '_class':
                instance.__dict__[key] = importToBasicData(val, **args)
        return instance
    # Handle array
    elif core._isDataList(_data):
        return [importToBasicData(v, **args) for v in _data]
    # Handle other types of data
    else:
        return _data
