"""
DEV: HOW TO RELOAD OMTK:
import omtk
from omtk.libs import libPython
reload libPython
libPython.reload_module_recursive(omtk)
"""
import sys, os

# Load dependencies (including git submodules) in sys.path
__dependencies__ = [
    ('deps',),
    ('..', 'libSerialization',),
    ('..', 'pyyaml', 'lib3')
]
current_dir = os.path.dirname(os.path.realpath(__file__))
for dependency in __dependencies__:
    path = os.path.realpath(os.path.join(current_dir, *dependency))
    sys.path.append(path)

# Usefull shell access
from libs import *
import animation, rigging

