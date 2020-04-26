"""
Align selected joints in 2D place facing the viewport camera.
This won't affect the start and end position.
"""
from omtk.core.macros import BaseMacro
from omtk.libs import libRigging


class AlignJointsToView(BaseMacro):
    def run(self):
        libRigging.align_selected_joints_to_persp()


def register_plugin():
    return AlignJointsToView
