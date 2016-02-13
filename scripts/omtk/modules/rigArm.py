from omtk.modules import rigIK
from omtk.modules import rigLimb
from omtk.libs import libCtrlShapes

class CtrlIkArm(rigIK.CtrlIk):
    def __createNode__(self, refs=None, *args, **kwargs):
        return libCtrlShapes.create_shape_box_arm(refs, *args, **kwargs)

class ArmIk(rigIK.IK):
    _CLASS_CTRL_IK = CtrlIkArm

class Arm(rigLimb.Limb):
    _CLASS_SYS_IK = ArmIk

    def __init__(self, *args, **kwargs):
        super(Arm, self).__init__(*args, **kwargs)
        self.sysFootRoll = None
