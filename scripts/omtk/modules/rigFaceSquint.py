"""
Logic for the "FaceSquint" module.
"""
import pymel.core as pymel

from omtk.libs import libCtrlShapes
from omtk.libs import libRigging
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps


class CtrlSquint(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()


class FaceSquint(rigFaceAvarGrps.AvarGrp):
    """
    AvarGrp setup customized for squint rigging.
    """

    _CLS_CTRL = CtrlSquint
    IS_SIDE_SPECIFIC = False
    SHOW_IN_UI = True
    CREATE_MACRO_AVAR_HORIZONTAL = True
    CREATE_MACRO_AVAR_VERTICAL = False
    CREATE_MACRO_AVAR_ALL = False

    def get_default_name(self):
        return "squint"

    def _create_avar_macro_l_ctrls(self, ctrl_tm=None, **kwargs):
        # Find the middle of l eyebrow.
        pos = libRigging.get_average_pos_between_vectors(self.get_jnts_l())
        ctrl_tm = pymel.datatypes.Matrix(
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, pos.x, pos.y, pos.z, 1
        )

        super(FaceSquint, self)._create_avar_macro_l_ctrls(ctrl_tm=ctrl_tm)

    def _create_avar_macro_r_ctrls(self, ctrl_tm=None, **kwargs):
        # Find the middle of l eyebrow.
        pos = libRigging.get_average_pos_between_vectors(self.get_jnts_r())
        ctrl_tm = pymel.datatypes.Matrix(
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, pos.x, pos.y, pos.z, 1
        )

        super(FaceSquint, self)._create_avar_macro_r_ctrls(ctrl_tm=ctrl_tm)


def register_plugin():
    return FaceSquint
