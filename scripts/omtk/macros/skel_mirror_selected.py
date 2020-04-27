"""
Mirror selected influences.
"""
from omtk.core.macros import BaseMacro


class SkelMirrorSelected(BaseMacro):
    def run(self):
        raise NotImplementedError


def register_plugin():
    return SkelMirrorSelected
