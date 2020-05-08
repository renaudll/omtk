import pytest
from maya import cmds
import pymel.core as pymel

from omtk.core.classRig import Rig
from omtk.models.model_avar_linear import AvarLinearModel
from omtk.models.model_avar_surface import AvarSurfaceModel
from omtk.models.model_ctrl_linear import ModelCtrlLinear
from omtk.models.model_ctrl_interactive import ModelInteractiveCtrl
from omtk.modules.rigFaceAvar import AvarSimple


class AvarImpl1(AvarSimple):
    """Implementation that test linear ctrl and influence models."""

    CLS_MODEL_CTRL = ModelCtrlLinear
    CLS_MODEL_INFL = AvarLinearModel


class AvarImpl2(AvarSimple):
    """Implementation that test surface based ctrl and influence models."""

    CLS_MODEL_CTRL = ModelInteractiveCtrl
    CLS_MODEL_INFL = AvarSurfaceModel


@pytest.fixture
def scene_joint():
    pymel.joint()


@pytest.fixture
def scene_joint_with_surface():
    pymel.joint()
    pymel.nurbsPlane()


@pytest.fixture
def scene_joint_with_parent():
    pymel.joint()
    pymel.joint()


@pytest.fixture
def scene_joint_with_parent_with_surface():
    pymel.joint()
    pymel.joint()
    pymel.nurbsPlane()


@pytest.mark.usefixtures("scene_joint")
def test_linear_avar_no_parent():
    avar = AvarImpl1(input=cmds.ls(type="joint"), rig=Rig())
    avar.build()
    # yield
    avar.unbuild()


@pytest.mark.usefixtures("scene_joint_with_surface")
def test_surface_avar_no_parent_with_surface(scene_joint_with_surface):
    pymel.joint()
    pymel.nurbsPlane()
    avar = AvarImpl1(input=["joint1", "nurbsPlane1"], rig=Rig())
    avar.build()
    # yield
    avar.unbuild()
