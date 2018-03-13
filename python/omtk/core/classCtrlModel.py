"""
A ctrl model is a small module that handle the logic between a ctrl and an influence.
This is necessary when the relationship between the ctrl and the influence is more complex than setting up a constraint.
"""
import pymel.core as pymel

from . import classModule
from . import classNode
from omtk.libs import libAttr
from omtk.libs import libRigging
from omtk.libs import libHistory
from omtk.libs import libPython


class BaseCtrlModel(classModule.Module):
    """
    Define a minimal implementation that only build the ctrl itself.
    """
    _CLS_CTRL = None

    def __init__(self, *args, **kwargs):
        super(BaseCtrlModel, self).__init__(*args, **kwargs)
        self.ctrl = None

        self._attr_inn_parent_tm = None

    def iter_ctrls(self):
        yield self.ctrl

    def create_interface(self):
        """
        Define the input and output of the module.
        The goal is to a a kind of component approach.
        """
        self._attr_inn_parent_tm = libAttr.addAttr(self.grp_rig, longName='innParentTm', dt='matrix')

    def build(self, module, ctrl_size=1.0, ctrl_name=None, **kwargs):
        """
        Build the the ctrl and the necessary logic.
        :param ctrl_size: The desired ctrl size if supported.
        :param ctrl_name: The desired ctrl name. If nothing is provided, the ctrl name will be automatically resolved.
        :param kwargs: Any additional keyword argument will be provided to the parent method.
        """
        super(BaseCtrlModel, self).build(**kwargs)
        self.create_interface()

        if not ctrl_name:
            ctrl_name = self.get_nomenclature_anm().resolve()

        # Create ctrl
        self.ctrl = self.init_ctrl(self._CLS_CTRL, self.ctrl)
        self.ctrl.build(
            name=ctrl_name,
            size=ctrl_size
        )
        self.ctrl.setParent(self.grp_anm)


