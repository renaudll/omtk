import pymel.core as pymel
from pymel.core.datatypes import Matrix, Vector, Point

from omtk.core.classCtrl import BaseCtrl
from omtk.core import classCtrlModel
from omtk.libs import libRigging
from omtk.libs import libPymel
from omtk.libs import libAttr
from omtk.libs import libHistory


class ModelCtrlLinear(classCtrlModel.BaseCtrlModel):
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

    _CLS_CTRL = BaseCtrl
    _ATTR_NAME_SENSITIVITY_TX = "sensitivityX"
    _ATTR_NAME_SENSITIVITY_TY = "sensitivityY"
    _ATTR_NAME_SENSITIVITY_TZ = "sensitivityZ"

    def __init__(self, *args, **kwargs):
        super(ModelCtrlLinear, self).__init__(*args, **kwargs)
        self.follicle = None  # Used for calibration
        self.mesh = None  # We should be able to provide the mesh
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None

        # The object containing the bind pose of the
        # influence controller by the controller.
        self._grp_bind_infl = None

        # The object containing the desired default position of the ctrl.
        # This can differ from the bind pose of the ctrl mode.
        # For example, the jaw ctrl model will influence a joint
        # inside the head but the controller will be outside.
        self._grp_bind_ctrl = None

        self._attr_inn_parent_tm = None

        self._stack = None

    def parent_to(self, parent):
        """
        Bypass default parent mecanism since it is computer internally.
        """
        pass

    def get_default_tm_ctrl(self):
        """
        :return: The ctrl transformation.
        """
        if self.jnt is None:
            self.log.warning("Cannot resolve ctrl matrix with no inputs!")
            return None

        tm = self.jnt.getMatrix(worldSpace=True)

        result = self.project_pos_on_face(tm.translate, geos=self.get_meshes())
        if result:
            tm.a30 = result.x
            tm.a31 = result.y
            tm.a32 = result.z
        return tm

    def project_pos_on_face(self, pos, geos=None):
        pos = Vector(pos.x, pos.y, 99999)
        dir = Point(0, 0, -1)
        result = self.rig.raycast_nearest(pos, dir, geos=geos)
        return result if result else pos

    def _create_follicle(
        self, ctrl_tm, influence, obj_mesh=None, u_coord=None, v_coord=None
    ):
        naming = self.get_nomenclature_rig()
        # Create a follicle, this will be used for callibration purpose.
        # If this affect performance we can create it only when necessary,
        # however being able to see it help with debugging.

        # Resolve u and v coordinates
        if obj_mesh is None:
            # We'll scan all available geometries and use
            # the one with the shortest distance.
            meshes = libHistory.get_affected_shapes(influence)
            meshes = list(set(meshes) & set(self.rig.get_shapes()))
            meshes = meshes or set(self.rig.get_shapes())
            obj_mesh, _, out_u, out_v = libRigging.get_closest_point_on_shapes(
                meshes, ctrl_tm.translate
            )

        else:
            _, out_u, out_v = libRigging.get_closest_point_on_shape(
                obj_mesh, ctrl_tm.translate
            )

        # Resolve u and v coordinates if necesary.
        u_coord = u_coord or out_u
        v_coord = v_coord or out_v

        fol_name = naming.resolve("follicle")
        fol_shape = libRigging.create_follicle(obj_mesh, u=u_coord, v=v_coord)
        fol_transform = fol_shape.getParent()
        fol_transform.rename(fol_name)
        fol_transform.setParent(self.grp_rig)

        return fol_transform, fol_shape

    def build(
        self,
        avar,
        ref=None,
        ref_tm=None,
        grp_rig=None,
        obj_mesh=None,
        u_coord=None,
        v_coord=None,
        flip_lr=False,
        follow_mesh=True,
        ctrl_tm=None,
        ctrl_size=1.0,
        parent_pos=None,
        parent_rot=None,
        parent_scl=None,
        constraint=False,
        cancel_t=True,
        cancel_r=True,
        attr_bind_tm=None,
        **kwargs
    ):
        # todo: get rid of the u_coods, v_coods etc, we should rely on the bind
        super(ModelCtrlLinear, self).build(avar, ctrl_size=ctrl_size, **kwargs)

        naming = self.get_nomenclature_rig()

        #
        # Resolve necessary informations
        #

        # Resolve which object will the InteractiveCtrl track.
        # If we don't want to follow a particular geometry,
        # we'll use the end of the stack.
        # Otherwise the influence will be used (to also resolve the geometry).
        # todo: it could be better to resolve the geometry ourself
        ref = ref or self.jnt

        # Resolve the ctrl default tm
        ctrl_tm = ctrl_tm or self.get_default_tm_ctrl()
        if ctrl_tm is None:
            raise Exception("Cannot resolve ctrl transformation matrix!")

        # By default, we expect the rigger to mirror the face joints using the 'behavior' mode.
        if flip_lr:
            ctrl_tm = (
                Matrix(
                    [1.0, 0.0, 0.0, 0.0],
                    [0.0, -1.0, 0.0, 0.0],
                    [0.0, 0.0, -1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                )
                * ctrl_tm
            )

        self._grp_bind_ctrl = pymel.createNode(
            "transform", name=naming.resolve("ctrlBindTm"), parent=self.grp_rig,
        )
        self._grp_bind_ctrl.setMatrix(ctrl_tm)

        # Resolve the influence bind tm
        # Create an offset node to easily change it.
        self._grp_bind_infl = pymel.createNode(
            "transform", name=naming.resolve("bind"), parent=self.grp_rig
        )
        if attr_bind_tm:
            util_decompose_bind = libRigging.create_utility_node(
                "decomposeMatrix", inputMatrix=attr_bind_tm,
            )
            pymel.connectAttr(
                util_decompose_bind.outputTranslate, self._grp_bind_infl.translate
            )
            pymel.connectAttr(
                util_decompose_bind.outputRotate, self._grp_bind_infl.rotate
            )
            pymel.connectAttr(
                util_decompose_bind.outputScale, self._grp_bind_infl.scale
            )
        else:  # todo: deprecate this?
            self._grp_bind_infl.setTranslation(ctrl_tm.translate)

        # Create a follicle, this will be used for calibration purpose.
        # If this affect performance we can create it only when necessary, however being able to
        # see it help with debugging.
        follicle_transform, follicle_shape = self._create_follicle(
            ctrl_tm, ref, obj_mesh=obj_mesh, u_coord=u_coord, v_coord=v_coord,
        )
        self.follicle = follicle_transform

        #
        # Add calibration-related attribute
        #

        def _add_attr(name):
            attr = libAttr.addAttr(self.grp_rig, longName=name, defaultValue=1.0)
            attr.set(channelBox=True)
            return attr

        # The values will be computed when attach_ctrl will be called
        libAttr.addAttr_separator(self.grp_rig, "ctrlCalibration")
        self.attr_sensitivity_tx = _add_attr(self._ATTR_NAME_SENSITIVITY_TX)
        self.attr_sensitivity_ty = _add_attr(self._ATTR_NAME_SENSITIVITY_TY)
        self.attr_sensitivity_tz = _add_attr(self._ATTR_NAME_SENSITIVITY_TZ)

        # Hack: Since there's scaling on the ctrl so the left and right side ctrl
        # channels matches, we need to flip the ctrl shapes.
        if flip_lr:
            self.ctrl.scaleX.set(-1)
            libPymel.makeIdentity_safe(self.ctrl, rotate=True, scale=True, apply=True)

        grp_output = pymel.createNode(
            "transform", name=naming.resolve("output"), parent=self.grp_rig
        )

        attr_output_tm = libRigging.create_utility_node(
            "multMatrix",
            matrixIn=(
                self._grp_bind_ctrl.matrix,
                self._attr_inn_parent_tm,
                self.rig.grp_anm.worldInverseMatrix,
            ),
        ).matrixSum
        libRigging.connect_matrix_to_node(attr_output_tm, grp_output)

        # Create inverted attributes for sensibility
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
        attr_sensibility_lr_inv = util_sensitivity_inv.outputX
        attr_sensibility_ud_inv = util_sensitivity_inv.outputY
        attr_sensibility_fb_inv = util_sensitivity_inv.outputZ

        attr_ctrl_offset_sx_inn = self.attr_sensitivity_tx
        attr_ctrl_offset_sy_inn = self.attr_sensitivity_ty
        attr_ctrl_offset_sz_inn = self.attr_sensitivity_tz

        # Connect any additionel scale source.
        if parent_scl:
            u = libRigging.create_utility_node(
                "multiplyDivide",
                name=naming.resolve("getAbsoluteCtrlOffsetScale"),
                input1X=attr_ctrl_offset_sx_inn,
                input1Y=attr_ctrl_offset_sy_inn,
                input1Z=attr_ctrl_offset_sz_inn,
                input2X=parent_scl.scaleX,
                input2Y=parent_scl.scaleY,
                input2Z=parent_scl.scaleZ,
            )
            (
                attr_ctrl_offset_sx_inn,
                attr_ctrl_offset_sy_inn,
                attr_ctrl_offset_sz_inn,
            ) = (u.outputX, u.outputY, u.outputZ)

        # Ensure the scaling of the parent is taken in account.
        attr_calibration_scale_tm = libRigging.create_utility_node(
            "composeMatrix",
            name=naming.resolve("composeCalibrationScaleTm"),
            inputScaleX=attr_ctrl_offset_sx_inn,
            inputScaleY=attr_ctrl_offset_sy_inn,
            inputScaleZ=attr_ctrl_offset_sz_inn,
        ).outputMatrix
        attr_ctrl_offset_scale_tm = libRigging.create_utility_node(
            "multMatrix",
            name=naming.resolve("getCtrlOffsetScaleTm"),
            matrixIn=(
                attr_calibration_scale_tm,
                self._attr_inn_parent_tm,
                self.rig.grp_anm.worldInverseMatrix,
            ),
        ).matrixSum
        attr_ctrl_offset_scale = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=attr_ctrl_offset_scale_tm
        ).outputScale

        # Flip the x axis if we are on the right side of the face.
        # We need to do it as the last step since this will result
        # in a right-handed matrix which will be canceled out if we feed it
        # into multMatrix or other maya nodes.
        if flip_lr:
            attr_ctrl_offset_scale = libRigging.create_utility_node(
                "multiplyDivide",
                input1=attr_ctrl_offset_scale,
                input2X=-1.0,
                input2Y=1.0,
                input2Z=1.0,
            ).output
        pymel.connectAttr(attr_ctrl_offset_scale, self.ctrl.offset.scale)

        # Apply sensibility on the ctrl shape
        ctrl_shape = self.ctrl.node.getShape()
        tmp = pymel.duplicate(self.ctrl.node.getShape())[0]
        ctrl_shape_orig = tmp.getShape()
        ctrl_shape_orig.setParent(self.ctrl.node, relative=True, shape=True)
        ctrl_shape_orig.rename(ctrl_shape.name() + "Orig")
        pymel.delete(tmp)
        ctrl_shape_orig.intermediateObject.set(True)

        for cp in ctrl_shape.cp:
            cp.set(0, 0, 0)

        # Counter-scale the shape
        attr_adjustement_sx_inn = attr_sensibility_lr_inv
        attr_adjustement_sy_inn = attr_sensibility_ud_inv
        attr_adjustement_sz_inn = attr_sensibility_fb_inv
        attr_adjustement_scale = libRigging.create_utility_node(
            "composeMatrix",
            inputScaleX=attr_adjustement_sx_inn,
            inputScaleY=attr_adjustement_sy_inn,
            inputScaleZ=attr_adjustement_sz_inn,
        ).outputMatrix

        attr_adjustement_rot = libRigging.create_utility_node(
            "composeMatrix",
            inputRotateX=self.ctrl.node.rotateX,
            inputRotateY=self.ctrl.node.rotateY,
            inputRotateZ=self.ctrl.node.rotateZ,
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

        pymel.connectAttr(grp_output.translate, self.ctrl.offset.translate)
        pymel.connectAttr(grp_output.rotate, self.ctrl.offset.rotate)

        if constraint and self.jnt:
            pymel.parentConstraint(self.ctrl.node, self.jnt, maintainOffset=True)

            # todo: merge with .connect_ctrl

    def connect(
        self,
        avar,
        avar_grp,
        ud=True,
        fb=True,
        lr=True,
        yw=True,
        pt=True,
        rl=True,
        sx=True,
        sy=True,
        sz=True,
    ):
        need_flip = avar.need_flip_lr()

        # Position
        if ud:
            libRigging.connectAttr_withBlendWeighted(self.ctrl.translateY, avar.attr_ud)

        if lr:
            attr = self.ctrl.translateX
            attr = _flip_attr(attr) if need_flip else attr
            libRigging.connectAttr_withBlendWeighted(attr, avar.attr_lr)

        if fb:
            libRigging.connectAttr_withBlendWeighted(self.ctrl.translateZ, avar.attr_fb)

        # Rotation
        if yw:
            attr = self.ctrl.rotateY
            attr = _flip_attr(attr) if need_flip else attr
            libRigging.connectAttr_withBlendWeighted(attr, avar.attr_yw)

        if pt:
            libRigging.connectAttr_withBlendWeighted(self.ctrl.rotateX, avar.attr_pt)

        if rl:
            attr = self.ctrl.rotateZ
            attr = _flip_attr(attr) if need_flip else attr
            libRigging.connectAttr_withBlendWeighted(attr, avar.attr_rl)

        # Scale
        if sx:
            libRigging.connectAttr_withBlendWeighted(self.ctrl.scaleX, avar.attr_sx)
        if sy:
            libRigging.connectAttr_withBlendWeighted(self.ctrl.scaleY, avar.attr_sy)
        if sz:
            libRigging.connectAttr_withBlendWeighted(self.ctrl.scaleZ, avar.attr_sz)

    def unbuild(self):
        # Ensure the shape stay consistent between rebuild.
        self._fix_ctrl_shape()

        super(ModelCtrlLinear, self).unbuild()
        # TODO: Maybe hold and fetch the senstivity? Will a doritos will ever be serialzied?
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None

        self.follicle = None

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
        if self.ctrl is None:
            return
        grp_offset = self.ctrl.offset

        def get_orig_shape(shape):
            return next(
                (
                    hist
                    for hist in shape.listHistory()
                    if isinstance(hist, pymel.nodetypes.NurbsCurve)
                    and hist != shape
                    and hist.intermediateObject.get()
                ),
                None,
            )

        def get_transformGeometry(shape):
            return next(
                (
                    hist
                    for hist in shape.listHistory()
                    if isinstance(hist, pymel.nodetypes.TransformGeometry)
                ),
                None,
            )

        for shape in self.ctrl.node.getShapes(noIntermediate=True):
            # Resolve orig shape
            shape_orig = get_orig_shape(shape)
            if not shape_orig:
                self.log.warning("Skipping %s. Cannot find orig shape.".shape)
                continue

            # Resolve compensation matrix
            util_transform_geometry = get_transformGeometry(shape)
            if not util_transform_geometry:
                self.log.warning("Skipping %s. Cannot find transformGeometry.", shape)
                continue
            attr_compensation_tm = next(
                iter(util_transform_geometry.transform.inputs(plugs=True)), None
            )
            if not attr_compensation_tm:
                self.log.warning("Skipping %s. Cannot find compensation matrix.", shape)
                continue

            tmp_shape = pymel.createNode("nurbsCurve")
            tmp_shape.getParent().setParent(grp_offset)

            # Apply the inverted compensation matrix to access the desired orig_shape 'create' attr.
            tmp_transform_geometry = libRigging.create_utility_node(
                "transformGeometry",
                inputGeometry=shape.local,
                transform=attr_compensation_tm,
                invertTransform=True,
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

    def swap_mesh(self, new_mesh, calibrate=True):
        """
        Change the mesh that the follicle is attached to.
        This is made to be used on a build InteractiveCtrlModel.
        :param new_mesh: A pymel.nodetypes.Mesh or pymel.nodetypes.Transform containing a mesh.
        """
        # Resolve the node driven by the follicle.
        # This node contain the bindPose of the ctrl and is linked via a parentConstraint which we'll want to re-create.
        # todo: how do we update the constraint again?
        constraint = next(
            obj
            for obj in self.follicle.translate.outputs()
            if isinstance(obj, pymel.nodetypes.ParentConstraint)
        )
        target = constraint.getParent()
        pymel.delete(constraint)
        pos = target.getTranslation(space="world")

        # Get the new uv coordinates and apply them
        _, new_u, new_v = libRigging.get_closest_point_on_mesh(new_mesh, pos)
        pymel.connectAttr(new_mesh.outMesh, self.follicle.inputMesh, force=True)
        self.follicle.attr("parameterU").set(new_u)
        self.follicle.attr("parameterV").set(new_v)

        # Recreate the constraint
        pymel.parentConstraint(self.follicle, target, maintainOffset=True)

        if calibrate:
            self.calibrate()

    def calibrate(self, tx=True, ty=True, tz=True):
        # TODO: use correct logger
        influence = self.follicle
        if not influence:
            self.log.warning("Can't calibrate %s, found no influences.", self)
            return

        self._fix_ctrl_shape()

        def _routine(attr, ref):
            calib_pos = libRigging.calibrate_attr_using_translation(
                attr, ref, step_size=0.1
            )
            calib_neg = libRigging.calibrate_attr_using_translation(
                attr, ref, step_size=-0.1
            )

            # Use the highest value between the positive and negative axis.
            # This is mainly because in lot of cases, the deformation will depend on the attribute sign.
            # For example, LLipCornerLR positive can be pure skinning but LLipCornerLR negative can be pure morph.
            # Using different calibration values depending on the sign is sadly not possible as
            # maya react badly when the parent scale of the ctrl parent we are dragging change suddenly.
            return calib_pos if calib_pos > calib_neg else calib_neg

        if tx and not self.ctrl.node.tx.isLocked():
            calib_val = _routine(self.ctrl.node.tx, influence)
            self.log.debug("Adjusting sensibility tx for %s to %s", self, calib_val)
            self.attr_sensitivity_tx.set(calib_val)

        if ty and not self.ctrl.node.ty.isLocked():
            calib_val = _routine(self.ctrl.node.ty, influence)
            self.log.debug("Adjusting sensibility ty for %s to %s", self, calib_val)
            self.attr_sensitivity_ty.set(calib_val)

        if tz and not self.ctrl.node.tz.isLocked():
            calib_val = _routine(self.ctrl.node.tz, influence)
            self.log.debug("Adjusting sensibility tz for %s to %s", self, calib_val)
            self.attr_sensitivity_tz.set(calib_val)


def _flip_attr(attr):  # TODO: Remove duplication
    return libRigging.create_utility_node(
        "multiplyDivide", input1X=attr, input2X=-1
    ).outputX
