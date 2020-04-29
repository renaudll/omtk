import pymel.core as pymel

from omtk.core.classCtrl import BaseCtrl
from omtk.core.classNode import Node
from omtk.core import classCtrlModel
from omtk.core.compounds import create_compound
from omtk.libs import libRigging
from omtk.libs import libPymel
from omtk.libs import libAttr
from omtk.libs import libHistory


class ModelInteractiveCtrl(classCtrlModel.BaseCtrlModel):
    """
    An InteractiveCtrl ctrl is directly constrained on a mesh via a layer_fol.
    To prevent double deformation, the trick is an additional layer before the final ctrl that invert the movement.
    For clarity purposes, this is built in the rig so the animator don't need to see the whole setup.

    However an InteractiveCtrl might still have to be ccalibrated
    This is necessary to keep the InteractiveCtrl values in a specific range (ex: -1 to 1) in any scale.
    The calibration apply non-uniform scaling on the ctrl parent to cheat the difference.

    For this reason an InteractiveCtrl is created using the following steps:
    1) Create the setup (using build)
    2) Connecting the doritos ctrl to something
    3) Optionally call .calibrate()

    WARNING: This ctrl model is deprecated and is NOT integrated into the system at the moment for time reasons.
    The default ctrl model for a face is model_ctrl_interactive.
    In an ideal scenario, the rigger would be able to choose which ctrl model he desire.
    """

    _CLS_CTRL = BaseCtrl
    _ATTR_NAME_SENSITIVITY_TX = "sensitivityX"
    _ATTR_NAME_SENSITIVITY_TY = "sensitivityY"
    _ATTR_NAME_SENSITIVITY_TZ = "sensitivityZ"

    def __init__(self, *args, **kwargs):
        super(ModelInteractiveCtrl, self).__init__(*args, **kwargs)
        self.follicle = None  # Used for calibration (legacy)
        self.folliclePos = None  # Used for calibration
        self.mesh = None  # We should be able to provide the mesh
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None

        self._parent_tm = None

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

        # We always try to position the controller on the surface of the face.
        # The face is always looking at the positive Z axis.
        pos = tm.translate
        dir_ = pymel.datatypes.Point(0, 0, 1)
        result = self.rig.raycast_farthest(pos, dir_)
        if result:
            tm.a30 = result.x
            tm.a31 = result.y
            tm.a32 = result.z

        return tm

    def project_pos_on_face(self, pos, geos=None):
        pos = pymel.datatypes.Vector(pos.x, pos.y, 99999)
        dir = pymel.datatypes.Point(0, 0, -1)
        result = self.rig.raycast_nearest(pos, dir, geos=geos)
        return result if result else pos

    def create_interface(self):
        super(ModelInteractiveCtrl, self).create_interface()

        # The values will be computed when attach_ctrl will be called
        libAttr.addAttr_separator(self.grp_rig, "ctrlCalibration")
        self.attr_sensitivity_tx = libAttr.addAttr(
            self.grp_rig, longName=self._ATTR_NAME_SENSITIVITY_TX, defaultValue=1.0
        )
        self.attr_sensitivity_ty = libAttr.addAttr(
            self.grp_rig, longName=self._ATTR_NAME_SENSITIVITY_TY, defaultValue=1.0
        )
        self.attr_sensitivity_tz = libAttr.addAttr(
            self.grp_rig, longName=self._ATTR_NAME_SENSITIVITY_TZ, defaultValue=1.0
        )
        self.attr_sensitivity_tx.set(channelBox=True)
        self.attr_sensitivity_ty.set(channelBox=True)
        self.attr_sensitivity_tz.set(channelBox=True)

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
        **kwargs
    ):
        super(ModelInteractiveCtrl, self).build(avar, ctrl_size=ctrl_size, **kwargs)

        nomenclature_rig = self.get_nomenclature_rig()

        #
        # Resolve necessary informations
        #

        # Resolve which object will the InteractiveCtrl track.
        # If we don't want to follow a particular geometry, we'll use the end of the stack.
        # Otherwise the influence will be used (to also resolve the geometry).
        # todo: it could be better to resolve the geometry ourself
        if ref is None:
            ref = self.jnt

        # Resolve ctrl matrix
        # It can differ from the influence to prevent the controller to appear in the geometry.
        if ctrl_tm is None:
            ctrl_tm = self.get_default_tm_ctrl()

        if ctrl_tm is None and ref_tm:
            ctrl_tm = ref_tm

        if ctrl_tm is None and self.jnt:
            ctrl_tm = self.jnt.getMatrix(worldSpace=True)

        if ctrl_tm is None:
            raise Exception("Cannot resolve ctrl transformation matrix!")

        pos_ref = self.project_pos_on_face(ctrl_tm.translate, geos=self.get_meshes())

        # Resolve u and v coordinates
        # todo: check if we really want to resolve the u and v ourself since it's now connected.

        # If a mesh was provided explicitly as input, use it.
        obj_mesh = obj_mesh or self.get_mesh()

        if obj_mesh is None:
            # We'll scan all available geometries and use the one with the shortest distance.
            meshes = libHistory.get_affected_shapes(ref)
            meshes = list(set(meshes) & set(self.rig.get_shapes()))
            if not meshes:
                meshes = set(self.rig.get_shapes())
            obj_mesh, _, out_u, out_v = libRigging.get_closest_point_on_shapes(
                meshes, pos_ref
            )

            if obj_mesh is None and follow_mesh:
                raise Exception("Can't find mesh affected by %s." % self.jnt)

        else:
            _, out_u, out_v = libRigging.get_closest_point_on_shape(obj_mesh, pos_ref)

        # Resolve u and v coordinates if necesary.
        if u_coord is None:
            u_coord = out_u
        if v_coord is None:
            v_coord = out_v

        if self.jnt:
            self.log.debug(
                "Creating doritos on %s using %s as reference", obj_mesh, self.jnt
            )
        else:
            self.log.debug("Creating doritos on %s", obj_mesh)

        # Hack: Since there's scaling on the ctrl so the left and right side ctrl channels matches, we need to flip the ctrl shapes.
        if flip_lr:
            self.ctrl.scaleX.set(-1)
            libPymel.makeIdentity_safe(self.ctrl, rotate=True, scale=True, apply=True)

        # Create a "shapeOrig" for the ctrl
        ctrl_shape = self.ctrl.node.getShape()
        tmp = pymel.duplicate(self.ctrl.node.getShape())[0]
        ctrl_shape_orig = tmp.getShape()
        ctrl_shape_orig.setParent(self.ctrl.node, relative=True, shape=True)
        ctrl_shape_orig.rename(ctrl_shape.name() + "Orig")
        pymel.delete(tmp)
        ctrl_shape_orig.intermediateObject.set(True)

        for cp in ctrl_shape.cp:
            cp.set(0, 0, 0)

        if parent_rot:
            rot_ref = pymel.createNode(
                "transform", name=nomenclature_rig.resolve("parentRotRef")
            )
            pymel.orientConstraint(parent_rot, rot_ref, maintainOffset=True)
        else:
            rot_ref = None

        compound = create_compound(
            "omtk.InteractiveCtrl",
            nomenclature_rig.resolve("ctrlModelInteractive"),
            inputs={
                "bindTM": ctrl_tm,
                "ctrlLocalTM": self.ctrl.matrix,
                "ctrlShapeOrig": ctrl_shape_orig.local,
                "mesh": obj_mesh.outMesh,
                "parameterU": u_coord,
                "parameterV": v_coord,
                "sensitivityX": self.attr_sensitivity_tx,
                "sensitivityY": self.attr_sensitivity_ty,
                "sensitivityZ": self.attr_sensitivity_tz,
                "parentTM": rot_ref.matrix if rot_ref else None,
            },
        )

        compound_ctrl_shape = pymel.Attribute("%s.ctrlShapeAdjusted" % compound.output)
        pymel.connectAttr(compound_ctrl_shape, ctrl_shape.create, force=True)
        pymel.connectAttr(
            "%s.ctrlOffsetTranslate" % compound.output, self.ctrl.offset.translate
        )
        pymel.connectAttr(
            "%s.ctrlOffsetRotate" % compound.output, self.ctrl.offset.rotate
        )
        pymel.connectAttr(
            "%s.ctrlOffsetScale" % compound.output, self.ctrl.offset.scale
        )
        self.folliclePos = pymel.Attribute("%s.folliclePos" % compound.output)

        # Create a temporary follicle to find the coords
        # Note: This is done in a particular order, need to clarify why.
        # TODO: Cleanup
        fol_shape = libRigging.create_follicle2(obj_mesh, u=u_coord, v=v_coord)
        fol_transform = fol_shape.getParent()
        fol_bind_tm = fol_transform.getMatrix()
        pymel.delete(fol_transform)
        pymel.Attribute("%s.follicleBindTM" % compound.input).set(fol_bind_tm)

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
            attr_inn_ud = self.ctrl.translateY
            libRigging.connectAttr_withBlendWeighted(attr_inn_ud, avar.attr_ud)

        if lr:
            attr_inn_lr = self.ctrl.translateX

            if need_flip:
                attr_inn_lr = libRigging.create_utility_node(
                    "multiplyDivide", input1X=attr_inn_lr, input2X=-1
                ).outputX

            libRigging.connectAttr_withBlendWeighted(attr_inn_lr, avar.attr_lr)

        if fb:
            attr_inn_fb = self.ctrl.translateZ
            libRigging.connectAttr_withBlendWeighted(attr_inn_fb, avar.attr_fb)

        # Rotation
        if yw:
            attr_inn_yw = self.ctrl.rotateY

            if need_flip:
                attr_inn_yw = libRigging.create_utility_node(
                    "multiplyDivide", input1X=attr_inn_yw, input2X=-1
                ).outputX

            libRigging.connectAttr_withBlendWeighted(attr_inn_yw, avar.attr_yw)

        if pt:
            attr_inn_pt = self.ctrl.rotateX
            libRigging.connectAttr_withBlendWeighted(attr_inn_pt, avar.attr_pt)

        if rl:
            attr_inn_rl = self.ctrl.rotateZ

            if need_flip:
                attr_inn_rl = libRigging.create_utility_node(
                    "multiplyDivide", input1X=attr_inn_rl, input2X=-1
                ).outputX

            libRigging.connectAttr_withBlendWeighted(attr_inn_rl, avar.attr_rl)

        # Scale
        if sx:
            attr_inn = self.ctrl.scaleX
            libRigging.connectAttr_withBlendWeighted(attr_inn, avar.attr_sx)
        if sy:
            attr_inn = self.ctrl.scaleY
            libRigging.connectAttr_withBlendWeighted(attr_inn, avar.attr_sy)
        if sz:
            attr_inn = self.ctrl.scaleZ
            libRigging.connectAttr_withBlendWeighted(attr_inn, avar.attr_sz)

    def unbuild(self):
        # Ensure the shape stay consistent between rebuild.
        self._fix_ctrl_shape()

        super(ModelInteractiveCtrl, self).unbuild()
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
                self.log.warning("Skipping %s. Cannot find orig shape.", shape)
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
        # Determine what to check during calibration
        # Previous versions kept a reference to the follicle in "self.follicle".
        # Newer version keep a reference to the follicle pos in "self.folliclePos".
        if self.follicle:
            influence = self.follicle
            fnCalibrate = libRigging.calibrate_attr_using_translation
        elif self.folliclePos:
            influence = self.folliclePos
            fnCalibrate = libRigging.calibrate_attr_using_translation_attribute
        else:
            self.log.warning("Can't calibrate %s, found no influences.", self)
            return

        self._fix_ctrl_shape()

        for enabled, attr_name, attr_dst in (
            (tx, "tx", self.attr_sensitivity_tx),
            (ty, "ty", self.attr_sensitivity_ty),
            (tz, "tz", self.attr_sensitivity_tz),
        ):
            callibration_attr = self.ctrl.node.attr(attr_name)
            if not enabled or callibration_attr.isLocked():
                continue
            sensitivity = fnCalibrate(callibration_attr, influence)
            self.log.debug(
                "Adjusting sensibility %s for %s to %s", attr_name, self, attr_dst
            )
            attr_dst.set(sensitivity)
