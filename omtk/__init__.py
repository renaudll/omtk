from libs import libPython

if libPython.does_module_exist("maya"):
	import animation
	import rigging

'''
# Here's how to reload:
import omtk
from omtk.libs import libPython
reload libPython
libPython.reload_module_recursive(omtk)
'''