from omtk.modules import rigFaceAvarGrps
from omtk.modules import rigFaceAvar
from omtk.libs import libCtrlShapes
import pymel.core as pymel

class CtrlLidUpp(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()


class CtrlLidLow(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()

class FaceLids(rigFaceAvarGrps.AvarGrpUppLow):
    """
    FaceLids behave the same a a standard AvarGrp with an Upp and Low section.
    However to adapt ourself to non-symetrical eyes, we use two surface to slide on.
    """
    _CLS_CTRL_UPP = CtrlLidUpp
    _CLS_CTRL_LOW = CtrlLidLow
    IS_SIDE_SPECIFIC=True

    SHOW_IN_UI = True

    def __init__(self, *args, **kwargs):
        super(FaceLids, self).__init__(*args, **kwargs)
        self.surface_upp = None
        self.surface_low = None

    def handle_surface(self, rig):
        if self.surface_upp is None:
            pymel.warning("Can't find surface for {0}, creating one.".format(self))
            self.surface_upp = self.create_surface(rig, name='SurfaceUpp')

        if self.surface_low is None:
            pymel.warning("Can't find surface for {0}, creating one.".format(self))
            self.surface_low = self.create_surface(rig, name='SurfaceLow')

    def configure_avar(self, rig, avar):
        inf = avar.jnt
        if inf in self.jnts_upp:
            avar.surface = self.surface_upp
        else:
            avar.surface = self.surface_low

    def get_module_name(self):
        return 'Lid'

    def get_multiplier_u(self):
        # Since the V go all around the sphere, it is too much range.
        # We'll restrict ourself only to a single quadrant.
        return 0.25
