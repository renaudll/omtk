import pymel.core as pymel
import collections

import omtk.classModuleFace
from omtk import classModuleFace
from omtk import classAvar
from omtk.classModule import Module
from omtk.classCtrl import BaseCtrl
from omtk.modules.rigIK import IK
from omtk.modules.rigFK import FK
from omtk.libs import libRigging
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel

class CtrlLidUpp(classAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()


class CtrlLidLow(classAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()

class FaceLids(classModuleFace.ModuleFaceUppDown):
    _CLS_CTRL_UPP = CtrlLidUpp
    _CLS_CTRL_LOW = CtrlLidLow

    ui_show = True

    def get_multiplier_u(self):
        # Since the V go all around the sphere, it is too much range.
        # We'll restrict ourself only to a single quadrant.
        return 0.25
