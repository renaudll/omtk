"""
Original code by Jimmy Goulet (https://github.com/goujin), thanks for the contribution!
"""
import pymel.core as pymel
from omtk.core import classMacro
from omtk.libs import libCtrlMatch


class CtrlMatchSelected(classMacro.BaseMacro):
    def run(self):
        libCtrlMatch.controller_matcher(selection=pymel.selected(), mirror_prefix=None, flip=False)


def register_plugin():
    return CtrlMatchSelected
