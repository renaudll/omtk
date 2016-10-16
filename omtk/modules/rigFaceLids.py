from omtk.modules import rigFaceAvarGrps
from omtk.modules import rigFaceAvar
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
import pymel.core as pymel

class CtrlLidUpp(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()


class CtrlLidLow(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()


class FaceLids(rigFaceAvarGrps.AvarGrpAreaOnSurface):
    """
    AvarGrp setup customized for Eyelids rigging.
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

    def handle_surface(self):
        """
        Create a separated surface for the upper and lower lids.
        This allow the rigger to easily tweak how each lids react which may be necessary with hyper-realistic characters.

        If the user provided it's own surface (via the input property), we'll use it for the upper AND lower lids.
        This is mainly to support custom surface like spheres for very cartoony characters.
        """
        # Get all surfaces provided by the input property.
        def get_surface(obj):
            if libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface):
                return obj
        surfaces = filter(None, map(get_surface, self.input))

        # If the user provided surface, pop them out of the input property and store them in the surface_[upp/low] property.
        if surfaces:
            surface = next(iter(surfaces), None)
            for surface in surfaces:
                self.input.remove(surface)
            self.surface_upp = surface
            self.surface_low = surface

        # Create surfaces if they were not provided
        if self.surface_upp is None:
            pymel.warning("Can't find surface for {0}, creating one.".format(self))
            self.surface_upp = self.create_surface(name='SurfaceUpp')

        if self.surface_low is None:
            pymel.warning("Can't find surface for {0}, creating one.".format(self))
            self.surface_low = self.create_surface(name='SurfaceLow')

        # We still provide the surface property in case we need a controller to be connected directly to it.
        self.surface = self.surface_upp

    def configure_avar(self, avar):
        inf = avar.jnt
        if inf in self.get_jnts_upp():
            avar.surface = self.surface_upp
        else:
            avar.surface = self.surface_low

    def get_module_name(self):
        return 'Lid'

    def get_multiplier_u(self):
        # Since the V go all around the sphere, it is too much range.
        # We'll restrict ourself only to a single quadrant.
        return 0.25

def register_plugin():
    return FaceLids
