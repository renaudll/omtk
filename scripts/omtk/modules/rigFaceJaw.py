"""
Logic for the "FaceJaw" module
"""
import pymel.core as pymel

from omtk.libs import libCtrlShapes
from omtk.libs import libRigging
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps


class CtrlJaw(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        node = libCtrlShapes.create_triangle_low()
        # node.r.lock()
        node.s.lock()
        return node


class AvarJaw(rigFaceAvar.Avar):
    """
    This avar is not designed to use any surface.
    """

    SHOW_IN_UI = False
    IS_SIDE_SPECIFIC = False
    CLS_CTRL = CtrlJaw

    def get_default_name(self):
        return "Jaw"

    def _get_ctrl_tm(self):
        """
        If the rigger provided an extra influence (jaw_end),
        we'll use it to define the ctrl and influence position.
        """
        ref = self.jnt.getMatrix(worldSpace=True)
        pos_s = pymel.datatypes.Point(self.jnt.getTranslation(space="world"))
        pos_e = pymel.datatypes.Point(1, 0, 0) * ref
        direction = pos_e - pos_s
        geos = self.rig.get_shapes()
        p = libRigging.ray_cast_farthest(pos_s, direction, geos)
        if p:
            return pymel.datatypes.Matrix(
                [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [p.x, p.y, p.z, 1]
            )

        self.log.warning(
            "Raycast failed. Using %s as the ctrl position reference.", self.jnt
        )
        return super(AvarJaw, self)._get_ctrl_tm()


class FaceJaw(rigFaceAvarGrps.AvarGrp):
    """
    AvarGrp customized for jaw rigging. Necessary for some facial modules.
    The Jaw is a special zone since it doesn't happen in pre-deform,
    it happen in the main skinCluster.
    The Jaw global avars are made
    """

    CLS_AVAR_MICRO = AvarJaw
    CLS_CTRL_MICRO = None
    SHOW_IN_UI = True
    SINGLE_INFLUENCE = True
    CREATE_MACRO_AVAR_ALL = False
    CREATE_MACRO_AVAR_HORIZONTAL = False
    CREATE_MACRO_AVAR_VERTICAL = False


def register_plugin():
    return FaceJaw
