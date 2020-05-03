import pymel.core as pymel

from omtk import constants
from omtk.modules import rigIK
from omtk.modules import rigLimb
from omtk.libs import libCtrlShapes
from omtk.libs import libRigging


class CtrlIkArm(rigIK.CtrlIk):
    def __createNode__(self, *args, **kwargs):
        return libCtrlShapes.create_shape_box_arm(*args, **kwargs)


class ArmIk(rigIK.IK):
    _CLASS_CTRL_IK = CtrlIkArm
    SHOW_IN_UI = False

    def _get_ik_ctrl_bound_refs_raycast(self):
        """
        Resolve what objects to use for computing the bound of the ik ctrl.
        This use the first phalanges to have a more precise bound height.
        :return: An array of influences
        :rtype: pymel.nodetypes.Joint
        """
        jnt_hand = self.input[self.iCtrlIndex]
        return [jnt_hand] + jnt_hand.getChildren()

    def _get_ik_ctrl_tms(self):
        """
        Compute the desired rotation for the ik ctrl.
        If the LEGACY_ARM_IK_CTRL_ORIENTATION is set, we'll simply align to the influence.
        :return: A two-size tuple containing the transformation matrix for the ctrl offset and the ctrl itself.
        """
        if self.rig.LEGACY_ARM_IK_CTRL_ORIENTATION:
            return super(ArmIk, self)._get_ik_ctrl_tms()

        naming = self.rig.nomenclature

        inf_tm = self.input[self.iCtrlIndex].getMatrix(worldSpace=True)
        side = self.get_side()

        # Resolve offset_tm
        offset_tm = pymel.datatypes.Matrix()

        # Resolve ctrl_tm
        axis_dir = constants.Axis.x
        axis_upp = self.rig.DEFAULT_UPP_AXIS  # normally the z axis
        inn_tm_dir = libRigging.get_matrix_axis(inf_tm, axis_dir)
        inn_tm_upp = libRigging.get_matrix_axis(inf_tm, axis_upp)

        upp_axis = pymel.datatypes.Vector(0, -1 if side == naming.SIDE_R else 1, 0)

        ctrl_tm = libRigging.get_matrix_from_direction(
            inn_tm_dir,
            inn_tm_upp,
            look_axis=pymel.datatypes.Vector(1, 0, 0),
            upp_axis=upp_axis,
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
