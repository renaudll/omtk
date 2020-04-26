from omtk.core import *
import constants
import pymel.core as pymel

__version__ = "0.0.6"

logging.basicConfig()

# HACK: Load matrixNodes.dll
pymel.loadPlugin("matrixNodes", quiet=True)


def show():
    from omtk.widgets import main_window

    main_window.show()
