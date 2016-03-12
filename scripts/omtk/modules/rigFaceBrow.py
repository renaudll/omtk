from omtk.modules import rigFaceAvarGrps
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libRigging
from omtk.modules import rigFaceAvar

class CtrlBrow(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()


class FaceBrow(rigFaceAvarGrps.ModuleFaceLftRgt):
    _CLS_CTRL = CtrlBrow

    ui_show = True