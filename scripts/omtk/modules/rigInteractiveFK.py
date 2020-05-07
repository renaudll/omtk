"""
The InteractiveFK is a generic module that use layered 'ribbons' to easily rig anything.
Common use cases are tentacles, ropes, props, clothing, tongue, etc.
This module is also one of the few that support non-uniform scaling, making it perfect for crazy scenarios.

You'll need to provide at least one surface for the system to work.
The surface can be driven by various deformer, however the common use case is to provide a skinned surface.
If you also provide the deformed surface influences as inputs, the InteractiveFK will automatically
detect the surface and it's influence as a 'layer' and will rig it accordingly.

You'll also want to provide the influences for the final deformer (generally a mesh).
Again, the InteractiveFK will reconize that thoses inputs are not related to any surface and
will ensure that they follow the last layer.

Warning:
Please note that to correctly support scaling, all the computation are done in LOCAL space.
This mean that you CANNOT use the skinned surface influences to drive the final mesh.
"""
import pymel.core as pymel

import omtk.models.model_ctrl_calibratable
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModuleMap import ModuleMap
from omtk.core.classModule import Module
from omtk.core.exceptions import ValidationError
from omtk.core import classCtrlModel
from omtk.libs import libRigging
from omtk.libs import libAttr
from omtk.libs import libPython
from omtk.libs import libHistory
from omtk.libs import libPymel
from omtk.libs import libSkinning


def _get_immediate_skincluster(transform):
    # Ensure we deal with a transform.
    if isinstance(transform, pymel.nodetypes.Shape):
        transform = transform.getParent()

    all_shapes = transform.getShapes()
    skinclusters = [
        hist
        for hist in transform.listHistory()
        if isinstance(hist, pymel.nodetypes.SkinCluster)
    ]
    for skincluster in skinclusters:
        for attr_output in skincluster.outputGeometry:
            next_shape = next(
                iter(
                    hist
                    for hist in attr_output.listHistory(future=True)
                    if isinstance(hist, pymel.nodetypes.Shape)
                ),
                None,
            )
            if next_shape in all_shapes:
                return skincluster


class InteractiveFKCtrl(BaseCtrl):
    pass


