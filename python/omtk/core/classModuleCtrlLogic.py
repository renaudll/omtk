"""
A ctrl model is a small module that handle the logic between a ctrl and an influence.
This is necessary when the relationship between the ctrl and the influence is more complex than setting up a constraint.
"""
import pymel.core as pymel

from omtk.core import classModule
from omtk.core import classNode
from omtk.core.classComponentAction import ComponentAction
from omtk.libs import libAttr
from omtk.libs import libRigging
from omtk.libs import libPymel
from omtk.libs import libHistory


class BaseCtrlModel(classModule.Module):
    """
    Define a minimal implementation that only build the ctrl itself.
    """
    _CLS_CTRL = None

    def __init__(self, *args, **kwargs):
        super(BaseCtrlModel, self).__init__(*args, **kwargs)
        self.ctrl = None

    def validate(self):
        super(BaseCtrlModel, self).validate(support_no_inputs=True)

    def iter_ctrls(self):
        yield self.ctrl

    def build(self, module, **kwargs):
        """
        Build the the ctrl and the necessary logic.
        :param ctrl_size: The desired ctrl size if supported.
        :param ctrl_name: The desired ctrl name. If nothing is provided, the ctrl name will be automatically resolved.
        :param kwargs: Any additional keyword argument will be provided to the parent method.
        """
        super(BaseCtrlModel, self).build(create_grp_anm=False, **kwargs)
        # todo: don't create a anm_grp

        # if not ctrl_name:
        #     ctrl_name = self.get_nomenclature_anm().resolve()
        # 
        # # Create ctrl
        # self.ctrl = self.init_ctrl(self._CLS_CTRL, self.ctrl)
        # self.ctrl.build(
        #     name=ctrl_name,
        #     size=ctrl_size
        # )
        # self.ctrl.setParent(self.grp_anm)

    def post_build(self):
        """
        Define any action that need to be applied on the ctrl model AFTER everything is built and connected.
        This might be necessary since the ctrl model depend on the avars which itself might depend on other avars.
        In thise situation we are not able to calibrate properly the ctrl model until everything is connected together. 
        """
        pass


