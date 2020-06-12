"""
Logic for the "FaceEyeLids" module
"""
import pymel.core as pymel
from omtk.libs import libCtrlShapes
from omtk.modules.face.avar import Avar, BaseCtrlFace
from omtk.modules.face.avar_grp import AvarGrp, AvarMacroUpp, AvarMacroLow


class CtrlEyeLidUpp(BaseCtrlFace):
    def create_ctrl(self, size=1.0, **kwargs):
        return libCtrlShapes.create_triangle_upp(size=size)


class CtrlEyeLidLow(BaseCtrlFace):
    def create_ctrl(self, size=1.0, **kwargs):
        return libCtrlShapes.create_triangle_low(size=size)


class FaceEyeLidsMacroUpp(AvarMacroUpp):
    CLS_CTRL = CtrlEyeLidUpp


class FaceEyeLidsMacroLow(AvarMacroLow):
    CLS_CTRL = CtrlEyeLidLow


class FaceEyeLids(AvarGrp):
    """
    AvarGrp setup customized for Eyelids rigging.
    FaceLids behave the same a a standard AvarGrp with an Upp and Low section.
    However to adapt ourself to non-symetrical eyes, we use two surface to slide on.
    """

    IS_SIDE_SPECIFIC = True
    CLS_AVAR_MACRO_UPP = FaceEyeLidsMacroUpp
    CLS_AVAR_MACRO_LOW = FaceEyeLidsMacroLow
    CREATE_MACRO_AVAR_HORIZONTAL = True
    CREATE_MACRO_AVAR_VERTICAL = True
    CREATE_MACRO_AVAR_ALL = True

    def __init__(self, *args, **kwargs):
        super(FaceEyeLids, self).__init__(*args, **kwargs)
        self.surface_upp = None
        self.surface_low = None

    def handle_surface(self):
        """
        Create a separated surface for the upper and lower lids.
        This allow the rigger to easily tweak how each lids react which
        may be necessary with hyper-realistic characters.

        If the user provided it's own surface (via the input property),
        we'll use it for the upper AND lower lids.
        This is allow spheres to be used for very cartoony characters.
        """
        surfaces = self.get_surfaces()

        # If the user provided surface, pop them out of the input property
        # and store them in the surface_[upp/low] property.
        if surfaces:
            surface = next(iter(surfaces), None)
            for surface in surfaces:
                self.input.remove(surface)
            self.surface_upp = surface
            self.surface_low = surface

        # Create surfaces if they were not provided
        if self.surface_upp is None:
            pymel.warning("Can't find surface for %s, creating one." % self)
            self.surface_upp = self.create_surface(name="SurfaceUpp")
            self.input.append(self.surface_upp)

        if self.surface_low is None:
            pymel.warning("Can't find surface for %s, creating one." % self)
            self.surface_low = self.create_surface(name="SurfaceLow")
            self.input.append(self.surface_low)

    def configure_avar(self, avar):
        inf = avar.jnt
        if inf in self.get_jnts_upp():
            avar.surface = self.surface_upp
        else:
            avar.surface = self.surface_low

    def get_default_name(self):
        return "eyelid"

    # def get_multiplier_u(self):
    #     # Since the V go all around the sphere, it is too much range.
    #     # We'll restrict ourself only to a single quadrant.
    #     return 0.25


def register_plugin():
    """
    Register the plugin. This function is expected by plugin_manager.

    :return: The plugin to register
    :rtype: omtk.core.modules.Module
    """
    return FaceEyeLids