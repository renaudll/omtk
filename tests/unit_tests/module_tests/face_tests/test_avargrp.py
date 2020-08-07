"""
Tests for the AvarGrp module.
"""
import os

from maya import cmds
import pymel.core as pymel
from pymel.core.datatypes import Matrix

from omtk.core.rig import Rig
from omtk.modules.face.models.avar_to_infl.linear import AvarLinearModel
from omtk.modules.face.models.avar_to_infl.surface import AvarSurfaceModel
from omtk.modules.face.models.avar_to_ctrl.linear import ModelCtrlLinear
from omtk.modules.face.models.avar_to_ctrl.interactive import ModelInteractiveCtrl
from omtk.modules.face.avar import Avar
from omtk.modules.face.avar_grp import AvarGrp
from omtk.libs import libRigging

from ... import helpers

_RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "..", "resources")


class AvarImpl1(Avar):
    """Implementation that test linear ctrl and influence models."""

    CLS_MODEL_CTRL = ModelCtrlLinear
    CLS_MODEL_INFL = AvarLinearModel


class MacroAvarImpl1(Avar):
    CLS_MODEL_CTRL = ModelCtrlLinear
    CLS_MODEL_INFL = None


class AvarImpl2(Avar):
    """Implementation that test surface based ctrl and influence models."""

    CLS_MODEL_CTRL = ModelInteractiveCtrl
    CLS_MODEL_INFL = AvarSurfaceModel


class AvarGrpImpl1(AvarGrp):
    """Implementation that test a grp of linear avars."""

    CLS_AVAR_MICRO = AvarImpl1
    CLS_AVAR_MACRO_ALL = MacroAvarImpl1
    CLS_AVAR_MACRO_LFT = MacroAvarImpl1
    CLS_AVAR_MACRO_RGT = MacroAvarImpl1
    CLS_AVAR_MACRO_UPP = MacroAvarImpl1
    CLS_AVAR_MACRO_LOW = MacroAvarImpl1


class AvarGrpImpl1SideSpecific(AvarGrpImpl1):
    """Implementation that is side specific."""

    IS_SIDE_SPECIFIC = True


def _create_joint(name, position=(0.0, 0.0, 0.0)):
    cmds.select(clear=True)
    jnt = cmds.joint(name=name, position=position)
    return jnt


def _create_joints(data):
    jnts = []
    for name, position in data:
        jnt = _create_joint(name, position)
        jnts.append(jnt)
    return jnts


def test_avar_grp_simple():
    """
    Test a very simple case of AvarGrp where all avar are linear and there is no parent.
    """
    parent = _create_joint("parent")
    jnts = _create_joints(
        [
            ("jnt_test_l", [1.0, 0.0, 0.0]),
            ("jnt_test_r", [-1.0, 0.0, 0.0]),
            ("jnt_test_upp", [0.0, 1.0, 0.0]),
            ("jnt_test_low", [0.0, -1.0, 0.0]),
        ]
    )
    for jnt in jnts:
        cmds.parent(jnt, parent)

    inst = AvarGrpImpl1(jnts, name="avargrp", rig=Rig())
    inst.build()

    helpers.assert_match_pose_from_file(os.path.join(_RESOURCE_DIR, "test_avargrp_rest.json"))

    # Ensure micros follow macros
    with helpers.temporary_changes(
        {
            inst.avar_l.ctrl.translateX: 1.0,
            inst.avar_r.ctrl.translateX: 1.0,
            inst.avar_upp.ctrl.translateY: 1.0,
            inst.avar_low.ctrl.translateY: -1.0,
        }
    ):
        helpers.assert_match_pose_from_file(os.path.join(_RESOURCE_DIR, "test_avargrp_pose1.json"))

    # # Ensure influence and ctrls follow parent
    # offset_tm = Matrix([0.0, 0.0, -0.5, 0.0], [0.0, 1.0, 0.0, 0.0], [2.0, 0.0, 0.0, 0.0], [1.0, 2.0, 3.0, 1.0])
    # with helpers.verified_offset(inst.jnts + inst.get_ctrls(), offset_tm):
    #     pymel.PyNode(parent).setMatrix(offset_tm)


def test_avarsidegrp_specific_l():
    """
    Test a very simple case of AvarGrp that is side specific.
    """
    jnts = _create_joints(
        [
            ("jnt_test_inn_l", [-1.0, 0.0, 0.0]),
            ("jnt_test_out_l", [1.0, 0.0, 0.0]),
            ("jnt_test_upp_l", [0.0, 1.0, 0.0]),
            ("jnt_test_low_l", [0.0, -1.0, 0.0]),
        ]
    )
    inst = AvarGrpImpl1SideSpecific(jnts, name="l_avargrp", rig=Rig())
    inst.build()

    helpers.assert_match_pose_from_file(os.path.join(_RESOURCE_DIR, "test_avarsidegrp_l_rest.json"))


def test_avarsidegrp_specific_r():
    """
    Test a very simple case of AvarGrp that is side specific.
    """
    jnts = _create_joints(
        [
            ("jnt_test_inn_r", [1.0, 0.0, 0.0]),
            ("jnt_test_out_r", [-1.0, 0.0, 0.0]),
            ("jnt_test_upp_r", [0.0, 1.0, 0.0]),
            ("jnt_test_low_r", [0.0, -1.0, 0.0]),
        ]
    )
    inst = AvarGrpImpl1SideSpecific(jnts, name="r_avargrp", rig=Rig())
    inst.build()

    helpers.assert_match_pose_from_file(os.path.join(_RESOURCE_DIR, "test_avarsidegrp_r_rest.json"))


def test_avargrp_connection_persistence():
    """Validate connection between avars is conserved between rebuilds."""
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

    # Connect some avars
    libRigging.connectAttr_withLinearDrivenKeys(inst.avar_l.attr_lr, inst.avar_r.attr_lr)

    # Validate that the connection work, moving the avar_l should move the avar_r
    with helpers.temporary_changes({inst.avar_l.attr_lr: 1.0}):
        assert inst.avar_r.attr_lr.get() == 1.0

    inst.unbuild()
    inst.build()

    # Validate that the connection still work
    with helpers.temporary_changes({inst.avar_l.attr_lr: 1.0}):
        assert inst.avar_r.attr_lr.get() == 1.0
