import pymel.core as pymel
from omtk.core.macros import BaseMacro
from omtk.libs import libSkeleton


class SkelResetJointRotation(BaseMacro):
    def run(self):
        jnts = pymel.selected(type="joint")
        for jnt in jnts:
            libSkeleton.transfer_rotation_to_joint_orient(jnt)


def register_plugin():
    return SkelResetJointRotation
