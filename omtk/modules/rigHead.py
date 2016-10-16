from omtk.modules import rigFK

class CtrlHead(rigFK.CtrlFk):
    pass

class Head(rigFK.FK):
    """
    Simple FK setup customized for head rigging. Mandatory when using facial modules.
    """
    _CLS_CTRL = CtrlHead

def register_plugin():
    return Head