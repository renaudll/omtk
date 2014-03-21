import imp

def _does_module_exist(_name):
    try:
        imp.find_module(_name)
        return True
    except ImportError:
        return False

import libs

if _does_module_exist("maya"):
	import animation
	import rigging

def _reload():
	# uncomment this when debugging
	'''
	reload(animation); animation._reload()
	reload(libs); libs._reload()
	reload(rigging); rigging._reload()
	'''

'''
# Here's how to reload for now:
import omtk
from omtk.libs import libPython
reload libPython
libPython.reload_module_recursive(omtk)
'''