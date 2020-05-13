"""
Tests for the FaceLips module
"""
import test
import pymel.core as pymel
import omtk_test
import omtk
from omtk.modules.head import Head
from omtk.modules import rigFaceJaw
from omtk.modules.rigFaceEyes import FaceEyes
from omtk.libs import libRigging


def test_eyes():
    for name in ["jnt_head", "jnt_eye_l", "jnt_eye_r"]:
        pymel.joint(name=name)
        pymel.select(clear=True)

    rig = omtk.create()
    rig.add_module(Head(["jnt_head"]))
    rig.add_module(FaceEyes(["jnt_eye_l", "jnt_eye_r"]))
    rig.build(strict=True)
