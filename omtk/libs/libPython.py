import os, types, imp, logging, re
logging = logging.getLogger('libPython')
logging.setLevel(0)

def does_module_exist(module_name):
    try:
        imp.find_module(module_name)
        return True
    except ImportError:
        return False

# @deprecated, use the reimport module instead
def reload_module_recursive(module, namespace=''):
    assert(hasattr(module, '__path__'))
    assert(isinstance(module.__path__, list))
    assert(len(module.__path__) > 0)
    module_path = module.__path__[0]
    namespace += module.__name__

    # traverse root directory, and list directories as dirs and files as files
    for cur_file in os.listdir(module_path):
        # File
        if os.path.isfile(os.path.join(module_path, cur_file)):
            file_name, file_ext = os.path.splitext(cur_file)
            if file_ext == '.py' and file_name != '__init__':
                if hasattr(module, file_name) and isinstance(getattr(module, file_name), types.ModuleType):
                    logging.debug("Found module {0} in {1}".format(file_name, module.__name__))
                    full_name = os.path.splitext(cur_file)[0].replace(os.path.sep, '.')
                    logging.debug(full_name, file_name, module_path)
                    logging.debug("Reloading module {0}".format(module.__name__ + '.' + full_name))
                    imp.load_module(full_name, *imp.find_module(file_name, [module_path]))
        # Directory
        else:
            if hasattr(module, cur_file) and isinstance(getattr(module, cur_file), types.ModuleType):
                logging.debug('Found folder {0}'.format(cur_file))
                reload_module_recursive(getattr(module, cur_file))

# Another potential solution (maybe more efficient than reload_module_recursive)
# src: http://stackoverflow.com/questions/15506971/recursive-version-of-reload/17194836#17194836
# @deprecated, use the reimport module instead
from types import ModuleType
def rreload(module, exceptions=['_.*', 'sys', 'os', 'imp', 're', 'logging', 'OpenMaya.*', 'pymel', 'Qt.*']):
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if type(attribute) is ModuleType:
            is_blacklisted = any((exception for exception in exceptions if re.match(exception, attribute_name)))
            if not is_blacklisted:
                print attribute_name
                rreload(attribute)
    try:
        reload(module)
    except ImportError, e:
        logging.info(str(e))

# src: http://code.activestate.com/recipes/66472/
def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)

    return L