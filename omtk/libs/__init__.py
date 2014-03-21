import imp
def _does_module_exist(_name):
    try:
        imp.find_module(_name)
        return True
    except ImportError:
        return False
       
import libSerialization
import libPython

if _does_module_exist("maya"):
	import libRigging
