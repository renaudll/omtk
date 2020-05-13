"""
Tests for the Leg module.
"""
import pytest
import pymel.core as pymel
from omtk.libs import libRigging
from omtk.modules.leg import Leg
from omtk.core.rig import Rig


@pytest.fixture
def leg():
    """
    Create a scene with an leg.
    """
    names = ["jnt_thigh_l", "jnt_calf_l", "jnt_foot_l", "jnt_toes_l", "jne_toes_l"]
    positions = [
        [0.0, 5.0, 0.0],
        [0.0, 3.0, 1.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 0.0, 2.0],
    ]
    jnts = [pymel.joint(name=name, position=pos) for name, pos in zip(names, positions)]
    libRigging.align_joints_to_direction(jnts, [0, 0.5, 0.5])

    return Leg(jnts, name="leg_l", rig=Rig())


def test_build_leg(leg):
    """
    Ensure we can build an leg.
    """
    leg.build()
