import collections

import pymel.core as pymel

from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule import Module
from omtk.core.classNode import Node
from omtk.modules.rigFK import FK
from omtk.libs import libRigging, libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libAttr
from omtk.models.modelInteractiveCtrl import ModelInteractiveCtrl

from omtk.libs.libRigging import _filter_shape

def get_history_farthest_sibling(shape, key=None):
    affected_meshes = [hist for hist in shape.listHistory(future=True) if _filter_shape(hist, key)]

    return next(iter(reversed(affected_meshes)), None)

def get_history_previous_sibling(shape, key=None):
    affected_meshes = [hist for hist in shape.listHistory() if hist != shape and _filter_shape(hist, key)]

    return next(iter(affected_meshes), None)


class InteractiveFKCtrl(BaseCtrl):
    pass

class InteractiveFKCtrlModel(ModelInteractiveCtrl):
    DEFAULT_NAME_USE_FIRST_INPUT = True

    def build(self, avar, parent_pos=None, parent_rot=None, follow_mesh=False, constraint=False, cancel_r=False, **kwargs):
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


        # driver_stack = self._create_stack_influence(input)
        # driver_stack.setParent(grp_parent)

        # Create two follicles, one for the position, one for the rotation.
        # The position follicle is on the farhest mesh in the construction history.
        # The rotation follicle is on the previous mesh in the construction history.
        meshes = libRigging.get_affected_geometries(self.jnt)
        meshes = list(set(meshes) & set(self.rig.get_meshes()))
        ref_mesh, _, out_u, out_v = libRigging.get_closest_point_on_shapes(meshes, pos_ref)

        pos_mesh = get_history_farthest_sibling(ref_mesh)
        rot_mesh = get_history_previous_sibling(ref_mesh)

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
            raise Exception("Cannot resolve mesh for {0}".format(pos_mesh))

        # Resolve rot parent
        # If we found a previous mesh in the construction history, we'll follow it.
        # This will ensure proper behavior when handling multiples layers like on tentacle rigs.
        # Otherwise we'll constraint the rotation to the parent of the module itself.
        if rot_mesh and rot_mesh != ref_mesh:
            self.debug("Rotation parent will use follicle on {0} at {1},{2}.".format(
                rot_mesh, out_u, out_v
            ))
            rot_fol = libRigging.create_follicle2(rot_mesh, out_u, out_v).getParent()
            rot_fol.rename(nomenclature_rig.resolve('rotFollicle'))
            rot_fol.setParent(grp_parent)

            parent_rot = pymel.createNode(
                'transform',
                name=nomenclature_rig.resolve('rotLocal'),
                parent=grp_offset
            )
            pymel.parentConstraint(rot_fol, parent_rot, maintainOffset=True)
        else:
            self.debug("Rotation parent will use {0}".format(self.parent))
            parent_rot = self.parent

        # if parent_rot:
        #     pymel.parentConstraint(parent_rot, grp_parent, maintainOffset=True)

        super(InteractiveFKCtrlModel, self).build(
            avar,
            ctrl_tm=tm_ref,
            parent_pos=parent_pos,
            parent_rot=parent_rot,
            follow_mesh=False,
            constraint=False,
            cancel_r=False,
            **kwargs
        )

        #
        # Compute influence position
        # offsetTM * parentTM * inv(rotLocalTM) * ctrlLocalTM * rotLocalTM
        #
        grp_output = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('output'),
            parent=grp_parent
        )
        attr_inf_tm = libRigging.create_utility_node(
            'multMatrix',
            name='getInfluenceLocalTM',
            matrixIn=(
                grp_offset.matrix,
                grp_parent.matrix,
                parent_rot.worldInverseMatrix,  # temporary enter follicle space
                self.ctrl.matrix,
                parent_rot.worldMatrix,  # exit follicle space to world space
                grp_parent.inverseMatrix,
            )
        ).matrixSum
        util_get_inf_tm = libRigging.create_utility_node(
            'decomposeMatrix',
            name='decomposeInfluenceLocalTM',
            inputMatrix=attr_inf_tm
        )
        pymel.connectAttr(util_get_inf_tm.outputTranslate, grp_output.t)
        pymel.connectAttr(util_get_inf_tm.outputRotate, grp_output.r)
        pymel.parentConstraint(grp_output, self.jnt, maintainOffset=True)

        # Cleanup
        if pos_fol:
            pos_fol.setParent(self.grp_rig)
        grp_offset.setParent(self.grp_rig)
        grp_parent.setParent(self.grp_rig)
        self.grp_rig.setParent(avar.grp_rig)

class InteractiveFK(Module):
    _CLS_CTRL_MODEL = InteractiveFKCtrlModel
    _CLS_CTRL = InteractiveFKCtrl
    DEFAULT_NAME_USE_FIRST_INPUT = True

    def __init__(self, *args, **kwargs):
        """
        Pre-declare here all the used members.
        """
        super(InteractiveFK, self).__init__(*args, **kwargs)

    def build(self, *args, **kwargs):
        super(InteractiveFK, self).build(parent=False, *args, **kwargs)

        for input in self.jnts:
            #m_name = self.get_nomenclature().copy()
            #m_name.tokens.append('ctrlModel')
            m = self._CLS_CTRL_MODEL(
                [input],
                rig=self.rig,
            )
            m._CLS_CTRL = self._CLS_CTRL
            m.name = m.get_default_name()
            m.build(self)
            m.grp_anm.setParent(self.grp_anm)  # todo: reduce cluttering by using direct connection and reducing grp_anm count
            m.grp_rig.setParent(self.grp_rig)

    def unbuild(self):
        """
        If you are using sub-modules, you might want to clean them here.
        :return:
        """
        super(InteractiveFK, self).unbuild()


def register_plugin():
    return InteractiveFK