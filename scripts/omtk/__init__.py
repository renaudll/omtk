"""
Public entry point.
"""


__version__ = "0.0.6"

# HACK: Load matrixNodes.dll
# from maya import cmds
# cmds.loadPlugin("matrixNodes", quiet=True)


def show():
    from omtk.widgets import main_window

    main_window.show()


def show_nodegraph():
    from omtk.qt_widgets import window_main

    window_main.show()


try:  # Necessary for demo_ui.py
    import maya.cmds
except ImportError:
    pass
else:
    from .core.api import *
    from omtk.vendor import libSerialization

    from omtk.core import plugin_manager

    # Load plugins
    plugin_manager.plugin_manager.get_plugins()

    # Register alias for deprecated classes
    for src, dst in (
        ("Node.BaseCtrl.BaseCtrlFace.BaseCtrlUpp", "Node.BaseCtrl.BaseCtrlFace.CtrlFaceUpp",),
        ("Node.BaseCtrl.BaseCtrlFace.BaseCtrlLow", "Node.BaseCtrl.BaseCtrlFace.CtrlFaceLow",),
        ("Module.AbstractAvar.AvarGrp.AvarGrpOnSurface", "Module.AbstractAvar.AvarGrp",),
        ("Module.AbstractAvar.AvarFollicle", "Module.AbstractAvar.AvarGrp",),
    ):
        libSerialization.register_alias("omtk", src, dst)
