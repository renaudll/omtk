from omtk.modules import rigFaceAvarGrps
from omtk.modules import rigFaceAvar
from omtk.libs import libCtrlShapes

class CtrlLidUpp(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()


class CtrlLidLow(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()

class FaceLids(rigFaceAvarGrps.ModuleFaceUppDown):
    _CLS_CTRL_UPP = CtrlLidUpp
    _CLS_CTRL_LOW = CtrlLidLow

    SHOW_IN_UI = True

    def get_multiplier_u(self):
        # Since the V go all around the sphere, it is too much range.
        # We'll restrict ourself only to a single quadrant.
        return 0.25
