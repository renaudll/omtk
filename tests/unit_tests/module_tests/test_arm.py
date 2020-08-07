"""
Tests for the Arm module.
"""
import pytest
import pymel.core as pymel
from omtk.libs import libRigging
from omtk.modules.arm import Arm
from omtk.core.rig import Rig


@pytest.fixture
def arm_without_parent():
    """
    Create a scene with an arm.
    """
    names = ["jnt_upperarm_l", "jnt_forearm_l", "jnt_hand_l"]
    positions = [[0, 0, 0], [3, 0, -2], [6, 0, 0]]
    jnts = [pymel.joint(name=name, position=pos) for name, pos in zip(names, positions)]
    libRigging.align_joints_to_direction(jnts, [0, 0, -1])

    return Arm(jnts, name="arm_l", rig=Rig())


def test_build_arm(arm_without_parent):
    """
    Ensure we can build an arm.
    """
    arm_without_parent.build()
    arm_without_parent.unbuild()
    arm_without_parent.build()
