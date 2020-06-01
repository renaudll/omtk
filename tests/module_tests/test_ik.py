"""
Tests for the Leg module.
"""
import os
import pytest
import pymel.core as pymel
from pymel.core.datatypes import Matrix

from omtk.libs import libRigging
from omtk.modules.ik import IK
from omtk.core.rig import Rig

from .. import helpers

_LOCAL_RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "resources")


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

    helpers.assert_match_pose_from_file(
        os.path.join(_LOCAL_RESOURCE_DIR, "test_ik_rest.json")
    )

    # Validate the IK does not stretch by default
    ik.ctrl_ik.translateX.set(1.0)  # This will stretch the IK beyond it's limit.

    helpers.assert_match_pose_from_file(
        os.path.join(_LOCAL_RESOURCE_DIR, "test_ik_extended.json")
    )

    # Validate the IK can stretch
    ik.ctrl_ik.stretch.set(1.0)
    ik.ctrl_ik.softIkRatio.set(0.0)

    helpers.assert_match_pose_from_file(
        os.path.join(_LOCAL_RESOURCE_DIR, "test_ik_extended_stretch.json")
    )

    # Validate the soft IK work
    ik.ctrl_ik.stretch.set(0.0)
    ik.ctrl_ik.softIkRatio.set(0.1)

    helpers.assert_match_pose_from_file(
        os.path.join(_LOCAL_RESOURCE_DIR, "test_ik_extended_soft.json")
    )

    # Validate the soft IK can stretch
    ik.ctrl_ik.stretch.set(1.0)
    ik.ctrl_ik.softIkRatio.set(0.1)

    helpers.assert_match_pose_from_file(
        os.path.join(_LOCAL_RESOURCE_DIR, "test_ik_extended_soft_stretch.json")
    )
