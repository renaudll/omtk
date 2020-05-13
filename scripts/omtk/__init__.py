"""
Public entry point.
"""

from omtk.core import *

from omtk.vendor import libSerialization
import constants
import pymel.core as pymel

# TODO: Set __all__


__version__ = "0.0.6"

# HACK: Load matrixNodes.dll
pymel.loadPlugin("matrixNodes", quiet=True)


def show():
    from omtk.widgets import main_window

    main_window.show()


# Register alias for deprecated classes
for src, dst in (
    ("Node.BaseCtrl.BaseCtrlFace.BaseCtrlUpp", "Node.BaseCtrl.BaseCtrlFace.CtrlFaceUpp"),
    ("Node.BaseCtrl.BaseCtrlFace.BaseCtrlLow", "Node.BaseCtrl.BaseCtrlFace.CtrlFaceLow"),
    ("Module.AbstractAvar.AvarGrp.AvarGrpOnSurface", "Module.AbstractAvar.AvarGrp"),
):
    libSerialization.register_alias("omtk", src, dst)
