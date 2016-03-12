import pymel.core as pymel
import collections

from omtk.modules import rigFaceAvar
from omtk.libs import libCtrlShapes
from omtk.core import classModuleFace

class CtrlSquint(rigFaceAvarfrom.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()

class FaceSquint(classModuleFace.ModuleFaceLftRgt):
    _CLS_CTRL = CtrlSquint

    ui_show = True
