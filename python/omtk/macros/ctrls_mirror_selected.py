import pymel.core as pymel
from omtk.core import macros
from omtk.libs import libCtrlMatch


class MacroMirrorSelectedCtrls(macros.BaseMacro):
    def run(self):
        libCtrlMatch.controller_matcher(selection=pymel.selected(), mirror_prefix=["L_", "R_"], flip=True)


def register_plugin():
    return MacroMirrorSelectedCtrls
