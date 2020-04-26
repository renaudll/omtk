from omtk.core import *
import constants
import pymel.core as pymel

logging.basicConfig()

# HACK: Load matrixNodes.dll
pymel.loadPlugin("matrixNodes", quiet=True)


def show():
    from omtk.widgets import main_window

    main_window.show()
