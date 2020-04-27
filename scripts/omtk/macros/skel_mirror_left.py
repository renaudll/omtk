"""
Mirror left side influences to right side influence.
"""
from omtk.core.macros import BaseMacro


class SkelMirrorLeftRoRight(BaseMacro):
    def run(self):
        raise NotImplementedError


def register_plugin():
    return SkelMirrorLeftRoRight
