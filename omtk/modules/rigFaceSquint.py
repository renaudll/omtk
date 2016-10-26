import pymel.core as pymel

from omtk.libs import libCtrlShapes
from omtk.libs import libRigging
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps

class CtrlSquint(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()

class FaceSquint(rigFaceAvarGrps.AvarGrpAreaOnSurface):
    """
    AvarGrp setup customized for squint rigging.
    """
    _CLS_CTRL = CtrlSquint
    IS_SIDE_SPECIFIC = False
    SHOW_IN_UI= True
    CREATE_MACRO_AVAR_HORIZONTAL = True
    CREATE_MACRO_AVAR_VERTICAL = False
    CREATE_MACRO_AVAR_ALL = False

    def _build_avar_macro_l(self, jnt_tm=None, ctrl_tm=None, **kwargs):
        # Find the middle of l squint.
        pos = libRigging.get_average_pos_between_vectors(self.get_jnts_l())
        jnt_tm = pymel.datatypes.Matrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            pos.x, pos.y, pos.z, 1
        )
        super(FaceSquint, self)._build_avar_macro_l(jnt_tm=jnt_tm, ctrl_tm=jnt_tm, **kwargs)


    def _build_avar_macro_r(self, jnt_tm=None, ctrl_tm=None, **kwargs):
        # Find the middle of r squint.
        pos = libRigging.get_average_pos_between_vectors(self.get_jnts_r())
        jnt_tm = pymel.datatypes.Matrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            pos.x, pos.y, pos.z, 1
        )
        super(FaceSquint, self)._build_avar_macro_r(jnt_tm=jnt_tm, ctrl_tm=jnt_tm, **kwargs)

def register_plugin():
    return FaceSquint