class CtrlModelCalibratable(BaseCtrlModel):
    # use as the base class for ctrl_interactive and ctrl_linear
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
    
    Note: The CtrlModel provide the ctrl offset LOCAL transformation.
    Since the default behavior for a module is to contraint it's anm_grp to it's parent this is logical
    and allow for better support of non-uniform scale.
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

        self._stack = None
        self._grp_offset = None  # determine the initial position of the system
        self._grp_parent = None
        self._grp_output = None

        self._layer_inv_t = None
        self._layer_inv_r = None

    # --- Component methods

    def iter_actions(self):
        for action in super(CtrlModelCalibratable, self).iter_actions():
            yield action
        yield ActionCalibrate(self)

    def build(self, module, cancel_t=True, cancel_r=True, flip_lr=False, **kwargs):
        super(CtrlModelCalibratable, self).build(module, **kwargs)
        nomenclature_rig = self.get_nomenclature_rig()

        #
        # Build the node structure
        #

        self._grp_offset = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('offset'),
            parent=self.grp_rig
        )

        # Initialize external stack
        stack_name = nomenclature_rig.resolve('stack')
        self._stack = classNode.Node(self)
        self._stack.build(name=stack_name)
        self._stack.setParent(self._grp_offset)

        self._grp_parent = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('parent'),
            parent=self.grp_rig
        )

        self._grp_output = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('output'),
            parent=self.grp_rig
        )

        tm = self.jnt.getMatrix(worldSpace=True)
        self._grp_offset.setMatrix(tm)

        # Configure grp_parent
        self._grp_parent.setMatrix(tm)
        parent = self.get_parent_obj()
        if parent:
            pymel.parentConstraint(parent, self._grp_parent, maintainOffset=True)
            pymel.scaleConstraint(parent, self._grp_parent)

        #
        # Add sensitivity attributes on the ctrl.
        # The values will be adjusted on calibration.
        #
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

        # Apply scaling on the ctrl parent
        # This where the black magic happen
        if flip_lr:
            attr_ctrl_offset_sx_inn = libRigging.create_utility_node(
                'multiplyDivide',
                input1X=self.attr_sensitivity_tx,
                input2X=-1
            ).outputX
        else:
            attr_ctrl_offset_sx_inn = self.attr_sensitivity_tx
        attr_ctrl_offset_sy_inn = self.attr_sensitivity_ty
        attr_ctrl_offset_sz_inn = self.attr_sensitivity_tz

        pymel.connectAttr(attr_ctrl_offset_sx_inn, self.ctrl.offset.scaleX)
        pymel.connectAttr(attr_ctrl_offset_sy_inn, self.ctrl.offset.scaleY)
        pymel.connectAttr(attr_ctrl_offset_sz_inn, self.ctrl.offset.scaleZ)

        #
        # Counter-scale the shape
        #

        # Hack: Since there's scaling on the ctrl so the left and right side ctrl channels matches, we need to flip the ctrl shapes. 
        if flip_lr:
            self.ctrl.scaleX.set(-1)
            libPymel.makeIdentity_safe(self.ctrl, rotate=True, scale=True, apply=True)

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

        attr_adjustement_scale = libRigging.create_utility_node(
            'composeMatrix',
            inputScaleX=util_sensitivity_inv.outputX,
            inputScaleY=util_sensitivity_inv.outputY,
            inputScaleZ=util_sensitivity_inv.outputZ
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

        #
        # Constraint a specic controller to the avar doritos stack.
        # Call this method after connecting the ctrl to the necessary avars.
        # The sensibility of the doritos will be automatically computed in this step if necessary.
        #

        #
        # Inverse translation
        #
        if cancel_t:
            attr_ctrl_inv_t = libRigging.create_utility_node(
                'multiplyDivide', input1=self.ctrl.node.t,
                input2=[-1, -1, -1]
            ).output

            attr_ctrl_inv_t = libRigging.create_utility_node(
                'multiplyDivide',
                input1=attr_ctrl_inv_t,
                input2X=self.attr_sensitivity_tx,
                input2Y=self.attr_sensitivity_ty,
                input2Z=self.attr_sensitivity_tz
            ).output

            layer_inv_t = self._stack.append_layer(name='inverseT')

            if flip_lr:
                attr_doritos_tx = libRigging.create_utility_node(
                    'multiplyDivide',
                    input1X=attr_ctrl_inv_t.outputX,
                    input2X=-1
                ).outputX
            else:
                attr_doritos_tx = attr_ctrl_inv_t.outputX
            attr_doritos_ty = attr_ctrl_inv_t.outputY
            attr_doritos_tz = attr_ctrl_inv_t.outputZ

            pymel.connectAttr(attr_doritos_tx, layer_inv_t.tx)
            pymel.connectAttr(attr_doritos_ty, layer_inv_t.ty)
            pymel.connectAttr(attr_doritos_tz, layer_inv_t.tz)

        #
        # Inverse rotation
        # Add an inverse node that will counter animate the position of the ctrl.
        # TODO: Rename
        #
        if cancel_r:
            layer_inv_r = self._stack.append_layer(name='inverseR')
            # layer_doritos = pymel.createNode('transform', name=layer_doritos_name)
            # layer_doritos.setParent(self._stack.node)

            # Create inverse attributes for the ctrl

            attr_ctrl_inv_r = libRigging.create_utility_node('multiplyDivide', input1=self.ctrl.node.r,
                                                             input2=[-1, -1, -1]).output

            pymel.connectAttr(attr_ctrl_inv_r, layer_inv_r.r)

        #
        # Apply scaling on the ctrl parent.
        # This is were the 'black magic' happen.
        #
        # flip_lr = False
        # if flip_lr:
        #     attr_ctrl_offset_sx_inn = libRigging.create_utility_node('multiplyDivide',
        #                                                              input1X=self.attr_sensitivity_tx,
        #                                                              input2X=-1
        #                                                              ).outputX
        # else:
        #     attr_ctrl_offset_sx_inn = self.attr_sensitivity_tx
        # attr_ctrl_offset_sy_inn = self.attr_sensitivity_ty
        # attr_ctrl_offset_sz_inn = self.attr_sensitivity_tz

        # Create an output object that will hold the world position of the ctrl offset.
        # We'll use direct connections to the animation controller to simplify the dag tree and support
        # non-uniform scaling (which is really hard to do using constraints).

        # Since the the model's ctrl will still be influenced by the root ctrl, we'll need to extract the offset
        # relative to the root ctrl.

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

        # Rotation
        # if parent_rot is None:
        #     parent_rot = stack_end
        # parent_rot = layer_inv_r.getParent()
        # pymel.orientConstraint(jnt_head, self._grp_output, maintainOffset=True)

        # Direct-connect the output group to the ctrl offset grp.
        # Since the ctrl is a child of the master ctrl, we'll need to take it's parent in consideration.
        parent = self.get_parent_obj()
        util_get_ctrl_offset_local_trs = libRigging.create_utility_node(
            'decomposeMatrix',
            name=nomenclature_rig.resolve('getOutputLocalTm'),
            inputMatrix=libRigging.create_utility_node(
                'multMatrix',
                matrixIn=(
                    self._grp_output.matrix,
                    parent.worldInverseMatrix,
                )
            ).matrixSum
        )
        pymel.connectAttr(util_get_ctrl_offset_local_trs.outputTranslate, self.ctrl.offset.translate)
        pymel.connectAttr(util_get_ctrl_offset_local_trs.outputRotate, self.ctrl.offset.rotate)

    def unbuild(self, **kwargs):
        super(CtrlModelCalibratable, self).unbuild(**kwargs)

        # todo: maybe hold sensitivity for faster rebuild?
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None

    # --- Custom methods

    def _get_calibration_reference(self):
        return self.jnt

    def calibrate(self, tx=True, ty=True, tz=True):
        ref = self._get_calibration_reference()
        if not ref:
            self.warning("Can't calibrate {0}, found no influences.".format(self))
            return

        self._fix_ctrl_shape()

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

    def post_build(self):
        self.calibrate()

    def _fix_ctrl_shape(self):
        """
        When the rigger want to resize an InteractiveCtrl, he will modify the ctrl shape 'controlPoints' attributes.
        This can be problematic since the shape 'create' attribute is feed from a transformGeometry node
        to compensate the non-uniform scaling caused by the calibration. This will 'skew' the shape which we don't want.
        We always want to make sure that there's only data in the orig shape 'controlPoints' attributes.
        This method will create a temporary shape that will receive the 'local' attribute from the ctrl shape (which
        contain the deformation from the 'controlPoints' attribute). The 'local' attribute of that shape will then be
        fed back to the orig shape. Finally, all the original 'controlPoints' will be set to zero.
        """
        grp_offset = self.ctrl.offset

        def get_orig_shape(shape):
            return next((hist for hist in shape.listHistory()
                         if isinstance(hist, pymel.nodetypes.NurbsCurve)
                         and hist != shape
                         and hist.intermediateObject.get()), None)

        def get_transformGeometry(shape):
            return next((hist for hist in shape.listHistory()
                         if isinstance(hist, pymel.nodetypes.TransformGeometry)), None)

        for shape in self.ctrl.node.getShapes(noIntermediate=True):
            # Resolve orig shape
            shape_orig = get_orig_shape(shape)
            if not shape_orig:
                self.warning("Skipping {}. Cannot find orig shape.".format(shape))
                continue

            # Resolve compensation matrix
            util_transform_geometry = get_transformGeometry(shape)
            if not util_transform_geometry:
                self.warning("Skipping {}. Cannot find transformGeometry.".format(shape))
                continue
            attr_compensation_tm = next(iter(util_transform_geometry.transform.inputs(plugs=True)), None)
            if not attr_compensation_tm:
                self.warning("Skipping {}. Cannot find compensation matrix.".format(shape))
                continue

            tmp_shape = pymel.createNode('nurbsCurve')
            tmp_shape.getParent().setParent(grp_offset)

            # Apply the inverted compensation matrix to access the desired orig_shape 'create' attr.
            tmp_transform_geometry = libRigging.create_utility_node(
                'transformGeometry',
                inputGeometry=shape.local,
                transform=attr_compensation_tm,
                invertTransform=True
            )
            attr_output_geometry = tmp_transform_geometry.outputGeometry
            pymel.connectAttr(attr_output_geometry, tmp_shape.create)
            pymel.disconnectAttr(tmp_shape.create)

            pymel.connectAttr(tmp_shape.local, shape_orig.create)

            # Remove any extraneous controlPoints coordinates.
            for attr_cp in shape.cp:
                attr_cp.set(0, 0, 0)
            for attr_cp in shape_orig.cp:
                attr_cp.set(0, 0, 0)

            # Cleanup
            pymel.disconnectAttr(shape_orig.create)
            pymel.delete(tmp_shape.getParent())
            pymel.delete(tmp_transform_geometry)


class CtrlLogicFaceCalibratable(CtrlModelCalibratable):
    """
    Base class for an InteractiveCtrl.
    """

    def validate(self):
        super(CtrlLogicFaceCalibratable, self).validate()

        # Ensure we have an head influence to base our rotation on.
        jnt_head = self.get_head_jnt()
        if not jnt_head:
            raise Exception("Can't resolve head influence. Please create a Head module.")

        # Ensure we have a mesh to slide on.
        meshes = libHistory.get_affected_shapes(self.jnts)
        if not meshes:
            raise Exception("Found no mesh associated with influences {0}".format(self.jnts))

    def build(self, avar, flip_lr=False, **kwargs):
        # todo: clean this shit!
        # if self.mesh is None:
        self.mesh = next(iter(libHistory.get_affected_shapes(self.jnts)), None)

        # Determine if we are controller a left or right sided ctrl
        pos_ref = self.ctrl.getTranslation(space='world')
        jnt_head = self.get_head_jnt()
        pos_ref_local = pos_ref * jnt_head.getMatrix(worldSpace=True).inverse()
        need_flip = pos_ref_local.x < 0

        super(CtrlLogicFaceCalibratable, self).build(avar, flip_lr=need_flip, **kwargs)


class ActionCalibrate(ComponentAction):
    def get_name(self):
        return 'Calibrate'

    def execute(self):
        self.component.calibrate()
