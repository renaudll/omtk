from collections import defaultdict
import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModuleMap import ModuleMap
from omtk.libs import libRigging
from omtk.libs import libHistory
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.models.modelInteractiveCtrl import ModelInteractiveCtrl

# todo: add calibation!
# todo: support uniform scaling!

class InteractiveFKCtrl(BaseCtrl):
    pass


class InteractiveFKCtrlModel(ModelInteractiveCtrl):
    DEFAULT_NAME_USE_FIRST_INPUT = True

    def build(self, avar, parent_pos=None, parent_rot=None, parent_scl=None, follow_mesh=False, constraint=False, cancel_r=False, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig()

        pos_ref = self.jnt.getTranslation(space='world')
        tm_ref = pymel.datatypes.Matrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            pos_ref.x, pos_ref.y, pos_ref.z, 1
        )

        # Store the original position.
        grp_offset_name = nomenclature_rig.resolve('offset')
        grp_offset = pymel.createNode(
            'transform',
            name=grp_offset_name
        )
        grp_offset.setTranslation(pos_ref)

        # Create a grp that follow the module parent.
        # We create the group even if we don't have any parent for easier further hacking.
        grp_parent = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('parent'),
            parent=self.grp_rig
        )
        if self.parent:
            pymel.parentConstraint(self.parent, grp_parent, maintainOffset=True)

        # Create two follicles, one for the position, one for the rotation.
        # The position follicle is on the farhest mesh in the construction history.
        # The rotation follicle is on the previous mesh in the construction history.
        meshes = libHistory.get_affected_shapes(self.jnt)
        ref_mesh, _, out_u, out_v = libRigging.get_closest_point_on_shapes(meshes, pos_ref)

        if not ref_mesh:
            self.error("Can't find mesh for {0}. Abording".format(self))
            return

        pos_mesh = libHistory.get_history_farthest_sibling(ref_mesh)
        if pos_mesh is None:
            pos_mesh = ref_mesh
        rot_mesh = libHistory.get_history_previous_sibling(ref_mesh)

        pos_fol = None
        if pos_mesh:
            self.debug("Position parent will use follicle on {0} at {1},{2}.".format(
                pos_mesh, out_u, out_v
            ))
            pos_fol = libRigging.create_follicle2(pos_mesh, out_u, out_v).getParent()
            pos_fol.rename(nomenclature_rig.resolve('posFollicle'))
            #pos_fol.setParent(grp_parent)

            parent_pos = pymel.createNode(
                'transform',
                name=nomenclature_rig.resolve('posLocal'),
                parent=grp_offset
            )
            pymel.parentConstraint(pos_fol, parent_pos, maintainOffset=True)
        else:
            # Should not happen
            raise Exception("Cannot resolve mesh for {0}".format(self))

        # Resolve rot parent
        # If we found a previous mesh in the construction history, we'll follow it.
        # This will ensure proper behavior when handling multiples layers like on tentacle rigs.
        # Otherwise we'll constraint the rotation to the parent of the module itself.
        parent_rot = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('rotLocal'),
            parent=grp_offset
        )
        if rot_mesh and rot_mesh != ref_mesh:
            self.debug("Rotation parent will use follicle on {0} at {1},{2}.".format(
                rot_mesh, out_u, out_v
            ))
            rot_fol = libRigging.create_follicle2(rot_mesh, out_u, out_v).getParent()
            rot_fol.rename(nomenclature_rig.resolve('rotFollicle'))
            rot_fol.setParent(grp_parent)


            pymel.parentConstraint(rot_fol, parent_rot, maintainOffset=True)
        else:
            self.debug("Rotation parent will use {0}".format(self.parent))
            if self.parent:
                pymel.parentConstraint(self.parent, parent_rot, maintainOffset=True)

        # if parent_rot:
        #     pymel.parentConstraint(parent_rot, grp_parent, maintainOffset=True)

        # todo: this call don't reach classModule.build, currently we'll connect the globalScale otherwise. However it might be a good idea to follow the rules.
        super(InteractiveFKCtrlModel, self).build(
            avar,
            ctrl_tm=tm_ref,
            parent_pos=parent_pos,
            parent_rot=parent_rot,
            parent_scl=parent_scl,
            follow_mesh=False,
            constraint=False,
            cancel_r=False,
            connect_global_scale=False,
            **kwargs
        )

        # Create a grp that contain the scale that we'll want to apply to the system.
        # This is currently only connected to the global scale.
        grp_scale = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('scale'),
            parent=self.grp_rig
        )
        if self.parent:
            pymel.scaleConstraint(self.parent, grp_scale, maintainOffset=True)

        #
        # Compute influence position
        # offsetTM * parentTM * inv(rotLocalTM) * ctrlLocalTM * rotLocalTM * scaleTM
        #

        # Hack: Ensure the rotLocalTM is not affected by the global uniform scale.
        # This introduce lots of nodes, we might want to find a clearer way.
        attr_parent_rot_noscale_raw = libRigging.create_utility_node(
            'multMatrix',
            matrixIn=(
                parent_rot.worldMatrix,
                grp_scale.inverseMatrix
            )
        ).matrixSum
        util_decomposeMatrix_parent_rot_noscale = libRigging.create_utility_node(
            'decomposeMatrix',
            inputMatrix=attr_parent_rot_noscale_raw
        )
        attr_parent_rot_noscale = libRigging.create_utility_node(
            'composeMatrix',
            inputTranslate=util_decomposeMatrix_parent_rot_noscale.outputTranslate,
            inputRotate=util_decomposeMatrix_parent_rot_noscale.outputRotate
        ).outputMatrix
        attr_parent_rot_noscale_inv = libRigging.create_utility_node(
            'inverseMatrix',
            inputMatrix=attr_parent_rot_noscale,
        ).outputMatrix

        # Hack: Ensure the parentTM is not affected by the global uniform scale.
        # This introduce lots of nodes, we might want to find a clearer way.
        attr_parent_noscale_raw = libRigging.create_utility_node(
            'multMatrix',
            matrixIn=(
                grp_parent.matrix,
                grp_scale.inverseMatrix
            )
        ).matrixSum
        util_decomposeMatrix_parent_noscale = libRigging.create_utility_node(
            'decomposeMatrix',
            inputMatrix=attr_parent_noscale_raw
        )
        attr_parent_noscale = libRigging.create_utility_node(
            'composeMatrix',
            inputTranslate=util_decomposeMatrix_parent_noscale.outputTranslate,
            inputRotate=util_decomposeMatrix_parent_noscale.outputRotate
        ).outputMatrix
        attr_parent_noscale_inv = libRigging.create_utility_node(
            'inverseMatrix',
            inputMatrix=attr_parent_noscale,
        ).outputMatrix

        #
        # Hack: Ensure the ctrl local matrix is affected by the global scale.
        #


        grp_output = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('output'),
            parent=grp_parent
        )
        attr_inf_tm = libRigging.create_utility_node(
            'multMatrix',
            name=nomenclature_rig.resolve('getInfluenceLocalTM'),
            matrixIn=(
                grp_offset.matrix,  # already in worldSpace
                attr_parent_noscale,  # already in worldSpace
                attr_parent_rot_noscale_inv,  # temporary enter follicle space
                self.ctrl.matrix,  # local space
                attr_parent_rot_noscale,  # exit follicle space to world space
                attr_parent_noscale_inv,
                grp_scale.matrix  # already in worldSpace
            )
        ).matrixSum
        util_get_inf_tm = libRigging.create_utility_node(
            'decomposeMatrix',
            name=nomenclature_rig.resolve('decomposeInfluenceLocalTM'),
            inputMatrix=attr_inf_tm
        )
        pymel.connectAttr(util_get_inf_tm.outputTranslate, grp_output.t)
        pymel.connectAttr(util_get_inf_tm.outputRotate, grp_output.r)
        pymel.connectAttr(util_get_inf_tm.outputScale, grp_output.s)
        pymel.parentConstraint(grp_output, self.jnt, maintainOffset=True)
        pymel.scaleConstraint(grp_output, self.jnt)

        # Cleanup
        if pos_fol:
            pos_fol.setParent(self.grp_rig)
        grp_offset.setParent(self.grp_rig)
        grp_parent.setParent(self.grp_rig)
        self.grp_rig.setParent(avar.grp_rig)


class InteractiveFK(ModuleMap):
    _CLS_CTRL_MODEL = InteractiveFKCtrlModel
    _CLS_CTRL = InteractiveFKCtrl

    @libPython.memoized_instancemethod
    def _get_parent(self):
        """
        Find the highest parent-level common parent to ALL the influences.
        This is necessary since we cannot handle different parent for each layers since
        the deformation is piped via blendshape.
        :return: A pymel.PyNode instance to use as parent.
        """
        parent_sets = None
        for jnt in self.jnts:
            parent_set = set(libPymel.get_parents(jnt))
            print parent_set
            if parent_sets is None:
                parent_sets = parent_set
            else:
                parent_sets &= parent_set

        common_parent = next(iter(reversed(sorted(parent_sets, key=libPymel.get_num_parents))), None)
        return common_parent

    def validate(self):
        # Ensure that all influences have a common parent for proprer scale handling.
        if not self._get_parent():
            raise Exception("Found no common parents for inputs.")

        super(InteractiveFK, self).validate()

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

    def build_models(self, **kwargs):
        parent = self._get_parent()

        for model in self.models:
            self.build_model(
                model,
                parent_scl=parent,
                **kwargs
            )


def register_plugin():
    return InteractiveFK