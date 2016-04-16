from omtk.modules import rigIK
from omtk.modules import rigLimb
from omtk.libs import libCtrlShapes

class CtrlIkArm(rigIK.CtrlIk):
    def __createNode__(self, refs=None, geometries=None, *args, **kwargs):
        return libCtrlShapes.create_shape_box_arm(refs, geometries=geometries, *args, **kwargs)

    def get_spaceswitch_targets(self, rig, *args, **kwargs):
        targets, labels = super(CtrlIkArm, self).get_spaceswitch_targets(rig, *args, **kwargs)
        jnt_head = rig.get_head_jnt()
        if jnt_head:
            targets.append(jnt_head)
            labels.append(None)
        return targets, labels

class ArmIk(rigIK.IK):
    _CLASS_CTRL_IK = CtrlIkArm
    SHOW_IN_UI = False

class Arm(rigLimb.Limb):
    _CLASS_SYS_IK = ArmIk

    def __init__(self, *args, **kwargs):
        super(Arm, self).__init__(*args, **kwargs)
        self.sysFootRoll = None



