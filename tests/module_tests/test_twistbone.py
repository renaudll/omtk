from maya import cmds
from omtk.core.rig import Rig
from omtk.modules.twistbone import Twistbone

from .. import helpers

@helpers.save_scene_on_assertion()
def test_twistbone():
    cmds.joint(position=[0.0,0.0,0.0])
    cmds.joint(position=[10.0,0.0,0.0])
    cmds.joint(position=[20.0,0.0,0.0])
    inst = Twistbone(["joint1", "joint2", "joint3"], rig=Rig())
    inst.build()

    raise AssertionError("test")
