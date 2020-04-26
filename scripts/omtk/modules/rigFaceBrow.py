import pymel.core as pymel
from omtk.modules import rigFaceAvarGrps
from omtk.libs import libCtrlShapes
from omtk.libs import libRigging
from omtk.modules import rigFaceAvar


class CtrlBrow(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()


class FaceBrow(rigFaceAvarGrps.AvarGrpOnSurface):
    """
    AvarGrp customized for Brow rigging.
    """

    _CLS_CTRL = CtrlBrow

    SHOW_IN_UI = True
    IS_SIDE_SPECIFIC = False
    CREATE_MACRO_AVAR_HORIZONTAL = True
    CREATE_MACRO_AVAR_VERTICAL = False
    CREATE_MACRO_AVAR_ALL = False

    def _create_avar_macro_l_ctrls(self, ctrl_tm=None, **kwargs):
        # Find the middle of l eyebrow.
        pos = libRigging.get_average_pos_between_vectors(self.get_jnts_l())
        ctrl_tm = pymel.datatypes.Matrix(
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, pos.x, pos.y, pos.z, 1
        )

        super(FaceBrow, self)._create_avar_macro_l_ctrls(ctrl_tm=ctrl_tm)

    def _create_avar_macro_r_ctrls(self, ctrl_tm=None, **kwargs):
        # Find the middle of l eyebrow.
        # We expect the right-side influence to be mirrored in behavior.
        # However this should be applied to to influence tm, not the ctrl tm. Clean this please.
        pos = libRigging.get_average_pos_between_vectors(self.get_jnts_r())
        ctrl_tm = pymel.datatypes.Matrix(
            1, 0, 0, 0, 0, -1.0, 0, 0, 0, 0, -1.0, 0, pos.x, pos.y, pos.z, 1
        )

        super(FaceBrow, self)._create_avar_macro_r_ctrls(ctrl_tm=ctrl_tm)

    def get_default_name(self):
        return "brow"


def register_plugin():
    return FaceBrow