class InteractiveFKCtrlModel(omtk.models.model_ctrl_calibratable.CtrlModelCalibratable):
    """
    This module allow the controller to follow a follicle and
    hijack the influence skinCluster to only consider the local space.
    """

    DEFAULT_NAME_USE_FIRST_INPUT = True

    def __init__(self, *args, **kwargs):
        super(InteractiveFKCtrlModel, self).__init__(*args, **kwargs)

        self.follicle = None

        self._stack = None
        self._grp_bind = None
        self._grp_offset = None
        self._grp_output = None

    def get_default_tm_ctrl(self):
        pos_ref = self.jnt.getTranslation(space="world")
        tm_ref = pymel.datatypes.Matrix(
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, pos_ref.x, pos_ref.y, pos_ref.z, 1
        )
        return tm_ref

    def _get_calibration_reference(self):
        return self.follicle

    def get_bind_tm(self):
        """
        :return: The ctrl transformation that will be used to determine the position of the follicle.
        """
        if not self.jnt:
            self.log.warning("Cannot resolve ctrl matrix with no inputs!")
            return None

        return self.jnt.getMatrix(worldSpace=True)

    def get_bind_pos(self):
        return self.get_bind_tm().translate

    def get_default_shape(self):
        # If a surface we provided in the inputs, use it.
        surface = self.get_surface()
        if surface:
            return surface

        # We'll scan all available geometries and use the one with the shortest distance.
        meshes = libHistory.get_affected_shapes(self.jnt)
        meshes = list(set(meshes) & set(self.rig.get_shapes()))
        return next(iter(meshes), None)

    def build(
        self,
        create_follicle=True,
        pos=None,
        shape=None,
        shape_next=None,
        u_coord=None,
        v_coord=None,
        constraint=True,
        **kwargs
    ):
        """
        :param pos: The position to use when seeking where to create the follicle. Can be resolved automatically if the module have an influence.
        :param shape: The shape to create the follicle on. Can be resolved automatically if the module have an influence.
        :param u_coord: The U coordinate to use for the follicle. Can be resolved automatically if the module have an influence.
        :param v_coord: The V coordinate to use for the follicle. Can be resolved automatically if the module have an influence.
        :param constraint: If True, the ctrl will drive the influence via direct connect.
        :param kwargs: Any additional keyword argument will be passed to the parent method.
        """
        super(InteractiveFKCtrlModel, self).build(
            parent=None, **kwargs  # We handle the parenting ourself!
        )

        nomenclature_rig = self.get_nomenclature_rig()

        # Resolve bind position.
        if pos is None:
            pos = self.get_bind_pos()

        #
        # Create the 'bind' node that will follow the follicle in translation and something else in rotation.
        #

        # Create the a group containing the local offset in case we have an hyerarchy to preserve.
        self._grp_offset = pymel.createNode(
            "transform", name=nomenclature_rig.resolve("offset"), parent=self.grp_rig
        )
        attr_offset_tm = self._grp_offset.matrix

        # Create a reference to the previous deformation
        self._grp_bind = pymel.createNode(
            "transform", name=nomenclature_rig.resolve("follicle"), parent=self.grp_rig
        )
        self._grp_bind.setMatrix(self.get_bind_tm())
        attr_bind_tm = self._grp_bind.matrix
        attr_bind_tm_inv = self._grp_bind.inverseMatrix

        # Compute the parent offset and the deformation offset toguether.
        attr_total_offset = libRigging.create_utility_node(
            "multMatrix",
            name=nomenclature_rig.resolve("getOffset"),
            matrixIn=(attr_offset_tm, attr_bind_tm,),
        ).matrixSum

        # Create follicle to track the transform BEFORE the ctrl.
        if create_follicle:
            # Resolve mesh if necessary.
            if not shape:
                shape = self.get_default_shape()
            if not shape:
                raise Exception("Can't resolve mesh to attach to!")

            # Resolve uv coords if necessary
            if u_coord is None or v_coord is None:
                _, u_coord, v_coord = libRigging.get_closest_point_on_shape(shape, pos)
            if u_coord is None or v_coord is None:
                raise Exception("Can't resolve uv coordinates to use!")

            fol_shape = libRigging.create_follicle(shape, u=u_coord, v=v_coord)
            ref_before = fol_shape.getParent()
            ref_before.rename(nomenclature_rig.resolve("preCtrl"))
            ref_before.setParent(self.grp_rig)
        else:
            ref_before = pymel.createNode(
                "transform",
                name=nomenclature_rig.resolve("preCtrl"),
                parent=self.grp_rig,
            )
            ref_before.setMatrix(self.get_bind_tm())

        pymel.parentConstraint(ref_before, self._grp_bind, maintainOffset=True)

        # Create follicle to track the transfort AFTER the ctrl.
        # This will be used to position the controller correctly.
        if shape_next:
            # Resolve uv coords if necessary
            _, u_coord, v_coord = libRigging.get_closest_point_on_shape(shape_next, pos)
            if u_coord is None or v_coord is None:
                raise Exception("Can't resolve uv coordinates to use!")

            fol_shape = libRigging.create_follicle(shape_next, u=u_coord, v=v_coord)
            ref_after = fol_shape.getParent()
            ref_after.rename(nomenclature_rig.resolve("postCtrl"))
            ref_after.setParent(self.grp_rig)

            self.follicle = ref_after

        #
        # Constraint grp_anm
        #

        # Create an output object that will hold the world position of the ctrl offset.
        # This allow us to create direct connection which simplify the dag tree for the animator
        # and allow us to easily scale the whole setup to support non-uniform scaling.

        util_decompose_offset = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=attr_total_offset
        )

        pymel.connectAttr(
            util_decompose_offset.outputTranslate, self.ctrl.offset.translate
        )
        pymel.connectAttr(util_decompose_offset.outputRotate, self.ctrl.offset.rotate)

        #
        # Create an output group that contain the new joint position
        #
        grp_scale = pymel.createNode(
            "transform", name=nomenclature_rig.resolve("parent"), parent=self.grp_rig
        )
        self._grp_output = pymel.createNode(
            "transform", name=nomenclature_rig.resolve("output"), parent=grp_scale
        )

        attr_get_local_tm = libRigging.create_utility_node(
            "multMatrix", matrixIn=(self.ctrl.matrix, attr_total_offset)
        ).matrixSum

        util_decompose_local_tm = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=attr_get_local_tm
        )

        pymel.connectAttr(
            util_decompose_local_tm.outputTranslate, self._grp_output.translate
        )
        pymel.connectAttr(util_decompose_local_tm.outputRotate, self._grp_output.rotate)
        pymel.connectAttr(util_decompose_local_tm.outputScale, self._grp_output.scale)

        pymel.parentConstraint(self._grp_output, self.jnt, maintainOffset=True)
        pymel.scaleConstraint(self._grp_output, self.jnt, maintainOffset=True)

        surface = self.get_surface()
        skincluster = _get_immediate_skincluster(surface)
        index = libSkinning.get_skin_cluster_influence_objects(skincluster).index(
            self.jnt
        )
        pymel.connectAttr(
            attr_bind_tm_inv, skincluster.bindPreMatrix[index], force=True
        )

    def unbuild(self):
        super(InteractiveFKCtrlModel, self).unbuild()

        self.follicle = None


