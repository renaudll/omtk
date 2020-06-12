"""
Tests for the AvarGrp module.
"""
import os

from maya import cmds

from omtk.core.rig import Rig
from omtk.modules.face.models.avar_to_infl.linear import AvarLinearModel
from omtk.modules.face.models.avar_to_infl.surface import AvarSurfaceModel
from omtk.modules.face.models.avar_to_ctrl.linear import ModelCtrlLinear
from omtk.modules.face.models.avar_to_ctrl.interactive import ModelInteractiveCtrl
from omtk.modules.face.avar import Avar
from omtk.modules.face.avar_grp import AvarGrp

from ... import helpers

_RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "..", "resources")


class AvarImpl1(Avar):
    """Implementation that test linear ctrl and influence models."""

    CLS_MODEL_CTRL = ModelCtrlLinear
    CLS_MODEL_INFL = AvarLinearModel


class AvarImpl2(Avar):
    """Implementation that test surface based ctrl and influence models."""

    CLS_MODEL_CTRL = ModelInteractiveCtrl
    CLS_MODEL_INFL = AvarSurfaceModel


class AvarGrpImpl1(AvarGrp):
    """Implementation that test a grp of linear avars."""

    CLS_AVAR_MICRO = AvarImpl1
    CLS_AVAR_MACRO_ALL = AvarImpl1
    CLS_AVAR_MACRO_LFT = AvarImpl1
    CLS_AVAR_MACRO_RGT = AvarImpl1
    CLS_AVAR_MACRO_UPP = AvarImpl1
    CLS_AVAR_MACRO_LOW = AvarImpl1


class AvarGrpImpl1SideSpecific(AvarGrpImpl1):
    """Implementation that is side specific."""

    IS_SIDE_SPECIFIC = True


def _create_joints(data):
    jnts = []
    for name, position in data:
        cmds.select(clear=True)
        jnt = cmds.joint(name=name, position=position)
        jnts.append(jnt)
    return jnts


def test_avar_grp_simple():
    """
    Test a very simple case of AvarGrp where all avar are linear and there is no parent.
    """
    jnts = _create_joints(
        [
            ("jnt_test_l", [1.0, 0.0, 0.0]),
            ("jnt_test_r", [-1.0, 0.0, 0.0]),
            ("jnt_test_upp", [0.0, 1.0, 0.0]),
            ("jnt_test_low", [0.0, -1.0, 0.0]),
        ]
    )
    inst = AvarGrpImpl1(jnts, name="avargrp", rig=Rig())
    inst.build()

    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avargrp_rest.json")
    )

    # Ensure micros follow macros
    inst.avar_l.ctrl.translateX.set(1.0)
    inst.avar_r.ctrl.translateX.set(-1.0)
    inst.avar_upp.ctrl.translateY.set(1.0)
    inst.avar_low.ctrl.translateY.set(-1.0)

    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avargrp_rest.json")
    )


def test_avarsidegrp_specific():
    """
    Test a very simple case of AvarGrp that is side specific.
    """
    jnts = _create_joints(
        [
            ("jnt_test_inn_l", [1.0, 0.0, 0.0]),
            ("jnt_test_out_l", [-1.0, 0.0, 0.0]),
            ("jnt_test_upp_l", [0.0, 1.0, 0.0]),
            ("jnt_test_low_l", [0.0, -1.0, 0.0]),
        ]
    )
    inst = AvarGrpImpl1SideSpecific(jnts, name="l_avargrp", rig=Rig())
    inst.build()

    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_avarsidegrp_rest.json")
    )
