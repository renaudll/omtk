from omtk.modules import rigFK

class CtrlNeck(rigFK.CtrlFk):
    pass

class Neck(rigFK.FK):
    """
    Simple FK setup with twistbone support.
    """
    _CLS_CTRL = CtrlNeck

def register_plugin():
    return Neck