class InteractiveFKLayer(ModuleMap):
    _CLS_CTRL_MODEL = InteractiveFKCtrlModel
    _CLS_CTRL = InteractiveFKCtrl
    _NAME_CTRL_ENUMERATE = True  # Same implementation than FK

    def __init__(self, *args, **kwargs):
        super(InteractiveFKLayer, self).__init__(*args, **kwargs)

        # Used for constraining if necessary
        self._grp_parent = None

    def init_model(self, model, inputs, **kwargs):
        """
        Ensure the surface is present in the inputs.
        """
        surface = self.get_surface()
        if not surface:
            raise Exception("Expected surface in inputs.")
        if surface not in inputs:
            inputs.append(surface)

        return super(InteractiveFKLayer, self).init_model(model, inputs, **kwargs)

    def build(self, parent=False, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig()

        super(InteractiveFKLayer, self).build(parent=False, **kwargs)

        # Create a group for all the influences
        grp_influences = pymel.createNode(
            "transform", name=nomenclature_rig.resolve("jnts"), parent=self.grp_rig
        )

        common_parent = libPymel.get_common_parents(self.jnts)
        for jnt in self.jnts:
            if jnt.getParent() == common_parent:
                jnt.setParent(grp_influences)

        # Parent the surface into the surface group
        for surface in self.get_surfaces():
            surface.setParent(self.grp_rig)

    def build_models(self, constraint=False, calibrate=True, **kwargs):
        nomenclature_anm = self.get_nomenclature_anm()
        nomenclature_rig = self.get_nomenclature_rig()

        # Create a parent grp
        # This will be used by the models if they need to follow the parent.
        # Normally this is only necessary on the last layer.
        self._grp_parent = pymel.createNode(
            "transform", name=nomenclature_rig.resolve("parent"), parent=self.grp_rig
        )

        for i, (jnt, model) in enumerate(zip(self.jnts, self.models)):
            # Resolve ctrl name.
            if self._NAME_CTRL_ENUMERATE:
                ctrl_name = nomenclature_anm.resolve("{0:02d}".format(i + 1))
            else:
                nomenclature = nomenclature_anm + self.rig.nomenclature(
                    jnt.stripNamespace().nodeName()
                )
                ctrl_name = nomenclature.resolve()

            self.build_model(model, ctrl_name=ctrl_name, **kwargs)

            if model._grp_output:
                model._grp_output.setParent(self._grp_parent)

            if calibrate:
                model.calibrate()

        # For each models, hijack the 'offset' group in case we have an hierarchy to keep.
        for model in self.models:
            # Resolve the parent influence
            model_parent = model.parent
            if not model_parent:
                continue

            if not isinstance(model_parent, pymel.nodetypes.Joint):
                self.log.warning(
                    "Cannot compute offset for parent. Unsupported node type %s for %s",
                    type(self.parent),
                    self.parent,
                )
                continue

            # Resolve the parent model
            parent_model = next(
                (model for model in self.models if model.jnt == model_parent), None
            )
            if not parent_model:
                self.log.warning(
                    "Cannot compute offset for parent. Found no model associated with %s",
                    model_parent,
                )
                continue

            self._constraint_model_virtual_offset(model, parent_model)

    def _constraint_model_virtual_offset(self, model, parent_model):
        """
        Create the equivalent of a parent constraint between two models.
        This allow us to support fk-style functionnality.
        :param model: A child InteractiveFKLayer instance.
        :param parent_model: A parent InteractiveFKLayer instance.
        """
        nomenclature_rig = self.get_nomenclature_rig()

        model_parent = parent_model.jnt

        parent_ctrl = parent_model.ctrl
        parent_grp_offset = parent_model._grp_offset
        attr_parent_world_bindpose_tm_inv = libRigging.create_utility_node(
            "inverseMatrix",
            name=nomenclature_rig.resolve("getParentBindPose"),
            inputMatrix=model_parent.bindPose,
        ).outputMatrix
        attr_local_bindpose_tm = libRigging.create_utility_node(
            "multMatrix",
            name=nomenclature_rig.resolve("getLocalBindPose"),
            matrixIn=(model.jnt.bindPose, attr_parent_world_bindpose_tm_inv),
        ).matrixSum
        attr_local_bindpose_tm_inv = libRigging.create_utility_node(
            "inverseMatrix",
            name=nomenclature_rig.resolve("getLocalBindPoseInv"),
            inputMatrix=attr_local_bindpose_tm,
        ).outputMatrix
        attr_parent_offset_world_tm = libRigging.create_utility_node(
            "multMatrix",
            matrixIn=(
                attr_local_bindpose_tm,
                parent_grp_offset.matrix,
                attr_local_bindpose_tm_inv,
            ),
        ).matrixSum

        #
        # Compute the distorsion introduced by the bind.
        #
        attr_follicle_world_tm = model._grp_bind.matrix
        attr_parent_follicle_world_tm_inv = parent_model._grp_bind.inverseMatrix
        attr_follicle_delta_tm = libRigging.create_utility_node(
            "multMatrix",
            matrixIn=(
                attr_follicle_world_tm,
                attr_parent_follicle_world_tm_inv,
                attr_local_bindpose_tm_inv,
            ),
        ).matrixSum
        attr_follicle_delta_tm_inv = libRigging.create_utility_node(
            "inverseMatrix",
            name=nomenclature_rig.resolve("getLocalBindPoseInv"),
            inputMatrix=attr_follicle_delta_tm,
        ).outputMatrix
        attr_offset_tm = libRigging.create_utility_node(
            "multMatrix",
            name=nomenclature_rig.resolve("getOffsetTM"),
            matrixIn=(
                attr_local_bindpose_tm,
                attr_follicle_delta_tm,
                parent_ctrl.matrix,
                attr_follicle_delta_tm_inv,
                attr_local_bindpose_tm_inv,
                attr_parent_offset_world_tm,
            ),
        ).matrixSum
        util_decompose_offset_tm = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=attr_offset_tm
        )
        pymel.connectAttr(
            util_decompose_offset_tm.outputTranslate, model._grp_offset.translate
        )
        pymel.connectAttr(
            util_decompose_offset_tm.outputRotate, model._grp_offset.rotate
        )
        pymel.connectAttr(util_decompose_offset_tm.outputScale, model._grp_offset.scale)

    def unbuild(self):
        # Ensure surface is not destroyed by the unbuild process.
        surface = self.get_surface()
        if libPymel.is_child_of(surface, self.grp_rig):
            surface.setParent(world=True)

        # Ensure influences are not destroyed by the unbuild process.
        influences = self.jnts
        common_parent = libPymel.get_common_parents(influences)
        for influence in influences:
            if influence.getParent() == common_parent:
                influence.setParent(world=True)

        super(InteractiveFKLayer, self).unbuild()

        # We have connection from rig parts in the skinCluster bindPreMatrix,
        # if we remove the rig, this would reset the bindPreMatrix and result in double transformation.
        # To cancel that, we'll need to reset the bindPreMatrix attributes.
        is_skin_cluster = lambda x: isinstance(x, pymel.nodetypes.SkinCluster)
        for skin_cluster in libHistory.iter_history_backward(
            surface, key=is_skin_cluster, stop_at_shape=True
        ):
            attr_matrices = skin_cluster.matrix
            attr_pre_matrices = skin_cluster.bindPreMatrix
            num_elements = attr_matrices.numElements()
            for i in range(num_elements):
                attr_matrix = attr_matrices[i]
                attr_pre_matrix = attr_pre_matrices[i]
                attr_pre_matrix.set(attr_matrix.get().inverse())


