import pymel.core as pymel
from omtk import constants
from omtk.libs import libCtrlShapes
from omtk.libs import libRigging
from omtk.modules import module_ik, rigLimb


class CtrlIkArm(module_ik.CtrlIk):
    def __createNode__(self, *args, **kwargs):
        return libCtrlShapes.create_shape_box_arm(*args, **kwargs)


def get_spaceswitch_targets(self, module, *args, **kwargs):
    targets, labels, indexes = super(CtrlIkArm, self).get_spaceswitch_targets(module, *args, **kwargs)
    jnt_head = module.get_head_jnt()
    if jnt_head:
        targets.append(jnt_head)
        labels.append(None)
        indexes.append(self.get_bestmatch_index(jnt_head))
    return targets, labels, indexes


class ArmIk(module_ik.IK):
    _CLASS_CTRL_IK = CtrlIkArm
    SHOW_IN_UI = False

    def _get_ik_ctrl_bound_refs_raycast(self):
        """
        Resolve what objects to use for computing the bound of the libs ctrl using raycasts.
        This also use the first phalanges to have a more precise bound height.
        :return: An array of pymel.general.PyNode instances.
        """
        jnt_hand = self.input[self.iCtrlIndex]
        return [jnt_hand] + jnt_hand.getChildren()

    def _get_ik_ctrl_tms(self):
        """
        Compute the desired rotation for the libs ctrl.
        If the LEGACY_ARM_IK_CTRL_ORIENTATION is set, we'll simply align to the influence.
        :return: A two-size tuple containing the transformation matrix for the ctrl offset and the ctrl itself.
        """
        if self.rig.LEGACY_ARM_IK_CTRL_ORIENTATION:
            return super(ArmIk, self)._get_ik_ctrl_tms()

        inf_tm = self.input[self.iCtrlIndex].getMatrix(worldSpace=True)
        side = self.get_side()

        # Resolve offset_tm
        offset_tm = pymel.datatypes.Matrix()

        # Resolve ctrl_tm
        axis_dir = constants.Axis.x
        axis_upp = self.rig.DEFAULT_UPP_AXIS  # normally the z axis
        inn_tm_dir = libRigging.get_matrix_axis(inf_tm, axis_dir)
        inn_tm_upp = libRigging.get_matrix_axis(inf_tm, axis_upp)

        ctrl_tm = libRigging.get_matrix_from_direction(
            inn_tm_dir,
            inn_tm_upp,
            look_axis=pymel.datatypes.Vector(1, 0, 0),
            upp_axis=pymel.datatypes.Vector(0, -1,
                                            0) if side == self.rig.nomenclature.SIDE_R else pymel.datatypes.Vector(0, 1,
                                                                                                                   0)
        )
        ctrl_tm.translate = inf_tm.translate

        return offset_tm, ctrl_tm


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