class CtrlModelCalibratable(BaseCtrlModel):
    """
    Define an implementation that solve the issue were the relation between the 
    ctrl movement and the influence is not a one-to-one relationship.

    In this case, we might want to 'calibrate' the ctrl.
    The calibration compute the relationship between the ctrl and the influence
    and compensate by injecting non-uniform scaling in the ctrl parent node.
    The reason we scale the ctrl parent instead of multiplying the ctrl influence
    if for retargeting reason. We want a 1.0 value to represent the same thing
    for a character that is 1m tall and a character that is 100m tall.

    However, applying non-uniform scaling on the ctrl parent will squash it's shape.
    This is bypassed by applying the inverse deformation to the ctrl shape itself, 
    like some kind of deformation history.
    Keep in mind that if you want to change the ctrl shape, you will need to preserve
    the ctrl shape construction history, otherwise re-calibrating would result
    in a squewed shape.
    """
    _ATTR_NAME_SENSITIVITY_TX = 'sensitivityX'
    _ATTR_NAME_SENSITIVITY_TY = 'sensitivityY'
    _ATTR_NAME_SENSITIVITY_TZ = 'sensitivityZ'

    def __init__(self, *args, **kwargs):
        super(CtrlModelCalibratable, self).__init__(*args, **kwargs)
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None

        # Keep in memory the inversed sensitivity attributes for future reuse.
        # Note that since theses attributes are protected, they won't get serialized
        # in the scene. Use them only in the build process.
        self._attr_sensitivity_tx_inv = None
        self._attr_sensitivity_ty_inv = None
        self._attr_sensitivity_tz_inv = None

    def create_interface(self):
        super(CtrlModelCalibratable, self).create_interface()

        # Add sensitivity attributes on the ctrl.
        # The values will be adjusted on calibration.
        libAttr.addAttr_separator(
            self.grp_rig,
            "ctrlCalibration"
        )
        self.attr_sensitivity_tx = libAttr.addAttr(
            self.grp_rig,
            longName=self._ATTR_NAME_SENSITIVITY_TX,
            defaultValue=1.0
        )
        self.attr_sensitivity_ty = libAttr.addAttr(
            self.grp_rig,
            longName=self._ATTR_NAME_SENSITIVITY_TY,
            defaultValue=1.0
        )
        self.attr_sensitivity_tz = libAttr.addAttr(
            self.grp_rig,
            longName=self._ATTR_NAME_SENSITIVITY_TZ,
            defaultValue=1.0
        )
        self.attr_sensitivity_tx.set(channelBox=True)
        self.attr_sensitivity_ty.set(channelBox=True)
        self.attr_sensitivity_tz.set(channelBox=True)

    def build(self, module, **kwargs):
        super(CtrlModelCalibratable, self).build(module, **kwargs)

        pymel.connectAttr(self.attr_sensitivity_tx, self.ctrl.offset.scaleX)
        pymel.connectAttr(self.attr_sensitivity_ty, self.ctrl.offset.scaleY)
        pymel.connectAttr(self.attr_sensitivity_tz, self.ctrl.offset.scaleZ)

        #
        # Counter-scale the shape
        #

        # Create an 'orig' shape that will store the ctrl appearance before
        # applying any non-uniform scaling.
        ctrl_shape = self.ctrl.node.getShape()
        tmp = pymel.duplicate(self.ctrl.node.getShape())[0]
        ctrl_shape_orig = tmp.getShape()
        ctrl_shape_orig.setParent(self.ctrl.node, relative=True, shape=True)
        ctrl_shape_orig.rename('{0}Orig'.format(ctrl_shape.name()))
        pymel.delete(tmp)
        ctrl_shape_orig.intermediateObject.set(True)
        for cp in ctrl_shape.cp:
            cp.set(0, 0, 0)

        #
        # Compute the compensation matrix to cancel the non-uniform scaling on the shape.
        # Note that we handle rotation separately to prevent any skewing when rotating.
        # to hide the non-uniform scaling.
        #
        util_sensitivity_inv = libRigging.create_utility_node(
            'multiplyDivide', operation=2,
            input1X=1.0, input1Y=1.0, input1Z=1.0,
            input2X=self.attr_sensitivity_tx,
            input2Y=self.attr_sensitivity_ty,
            input2Z=self.attr_sensitivity_tz
        )
        self._attr_sensibility_lr_inv = util_sensitivity_inv.outputX
        self._attr_sensibility_ud_inv = util_sensitivity_inv.outputY
        self._attr_sensibility_fb_inv = util_sensitivity_inv.outputZ

        attr_adjustement_scale = libRigging.create_utility_node(
            'composeMatrix',
            inputScaleX=self._attr_sensibility_lr_inv,
            inputScaleY=self._attr_sensibility_ud_inv,
            inputScaleZ=self._attr_sensibility_fb_inv
        ).outputMatrix

        attr_adjustement_rot = libRigging.create_utility_node(
            'composeMatrix',
            inputRotateX=self.ctrl.node.rotateX,
            inputRotateY=self.ctrl.node.rotateY,
            inputRotateZ=self.ctrl.node.rotateZ
        ).outputMatrix

        attr_adjustement_rot_inv = libRigging.create_utility_node(
            'inverseMatrix',
            inputMatrix=attr_adjustement_rot
        ).outputMatrix

        attr_adjustement_tm = libRigging.create_utility_node(
            'multMatrix', matrixIn=[
                attr_adjustement_rot,
                attr_adjustement_scale,
                attr_adjustement_rot_inv
            ]
        ).matrixSum

        attr_transform_geometry = libRigging.create_utility_node(
            'transformGeometry',
            transform=attr_adjustement_tm,
            inputGeometry=ctrl_shape_orig.local
        ).outputGeometry
        pymel.connectAttr(attr_transform_geometry, ctrl_shape.create, force=True)

    def _get_calibration_reference(self):
        return self.jnt

    def calibrate(self, tx=True, ty=True, tz=True):
        ref = self._get_calibration_reference()
        if not ref:
            self.warning("Can't calibrate {0}, found no influences.".format(self))
            return

        if tx and not self.ctrl.node.tx.isLocked():
            sensitivity_tx = libRigging.calibrate_attr_using_translation(self.ctrl.node.tx, ref)
            self.debug('Adjusting sensibility tx for {0} to {1}'.format(self, sensitivity_tx))
            self.attr_sensitivity_tx.set(sensitivity_tx)

        if ty and not self.ctrl.node.ty.isLocked():
            sensitivity_ty = libRigging.calibrate_attr_using_translation(self.ctrl.node.ty, ref)
            self.debug('Adjusting sensibility ty for {0} to {1}'.format(self, sensitivity_ty))
            self.attr_sensitivity_ty.set(sensitivity_ty)

        if tz and not self.ctrl.node.tz.isLocked():
            sensitivity_tz = libRigging.calibrate_attr_using_translation(self.ctrl.node.tz, ref)
            self.debug('Adjusting sensibility tz for {0} to {1}'.format(self, sensitivity_tz))
            self.attr_sensitivity_tz.set(sensitivity_tz)

    def unbuild(self, **kwargs):
        super(CtrlModelCalibratable, self).unbuild(**kwargs)

        # todo: maybe hold sensitivity for faster rebuild?
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None
