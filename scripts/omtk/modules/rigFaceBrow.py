from omtk.modules import rigFaceAvarGrps
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libRigging
from omtk.modules import rigFaceAvar

class CtrlBrow(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()


class FaceBrow(rigFaceAvarGrps.AvarGrpLftRgt):
    _CLS_CTRL = CtrlBrow

    SHOW_IN_UI= True
    IS_SIDE_SPECIFIC = False