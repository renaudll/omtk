"""
DEV: HOW TO RELOAD OMTK:
import omtk
from omtk.libs import libPython
reload libPython
libPython.reload_module_recursive(omtk)
"""


# Add dependencies to sys paths
import sys, os, inspect
module_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.abspath(os.path.join(module_dir, 'deps')))

from libs import *

import animation
import managing
import rigging

def test(**kwargs):
    import libSerialization; reload(libSerialization)

    # Test libSerialization
    from omtk.libs import libSerialization; reload(libSerialization)
    libSerialization.test(**kwargs)

    # Test libFormula
    from omtk.libs import libFormula; reload(libFormula)
    libFormula.test(**kwargs)

    # Test autorig
    from omtk.rigging import autorig; reload(autorig)
    autorig.test(**kwargs)
