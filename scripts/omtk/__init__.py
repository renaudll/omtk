import logging
import os
import sys
import pymel.core as pymel

# Load dependencies (including git submodules) in sys.path
__dependencies__ = [
    ('deps',)
]
current_dir = os.path.dirname(os.path.realpath(__file__))
for dependency in __dependencies__:
    path = os.path.realpath(os.path.join(current_dir, *dependency))
    sys.path.append(path)

# HACK: Load matrixNodes.dll
pymel.loadPlugin('matrixNodes', quiet=True)

import core
from core import *

import modules
from modules import *

import rigs
from rigs import *

import libs
from libs import *

from omtk.libs import libPython

import uiLogic

def _reload(kill_ui=True):
    """
    Reload all module in their respective order.
    """
    reload(core)
    core._reload()

    reload(modules)
    modules._reload()

    reload(rigs)
    rigs._reload()

    reload(libs)
    libs._reload()

    if kill_ui:
        #Try to kill the window to prevent any close event error
        try:
            pymel.deleteUI('OpenRiggingToolkit')
        except:
            pass

    reload(uiLogic)

def show():
    """
    Show a simple gui. Note that PySide or PyQt4 is needed.
    """

    import uiLogic
    uiLogic.show()
