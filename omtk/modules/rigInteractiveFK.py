from collections import defaultdict
import itertools
import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModuleMap import ModuleMap
from omtk.libs import libRigging
from omtk.libs import libHistory
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libAttr
from omtk.models.modelInteractiveCtrl import ModelInteractiveCtrl
from omtk.core.classModule import Module

# todo: add calibation!
# todo: support uniform scaling!

class InteractiveFKCtrl(BaseCtrl):
    pass


class InteractiveFKCtrlModel(ModelInteractiveCtrl):
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

    # def build(self, avar, parent_pos=None, parent_rot=None, parent_scl=None, follow_mesh=False, constraint=False, cancel_r=False, **kwargs):
    #     nomenclature_rig = self.get_nomenclature_rig()
    #
    #     pos_ref = self.jnt.getTranslation(space='world')
    #     tm_ref = pymel.datatypes.Matrix(
    #         1, 0, 0, 0,
    #         0, 1, 0, 0,
    #         0, 0, 1, 0,
    #         pos_ref.x, pos_ref.y, pos_ref.z, 1
    #     )
    #
    #     # Store the original position.
    #     grp_offset_name = nomenclature_rig.resolve('offset')
    #     grp_offset = pymel.createNode(
    #         'transform',
    #         name=grp_offset_name
    #     )
    #     grp_offset.setTranslation(pos_ref)
    #
    #     # Create a grp that follow the module parent.
    #     # We create the group even if we don't have any parent for easier further hacking.
    #     grp_parent = pymel.createNode(
    #         'transform',
    #         name=nomenclature_rig.resolve('parent'),
    #         parent=self.grp_rig
    #     )
    #     if self.parent:
    #         pymel.parentConstraint(self.parent, grp_parent, maintainOffset=True)
    #
    #     # Create two follicles, one for the position, one for the rotation.
    #     # The position follicle is on the farhest mesh in the construction history.
    #     # The rotation follicle is on the previous mesh in the construction history.
    #     meshes = libHistory.get_affected_shapes(self.jnt)
    #     ref_mesh, _, out_u, out_v = libRigging.get_closest_point_on_shapes(meshes, pos_ref)
    #
    #     if not ref_mesh:
    #         self.error("Can't find mesh for {0}. Abording".format(self))
    #         return
    #
    #     pos_mesh = libHistory.get_history_farthest_sibling(ref_mesh)
    #     if pos_mesh is None:
    #         pos_mesh = ref_mesh
    #     rot_mesh = libHistory.get_history_previous_sibling(ref_mesh)
    #
    #     pos_fol = None
    #     if pos_mesh:
    #         self.debug("Position parent will use follicle on {0} at {1},{2}.".format(
    #             pos_mesh, out_u, out_v
    #         ))
    #         pos_fol = libRigging.create_follicle2(pos_mesh, out_u, out_v).getParent()
    #         pos_fol.rename(nomenclature_rig.resolve('posFollicle'))
    #         #pos_fol.setParent(grp_parent)
    #
    #         parent_pos = pymel.createNode(
    #             'transform',
    #             name=nomenclature_rig.resolve('posLocal'),
    #             parent=grp_offset
    #         )
    #         pymel.parentConstraint(pos_fol, parent_pos, maintainOffset=True)
    #     else:
    #         # Should not happen
    #         raise Exception("Cannot resolve mesh for {0}".format(self))
    #
    #     # Resolve rot parent
    #     # If we found a previous mesh in the construction history, we'll follow it.
    #     # This will ensure proper behavior when handling multiples layers like on tentacle rigs.
    #     # Otherwise we'll constraint the rotation to the parent of the module itself.
    #     parent_rot = pymel.createNode(
    #         'transform',
    #         name=nomenclature_rig.resolve('rotLocal'),
    #         parent=grp_offset
    #     )
    #     if rot_mesh and rot_mesh != ref_mesh:
    #         self.debug("Rotation parent will use follicle on {0} at {1},{2}.".format(
    #             rot_mesh, out_u, out_v
    #         ))
    #         rot_fol = libRigging.create_follicle2(rot_mesh, out_u, out_v).getParent()
    #         rot_fol.rename(nomenclature_rig.resolve('rotFollicle'))
    #         rot_fol.setParent(grp_parent)
    #
    #
    #         pymel.parentConstraint(rot_fol, parent_rot, maintainOffset=True)
    #     else:
    #         self.debug("Rotation parent will use {0}".format(self.parent))
    #         if self.parent:
    #             pymel.parentConstraint(self.parent, parent_rot, maintainOffset=True)
    #
    #     # if parent_rot:
    #     #     pymel.parentConstraint(parent_rot, grp_parent, maintainOffset=True)
    #
    #     # todo: this call don't reach classModule.build, currently we'll connect the globalScale otherwise. However it might be a good idea to follow the rules.
    #     super(InteractiveFKCtrlModel, self).build(
    #         avar,
    #         ctrl_tm=tm_ref,
    #         parent_pos=parent_pos,
    #         parent_rot=parent_rot,
    #         parent_scl=parent_scl,
    #         follow_mesh=False,
    #         constraint=False,
    #         cancel_r=False,
    #         connect_global_scale=False,
    #         **kwargs
    #     )
    #
    #     # todo: This whole setup might be overkill.
    #     # Maybe use the skinCluster bindPreMatrix like in
    #     # https://github.com/fsanges/weightedRibbon/blob/master/core.py#L234
    #
    #     # Create a grp that contain the scale that we'll want to apply to the system.
    #     # This is currently only connected to the global scale.
    #     grp_scale = pymel.createNode(
    #         'transform',
    #         name=nomenclature_rig.resolve('scale'),
    #         parent=self.grp_rig
    #     )
    #     if self.parent:
    #         pymel.scaleConstraint(self.parent, grp_scale, maintainOffset=True)
    #
    #     #
    #     # Compute influence position
    #     # offsetTM * parentTM * inv(rotLocalTM) * ctrlLocalTM * rotLocalTM * scaleTM
    #     #
    #
    #     # Hack: Ensure the rotLocalTM is not affected by the global uniform scale.
    #     # This introduce lots of nodes, we might want to find a clearer way.
    #     attr_parent_rot_noscale_raw = libRigging.create_utility_node(
    #         'multMatrix',
    #         matrixIn=(
    #             parent_rot.worldMatrix,
    #             grp_scale.inverseMatrix
    #         )
    #     ).matrixSum
    #     util_decomposeMatrix_parent_rot_noscale = libRigging.create_utility_node(
    #         'decomposeMatrix',
    #         inputMatrix=attr_parent_rot_noscale_raw
    #     )
    #     attr_parent_rot_noscale = libRigging.create_utility_node(
    #         'composeMatrix',
    #         inputTranslate=util_decomposeMatrix_parent_rot_noscale.outputTranslate,
    #         inputRotate=util_decomposeMatrix_parent_rot_noscale.outputRotate
    #     ).outputMatrix
    #     attr_parent_rot_noscale_inv = libRigging.create_utility_node(
    #         'inverseMatrix',
    #         inputMatrix=attr_parent_rot_noscale,
    #     ).outputMatrix
    #
    #     # Hack: Ensure the parentTM is not affected by the global uniform scale.
    #     # This introduce lots of nodes, we might want to find a clearer way.
    #     attr_parent_noscale_raw = libRigging.create_utility_node(
    #         'multMatrix',
    #         matrixIn=(
    #             grp_parent.matrix,
    #             grp_scale.inverseMatrix
    #         )
    #     ).matrixSum
    #     util_decomposeMatrix_parent_noscale = libRigging.create_utility_node(
    #         'decomposeMatrix',
    #         inputMatrix=attr_parent_noscale_raw
    #     )
    #     attr_parent_noscale = libRigging.create_utility_node(
    #         'composeMatrix',
    #         inputTranslate=util_decomposeMatrix_parent_noscale.outputTranslate,
    #         inputRotate=util_decomposeMatrix_parent_noscale.outputRotate
    #     ).outputMatrix
    #     attr_parent_noscale_inv = libRigging.create_utility_node(
    #         'inverseMatrix',
    #         inputMatrix=attr_parent_noscale,
    #     ).outputMatrix
    #
    #     #
    #     # Hack: Ensure the ctrl local matrix is affected by the global scale.
    #     #
    #
    #     grp_output = pymel.createNode(
    #         'transform',
    #         name=nomenclature_rig.resolve('output'),
    #         parent=grp_parent
    #     )
    #     attr_inf_tm = libRigging.create_utility_node(
    #         'multMatrix',
    #         name=nomenclature_rig.resolve('getInfluenceLocalTM'),
    #         matrixIn=(
    #             grp_offset.matrix,  # already in worldSpace
    #             attr_parent_noscale,  # already in worldSpace
    #             attr_parent_rot_noscale_inv,  # temporary enter follicle space
    #             self.ctrl.matrix,  # local space
    #             attr_parent_rot_noscale,  # exit follicle space to world space
    #             attr_parent_noscale_inv,
    #             grp_scale.matrix  # already in worldSpace
    #         )
    #     ).matrixSum
    #     util_get_inf_tm = libRigging.create_utility_node(
    #         'decomposeMatrix',
    #         name=nomenclature_rig.resolve('decomposeInfluenceLocalTM'),
    #         inputMatrix=attr_inf_tm
    #     )
    #     pymel.connectAttr(util_get_inf_tm.outputTranslate, grp_output.t)
    #     pymel.connectAttr(util_get_inf_tm.outputRotate, grp_output.r)
    #     pymel.connectAttr(util_get_inf_tm.outputScale, grp_output.s)
    #     pymel.parentConstraint(grp_output, self.jnt, maintainOffset=True)
    #     pymel.scaleConstraint(grp_output, self.jnt)
    #
    #
    #     # Cleanup
    #     if pos_fol:
    #         pos_fol.setParent(self.grp_rig)
    #     grp_offset.setParent(self.grp_rig)
    #     grp_parent.setParent(self.grp_rig)
    #     self.grp_rig.setParent(avar.grp_rig)


