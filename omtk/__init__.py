import os
import sys

# Load dependencies (including git submodules) in sys.path
__dependencies__ = [
    ('deps',),
    ('../..', 'libSerialization',)
]
current_dir = os.path.dirname(os.path.realpath(__file__))
for dependency in __dependencies__:
    path = os.path.realpath(os.path.join(current_dir, *dependency))
    sys.path.append(path)

import core
from core import *

import modules
from modules import *

import rigs
from rigs import *

import libSerialization
from libs import libPython

import uiLogic

def _reload():
    """
    Reload all module in their respective order.
    """
    reload(core)
    core._reload()

    reload(modules)
    modules._reload()

    reload(rigs)
    rigs._reload()

    reload(uiLogic)

    from omtk.libs import libAttr; reload(libAttr)
    from omtk.libs import libCtrlShapes; reload(libCtrlShapes)
    from omtk.libs import libFormula; reload(libFormula)
    from omtk.libs import libPython; reload(libPython)
    from omtk.libs import libQt; reload(libQt)
    from omtk.libs import libRigging; reload(libRigging)
    from omtk.libs import libSkinning; reload(libSkinning)
    from omtk.libs import libStringMap; reload(libStringMap)
    from omtk.libs import libUtils; reload(libUtils)

    # Ensure libSerialization don't hold outdated definition of the classes.
    libSerialization.clear_maya_cache()

def show():
    """
    Show a simple gui. Note that PySide or PyQt4 is needed.
    """

    import uiLogic
    uiLogic.show()
