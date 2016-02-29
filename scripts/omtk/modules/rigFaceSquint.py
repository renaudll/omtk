import pymel.core as pymel
import collections

import omtk.classAvar
from omtk import classModule
from omtk.classModule import Module
from omtk.classCtrl import BaseCtrl
from omtk.libs import libRigging
from omtk.libs import libCtrlShapes
from omtk.libs import libPython
from omtk.libs import libPymel
from omtk import classModuleFace

class CtrlSquint(omtk.classAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()

class FaceSquint(classModuleFace.ModuleFace):
    pass