class InteractiveFK(Module):
    _CLS_LAYER = InteractiveFKLayer
    _VALIDATE_NEED_SURFACE = True

    def __init__(self, *args, **kwargs):
        super(InteractiveFK, self).__init__(*args, **kwargs)

        # This will contain all the layers that take part in the system.
        self.layers = []

        # The group that all surface will be parented to.
        self._grp_surfaces = None

        self._grp_parent = None

    @property
    def parent(self):
        return libPymel.get_common_parents(self._get_unassigned_influences())

    def validate(self, epsilon=0.001):
        """
        Check if the module can be built in it's current state.

        :raises ValidationError: If the module fail to validate.
        """
        super(InteractiveFK, self).validate()

        surfaces = self.get_surfaces()
        if self._VALIDATE_NEED_SURFACE and not surfaces:
            raise ValidationError("Missing required input of type NurbsSurface")

        # Ensure there's no useless surface in the inputs.
        unassigned_surfaces = self._get_unassigned_surfaces()
        if unassigned_surfaces:
            raise ValidationError(
                "Useless surface(s) found: %s"
                % ", ".join((surface.name() for surface in unassigned_surfaces))
            )

        # todo: Ensure all surface have an identity matrix
        attr_to_check = {
            "translateX": 0.0,
            "translateY": 0.0,
            "translateZ": 0.0,
            "rotateX": 0.0,
            "rotateY": 0.0,
            "rotateZ": 0.0,
            "scaleX": 1.0,
            "scaleY": 1.0,
            "scaleZ": 1.0,
        }
        for surface in surfaces:
            for attr_name, desired_val in attr_to_check.iteritems():
                attr = surface.attr(attr_name)
                attr_val = attr.get()
                if abs(attr_val - desired_val) > epsilon:
                    raise ValidationError(
                        "Surface %s have invalid transform! Expected %s for %s, got %s."
                        % (surface, desired_val, attr_name, attr_val)
                    )

    def get_influences_by_surfaces(self):
        """
        Analyze the inputs to resolve what influence are skinned to which surface.
        This allow us to interpret the inputs and create layers accordingly.
        :return: A list of two-sized tuple containing the surface and influence for each layers.
        """
        result = []
        jnts = set(self.jnts)
        unassigned_jnts = set(self.jnts)

        # Sort surface by deformation history.
        surfaces = self.get_surfaces()

        # Ensure we are working directly with shapes.
        surfaces = [
            surface.getShape(noIntermediate=True)
            if isinstance(surface, pymel.nodetypes.Transform)
            else surface
            for surface in surfaces
        ]

        # Sort the surface by their construction history.
        # If the surface are already blendshaped toguether, this will work.
        def _fn_compare(obj_a, obj_b):
            hist_a = [
                hist
                for hist in obj_a.listHistory()
                if isinstance(hist, pymel.nodetypes.Shape)
            ]
            hist_b = [
                hist
                for hist in obj_b.listHistory()
                if isinstance(hist, pymel.nodetypes.Shape)
            ]
            if obj_b in hist_a:
                return 1
            elif obj_a in hist_b:
                return -1
            # If nothing works, compare their name...
            # We might get lucky and have correctly named objects like layer0, layer1, etc.
            self.log.warning(
                "Saw no relationship between %s and %s. Will sort them by name.",
                obj_a,
                obj_b,
            )
            return cmp(obj_a.name(), obj_b.name())

        surfaces = sorted(surfaces, cmp=_fn_compare)

        for surface in surfaces:
            skincluster = _get_immediate_skincluster(surface)
            if not skincluster:
                self.log.warning("Found no skinCluster for %s", surface)
                continue

            cur_influences = set(
                libSkinning.get_skin_cluster_influence_objects(skincluster)
            )
            cur_jnts = list(jnts & cur_influences)
            unassigned_jnts -= cur_influences

            result.append((surface.getParent(), cur_jnts))

        return result

    def _get_unassigned_influences(self):
        """
        Return all influences that don't affect any layers.
        Theses influences will be automatically constrained to the last layer.
        :return: A list of pymel.nodetypes.Joint instances.
        """
        jnts = set(self.jnts)
        for _, influences in self.get_influences_by_surfaces():
            jnts -= set(influences)
        return list(jnts)

    def _get_unassigned_surfaces(self):
        """
        Return all surface that are not affected by any influences.
        We currently do nothing with theses surfaces.
        :return: A list of pymel.PyNode representing the surfaces.
        """
        surfaces = set(self.get_surfaces())
        for surface, _ in self.get_influences_by_surfaces():
            surfaces.discard(surface)
        return list(surfaces) if surfaces else []

    @staticmethod
    def iter_uvs(num_u, num_v, min_u=0.0, max_u=1.0, min_v=0.0, max_v=1.0):
        """
        Generator for creating multiples objects on a surface.
        Note that if only one influence is provided for U or V space, it will be located at the center.
        :param num_u: The number of influences to create on U space.
        :param num_v: The number of influences to create on V space.
        :return: Wield a tuple of size four that contain the u counter, v counter, u coordinate and v coordinate.
        """
        for u_index in range(num_u):
            if num_u > 1:
                ratio = u_index / float(num_u - 1)
                u = libRigging.interp_linear(ratio, min_u, max_u)
            else:
                u = 0.5
            for v_index in range(num_v):
                if num_v > 1:
                    ratio = v_index / float(num_v - 1)
                    v = libRigging.interp_linear(ratio, min_v, max_v)
                else:
                    v = 0.5
                yield u_index, v_index, u, v

    def create_layer_from_surface(
        self,
        num_u=3,
        num_v=1,
        min_u=0.0,
        max_u=1.0,
        min_v=0.0,
        max_v=1.0,
        format_str="U{:02d}V{:02d}",
        cls_ctrl=None,
        suffix=None,
    ):
        """
        Create a new layer module by duplicating the reference surface and generating influences using predefined rules.
        Note that this does not add it to the layer stack.
        :param num_u: How much influences to generate in the surface U space.
        :param num_v: How much influences to generate in the surface U space.
        :param format_str: An str instance that drive how the influence are named using python string formatting mechanismm.
        :param suffix: The suffix to add to the moduel name.
        :return: An instance of the module class defined in self._CLS_LAYER.
        """
        nomenclature_jnt = self.get_nomenclature_jnt()
        nomenclature_rig = self.get_nomenclature_rig()

        # Create surface
        surface = self._create_surface(
            name=nomenclature_rig.resolve(suffix, "surface"),
        )

        jnts = []
        for u_index, v_index, u_coord, v_coord in self.iter_uvs(
            num_u, num_v, min_u=min_u, max_u=max_u, min_v=min_v, max_v=max_v
        ):
            pos = libRigging.get_point_on_surface_from_uv(surface, u_coord, v_coord)
            jnt = pymel.createNode(
                "joint",
                name=nomenclature_jnt.resolve(
                    suffix, format_str.format(u_index, v_index)
                ),
            )
            jnt.setTranslation(pos)
            jnts.append(jnt)

        # Assign a skinCluster on the surface using the influences.
        pymel.skinCluster(jnts, surface, mi=3)

        module = self.init_layer(
            None, inputs=jnts + [surface], cls_ctrl=cls_ctrl, suffix=suffix
        )
        return module

    def init_layer(self, inst, inputs=None, suffix=None, cls_layer=None, cls_ctrl=None):
        cls_layer = cls_layer or self._CLS_LAYER
        # TODO: Simplify name logic?
        name = (self.get_nomenclature() + suffix).resolve() if suffix else self.name
        module = cls_layer.from_instance(self.rig, inst, name, inputs=inputs)
        if cls_ctrl:
            module._CLS_CTRL = cls_ctrl

        return module

    def _init_layers(self):
        """
        Initialize any preset of layer configuration.
        Override this if you define a custom Module from this one.
        """
        # Build layers from inputs.
        data = self.get_influences_by_surfaces()

        # Ensure we have at least as many slots allocated that we have groups.
        num_layers = len(self.layers)
        num_data = len(data)
        if num_layers < num_data:
            libPython.resize_list(self.layers, num_data)

        self.log.debug("Found %s layer groups", len(data))
        for i, sub_data in enumerate(data):
            self.log.debug("Creating layer %s using %s", i + 1, sub_data)
            surface, influences = sub_data
            self.layers[i] = self.init_layer(
                self.layers[i],
                inputs=[surface] + influences,
                suffix="layer%s" % (i + 1),
            )

    def _build_layers(self, ctrl_size_max=None, ctrl_size_min=None):
        layers = self.layers
        num_layers = len(layers)

        for i in range(num_layers):
            prev_layer = layers[i - 1] if i > 0 else None
            curr_layer = layers[i]

            # Define desired ctrl size
            ratio = float(i) / (num_layers - 1) if num_layers > 1 else 1
            ctrl_size = (
                libRigging.interp_linear(ratio, ctrl_size_max, ctrl_size_min)
                if ctrl_size_max and ctrl_size_min
                else None
            )

            shape = prev_layer.get_surface() if prev_layer else None
            shape_skinned = curr_layer.get_surface()
            create_follicle = True if prev_layer else None
            curr_layer.build(
                create_follicle=create_follicle,
                shape=shape,
                shape_next=shape_skinned,
                ctrl_size=ctrl_size,
                parent=False,
            )

            is_last_layer = i == num_layers - 1
            if is_last_layer and self.parent:
                curr_layer.parent_to(self.parent)
            curr_layer.grp_anm.setParent(self.grp_anm)
            curr_layer.grp_rig.setParent(self.grp_rig)

    def _create_surface(self, ref_surface=None, parent=None, name=None, **kwargs):
        """
        Create a new surface for layer user.
        The resulting surface will be 'safe' to use with no scale or locked attributes.
        :param kwargs:
        :return:
        """
        if ref_surface is None:
            ref_surface = self.get_surface()
        new_surface = pymel.duplicate(ref_surface, **kwargs)[0]
        if parent:
            new_surface.setParent(parent)
        if name:
            new_surface.rename(name)
        libAttr.unlock_trs(new_surface)
        pymel.makeIdentity(new_surface, apply=True, scale=True)
        return new_surface

    def _get_default_ctrl_size(self):
        surface = self.get_surface()
        length_u, length_v = _get_surface_length(surface)
        return min(length_u, length_v)

    def build(self, ctrl_size_max=None, ctrl_size_min=None, parent=True, **kwargs):
        """
        :param ctrl_size_max: Used to automatically size layer ctrls. Define the maximum size (applied on first layer)
        :param ctrl_size_min: Used to automatically size layer ctrls. Define the minimum size (applied on last layer)
        :param parent: Redefined to compensate for bad design. Identical implementation than base class.
        :param kwargs: Any keyword argument will be forwarded to the base method.
        """
        super(InteractiveFK, self).build(parent=None, **kwargs)

        nomenclature_rig_grp = self.get_nomenclature_rig_grp()
        nomenclature_jnt = self.get_nomenclature_jnt()

        # Create a group that we will parent all surfaces to.
        self._grp_surfaces = pymel.createNode(
            "transform",
            name=nomenclature_rig_grp.resolve("surfaces"),
            parent=self.grp_rig,
        )

        self._init_layers()

        # Resolve default ctrl_size
        if ctrl_size_min is None or ctrl_size_max is None:
            val = self._get_default_ctrl_size()
            ctrl_size_max = val * 0.25
            ctrl_size_min = ctrl_size_max / float(len(self.layers))
            self.log.info(
                "Default ctrl size is adjusted from bettwen %s at %s",
                ctrl_size_min,
                ctrl_size_max,
            )

        self._build_layers(ctrl_size_max=ctrl_size_max, ctrl_size_min=ctrl_size_min)
        # Create a group that represent the original parent of everything.
        # This allow use to supported non-uniform scaling by using direct connections instead of parent/scaleConstraint.
        parent_obj = self.get_parent_obj()
        self._grp_parent = pymel.createNode(
            "transform",
            name=nomenclature_rig_grp.resolve("parent"),
            parent=self.grp_rig,
        )
        # Rig parenting
        if parent_obj:
            self._grp_parent.setMatrix(parent_obj.getMatrix(worldSpace=True))

        # For each influence, create a follicle that will follow the final mesh.
        unassigned_influences = self._get_unassigned_influences()
        last_surface = self.layers[-1].get_surface()

        if unassigned_influences and last_surface:
            grp_follicles = pymel.createNode(
                "transform",
                name=nomenclature_rig_grp.resolve("follicles"),
                parent=self.grp_rig,
            )

            for i, jnt in enumerate(unassigned_influences):
                nomenclature = nomenclature_jnt + self.rig.nomenclature(
                    jnt.stripNamespace().nodeName()
                )

                # Get the final LOCAL transformation of the influence.
                # If we have a parent, we'll want to convert it to WORLD transformation.
                pos = jnt.getTranslation(space="world")
                _, u, v = libRigging.get_closest_point_on_surface(last_surface, pos)
                fol_shape = libRigging.create_follicle(
                    last_surface, u, v, connect_transform=True
                )
                fol_transform = fol_shape.getParent()
                fol_transform.rename(nomenclature.resolve())
                fol_transform.setParent(grp_follicles)

                # Connect the influence.
                # Note that we don't apply any scale constraining since we assume that all influence have
                # the same common parent that drive the scale.
                if parent_obj:
                    # Use an extra object to match original influence transform.
                    grp_output = pymel.createNode(
                        "transform",
                        name=nomenclature_jnt.resolve("output%s" % i),
                        parent=self._grp_parent,
                    )
                    grp_output.setMatrix(
                        jnt.getMatrix(worldSpace=True), worldSpace=True
                    )
                    pymel.parentConstraint(
                        fol_transform, grp_output, maintainOffset=True
                    )

                    # Hack: Reset joint orient so our direct connection work...
                    # todo: use compose matrix?
                    if isinstance(jnt, pymel.nodetypes.Joint):
                        jnt.jointOrientX.set(0.0)
                        jnt.jointOrientY.set(0.0)
                        jnt.jointOrientZ.set(0.0)

                    libAttr.connect_transform_attrs(
                        grp_output, jnt, sx=False, sy=False, sz=False
                    )

                else:
                    pymel.parentConstraint(fol_transform, jnt, maintainOffset=True)

        # Manually parent the module with support for scaling.
        if parent_obj and parent_obj != self.grp_anm:
            pymel.parentConstraint(parent_obj, self.grp_anm, maintainOffset=True)
            pymel.scaleConstraint(parent_obj, self.grp_anm, maintainOffset=True)

    def unbuild(self):
        for layer in self.layers:
            if layer.is_built():
                layer.unbuild()

        super(InteractiveFK, self).unbuild()


def _get_surface_length(surface, u=1.0, v=1.0):
    attr_u, attr_v, util = libRigging.create_arclengthdimension_for_nurbsplane(
        surface, u=u, v=v
    )
    length_u = attr_u.get()
    length_v = attr_v.get()
    pymel.delete(util.getParent())
    return length_u, length_v


def register_plugin():
    return InteractiveFK
