from omtk.core.macros import BaseMacro
from omtk.libs import libSkeleton


class SkelResetJointRotation(BaseMacro):
    def run(self):
        libSkeleton.freeze_selected_joints_rotation()


def register_plugin():
    return SkelResetJointRotation
