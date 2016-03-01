from omtk import classModuleFace
from omtk import classAvar
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libRigging

class CtrlBrow(classAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()


class FaceBrow(classModuleFace.ModuleFaceLftRgt):
    _CLS_CTRL = CtrlBrow