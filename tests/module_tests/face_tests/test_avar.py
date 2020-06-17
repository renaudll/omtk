"""
Tests for the Avar module.
"""
import os

from maya import cmds

from omtk.core.rig import Rig
from omtk.modules.face.models.avar_to_infl.linear import AvarLinearModel
from omtk.modules.face.models.avar_to_infl.surface import AvarSurfaceModel
from omtk.modules.face.models.avar_to_ctrl.linear import ModelCtrlLinear
from omtk.modules.face.models.avar_to_ctrl.interactive import ModelInteractiveCtrl
from omtk.modules.face.avar import Avar

from ... import helpers


_RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "..", "resources")


class AvarImplCtrlLinear(Avar):
    """Implementation with a linear ctrl model."""

    CLS_MODEL_CTRL = ModelCtrlLinear
    CLS_MODEL_INFL = None


class AvarImplInflLinear(Avar):
    """Implement with a linear influence model."""

    CLS_MODEL_CTRL = None
    CLS_MODEL_INFL = AvarLinearModel


class AvarImplCtrlSurface(Avar):
    """Implement with an interactive ctrl model."""

    CLS_MODEL_CTRL = ModelInteractiveCtrl
    CLS_MODEL_INFL = None


class AvarImplInflSurface(Avar):
    """Implementation with a surface influence model."""

    CLS_MODEL_CTRL = None
    CLS_MODEL_INFL = AvarSurfaceModel


class AvarImplCtrlSurfaceWithInfl(Avar):
    """Implementation where the ctrl follow a mesh."""

    CLS_MODEL_CTRL = ModelInteractiveCtrl
    CLS_MODEL_INFL = AvarLinearModel


def test_ctrl_model_linear():
    """Test an avar with a linear ctrl model."""
    cmds.joint(position=[0.0, 0.0, 0.1])
    avar = AvarImplCtrlLinear(input=["joint1"], name="test", rig=Rig())
    avar.build()
    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avar_ctrl_linear_rest.json")
    )

    # Validate that moving the avar will move the controller.
    avar.attr_lr.set(1.0)
    avar.attr_ud.set(2.0)
    avar.attr_fb.set(3.0)
    avar.attr_pt.set(90.0)
    avar.attr_yw.set(45.0)
    avar.attr_rl.set(22.5)

    # Validate the infl model
    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avar_ctrl_linear_pose.json")
    )

    # Validate that moving the ctrl affect the avar
    avar.attr_lr.set(0.0)
    avar.attr_ud.set(0.0)
    avar.attr_fb.set(0.0)
    avar.attr_pt.set(0.0)
    avar.attr_yw.set(0.0)
    avar.attr_rl.set(0.0)
    avar.ctrl.translateX.set(1.0)
    avar.ctrl.translateY.set(2.0)
    avar.ctrl.translateZ.set(3.0)
    avar.ctrl.rotateX.set(90.0)
    avar.ctrl.rotateY.set(45.0)
    avar.ctrl.rotateZ.set(22.5)

    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avar_ctrl_linear_pose.json")
    )
    assert avar.attr_lr.get() == 1.0
    assert avar.attr_ud.get() == 2.0
    assert avar.attr_fb.get() == 3.0
    assert avar.attr_pt.get() == 90.0
    assert avar.attr_yw.get() == 45.0
    assert avar.attr_rl.get() == 22.5


def test_infl_model_linear():
    """Test an avar with a linear influence model."""
    cmds.joint(position=[0.0, 0.0, 0.1])
    avar = AvarImplInflLinear(input=["joint1"], name="test", rig=Rig())
    avar.build()
    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avar_ctrl_linear_rest.json")
    )

    # Validate that moving the avar will move the the influence.
    avar.attr_lr.set(1.0)
    avar.attr_ud.set(2.0)
    avar.attr_fb.set(3.0)
    avar.attr_pt.set(90.0)
    avar.attr_yw.set(45.0)
    avar.attr_rl.set(22.5)

    # Validate the infl model
    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avar_infl_linear_pose.json")
    )

    avar.unbuild()


