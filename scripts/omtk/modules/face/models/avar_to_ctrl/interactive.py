"""
Logic for "ModelInteractiveCtrl"
"""
import pymel.core as pymel

from omtk.core.exceptions import ValidationError
from omtk.modules.face.models.avar_to_ctrl import base
from omtk.core.compounds import create_compound
from omtk.libs import libRigging
from omtk.libs import libPymel
from omtk.libs import libAttr
from omtk.libs import libHistory


class ModelInteractiveCtrl(base.BaseCtrlModel):
    """
    An InteractiveCtrl ctrl is directly constrained on a mesh via a layer_fol.
    To prevent double deformation, the trick is an additional
    layer before the final ctrl that invert the movement.
    For clarity purposes, this is built in the rig so
    the animator don't need to see the whole setup.

    However an InteractiveCtrl might still have to be calibrated
    This is necessary to keep the InteractiveCtrl values
    in a specific range (ex: -1 to 1) in any scale.
    The calibration apply non-uniform scaling on
    the ctrl parent to cheat the difference.

    For this reason an InteractiveCtrl is created using the following steps:
    1) Create the setup (using build)
    2) Connecting the doritos ctrl to something
    3) Optionally call .calibrate()

    WARNING: This ctrl model is deprecated and is NOT integrated
    into the system at the moment for time reasons.
    The default ctrl model for a face is model_ctrl_interactive.
    In an ideal scenario, the rigger would be able to choose which ctrl model he desire.
    """

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

    def validate(self):
        """
        Check if the module can be built in it's current state.

        :raises ValidationError: If the module fail to validate.
        """
        super(ModelInteractiveCtrl, self).validate()

        # Ensure that we have a mesh to follow.
        if not self.get_meshes():
            raise ValidationError("Please provide one reference mesh to follow.")

    def parent_to(self, parent):
        """
        Bypass default parent mecanism since it is computer internally.
        """
        pass

    def project_pos_on_face(self, pos, geos=None):
        pos = pymel.datatypes.Vector(pos.x, pos.y, 99999)
        dir = pymel.datatypes.Point(0, 0, -1)
        geos = geos or self.rig.get_shapes()
        return libRigging.ray_cast_nearest(pos, dir, geos) or pos

    def create_interface(self):
        super(ModelInteractiveCtrl, self).create_interface()

        def _fn(name):
            attr = libAttr.addAttr(self.grp_rig, longName=name, defaultValue=1.0)
            attr.set(channelBox=True)
            return attr

        # The values will be computed when attach_ctrl will be called
        libAttr.addAttr_separator(self.grp_rig, "ctrlCalibration")
        self.attr_sensitivity_tx = _fn(self._ATTR_NAME_SENSITIVITY_TX)
        self.attr_sensitivity_ty = _fn(self._ATTR_NAME_SENSITIVITY_TY)
        self.attr_sensitivity_tz = _fn(self._ATTR_NAME_SENSITIVITY_TZ)

    # TODO: Too many kwargs, simplify!
    def build(
        self,
        ctrl,
        ref=None,
        ref_tm=None,
        grp_rig=None,
        obj_mesh=None,
        u_coord=None,
        v_coord=None,
        flip_lr=False,
        follow_mesh=True,
        **kwargs
    ):
        super(ModelInteractiveCtrl, self).build(ctrl, **kwargs)

        naming = self.get_nomenclature_rig()

        # Resolve which object will the InteractiveCtrl track.
        # If we don't want to follow a particular geometry, we'll use the stack end.
        # Otherwise the influence will be used (to also resolve the geometry).
        # todo: it could be better to resolve the geometry ourself
        ref = ref or self.jnt

        # Resolve ctrl matrix
        # It can differ from the influence to prevent to prevent issues where the
        # controller dissapear under the geometry.
        ctrl_tm = ctrl.getMatrix(worldSpace=True)

        pos_ref = self.project_pos_on_face(ctrl_tm.translate, geos=self.get_meshes())

        # Resolve u and v coordinates
        obj_mesh = obj_mesh or self.get_mesh()
        if not obj_mesh:
            # Scan all available geometries and use the one with the shortest distance.
            meshes = libHistory.get_affected_shapes(ref)
            meshes = list(set(meshes) & set(self.rig.get_shapes()))
            meshes = meshes or set(self.rig.get_shapes())
            obj_mesh, _, out_u, out_v = libRigging.get_closest_point_on_shapes(
                meshes, pos_ref
            )
            if not obj_mesh and follow_mesh:
                raise Exception("Can't find mesh affected by %s." % self.jnt)
        else:
            _, out_u, out_v = libRigging.get_closest_point_on_shape(obj_mesh, pos_ref)

        # Fallback on automatically resolved UVs
        u_coord = u_coord or out_u
        v_coord = v_coord or out_v

        # Hack: Since there's scaling on the ctrl so the left and right side
        # ctrl channels matches, we need to flip the ctrl shapes.
        if flip_lr:
            ctrl.scaleX.set(-1)
            libPymel.makeIdentity_safe(ctrl, rotate=True, scale=True, apply=True)

        # Create a "shapeOrig" for the ctrl
        ctrl_shape = ctrl.node.getShape()
        tmp = pymel.duplicate(ctrl.node.getShape())[0]
        ctrl_shape_orig = tmp.getShape()
        ctrl_shape_orig.setParent(ctrl.node, relative=True, shape=True)
        ctrl_shape_orig.rename(ctrl_shape.name() + "Orig")
        pymel.delete(tmp)
        ctrl_shape_orig.intermediateObject.set(True)

        for control_point in ctrl_shape.cp:
            control_point.set(0, 0, 0)

        def _create_grp(suffix, tm=None):
            grp = pymel.createNode(
                "transform", name=naming.resolve(suffix), parent=self.grp_rig
            )
            if tm:
                grp.setMatrix(tm)
            return grp

        rot_ref = _create_grp("parent")
        pymel.parentConstraint(self.parent_jnt, rot_ref, maintainOffset=True)

        compound = create_compound(
            "omtk.InteractiveCtrl",
            naming.resolve("ctrlModelInteractive"),
            inputs={
                "bindTM": ctrl_tm,
                "ctrlLocalTM": ctrl.matrix,
                "ctrlShapeOrig": ctrl_shape_orig.local,
                "mesh": obj_mesh.outMesh,
                "parameterU": u_coord,
                "parameterV": v_coord,
                "sensitivityX": self.attr_sensitivity_tx,
                "sensitivityY": self.attr_sensitivity_ty,
                "sensitivityZ": self.attr_sensitivity_tz,
                "parentTM": rot_ref.matrix if rot_ref else None,
            },
            outputs={
                "ctrlOffsetTranslate": ctrl.offset.translate,
                "ctrlOffsetRotate": ctrl.offset.rotate,
                "ctrlOffsetScale": ctrl.offset.scale,
                "ctrlShapeAdjusted": ctrl_shape.create,
            },
        )
        pymel.PyNode("%s:dag" % compound.namespace).setParent(self.grp_rig)

        self.folliclePos = pymel.Attribute("%s.folliclePos" % compound.output)

        # if constraint and self.jnt:
        #     pymel.parentConstraint(ctrl.node, self.jnt, maintainOffset=True)

        self.calibrate(ctrl)

    def unbuild(self):
        # Ensure the shape stay consistent between rebuild.
        # self._fix_ctrl_shape()  # TODO: Find ctrl

        super(ModelInteractiveCtrl, self).unbuild()

        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None
        self.follicle = None

    def _fix_ctrl_shape(self, ctrl):
        """
        When the rigger want to resize an InteractiveCtrl, he will modify
        the ctrl shape 'controlPoints' attributes. This can be problematic since
        the shape 'create' attribute is feed from a transformGeometry node
        to compensate the non-uniform scaling caused by the calibration.
        This will 'skew' the shape which we don't want.
        We always want to make sure that there's only data in the
        orig shape 'controlPoints' attributes. This method will create a
        temporary shape that will receive the 'local' attribute from the
        ctrl shape (which contain the deformation from the 'controlPoints' attribute).
        The 'local' attribute of that shape will then be fed back to the orig shape.
        Finally, all the original 'controlPoints' will be set to zero.
        """
        if ctrl is None:
            return
        grp_offset = ctrl.offset

        def _get_orig_shape(shape):
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

        def _get_transformGeometry(shape):
            return next(
                (
                    hist
                    for hist in shape.listHistory()
                    if isinstance(hist, pymel.nodetypes.TransformGeometry)
                ),
                None,
            )

        for shape in ctrl.node.getShapes(noIntermediate=True):
            # Resolve orig shape
            shape_orig = _get_orig_shape(shape)
            if not shape_orig:
                self.log.warning("Skipping %s. Cannot find orig shape.", shape)
                continue

            # Resolve compensation matrix
            util_transform_geometry = _get_transformGeometry(shape)
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

            # Apply the inverted compensation matrix to
            # access the desired orig_shape 'create' attr.
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

    def swap_mesh(self, new_mesh, ctrl, calibrate=True):
        """
        Change the mesh that the follicle is attached to.
        This is made to be used on a build InteractiveCtrlModel.
        :param new_mesh: A mesh of transform containing a mesh.
        :type new_mesh: pymel.nodetypes.Mesh or pymel.nodetypes.Transform
        """
        # TODO: TEST
        # Resolve the node driven by the follicle.
        # This node contain the bindPose of the ctrl and is linked
        # via a parentConstraint which we'll want to re-create.
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
            self.calibrate(ctrl)

    def calibrate(self, ctrl):
        # Determine what to check during calibration
        # Previous versions kept a reference to the follicle in "self.follicle".
        # Newer version keep a reference to the follicle pos in "self.folliclePos".
        if self.follicle:
            influence = self.follicle
            fn = libRigging.calibrate_attr_using_translation
        elif self.folliclePos:
            influence = self.folliclePos
            fn = libRigging.calibrate_attr_using_translation_attribute
        else:
            self.log.warning("Can't calibrate %s, found no influences.", self)
            return

        self._fix_ctrl_shape(ctrl)

        for attr_name, attr_dst in (
            ("tx", self.attr_sensitivity_tx),
            ("ty", self.attr_sensitivity_ty),
            ("tz", self.attr_sensitivity_tz),
        ):
            callibration_attr = ctrl.node.attr(attr_name)
            if callibration_attr.isLocked():
                continue
            sensitivity = fn(callibration_attr, influence)
            self.log.debug(
                "Adjusting sensibility %s for %s to %s", attr_name, self, attr_dst
            )
            attr_dst.set(sensitivity)


def _flip_attr(attr):  # TODO: Remove duplication
    return libRigging.create_utility_node(
        "multiplyDivide", input1X=attr, input2X=-1
    ).outputX
