import pymel.core as pymel
from omtk.core import classMacro
from omtk.libs import libCtrlMatch


class MacroMirrorSelectedCtrls(classMacro.BaseMacro):
    def run(self):
        libCtrlMatch.controller_matcher(selection=pymel.selected(), mirror_prefix=["L_", "R_"], flip=True)


def register_plugin():
    return MacroMirrorSelectedCtrls