class InteractiveFKLayer(ModuleMap):
    _CLS_CTRL_MODEL = InteractiveFKCtrlModel
    _CLS_CTRL = InteractiveFKCtrl

    # @libPython.memoized_instancemethod
    # def _get_parent(self):
    #     """
    #     Find the highest parent-level common parent to ALL the influences.
    #     This is necessary since we cannot handle different parent for each layers since
    #     the deformation is piped via blendshape.
    #     :return: A pymel.PyNode instance to use as parent.
    #     """
    #     parent_sets = None
    #     for jnt in self.jnts:
    #         parent_set = set(libPymel.get_parents(jnt))
    #         print parent_set
    #         if parent_sets is None:
    #             parent_sets = parent_set
    #         else:
    #             parent_sets &= parent_set
    #     if not parent_sets:
    #         return None
    #
    #     common_parent = next(iter(reversed(sorted(parent_sets, key=libPymel.get_num_parents))), None)
    #     return common_parent

    # def validate(self):
    #     # Ensure that all influences have a common parent for proprer scale handling.
    #     if not self._get_parent():
    #         raise Exception("Found no common parents for inputs.")
    #
    #     super(InteractiveFK, self).validate()

    # def build_models(self, **kwargs):
    #     # Since all layers are blendshaped into each others, we don't
    #     # want to propagate any scale from one system to another, at least
    #     # not from the influence. However the ctrls will still get affected
    #     # and for this reason, we'll need to ensure all layers daisy-chain
    #     # their scale to each others.
    #     nomenclature_rig = self.get_nomenclature_rig()
    #
    #     # Group inputs by their associated mesh.
    #     meshes_by_input = defaultdict(list)
    #     for jnt in self.jnts:
    #         meshes = libHistory.get_affected_shapes(self.jnt)
    #         mesh = next(iter(meshes), None)
    #         meshes_by_input[mesh].append(jnt)
    #
    #     # todo: sort meshes?
    #
    #     # Resolve scale matrix for each models.
    #     models_scale_tms = []
    #     for model in self.models:
    #         util_decompose_world_tm = libRigging.create_utility_node(
    #             'decomposeMatrix',
    #             inputMatrix=model.parent.worldMatrix
    #         )
    #         attr_get_scale_tm = libRigging.create_utility_node(
    #             'composeMatrix',
    #             inputScale=util_decompose_world_tm.outputScale
    #         ).outputMatrix
    #         models_scale_tms.append(attr_get_scale_tm)
    #
    #     # For each models, resolve their effective scale.
    #     models_scale_grps = []
    #     for i, model in enumerate(self.models):
    #         scale_tms = models_scale_tms[:i+1]
    #         attr_total_scale_tm = libRigging.create_utility_node(
    #             'multMatrix',
    #             matrixIn=scale_tms
    #         ).matrixSum
    #         util_composeMatrix = libRigging.create_utility_node(
    #             'decomposeMatrix',
    #             inputMatrix=attr_total_scale_tm
    #         )
    #         grp_scale = pymel.createNode(
    #             'transform',
    #             name=nomenclature_rig.resolve('scaleLayer{}'.format(i)),
    #             parent=self.grp_rig
    #         )
    #         pymel.connectAttr(util_composeMatrix.outputTranslate, grp_scale.t)
    #         pymel.connectAttr(util_composeMatrix.outputRotate, grp_scale.r)
    #         pymel.connectAttr(util_composeMatrix.outputScale, grp_scale.s)
    #
    #     for model, scale_grp in zip(self.models, models_scale_grps):
    #         self.build_model(
    #             model,
    #             parent_scl=scale_grp,
    #             **kwargs
    #         )

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

    def build_model(self, model, obj_mesh=None, **kwargs):
        super(InteractiveFKLayer, self).build_model(
            model,
            obj_mesh=self.get_surface(),
            **kwargs)

        nomenclature_rig = self.get_nomenclature_rig()

        offset = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('offset'),
            parent=self.grp_rig
        )
        offset.setMatrix(model.jnt.getMatrix(worldSpace=True), worldSpace=True)
        model.jnt.setParent(offset)
        # print model.ctrl.node, model.jnt
        libAttr.connect_transform_attrs(model.ctrl.node, model.jnt)


