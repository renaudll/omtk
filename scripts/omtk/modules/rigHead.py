from omtk.modules import rigFK

class CtrlHead(rigFK.CtrlFk):
    pass

class Head(rigFK.FK):
    """
    Note that the influence assigned to the head module will be used by each 'face' modules.
    """
    _CLS_CTRL = CtrlHead