"""
Tests for the FaceLips module
"""
import os

import pytest
from maya import cmds
import pymel.core as pymel

import omtk
from omtk.libs import libRigging
from omtk.modules.head import Head
from omtk.modules.face.jaw import FaceJaw
from omtk.modules.face.lips import FaceLips


_RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "resources",)


@pytest.mark.skip("disabled for now")
def test_avar_connection_persistence():  # TODO: Move to test_avargrp
    """Validate connection between avars is conserved between rebuilds."""
    cmds.file(os.path.join(_RESOURCE_DIR, "test_lips.ma"), open=True, force=True)

    # Create a base rig
    rig = omtk.create()
    Head(["jnt_head"], rig=rig)
    module_jaw = FaceJaw(["jnt_jaw", "pSphereShape1"], rig=rig)
    module_lips = FaceLips(cmds.ls("jnt_lip*", type="joint") + ["pSphereShape1"])
    rig.build(strict=True)

    # Connect some avars
    avar_src = next(iter(module_jaw.avars), None).attr_ud
    for avar in module_lips.avars:
        avar_dst = avar.attr_ud
        libRigging.connectAttr_withLinearDrivenKeys(avar_src, avar_dst)

    # Re-build the rig
    rig.unbuild(strict=True)
    rig.build(strict=True)

    # Ensure the avars are still connected.
    avar_src = next(iter(module_jaw.avars), None).attr_ud
    avar_src.set(1.0)
    for avar in module_lips.avars:
        avar_dst = avar.attr_ud
        assert avar_dst.get() == pytest.approx(1.0)


@pytest.mark.skip("disabled for now")
def test_avargrp_withsurface():
    cmds.file(os.path.join(_RESOURCE_DIR, "test_lips.ma"), open=True, force=True)

    # Create a base rig
    rig = omtk.create()
    Head(["jnt_head"], rig=rig)
    FaceJaw(["jnt_jaw", "surface_lips", "pSphereShape1"], rig=rig)
    FaceLips(cmds.ls("jnt_lip*", type="joint") + ["surface_lips", "pSphereShape1"], rig=rig)

    rig.build(strict=True)


def _get_scene_surface_count():
    """
    :return: The number of non-intermediate surfaces in the scene.
    """
    surface_shapes = [
        shape
        for shape in pymel.ls(type="nurbsSurface")
        if not shape.intermediateObject.get()
    ]
    return len(surface_shapes)
