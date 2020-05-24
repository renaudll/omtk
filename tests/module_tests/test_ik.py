"""
Tests for the Leg module.
"""
import pytest
import pymel.core as pymel
from omtk.libs import libRigging
from omtk.modules.leg import Leg
from omtk.modules.ik import IK
from omtk.core.rig import Rig


@pytest.fixture
def ik():
    """
    Create a scene with an ik.
    """
    names = ["jnt_thigh", "jnt_calf", "jnt_foot"]
    positions = [[0.0, 5.0, 0.0], [0.0, 3.0, 1.0], [0.0, 1.0, 0.0]]
    jnts = [pymel.joint(name=name, position=pos) for name, pos in zip(names, positions)]
    libRigging.align_joints_to_direction(jnts, [0, 0.5, 0.5])

    return IK(jnts, name="ik", rig=Rig())


def test_build_ik(ik):
    """
    Ensure we can build an ik.
    """
    ik.build()
