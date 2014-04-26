import os
import types
import imp
import logging
logging = logging.getLogger('libPython')
logging.setLevel(0)

def does_module_exist(module_name):
    try:
        imp.find_module(module_name)
        return True
    except ImportError:
        return False

# OMW IT WORK!
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
