# Add dependencies to sys paths
import sys, os, inspect
module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.abspath(os.path.join(module_dir, 'deps')))

from libs import libPython

import animation
import rigging

'''
# Here's how to reload:
import omtk
from omtk.libs import libPython
reload libPython
libPython.reload_module_recursive(omtk)
'''