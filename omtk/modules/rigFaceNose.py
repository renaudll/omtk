from omtk.modules import rigFaceAvarGrps
from omtk.modules import rigFaceAvar
from omtk.libs import libRigging
import pymel.core as pymel
from maya import cmds

class CtrlNose(rigFaceAvar.CtrlFaceMicro):
    pass


class FaceNose(rigFaceAvarGrps.AvarGrpAreaOnSurface):
    """
    The Nose is composed of two zones. The uppernose and the lower nose.
    The uppernose is user specifically for it's yaw and pitch rotation.
    Everything under is considered a nostril.

    Note that this was done reallllly quickly and cleanup may be needed in the future.
    """
    # TODO: Implement AvarGrpAreaOnSurface class
    #_DEFORMATION_ORDER = 'post'
    #_CLS_AVAR = AvarJaw
    SHOW_IN_UI = True
    IS_SIDE_SPECIFIC = False
    _CLS_CTRL = CtrlNose
    CREATE_MACRO_AVAR_ALL = True
    CREATE_MACRO_AVAR_HORIZONTAL = False
    CREATE_MACRO_AVAR_VERTICAL = False


def register_plugin():
    return FaceNose
