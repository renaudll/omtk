import os

import pytest
from maya import cmds
import pymel.core as pymel

import omtk
from omtk.core.rig import Rig
from omtk.core import plugin_manager

from . import helpers

_RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "resources")
_EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")


def test_create():
    rig_name = "TestRig"
    rig = omtk.create(name=rig_name)
    assert isinstance(rig, Rig)
    assert rig.name == rig_name


def test_plugins():
    """
    Ensure that the basic built-in plugins are successfully loaded.
    """

    manager = plugin_manager.plugin_manager

    loaded_plugin_names = [
        plugin.cls.__name__ for plugin in manager.get_loaded_plugins_by_type("modules")
    ]

    builtin_plugin_names = (
        "Arm",
        "FK",
        "AdditiveFK",
        "AvarGrp",
        "FaceBrow",
        "FaceEyeLids",
        "FaceEyes",
        "FaceJaw",
        "FaceLips",
        "FaceNose",
        "FaceSquint",
        "Hand",
        "Head",
        "IK",
        "Leg",
        "LegQuad",
        "Limb",
        "Neck",
        "Ribbon",
        "SplineIK",
        "Twistbone",
    )

    for plugin_name in builtin_plugin_names:
        assert plugin_name in loaded_plugin_names


def test_rig_rlessard():
    cmds.file(
        os.path.join(_EXAMPLES_DIR, "rig_rlessard_template01.ma"), open=True, force=True
    )
    helpers.build_unbuild_build_all(
        test_translate=True, test_rotate=True, test_scale=True
    )


def test_interactivefk01():
    cmds.file(
        os.path.join(_RESOURCE_DIR, "test_interactivefk01.ma"), open=True, force=True
    )
    helpers.build_unbuild_build_all(
        test_translate=False, test_rotate=False, test_scale=False
    )  # todo: re-enabled test t/r/s


def test_interactivefk02():
    cmds.file(
        os.path.join(_RESOURCE_DIR, "test_interactivefk02.ma"), open=True, force=True
    )
    helpers.build_unbuild_build_all(
        test_translate=False, test_rotate=False, test_scale=False
    )  # todo: re-enabled test t/r/s


def test_interactivefk03():
    cmds.file(
        os.path.join(_RESOURCE_DIR, "test_interactivefk03.ma"), open=True, force=True
    )

    helpers.build_unbuild_build_all(
        test_translate=False, test_rotate=False, test_scale=False
    )  # todo: re-enabled test t/r/s


@pytest.mark.skip(
    "Disabled since break when the default rig is not the standard. Need to extend omtk.create."
)
def test_ctrl_space_index_preservation(self):
    """
    Check that after a ctrl have been built once, if we change it's hierarchy's and
    rebuild it, we will keep the old index.
    This ensure any rig update will never break an old animation.
    """
    from omtk.modules import fk

    def check_targets_index_match(ctrl):
        self.assertEqual(len(ctrl.targets), len(ctrl.targets_indexes))
        attr_space = ctrl.node.space
        for target, target_index in attr_space.getEnums().iteritems():
            if target == "Local":
                continue
            target = pymel.PyNode(target)
            self.assertIn(target, ctrl.targets)  # Ensure the target is stored
            logical_index = ctrl.targets.index(target)
            self.assertEqual(target_index, ctrl.targets_indexes[logical_index])

    # Create a simple influence hierarhy
    inf_a = pymel.createNode("joint")
    inf_b = pymel.createNode("joint", parent=inf_a)
    inf_c = pymel.createNode("joint", parent=inf_b)
    inf_d = pymel.createNode("joint", parent=inf_c)

    # Create a simple rig
    rig = omtk.create()
    rig.add_module(fk.FK([inf_a]))
    rig.add_module(fk.FK([inf_b]))
    rig.add_module(fk.FK([inf_c]))
    mod_d = rig.add_module(fk.FK([inf_d]))

    # Build the last module
    mod_d.build()

    # Analyse the indexes
    ctrl = mod_d.ctrls[0]
    old_targets = ctrl.targets
    old_targets_indexes = ctrl.targets_indexes
    check_targets_index_match(ctrl)

    # Unbulid the last module, change the hierarchy and rebuilt it
    mod_d.unbuild()
    inf_d.setParent(inf_b)
    mod_d.build()

    # Analyse the indexes
    ctrl = mod_d.ctrls[0]
    new_targets = ctrl.targets
    new_targets_indexes = ctrl.targets_indexes
    check_targets_index_match(ctrl)

    self.assertListEqual(old_targets, new_targets)
    self.assertListEqual(old_targets_indexes, new_targets_indexes)
