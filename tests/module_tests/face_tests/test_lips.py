"""
Tests for the FaceLips module
"""
import os

import pytest
from maya import cmds
import pymel.core as pymel

import omtk
from omtk.modules.head import Head
from omtk.modules.face.jaw import FaceJaw
from omtk.modules.face.lips import FaceLips

from ... import helpers

_RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "resources",)


def test_lips():
    cmds.file(os.path.join(_RESOURCE_DIR, "test_lips.ma"), open=True, force=True)

    # Create a base rig
    rig = omtk.create()
    Head(["jnt_head"], rig=rig)
    jaw = FaceJaw(["jnt_jaw", "surface_lips", "pSphereShape1"], rig=rig)
    FaceLips(
        cmds.ls("jnt_lip*", type="joint") + ["surface_lips", "pSphereShape1"], rig=rig
    )

    rig.build(strict=True)

    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_lips_rest.json")
    )

    jaw.ctrl.rotateX.set(45.0)
    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_lips_open_45.json")
    )


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