class InteractiveFK(Module):
    _CLS_LAYER = InteractiveFKLayer
    SHOW_IN_UI = False

    def __init__(self, *args, **kwargs):
        super(InteractiveFK, self).__init__(*args, **kwargs)

        # This will contain all the layers that take part in the system.
        self.layers = []

        # The preSurface define the 'bind' pose of the system.
        self.preSurface = None

        # The postSurface define the 'final' shape of the system and inherit any scale.
        self.postSurface = None

    def validate(self):
        super(InteractiveFK, self).validate()

        if not self.get_surface():
            raise Exception("Missing required input of type NurbsSurface")

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

    def create_layer_from_surface(self, num_u=3, num_v=1, min_u=0.0, max_u=1.0, min_v=0.0, max_v=1.0, format_str='U{:02d}V{:02d}', suffix=None):
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
        return module

    def create_layer_from_inputs(self, inputs, suffix=None):
        """
        Initialize a new deformation layer at the end of the stack.
        Please use this function before calling build().
        :param inputs: Inputs for the new layer. Should normally contain joints and one surface.
        :param suffix: The suffix to use for naming purposes.
        :return:
        """
        layer = self.init_module(self._CLS_LAYER, None, inputs=inputs, suffix=suffix)
        return layer

    def _init_layers(self):
        """
        Initialize any preset of layer configuration.
        Override this if you define a custom Module from this one.
        """
        pass

    def _build_layers(self, ctrl_size_max=None, ctrl_size_min=None):
        num_layers = len(self.layers)
        for i, layer in enumerate(self.layers):
            ratio = float(i) / (num_layers - 1) if num_layers > 1 else 1
            ctrl_size = libRigging.interp_linear(ratio, ctrl_size_max, ctrl_size_min) if ctrl_size_max and ctrl_size_min else None

            layer.build(ctrl_size=ctrl_size)
            layer.grp_anm.setParent(self.grp_anm)
            layer.grp_rig.setParent(self.grp_rig)

    def _create_surface(self, parent=None, name=None, **kwargs):
        """
        Create a new surface for layer user.
        The resulting surface will be 'safe' to use with no scale or locked attributes.
        :param kwargs:
        :return:
        """
        ref_surface = self.get_surface()
        new_surface = pymel.duplicate(ref_surface, **kwargs)[0]
        if parent:
            new_surface.setParent(parent)
        if name:
            new_surface.rename(name)
        libAttr.unlock_trs(new_surface)
        pymel.makeIdentity(new_surface, apply=True, scale=True)
        return new_surface

    def build(self, ctrl_size_max=10, ctrl_size_min=5, parent=True, **kwargs):
        """
        :param ctrl_size_max: Used to automatically size layer ctrls. Define the maximum size (applied on first layer)
        :param ctrl_size_min: Used to automatically size layer ctrls. Define the minimum size (applied on last layer)
        :param parent: Redefined to compensate for bad design. Identicall implementation than base class.
        :param kwargs: Any keyword argument will be forwarded to the base method.
        """
        super(InteractiveFK, self).build(parent=None, **kwargs)

        nomenclature_rig = self.get_nomenclature_rig()
        nomenclature_rig_grp = self.get_nomenclature_rig_grp()
        nomenclature_jnt = self.get_nomenclature_jnt()

        grp_surfaces = pymel.createNode(
            'transform',
            name=nomenclature_rig_grp.resolve('surfaces'),
            parent=self.grp_rig
        )

        # Create the 'preSurface'
        # This will serve as reference for ulterior surfaces.
        # Note that we try to 're-use' the provided surface in
        self.preSurface = self._create_surface(
            name=nomenclature_rig.resolve('preSurface'),
            parent=grp_surfaces
        )

        # Create the 'postSurface'
        # We ensure the 'postSurface' will be scaled by the parent.
        self.postSurface = self._create_surface(
            name=nomenclature_rig.resolve('postSurface'),
            parent=grp_surfaces
        )

        # For each influence, create a follicle that will follow the final mesh.
        grp_follicles = pymel.createNode(
            'transform',
            name=nomenclature_rig_grp.resolve('follicles'),
            parent=self.grp_rig,
        )
        out_follicles = []
        for jnt in self.jnts:
            nomenclature = nomenclature_jnt + self.rig.nomenclature(jnt.nodeName())
            _, u, v = libRigging.get_closest_point_on_surface(self.preSurface, jnt.getTranslation(space='world'))
            fol_shape = libRigging.create_follicle2(self.postSurface, u, v, connect_transform=True)
            fol_transform = fol_shape.getParent()
            fol_transform.rename(nomenclature.resolve())
            fol_transform.setParent(grp_follicles)
            if self.parent:
                pymel.scaleConstraint(self.parent, fol_transform)
            out_follicles.append(fol_transform)

        # Constraint the influence to the final layer follicles.
        for jnt, fol in zip(self.jnts, out_follicles):
            pymel.parentConstraint(fol, jnt, maintainOffset=True)
            pymel.scaleConstraint(fol, jnt)

        self._init_layers()
        self._build_layers(
            ctrl_size_max=ctrl_size_max,
            ctrl_size_min=ctrl_size_min
        )

        # Blendshape each layers together.
        all_surfaces = [self.preSurface] + [layer.get_surface() for layer in self.layers] + [self.postSurface]
        for a, b in itertools.izip(all_surfaces[:-1], all_surfaces[1:]):
            pymel.blendShape(a, b, w=[0, 1], frontOfChain=True)

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