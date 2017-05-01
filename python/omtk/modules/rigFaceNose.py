from omtk.modules import rigFaceAvarGrps
from omtk.modules import rigFaceAvar
from omtk.models import modelInteractiveCtrl


class CtrlNose(rigFaceAvar.CtrlFaceMicro):
    pass


class ModelMicroAvarNose(modelInteractiveCtrl.ModelInteractiveCtrl):
    def connect(self, avar, ud=True, fb=True, lr=True, yw=True, pt=True, rl=True, sx=True, sy=True, sz=True):
        # avar_tweak = avar_grp._get_micro_tweak_avars_dict().get(avar, None)
        avar_tweak = False  # todo: fix me!
        # if avar_tweak:
        #     super(ModelMicroAvarNose, self).connect(avar, avar_grp, ud=ud, fb=fb, lr=False, yw=False, pt=False,
        #                                             rl=False, sx=False, sy=False, sz=False)
        #     super(ModelMicroAvarNose, self).connect(avar_tweak, avar_grp, ud=False, fb=False, lr=lr, yw=yw, pt=pt,
        #                                             rl=rl, sx=sx, sy=sy, sz=sz)
        # else:
        super(ModelMicroAvarNose, self).connect(avar, ud=ud, fb=fb, lr=lr, yw=yw, pt=pt, rl=rl, sx=sx,
                                                sy=sy, sz=sz)


class FaceNose(rigFaceAvarGrps.AvarGrp):
    """
    The Nose is composed of two zones. The uppernose and the lower nose.
    The uppernose is user specifically for it's yaw and pitch rotation.
    Everything under is considered a nostril.

    Note that this was done reallllly quickly and cleanup may be needed in the future.
    """
    # _DEFORMATION_ORDER = 'post'
    # _CLS_AVAR = AvarJaw
    SHOW_IN_UI = True
    IS_SIDE_SPECIFIC = False
    _CLS_CTRL = CtrlNose
    _CLS_MODEL_CTRL_MICRO = ModelMicroAvarNose
    CREATE_MACRO_AVAR_ALL = True
    CREATE_MACRO_AVAR_HORIZONTAL = False
    CREATE_MACRO_AVAR_VERTICAL = False

    def get_default_name(self):
        return 'nose'


def register_plugin():
    return FaceNose
