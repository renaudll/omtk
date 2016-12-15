from collections import defaultdict
import itertools
import pymel.core as pymel
from omtk.core.classNode import Node
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModuleMap import ModuleMap
from omtk.core.classModule import Module
from omtk.core import classCtrlModel
from omtk.libs import libRigging
from omtk.libs import libAttr
from omtk.libs import libPython
from omtk.libs import libHistory

# todo: add calibation!
# todo: support uniform scaling!

def _get_immediate_skincluster(transform):
    # Ensure we deal with a transform.
    if isinstance(transform, pymel.nodetypes.Shape):
        transform = transform.getParent()

    all_shapes = transform.getShapes()
    skinclusters = [hist for hist in transform.listHistory() if isinstance(hist, pymel.nodetypes.SkinCluster)]
    for skincluster in skinclusters:
        for attr_output in skincluster.outputGeometry:
            next_shape = next(iter(hist for hist in attr_output.listHistory(future=True) if
                                   isinstance(hist, pymel.nodetypes.Shape)), None)
            if next_shape in all_shapes:
                return skincluster


class InteractiveFKCtrl(BaseCtrl):
    pass


class InteractiveFKCtrlModel(classCtrlModel.CtrlModelCalibratable):
    """
    This module allow the controller to follow a follicle and
    hijack the influence skinCluster to only consider the local space.
    """
    DEFAULT_NAME_USE_FIRST_INPUT = True

    def get_default_tm_ctrl(self):
        pos_ref = self.jnt.getTranslation(space='world')
        tm_ref = pymel.datatypes.Matrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            pos_ref.x, pos_ref.y, pos_ref.z, 1
        )
        return tm_ref

    def __init__(self, *args, **kwargs):
        super(InteractiveFKCtrlModel, self).__init__(*args, **kwargs)

        self.follicle = None

        self._stack = None
        self._layer_bind = None

    def _get_calibration_reference(self):
        return self.follicle

    @libPython.memoized_instancemethod
    def get_bind_tm(self):
        """
        :return: The ctrl transformation that will be used to determine the position of the follicle.
        """
        if self.jnt is None:
            self.warning("Cannot resolve ctrl matrix with no inputs!")
            return None

        tm = self.jnt.getMatrix(worldSpace=True)
        return tm

    @libPython.memoized_instancemethod
    def get_bind_pos(self):
        return self.get_bind_tm().translate

    @libPython.memoized_instancemethod
    def get_default_shape(self):
        # If a surface we provided in the inputs, use it.
        surface = self.get_surface()
        if surface:
            return surface

        # We'll scan all available geometries and use the one with the shortest distance.
        meshes = libHistory.get_affected_shapes(self.jnt)
        meshes = list(set(meshes) & set(self.rig.get_shapes()))
        return next(iter(meshes), None)

    def build(self, parent, create_follicle=True, pos=None, shape=None, shape_next=None, u_coord=None, v_coord=None,
              constraint=True, **kwargs):
        """
        :param pos: The position to use when seeking where to create the follicle. Can be resolved automatically if the module have an influence.
        :param shape: The shape to create the follicle on. Can be resolved automatically if the module have an influence.
        :param u_coord: The U coordinate to use for the follicle. Can be resolved automatically if the module have an influence.
        :param v_coord: The V coordinate to use for the follicle. Can be resolved automatically if the module have an influence.
        :param constraint: If True, the ctrl will drive the influence via direct connect.
        :param kwargs: Any additional keyword argument will be passed to the parent method.
        """
        super(InteractiveFKCtrlModel, self).build(parent, **kwargs)

        nomenclature_rig = self.get_nomenclature_rig()

        # Resolve bind position.
        if pos is None:
            pos = self.get_bind_pos()

        #
        # Create the 'bind' node that will follow the follicle in translation and something else in rotation.
        #

        # Initialize external stack
        # Normally this would be hidden from animators.
        stack_name = nomenclature_rig.resolve('stack')
        self._stack = Node(self)
        self._stack.build(name=stack_name)
        self._stack.setTranslation(pos)

        # Create the layer_fol that will follow the geometry
        layer_fol_name = nomenclature_rig.resolve('bind')
        self._layer_bind = self._stack.append_layer()
        self._layer_bind.rename(layer_fol_name)
        self._layer_bind.setMatrix(self.get_bind_tm())
        self._layer_bind.setParent(self.grp_rig)

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

            fol_shape = libRigging.create_follicle2(shape, u=u_coord, v=v_coord)
            ref_before = fol_shape.getParent()
            ref_before.rename(nomenclature_rig.resolve('preCtrl'))
            ref_before.setParent(self.grp_rig)
        else:
            ref_before = pymel.createNode(
                'transform',
                name=nomenclature_rig.resolve('preCtrl'),
                parent=self.grp_rig
            )
            ref_before.setMatrix(self.get_bind_tm())

        pymel.parentConstraint(ref_before, self._layer_bind, maintainOffset=True)

        # Create follicle to track the transfort AFTER the ctrl.
        # This will be used to position the controller correctly.
        if shape_next:
            # Resolve uv coords if necessary
            _, u_coord, v_coord = libRigging.get_closest_point_on_shape(shape_next, pos)
            if u_coord is None or v_coord is None:
                raise Exception("Can't resolve uv coordinates to use!")

            fol_shape = libRigging.create_follicle2(shape_next, u=u_coord, v=v_coord)
            ref_after = fol_shape.getParent()
            ref_after.rename(nomenclature_rig.resolve('postCtrl'))
            ref_after.setParent(self.grp_rig)
            print ref_after, pos

            self.follicle = ref_after

        #
        # Constraint grp_anm
        #

        # Create an output object that will hold the world position of the ctrl offset.
        # This allow us to create direct connection which simplify the dag tree for the animator
        # and allow us to easily scale the whole setup to support non-uniform scaling.

        pymel.connectAttr(self._layer_bind.tx, self.ctrl.offset.tx)
        pymel.connectAttr(self._layer_bind.ty, self.ctrl.offset.ty)
        pymel.connectAttr(self._layer_bind.tz, self.ctrl.offset.tz)
        pymel.connectAttr(self._layer_bind.rx, self.ctrl.offset.rx)
        pymel.connectAttr(self._layer_bind.ry, self.ctrl.offset.ry)
        pymel.connectAttr(self._layer_bind.rz, self.ctrl.offset.rz)

        # Constraint
        if constraint:
            #
            # Compute influence position
            # offsetTM * inv(rotLocalTM) * ctrlLocalTM * rotLocalTM * scaleTM
            #

            # Bypass cyclic-dependency by using an offet node.
            grp_offset = pymel.createNode(
                'transform',
                name=nomenclature_rig.resolve('offset'),
                parent=self.grp_rig
            )
            grp_offset.setMatrix(self.get_bind_tm())
            grp_output = pymel.createNode(
                'transform',
                name=nomenclature_rig.resolve('output'),
                parent=self.grp_rig
            )

            attr_get_tm = libRigging.create_utility_node(
                'multMatrix',
                name=nomenclature_rig.resolve('computeWorldDelta'),
                matrixIn=(
                    grp_offset.matrix,
                    self._layer_bind.inverseMatrix,
                    self.ctrl.node.matrix,
                    self._layer_bind.matrix
                )
            ).matrixSum

            util_decompose_tm = libRigging.create_utility_node(
                'decomposeMatrix',
                name=nomenclature_rig.resolve('decomposeWorldDelta'),
                inputMatrix=attr_get_tm
            )

            pymel.connectAttr(util_decompose_tm.outputTranslate, grp_output.translate)
            pymel.connectAttr(util_decompose_tm.outputRotate, grp_output.rotate)
            pymel.connectAttr(util_decompose_tm.outputScale, grp_output.scale)

            pymel.parentConstraint(grp_output, self.jnt)
            pymel.scaleConstraint(grp_output, self.jnt)


