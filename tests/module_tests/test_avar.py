"""
Tests for the Avar module.
"""
import pytest
from maya import cmds
from pymel.core.datatypes import Matrix

from omtk.core.rig import Rig
from omtk.modules.face.models.avar_to_infl.linear import AvarLinearModel
from omtk.modules.face.models.avar_to_infl.surface import AvarSurfaceModel
from omtk.modules.face.models.avar_to_ctrl.linear import ModelCtrlLinear
from omtk.modules.face.models.avar_to_ctrl.interactive import ModelInteractiveCtrl
from omtk.modules.face.avar import Avar

from .. import helpers


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
    "test_anm": Matrix(
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


def test_linear_no_parent():
    """
    Validate we can build our first Avar implementation.
    This implementation is totally linear.
    """
    cmds.joint()
    avar = AvarImpl1(input=["joint1"], name="test", rig=Rig())
    avar.build()
    helpers.assert_match_pose(_POSE_REST)
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
    avar.ctrl.translateY.set(2.0)  # TODO: Should the max be 1.0 and not 2.0???
    helpers.assert_match_pose(
        {
            "joint1": Matrix(
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 0.725374376984, -0.688354569401, 0.0],
                [0.0, 0.688354569401, 0.725374376984, 0.0],
                [0.0, 0.450158148982, -0.183848992013, 1.0],
            ),
            "test_anm": Matrix(
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 2.0, 0.0, 1.0],
            ),
        }
    )

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
            "test_anm": Matrix(
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
            "test_anm": Matrix(
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.5, 1.0, 1.0],
            ),
        }
    )
