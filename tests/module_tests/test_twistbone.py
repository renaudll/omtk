import os

from maya import cmds
from omtk.core.rig import Rig
from omtk.modules.twistbone import Twistbone

from .. import helpers

_RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "resources")


def test_twistbone():
    cmds.joint(position=[0.0, 0.0, 0.0])
    cmds.joint(position=[10.0, 0.0, 0.0])
    cmds.joint(position=[20.0, 0.0, 0.0])
    cmds.joint(position=[30.0, 0.0, 0.0])
    inst = Twistbone(["joint2", "joint3", "joint4"], rig=Rig())
    inst.build()

    helpers.assert_match_pose_from_file(
        os.path.join(_RESOURCE_DIR, "test_twistbone_rest.json")
    )
