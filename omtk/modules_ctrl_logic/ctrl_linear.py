import pymel.core as pymel

from omtk.core.classCtrl import BaseCtrl
from omtk.core import classModuleCtrlLogic
from omtk.core.utils import decorator_uiexpose
from omtk.libs import libRigging
from omtk.libs import libHistory


class CtrlLogicLinear(classModuleCtrlLogic.CtrlLogicFaceCalibratable):
    """
    An InteractiveCtrl ctrl is directly constrained on a mesh via a layer_fol.
    To prevent double deformation, the trick is an additional layer before the final ctrl that invert the movement.
    For clarity purposes, this is built in the rig so the animator don't need to see the whole setup.

    However an InterfactiveCtrl might still have to be callibrated.
    This is necessay to keep the InteractiveCtrl values in a specific range (ex: -1 to 1) in any scale.
    The calibration apply non-uniform scaling on the ctrl parent to cheat the difference.

    For this reason an InteractiveCtrl is created using the following steps:
    1) Create the setup (using build)
    2) Connecting the doritos ctrl to something
    3) Optionally call .calibrate()
    """
    name = 'Linear'

    def __init__(self, *args, **kwargs):
        self._tmp_follicle = None
        super(CtrlLogicLinear, self).__init__(*args, **kwargs)

    def parent_to(self, parent):
        """
        Bypass default parent mecanism since it is computer internally.
        """
        pass

    def get_default_tm_ctrl(self):
        """
        :return: The ctrl transformation.
        """
        # todo: move to avar?
        if self.jnt is None:
            self.warning("Cannot resolve ctrl matrix with no inputs!")
            return None

        tm = self.jnt.getMatrix(worldSpace=True)

        # We always try to position the controller on the surface of the face.
        # The face is always looking at the positive Z axis.
        pos = tm.translate
        dir = pymel.datatypes.Point(0, 0, 1)
        result = self.rig.raycast_farthest(pos, dir)
        if result:
            tm.a30 = result.x
            tm.a31 = result.y
            tm.a32 = result.z

        return tm

    def build(self, module, **kwargs):
        super(CtrlLogicLinear, self).build(module, **kwargs)

        # # todo: use property?
        # self.mesh = next(iter(libHistory.get_affected_shapes(self.jnts)), None)

        # Apply the inverted sensibility
        util_get_adjusted_t = libRigging.create_utility_node(
            'multiplyDivide',
            input1X=module.attr_lr,
            input1Y=module.attr_ud,
            input1Z=module.attr_fb,
            input2X=self.attr_sensitivity_tx,
            input2Y=self.attr_sensitivity_ty,
            input2Z=self.attr_sensitivity_tz
        )

        # Hack: insert before the inverseT
        layer_avar = self._stack.insert_layer(1,  'avar')
        pymel.connectAttr(util_get_adjusted_t.outputX, layer_avar.tx)
        pymel.connectAttr(util_get_adjusted_t.outputY, layer_avar.ty)
        pymel.connectAttr(util_get_adjusted_t.outputZ, layer_avar.tz)
        pymel.connectAttr(module.attr_pt, layer_avar.rx)
        pymel.connectAttr(module.attr_yw, layer_avar.ry)
        pymel.connectAttr(module.attr_rl, layer_avar.rz)

    def _connect_output_tr(self):
        # Position
        stack_end = self._stack.get_stack_end()
        attr_local_tm = libRigging.create_utility_node(
            'multMatrix',
            matrixIn=(
                stack_end.worldMatrix,
                self._grp_offset.worldInverseMatrix,
                self._grp_parent.worldMatrix
            )
        ).matrixSum
        util_decompose_local_tm = libRigging.create_utility_node(
            'decomposeMatrix',
            inputMatrix=attr_local_tm
        )

        pymel.connectAttr(util_decompose_local_tm.outputTranslate, self._grp_output.translate)
        pymel.connectAttr(util_decompose_local_tm.outputRotate, self._grp_output.rotate)

    def _get_calibration_reference(self):
        pos_ref = self.jnt.getTranslation(space='world')
        _, u_coord, v_coord = libRigging.get_closest_point_on_shape(self.mesh, pos_ref)
        fol_shape = libRigging.create_follicle2(self.mesh, u=u_coord, v=v_coord)
        self._tmp_follicle = fol_shape.getParent()
        return self._tmp_follicle

    @decorator_uiexpose()
    def calibrate(self, **kwargs):
        super(CtrlLogicLinear, self).calibrate(**kwargs)
        pymel.delete(self._tmp_follicle)


def register_plugin():
    return CtrlLogicLinear
