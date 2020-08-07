"""
Tests for the FaceLips module
"""
import os

import pytest

from maya import cmds

import omtk
from omtk.modules.head import Head
from omtk.modules.face.lids import FaceEyeLids

_RESOURCE_DIR = os.path.join(
    os.path.dirname(__file__),  # /tests/module_tests/face_tests
    "..",  # /test/module_tests
    "..",  # /test
    "..",  # /
    "examples",
)


@pytest.mark.skip("disabled for now")
def test_eyelids():
    """
    Test we can build the FaceEyes module
    """
    cmds.file(os.path.join(_RESOURCE_DIR, "example_face.ma"), open=True, force=True)

    rig = omtk.create()
    Head(["jnt_head"], rig=rig)
    inst = FaceEyeLids(
        cmds.ls("jnt_eyelid_*_l", type="joint") + ["Face_Mesh"], name="test", rig=rig
    )
    inst.build()

    # Note: Theses are the name when built with v6
    expected = {
        "l_test_eyelid_inn_anm",
        "l_test_eyelid_low_anm",
        "l_test_eyelid_low_inn_anm",
        "l_test_eyelid_low_out_anm",
        "l_test_eyelid_out_anm",
        "l_test_eyelid_upp_anm",
        "l_test_eyelid_upp_inn_anm",
        "l_test_eyelid_upp_out_anm",
        "l_test_macro_inn_anm",
        "l_test_macro_out_anm",
        "l_test_macro_out_anm",
        "l_test_macro_inn_anm",
        "l_test_macro_all_anm,",
    }
    actual = set(cmds.ls("*_anm"))
    assert not expected - actual

    # TODO: Write more tests
