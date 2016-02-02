from omtk.modules import rigIK
from omtk.modules import rigLimb
from omtk.libs import libCtrlShapes

class CtrlIkArm(rigIK.CtrlIk):
    def __createNode__(self, refs=None, *args, **kwargs):
        return libCtrlShapes.create_shape_box_feet(refs, *args, **kwargs)

class Arm(rigLimb.Limb):
    def __init__(self, *args, **kwargs):
        super(Arm, self).__init__(*args, **kwargs)
        self.sysFootRoll = None
