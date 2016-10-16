from omtk.modules import rigIK
from omtk.modules import rigLimb
from omtk.libs import libCtrlShapes


class CtrlIkArm(rigIK.CtrlIk):
    def __createNode__(self, refs=None, geometries=None):
        return libCtrlShapes.create_shape_box_arm(refs, geometries=geometries)

def get_spaceswitch_targets(self, module, *args, **kwargs):
        targets, labels, indexes = super(CtrlIkArm, self).get_spaceswitch_targets(module, *args, **kwargs)
        jnt_head = module.rig.get_head_jnt()
        if jnt_head:
            targets.append(jnt_head)
            labels.append(None)
            indexes.append(self.get_bestmatch_index(jnt_head))
        return targets, labels, indexes


class ArmIk(rigIK.IK):
    _CLASS_CTRL_IK = CtrlIkArm
    SHOW_IN_UI = False


class Arm(rigLimb.Limb):
    """
    IK/FK Setup customized for Arm riging.
    """
    _CLASS_SYS_IK = ArmIk

    def __init__(self, *args, **kwargs):
        super(Arm, self).__init__(*args, **kwargs)
        self.sysFootRoll = None

def register_plugin():
    return Arm