def test_infl_model_surface():
    """Test an avar with an interactive ctrl model."""
    cmds.joint(position=[0.0, 0.0, 0.1])
    cmds.nurbsPlane(axis=[0.0, 0.0, 1.0], patchesV=10)  # Face the Z axis
    cmds.nonLinear("nurbsPlane1", type="bend", curvature=45)
    cmds.setAttr("bend1Handle.rotateY", 90)  # Bend vertically

    avar = AvarImplInflSurface(input=["joint1", "nurbsPlane1"], name="test", rig=Rig())
    avar.build()
    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avar_infl_surface_rest.json")
    )

    # Validate that moving the avar will move the the influence.
    avar.attr_lr.set(1.0)
    avar.attr_ud.set(2.0)
    avar.attr_fb.set(3.0)
    avar.attr_pt.set(90.0)
    avar.attr_yw.set(45.0)
    avar.attr_rl.set(22.5)

    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avar_infl_surface_pose.json")
    )

    avar.unbuild()


def test_ctrl_model_surface():
    """Test an avar with an interactive ctrl model and no influence model.
    """
    cmds.polySphere()
    cmds.select(clear=True)
    cmds.joint()
    # Note that the sphere end a 1.0, 0.75 is a little inside.
    cmds.joint(position=[0.0, 0.0, 0.75])
    cmds.skinCluster("pSphere1", "joint1", "joint2")

    avar = AvarImplCtrlSurface(input=["joint2", "pSphere1"], name="test", rig=Rig())
    avar.build()
    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avar_ctrl_surface_rest.json")
    )

    # Validate that moving the avar DONT affect the ctrl.
    # This is expected as the interactive controller follow the geometry and the influence don't move.
    avar.attr_lr.set(1.0)
    avar.attr_ud.set(2.0)
    avar.attr_fb.set(3.0)
    avar.attr_pt.set(90.0)
    avar.attr_yw.set(45.0)
    avar.attr_rl.set(22.5)

    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avar_ctrl_surface_rest.json")
    )


def test_ctrl_model_surface_with_infl():
    """Test an avar with an interactive ctrl model and a linear influence model."""
    cmds.polySphere()
    cmds.select(clear=True)
    cmds.joint()
    # Note that the sphere end a 1.0, 0.75 is a little inside.
    cmds.joint(position=[0.0, 0.0, 0.75])
    cmds.skinCluster("pSphere1", "joint1", "joint2")

    avar = AvarImplCtrlSurfaceWithInfl(
        input=["joint2", "pSphere1"], name="test", rig=Rig()
    )
    avar.build()
    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avar_ctrl_surface_rest.json")
    )

    # Validate that moving the avar influence the controller.
    avar.attr_lr.set(1.0)
    avar.attr_ud.set(2.0)
    avar.attr_fb.set(3.0)
    avar.attr_pt.set(90.0)
    avar.attr_yw.set(45.0)
    avar.attr_rl.set(22.5)

    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avar_ctrl_surface_pose_1.json")
    )

    # Validate that moving the ctrl influence the influence.
    # Note that this won't affect the controller rotation which DONT follow the deformation.
    avar.attr_lr.set(0.0)
    avar.attr_ud.set(0.0)
    avar.attr_fb.set(0.0)
    avar.attr_pt.set(0.0)
    avar.attr_yw.set(0.0)
    avar.attr_rl.set(0.0)
    avar.ctrl.translateX.set(1.0)
    avar.ctrl.translateY.set(2.0)
    avar.ctrl.translateZ.set(3.0)
    avar.ctrl.rotateX.set(90.0)
    avar.ctrl.rotateY.set(45.0)
    avar.ctrl.rotateZ.set(22.5)

    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avar_ctrl_surface_pose_2.json")
    )
