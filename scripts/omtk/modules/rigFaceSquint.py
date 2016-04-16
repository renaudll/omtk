import pymel.core as pymel
import collections

from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps

from omtk.libs import libCtrlShapes

class CtrlSquint(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()

class FaceSquint(rigFaceAvarGrps.ModuleFaceLftRgt):
    _CLS_CTRL = CtrlSquint
    IS_SIDE_SPECIFIC = False

    SHOW_IN_UI= True
