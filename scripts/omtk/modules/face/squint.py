"""
Logic for the "FaceSquint" module.
"""
import pymel.core as pymel

from omtk.libs import libCtrlShapes
from omtk.libs import libRigging
from omtk.modules.face.avar import Avar, BaseCtrlFace
from omtk.modules.face.avar_grp import AvarGrp


class CtrlSquint(BaseCtrlFace):
    def create_ctrl(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()


class FaceSquint(AvarGrp):
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

    def _get_ctrl_tm_hint(self, avar):
        """
        For the upp and low macro, instead of finding an influence
        to match it's transform, use the average of all upp/low micros.

        :param avar: An avar to query a transform hint from
        :type avar: omtk.modules.avar.Avar
        :return: A transform hint if applicable
        :rtype: Matrix or None
        """
        # TODO: This is duplicate code from FaceBrow, find a better way?
        if avar is self.avar_l:
            pos = libRigging.get_average_pos_between_vectors(self.get_jnts_l())
            return Matrix(
                [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [pos.x, pos.y, pos.z, 1]
            )
        if avar is self.avar_r:
            pos = libRigging.get_average_pos_between_vectors(self.get_jnts_r())
            return Matrix(
                [1, 0, 0, 0], [0, -1.0, 0, 0], [0, 0, -1.0, 0], [pos.x, pos.y, pos.z, 1]
            )

        return super(FaceBrow, self)._get_ctrl_tm_hint(avar)


def register_plugin():
    return FaceSquint
