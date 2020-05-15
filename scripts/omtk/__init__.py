"""
Public entry point.
"""
import pymel.core as pymel
from maya import cmds

from omtk.core import *
from omtk.vendor import libSerialization


__version__ = "0.0.6"

# HACK: Load matrixNodes.dll
cmds.loadPlugin("matrixNodes", quiet=True)


def show():
    from omtk.widgets import main_window

    main_window.show()


# Register alias for deprecated classes
for src, dst in (
    (
        "Node.BaseCtrl.BaseCtrlFace.BaseCtrlUpp",
        "Node.BaseCtrl.BaseCtrlFace.CtrlFaceUpp",
    ),
    (
        "Node.BaseCtrl.BaseCtrlFace.BaseCtrlLow",
        "Node.BaseCtrl.BaseCtrlFace.CtrlFaceLow",
    ),
    ("Module.AbstractAvar.AvarGrp.AvarGrpOnSurface", "Module.AbstractAvar.AvarGrp"),
):
    libSerialization.register_alias("omtk", src, dst)

from omtk.core import plugin_manager

# Load plugins
plugin_manager.plugin_manager.get_plugins()
