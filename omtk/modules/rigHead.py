from omtk.modules import rigFK


class CtrlHead(rigFK.CtrlFk):
    pass


class Head(rigFK.FK):
    """
    Simple FK setup customized for head rigging. Mandatory when using facial modules.
    """
    _CLS_CTRL = CtrlHead
    _NAME_CTRL_MERGE = True  # By default we only expect one controller for the head. (Head_Ctrl > than Head_Head_Ctrl)
    _NAME_CTRL_ENUMERATE = True  # If we find additional influences, we'll use enumeration.


def register_plugin():
    return Head
