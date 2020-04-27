"""
Mirror right side influences to left side influence.
"""
from omtk.core.macros import BaseMacro


class SkelMirrorRightToLeft(BaseMacro):
    def run(self):
        raise NotImplementedError


def register_plugin():
    return SkelMirrorRightToLeft
