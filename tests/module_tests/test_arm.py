"""
Tests for the Arm module.
"""
import pytest
import pymel.core as pymel
from omtk.libs import libRigging
from omtk.modules.rigArm import Arm
from omtk.core.classRig import Rig


@pytest.fixture
def arm_without_parent():
    """
    Create a scene with an arm.
    """
    names = ["jnt_upperarm_l", "jnt_forearm_l", "jnt_hand_l"]
    positions = [[0, 0, 0], [3, 0, -2], [6, 0, 0]]
    jnts = [pymel.joint(name=name, position=pos) for name, pos in zip(names, positions)]
    libRigging.align_joints_to_direction(jnts, [0, 0, -1])

    arm = Arm(jnts, name="arm_l", rig=Rig())
    return arm


def test_build_arm(arm_without_parent):
    """
    Ensure we can build an arm.
    """
    arm_without_parent.build()
