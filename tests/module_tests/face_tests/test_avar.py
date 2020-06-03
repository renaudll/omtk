"""
Tests for the Avar module.
"""
import os

import pytest

from maya import cmds
from pymel.core.datatypes import Matrix

from omtk.core.rig import Rig
from omtk.modules.face.models.avar_to_infl.linear import AvarLinearModel
from omtk.modules.face.models.avar_to_infl.surface import AvarSurfaceModel
from omtk.modules.face.models.avar_to_ctrl.linear import ModelCtrlLinear
from omtk.modules.face.models.avar_to_ctrl.interactive import ModelInteractiveCtrl
from omtk.modules.face.avar import Avar

from ... import helpers


_RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "..", "resources")


class AvarImpl1(Avar):
    """Implementation that test linear ctrl and influence models."""

    CLS_MODEL_CTRL = ModelCtrlLinear
    CLS_MODEL_INFL = AvarLinearModel


class AvarImpl2(Avar):
    """Implementation which influence follow a surface."""

    CLS_MODEL_CTRL = ModelCtrlLinear
    CLS_MODEL_INFL = AvarSurfaceModel


class AvarImpl3(Avar):
    """Implementation where the ctrl follow a mesh."""

    CLS_MODEL_CTRL = ModelInteractiveCtrl
    CLS_MODEL_INFL = AvarLinearModel


_POSE_REST = {
    "anm_test": Matrix(
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ),
    "joint1": Matrix(
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ),
}


def test_linear_unit_no_parent():
    """
    Validate we can build our first Avar implementation.
    This implementation is totally linear.
    """
    cmds.joint()
    avar = AvarImpl1(input=["joint1"], name="test", rig=Rig())
    avar.build()
    helpers.assert_match_pose(_POSE_REST)

    # Validate that moving the avar will move the controller.
    avar.attr_lr.set(1.0)
    avar.attr_ud.set(2.0)
    avar.attr_fb.set(3.0)
    avar.attr_yw.set(10.0)
    avar.attr_pt.set(20.0)
    avar.attr_rl.set(30.0)

    # Validate the infl model
    helpers.assert_match_pose_from_file(os.path.join(_RESOURCE_DIR, "test_avar_infl_linear.json"))

    # Validate the ctrl model
    helpers.assert_match_pose_from_file(os.path.join(_RESOURCE_DIR, "test_avar_ctrl_linear.json"))

    avar.unbuild()


@pytest.mark.usefixtures()
def test_influence_surface_no_parent():
    """
    Validate we can build our 2nd Avar implementation.
    This implementation influence follow a surface instead of moving in linear space.
    """
    cmds.joint()
    cmds.nurbsPlane(axis=[0.0, 0.0, 1.0], patchesV=10)  # Face the Z axis
    cmds.nonLinear("nurbsPlane1", type="bend", curvature=45)
    cmds.setAttr("bend1Handle.rotateY", 90)  # Bend vertically

    avar = AvarImpl2(input=["joint1", "nurbsPlane1"], name="test", rig=Rig())
    avar.build()
    helpers.assert_match_pose(_POSE_REST)

    # Move the ctrl and see if the influence follow properly
    avar.ctrl.translateY.set(2.0)  # TODO: Validate default sensitivity
    helpers.assert_match_pose_from_file(os.path.join(_RESOURCE_DIR, "test_avar_ctrl_surface.json"))

    avar.unbuild()


def test_interactive_ctrl_no_parent():
    """
    Validate we can build our 3nd Avar implementation.
    This implementation ctrl follow a surface.
    """
    cmds.polySphere()
    cmds.select(clear=True)
    cmds.joint()
    cmds.joint(
        position=[0.0, 0.0, 0.75]
    )  # Note that the sphere end a 1.0, 0.75 is a little inside.
    cmds.skinCluster("pSphere1", "joint1", "joint2")

    avar = AvarImpl3(input=["joint2", "pSphere1"], name="test", rig=Rig())
    avar.build()
    helpers.assert_match_pose(
        {
            "joint2": Matrix(
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.75, 1.0],
            ),
            "anm_test": Matrix(
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0, 1.0],
            ),
        }
    )

    # Move the ctrl and see if the influence follow properly
    avar.ctrl.translateY.set(1.0)
    helpers.assert_match_pose(
        {
            "joint2": Matrix(
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 1.0, 0.75, 1.0],
            ),
            "anm_test": Matrix(
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.5, 1.0, 1.0],
            ),
        }
    )
