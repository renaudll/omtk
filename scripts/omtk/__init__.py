"""
Public entry point.
"""

from omtk.core import *
import constants
import pymel.core as pymel

# TODO: Set __all__


__version__ = "0.0.6"

# HACK: Load matrixNodes.dll
pymel.loadPlugin("matrixNodes", quiet=True)


def show():
    from omtk.widgets import main_window

    main_window.show()
