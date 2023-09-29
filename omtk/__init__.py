import sys

from .core import *
import constants
import pymel.core as pymel

# HACK: Load matrixNodes.dll
pymel.loadPlugin('matrixNodes', quiet=True)


def _reload():
    """
    Reload all module in their respective order.
    """
    # Hack: prevent a crash related to loosing our OpenMaya.MSceneMessage events.
    try:
        pymel.deleteUI('OpenRiggingToolkit')
    except:
        pass

    import omtk
    libPython.rreload(omtk)


def show():
    import main_window
    main_window.show()
