"""
Tests for the FaceLips module
"""
from maya import cmds
import pymel.core as pymel

import omtk
from omtk.modules.head import Head
from omtk.modules.face.eyes import FaceEyes


def test_eyes():
    """
    Test we can build the FaceEyes module
    """
    for name in ["jnt_head", "jnt_eye_l", "jnt_eye_r"]:
        pymel.joint(name=name)
        pymel.select(clear=True)
    cmds.parent("jnt_eye_l", "jnt_head")
    cmds.parent("jnt_eye_r", "jnt_head")

    rig = omtk.create()
    Head(["jnt_head"], rig=rig)
    FaceEyes(["jnt_eye_l", "jnt_eye_r"], rig=rig)
    rig.build(strict=True)
