"""
Logic for the "Head" module
"""
from omtk.modules.fk import CtrlFk, FK


class CtrlHead(CtrlFk):
    """
    Head single controller
    """

    pass


class Head(FK):
    """
    Simple FK setup customized for head rigging. Mandatory when using facial modules.
    """

    _CLS_CTRL = CtrlHead
    _FORCE_INPUT_NAME = True


def register_plugin():
    """
    Register the plugin. This function is expected by plugin_manager.

    :return: The plugin to register
    :rtype: omtk.core.modules.Module
    """
    return Head
