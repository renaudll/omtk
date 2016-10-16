import pymel.core as pymel
from omtk.modules import rigFaceAvarGrps
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libRigging
from omtk.modules import rigFaceAvar

class CtrlBrow(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()


class FaceBrow(rigFaceAvarGrps.AvarGrpAreaOnSurface):
    """
    AvarGrp customized for Brow rigging.
    """
    _CLS_CTRL = CtrlBrow

    SHOW_IN_UI= True
    IS_SIDE_SPECIFIC = False
    CREATE_MACRO_AVAR_HORIZONTAL = True
    CREATE_MACRO_AVAR_VERTICAL = False
    CREATE_MACRO_AVAR_ALL = False

    def _build_avar_macro_l(self, jnt_tm=None, ctrl_tm=None, **kwargs):
        # Find the middle of l eyebrow.
        pos = libRigging.get_average_pos_between_vectors(self.get_jnts_l())
        jnt_tm = pymel.datatypes.Matrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            pos.x, pos.y, pos.z, 1
        )
        super(FaceBrow, self)._build_avar_macro_l(jnt_tm=jnt_tm, ctrl_tm=jnt_tm, **kwargs)


    def _build_avar_macro_r(self, jnt_tm=None, ctrl_tm=None, **kwargs):# Create right avar if necessary
        pos = libRigging.get_average_pos_between_vectors(self.get_jnts_r())
        jnt_tm = pymel.datatypes.Matrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            pos.x, pos.y, pos.z, 1
        )
        super(FaceBrow, self)._build_avar_macro_r(jnt_tm=jnt_tm, ctrl_tm=jnt_tm, **kwargs)

    def get_module_name(self):
        return 'brow'

def register_plugin():
    return FaceBrow
