from omtk.modules import rigFK

class CtrlNeck(rigFK.CtrlFk):
    pass

class Neck(rigFK.FK):
    _CLS_CTRL = CtrlNeck