from omtk.core.classCtrlModel import BaseCtrlModel
from omtk.libs import libAttr, libRigging


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
    in a skewed shape.
    """

    # TODO: This should inherit from ModelInteractiveCtrl

    _ATTR_NAME_SENSITIVITY_TX = "sensitivityX"
    _ATTR_NAME_SENSITIVITY_TY = "sensitivityY"
    _ATTR_NAME_SENSITIVITY_TZ = "sensitivityZ"

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
        libAttr.addAttr_separator(self.grp_rig, "ctrlCalibration")

        def _fn(name):
            attr = libAttr.addAttr(self.grp_rig, longName=name, defaultValue=1.0)
            attr.set(channelBox=True)
            return attr

        self.attr_sensitivity_tx = _fn(self._ATTR_NAME_SENSITIVITY_TX)
        self.attr_sensitivity_ty = _fn(self._ATTR_NAME_SENSITIVITY_TY)
        self.attr_sensitivity_tz = _fn(self._ATTR_NAME_SENSITIVITY_TZ)

    def build(self, ctrl, **kwargs):
        super(CtrlModelCalibratable, self).build(**kwargs)

        pymel.connectAttr(self.attr_sensitivity_tx, ctrl.offset.scaleX)
        pymel.connectAttr(self.attr_sensitivity_ty, ctrl.offset.scaleY)
        pymel.connectAttr(self.attr_sensitivity_tz, ctrl.offset.scaleZ)

        #
        # Counter-scale the shape
        #

        # Create an 'orig' shape that will store the ctrl appearance before
        # applying any non-uniform scaling.
        ctrl_shape = ctrl.node.getShape()
        tmp = pymel.duplicate(ctrl.node.getShape())[0]
        ctrl_shape_orig = tmp.getShape()
        ctrl_shape_orig.setParent(ctrl.node, relative=True, shape=True)
        ctrl_shape_orig.rename(ctrl_shape.name() + "Orig")
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
            "multiplyDivide",
            operation=2,
            input1X=1.0,
            input1Y=1.0,
            input1Z=1.0,
            input2X=self.attr_sensitivity_tx,
            input2Y=self.attr_sensitivity_ty,
            input2Z=self.attr_sensitivity_tz,
        )
        self._attr_sensibility_lr_inv = util_sensitivity_inv.outputX
        self._attr_sensibility_ud_inv = util_sensitivity_inv.outputY
        self._attr_sensibility_fb_inv = util_sensitivity_inv.outputZ

        attr_adjustement_scale = libRigging.create_utility_node(
            "composeMatrix",
            inputScaleX=self._attr_sensibility_lr_inv,
            inputScaleY=self._attr_sensibility_ud_inv,
            inputScaleZ=self._attr_sensibility_fb_inv,
        ).outputMatrix

        attr_adjustement_rot = libRigging.create_utility_node(
            "composeMatrix",
            inputRotateX=ctrl.node.rotateX,
            inputRotateY=ctrl.node.rotateY,
            inputRotateZ=ctrl.node.rotateZ,
        ).outputMatrix

        attr_adjustement_rot_inv = libRigging.create_utility_node(
            "inverseMatrix", inputMatrix=attr_adjustement_rot
        ).outputMatrix

        attr_adjustement_tm = libRigging.create_utility_node(
            "multMatrix",
            matrixIn=[
                attr_adjustement_rot,
                attr_adjustement_scale,
                attr_adjustement_rot_inv,
            ],
        ).matrixSum

        attr_transform_geometry = libRigging.create_utility_node(
            "transformGeometry",
            transform=attr_adjustement_tm,
            inputGeometry=ctrl_shape_orig.local,
        ).outputGeometry
        pymel.connectAttr(attr_transform_geometry, ctrl_shape.create, force=True)

    def _get_calibration_reference(self):
        return self.jnt

    def calibrate(self, ctrl, tx=True, ty=True, tz=True):
        ref = self._get_calibration_reference()
        if not ref:
            self.log.warning("Can't calibrate %s, found no influences.", self)
            return

        if tx and not ctrl.node.tx.isLocked():
            sensitivity_tx = libRigging.calibrate_attr_using_translation(
                ctrl.node.tx, ref
            )
            self.log.debug(
                "Adjusting sensibility tx for %s to %s", self, sensitivity_tx
            )
            self.attr_sensitivity_tx.set(sensitivity_tx)

        if ty and not ctrl.node.ty.isLocked():
            sensitivity_ty = libRigging.calibrate_attr_using_translation(
                ctrl.node.ty, ref
            )
            self.log.debug(
                "Adjusting sensibility ty for %s to %s", self, sensitivity_ty
            )
            self.attr_sensitivity_ty.set(sensitivity_ty)

        if tz and not ctrl.node.tz.isLocked():
            sensitivity_tz = libRigging.calibrate_attr_using_translation(
                ctrl.node.tz, ref
            )
            self.log.debug(
                "Adjusting sensibility tz for %s to %s", self, sensitivity_tz
            )
            self.attr_sensitivity_tz.set(sensitivity_tz)

    def unbuild(self):
        super(CtrlModelCalibratable, self).unbuild()

        # todo: maybe hold sensitivity for faster rebuild?
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None
