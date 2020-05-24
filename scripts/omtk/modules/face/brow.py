"""
Logic for the "FaceBrow" module
"""
import pymel.core as pymel
from pymel.core.datatypes import Matrix

from omtk.libs import libCtrlShapes
from omtk.libs import libRigging
from omtk.modules.face.avar import Avar, BaseCtrlFace
from omtk.modules.face.avar_grp import AvarGrp


class CtrlBrow(BaseCtrlFace):
    """
    Ctrl for brow avars
    """

    def create_ctrl(self, **kwargs):
        """
        Build the
        :param dict kwargs: Keyword arguments, unused
        :return:
        """
        return libCtrlShapes.create_triangle_low()


class AvarBrow(Avar):
    CLS_CTRL = CtrlBrow


class FaceBrow(AvarGrp):
    """
    AvarGrp customized for Brow rigging.
    """

    CLS_AVAR_MICRO = AvarBrow

    SHOW_IN_UI = True
    IS_SIDE_SPECIFIC = False
    CREATE_MACRO_AVAR_HORIZONTAL = True
    CREATE_MACRO_AVAR_VERTICAL = False
    CREATE_MACRO_AVAR_ALL = False

    def _get_ctrl_tm_hint(self, avar):
        """
        For the upp and low macro, instead of finding an influence
        to match it's transform, use the average of all upp/low micros.

        :param avar: An avar to query a transform hint from
        :type avar: omtk.modules.avar.Avar
        :return: A transform hint if applicable
        :rtype: Matrix or None
        """
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

    def get_default_name(self):
        return "brow"


def register_plugin():
    """
    Register the plugin. This function is expected by plugin_manager.

    :return: The plugin to register
    :rtype: omtk.core.modules.Module
    """
    return FaceBrow
