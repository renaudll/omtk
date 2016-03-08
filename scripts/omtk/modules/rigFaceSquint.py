import pymel.core as pymel
import collections

import omtk.classAvar
from omtk.libs import libCtrlShapes
from omtk import classModuleFace

class CtrlSquint(omtk.classAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()

class FaceSquint(classModuleFace.ModuleFaceLftRgt):
    _CLS_CTRL = CtrlSquint

    ui_show = True