class InteractiveFKLayer(ModuleMap):
    _CLS_CTRL_MODEL = InteractiveFKCtrlModel
    _CLS_CTRL = InteractiveFKCtrl

    def init_model(self, model, inputs, **kwargs):
        """
        Ensure the surface is present in the inputs.
        """
        surface = self.get_surface()
        if not surface:
            raise Exception("Expected surface in inputs.")
        if not surface in inputs:
            inputs.append(surface)

        return super(InteractiveFKLayer, self).init_model(model, inputs, **kwargs)

    def build(self, parent=None, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig()

        super(InteractiveFKLayer, self).build(**kwargs)

        # Handle scale
        # There can be other layers influenced by this one so we don't want to apply it on the influences directly.
        # A hacky way is to scale the nurbs surface.
        grp_surface = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('surface'),
            parent=self.grp_rig
        )
        for surface in self.get_surfaces():
            surface.setParent(
                grp_surface
            )

        # Connect to parent
        if parent is None:
            parent = self.parent
        if parent:
            pymel.scaleConstraint(self.parent, grp_surface)

    def build_models(self, calibrate=True, **kwargs):
        for model in self.models:
            self.build_model(
                model,
                **kwargs
            )
            if calibrate:
                model.calibrate()


class InteractiveFK(Module):
    _CLS_LAYER = InteractiveFKLayer

    def __init__(self, *args, **kwargs):
        super(InteractiveFK, self).__init__(*args, **kwargs)

        # This will contain all the layers that take part in the system.
        self.layers = []

        # # The preSurface define the 'bind' pose of the system.
        # self.preSurface = None
        #
        # The postSurface define the 'final' shape of the system and inherit any scale.
        self.postSurface = None

    def validate(self, epsilon=0.001):
        super(InteractiveFK, self).validate()

        surfaces = self.get_surfaces()
        if not surfaces:
            raise Exception("Missing required input of type NurbsSurface")

        # Ensure there's no useless surface in the inputs.
        unassigned_surfaces = self._get_unassigned_surfaces()
        if unassigned_surfaces:
            raise Exception("Useless surface(s) found: {}".format(','.join((surface for surface in unassigned_surfaces))))

        # todo: Ensure all surface have an identity matrix
        attr_to_check = {
            'translateX': 0.0,
            'translateY': 0.0,
            'translateZ': 0.0,
            'rotateX': 0.0,
            'rotateY': 0.0,
            'rotateZ': 0.0,
            'scaleX': 1.0,
            'scaleY': 1.0,
            'scaleZ': 1.0,
        }
        for surface in surfaces:
            for attr_name, desired_val in attr_to_check.iteritems():
                attr = surface.attr(attr_name)
                attr_val = attr.get()
                if abs(attr_val - desired_val) > epsilon:
                    raise Exception("Surface {} have invalid transform! Expected {} for {}, got {}.".format(surface, desired_val, attr_name, attr_val))

        # Ensure all provided surfaces have the same cv count.
        # num_cvs = None
        # for surface in surfaces:
        #     cur_num_cvs = len(surface.cv)
        #     if num_cvs is None:
        #         num_cvs = cur_num_cvs
        #     elif cur_num_cvs != num_cvs:
        #         raise Exception("Not all input NurbsSurface have the same cv count!")

    @libPython.memoized_instancemethod
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
        surfaces = [surface.getShape(noIntermediate=True) if isinstance(surface, pymel.nodetypes.Transform) else surface for surface in surfaces]

        # Sort the surface by their construction history.
        # If the surface are already blendshaped toguether, this will work.
        def _fn_compare(obj_a, obj_b):
            hist_a = [hist for hist in obj_a.listHistory() if isinstance(hist, pymel.nodetypes.Shape)]
            hist_b = [hist for hist in obj_b.listHistory() if isinstance(hist, pymel.nodetypes.Shape)]
            if obj_b in hist_a:
                return 1
            elif obj_a in hist_b:
                return -1
            # If nothing works, compare their name...
            # We might get lucky and have correctly named objects like layer0, layer1, etc.
            self.warning("Saw no relationship between {} and {}. Will sort them by name.".format(obj_a, obj_b))
            return cmp(obj_a.name(), obj_b.name())
        surfaces = sorted(surfaces, cmp=_fn_compare)

        for surface in surfaces:
            skincluster = _get_immediate_skincluster(surface)
            if not skincluster:
                self.warning("Found no skinCluster for {}".format(surface))
                continue

            cur_influences = set(skincluster.influenceObjects())
            cur_jnts = list(jnts & cur_influences)
            unassigned_jnts -= cur_influences

            result.append(
                (surface.getParent(), cur_jnts)
            )

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
        return list(surfaces)

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
                ratio = (u_index / float(num_u-1))
                u = libRigging.interp_linear(ratio, min_u, max_u)
            else:
                u = 0.5
            for v_index in range(num_v):
                if num_v > 1:
                    ratio = (v_index / float(num_v-1))
                    v = libRigging.interp_linear(ratio, min_v, max_v)
                else:
                    v = 0.5
                yield u_index, v_index, u, v

    def create_layer_from_surface(self, num_u=3, num_v=1, min_u=0.0, max_u=1.0, min_v=0.0, max_v=1.0, format_str='U{:02d}V{:02d}', cls_ctrl=None, suffix=None):
        """
        Create a new layer module by duplicating the reference surface and generating influences using predefined rules.
        Note that this does not add it to the layer stack.
        :param num_u: How much influences to generate in the surface U space.
        :param num_v: How much influences to generate in the surface U space.
        :param format_str: An str instance that drive how the influence are named using python string formattingmechanismm.
        :param suffix: The suffix to add to the moduel name.
        :return: An instance of the module class defined in self._CLS_LAYER.
        """
        # Create the module first so we can access it's nomenclature.
        # We'll add the inputs afterward.
        module = self.init_module(self._CLS_LAYER, None, suffix=suffix)

        nomenclature_jnt = module.get_nomenclature_jnt()
        nomenclature_rig = module.get_nomenclature_rig()

        # Create surface
        surface = self._create_surface(
            name=nomenclature_rig.resolve('surface')
        )

        # Create influences
        jnts = []
        for u_index, v_index, u_coord, v_coord in self.iter_uvs(num_u, num_v, min_u=min_u, max_u=max_u, min_v=min_v, max_v=max_v):
            pos = libRigging.get_point_on_surface_from_uv(surface, u_coord, v_coord)
            jnt = pymel.createNode(
                'joint',
                name=nomenclature_jnt.resolve(format_str.format(u_index, v_index))
            )
            jnt.setTranslation(pos)
            jnts.append(jnt)

        # Assign a skinCluster on the surface using the influences.
        pymel.skinCluster(jnts, surface, mi=3)

        # Assign inputs and return module
        module.input = jnts + [surface]
        if cls_ctrl:
            module._CLS_CTRL = cls_ctrl

        return module

    def init_layer(self, inst, inputs=None, suffix=None, cls_layer=None, cls_ctrl=None):
        cls_layer = cls_layer or self._CLS_LAYER
        layer = self.init_module(cls_layer, inst, inputs=inputs, suffix=suffix)
        if cls_ctrl:
            layer._CLS_CTRL = cls_ctrl
        return layer

    def _init_layers(self):
        """
        Initialize any preset of layer configuration.
        Override this if you define a custom Module from this one.
        """
        # Build layers from inputs.
        data = self.get_influences_by_surfaces()

        # Ensure we have at least as many slots allocated that we have groups.
        num_layers = len(self.layers)
        if num_layers < len(data):
            libPython.resize_list(self.layers, num_layers)

        self.debug('Found {} layer groups'.format(len(data)))
        for i, sub_data in enumerate(data):
            self.debug('Creating layer {} using {}'.format(i + 1, sub_data))
            surface, influences = sub_data
            self.layers[i] = self.init_layer(self.layers[i], inputs=[surface] + influences, suffix='layer{}'.format(i + 1))

    def _build_layers(self, ctrl_size_max=None, ctrl_size_min=None):
        nomenclature_rig = self.get_nomenclature_rig()

        layers = self.layers
        num_layers = len(layers)

        for i in range(num_layers):
            prev_layer = layers[i-1] if i > 0 else None
            curr_layer = layers[i]

            # Define desired ctrl size
            ratio = float(i) / (num_layers - 1) if num_layers > 1 else 1
            ctrl_size = libRigging.interp_linear(ratio, ctrl_size_max, ctrl_size_min) if ctrl_size_max and ctrl_size_min else None

            shape = prev_layer.get_surface() if prev_layer else None
            shape_skinned = curr_layer.get_surface()
            create_follicle = True if prev_layer else None
            curr_layer.build(
                create_follicle=create_follicle,
                shape=shape,
                shape_next=shape_skinned,
                ctrl_size=ctrl_size,
            )
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
        length_u, length_v = libRigging.get_surface_length(surface)
        return min(length_u, length_v)

    def build(self, ctrl_size_max=None, ctrl_size_min=None, parent=True, **kwargs):
        """
        :param ctrl_size_max: Used to automatically size layer ctrls. Define the maximum size (applied on first layer)
        :param ctrl_size_min: Used to automatically size layer ctrls. Define the minimum size (applied on last layer)
        :param parent: Redefined to compensate for bad design. Identicall implementation than base class.
        :param kwargs: Any keyword argument will be forwarded to the base method.
        """
        super(InteractiveFK, self).build(parent=None, **kwargs)

        self._init_layers()



        # Resolve default ctrl_size
        if ctrl_size_min is None or ctrl_size_max is None:
            val = self._get_default_ctrl_size()
            ctrl_size_max = val * 0.1
            ctrl_size_min = ctrl_size_max / float(len(self.layers))
            self.info('Default ctrl size is adjusted from bettwen {} at {}'.format(ctrl_size_min, ctrl_size_max))

        nomenclature_rig = self.get_nomenclature_rig()
        nomenclature_rig_grp = self.get_nomenclature_rig_grp()
        nomenclature_jnt = self.get_nomenclature_jnt()

        grp_surfaces = pymel.createNode(
            'transform',
            name=nomenclature_rig_grp.resolve('surfaces'),
            parent=self.grp_rig
        )

        # # Create the 'preSurface'
        # # This will serve as reference for ulterior surfaces.
        # # Note that we try to 're-use' the provided surface in
        # self.preSurface = self._create_surface(
        #     name=nomenclature_rig.resolve('preSurface'),
        #     parent=grp_surfaces
        # )

        # Create the 'postSurface'
        # We ensure the 'postSurface' will be scaled by the parent.
        last_surface = self.layers[-1].get_surface()
        self.postSurface = self._create_surface(
            ref_surface=last_surface,  # todo: resolve correctly the last surface
            name=nomenclature_rig.resolve('postSurface'),
            parent=grp_surfaces
        )
        pymel.blendShape(last_surface, self.postSurface, w=[0, 1], frontOfChain=True)



        self._build_layers(
            ctrl_size_max=ctrl_size_max,
            ctrl_size_min=ctrl_size_min
        )

        # Blendshape each layers together.
        # all_surfaces = [self.preSurface] + [layer.get_surface() for layer in self.layers] + [self.postSurface]
        # pymel.blendShape(self.layers[-1].get_surface(), self.postSurface, w=[0, 1], frontOfChain=True)


        # For each influence, create a follicle that will follow the final mesh.
        grp_follicles = pymel.createNode(
            'transform',
            name=nomenclature_rig_grp.resolve('follicles'),
            parent=self.grp_rig,
        )
        unassigned_influences = self._get_unassigned_influences()
        for jnt in unassigned_influences:
            nomenclature = nomenclature_jnt + self.rig.nomenclature(jnt.nodeName())
            pos = jnt.getTranslation(space='world')
            _, u, v = libRigging.get_closest_point_on_surface(self.postSurface, pos)
            fol_shape = libRigging.create_follicle2(self.postSurface, u, v, connect_transform=True)
            fol_transform = fol_shape.getParent()
            fol_transform.rename(nomenclature.resolve())
            fol_transform.setParent(grp_follicles)

            pymel.parentConstraint(fol_transform, jnt, maintainOffset=True)
            if self.parent:
                pymel.scaleConstraint(self.parent, jnt)

        # # Blendshape each layers together.
        # all_surfaces = [self.preSurface] + [layer.get_surface() for layer in self.layers] + [self.postSurface]
        # for a, b in itertools.izip(all_surfaces[:-1], all_surfaces[1:]):
        #     pymel.blendShape(a, b, w=[0, 1], frontOfChain=True)

        # Manually parent the module with support for scaling.
        if parent and self.parent:
            self.parent_to(self.parent)

    def parent_to(self, parent):
        pymel.parentConstraint(parent, self.postSurface, maintainOffset=True)
        pymel.scaleConstraint(parent, self.postSurface, maintainOffset=True)
        # Same thing for self.grp_anm by use direct connection to keep the anim dag tree clean.
        libAttr.connect_transform_attrs(self.postSurface, self.grp_anm)




def register_plugin():
    return InteractiveFK