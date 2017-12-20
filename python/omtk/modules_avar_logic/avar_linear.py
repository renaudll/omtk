import pymel.core as pymel
from omtk.core import node
from omtk.core import module_logic_avar
from omtk.libs import libRigging


class AvarLogicLinear(module_logic_avar.BaseAvarRigConnectionModel):
    """
    This represent a single deformer influence that is moved in space using avars.
    By default it come with a Deformer driven by a doritos setup.
    A doritos setup allow the controller to always be on the surface of the face.
    """
    name = 'Linear'

    def __init__(self, *args, **kwargs):
        super(AvarLogicLinear, self).__init__(*args, **kwargs)

        self._stack = None
        self._grp_offset = None
        self._grp_parent = None
        self.avar = None  # Point to the original avar which contain all attributes that will drive the model.

    def build_stack(self, stack):
        """
        The dag stack is a stock of dagnode that act as additive deformer to controler the final position of
        the drived joint.
        """
        layer_pos = stack.append_layer('pos')
        pymel.connectAttr(self.avar.attr_lr, layer_pos.tx)
        pymel.connectAttr(self.avar.attr_ud, layer_pos.ty)
        pymel.connectAttr(self.avar.attr_fb, layer_pos.tz)
        pymel.connectAttr(self.avar.attr_yw, layer_pos.ry)
        pymel.connectAttr(self.avar.attr_pt, layer_pos.rx)
        pymel.connectAttr(self.avar.attr_rl, layer_pos.rz)
        pymel.connectAttr(self.avar.attr_sx, layer_pos.sx)
        pymel.connectAttr(self.avar.attr_sy, layer_pos.sy)
        pymel.connectAttr(self.avar.attr_sz, layer_pos.sz)

        return stack

    def get_jnt_tm(self):
        """
        :return: The deformer pivot transformation.
        """
        # todo: do we want to handle rotation?
        if self.jnt:
            pos = self.jnt.getTranslation(space='world')
            return pymel.datatypes.Matrix(
                1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, pos.x, pos.y, pos.z, 1
            )
        raise Exception("Found no influence in {0}".format(self))

    def build(self, constraint=True, ctrl_tm=None, jnt_tm=None, obj_mesh=None, follow_mesh=True,
              **kwargs):
        """
        :param constraint:
        :param ctrl_size: DEPRECATED, PLEASE MOVE TO ._create_ctrl
        :param ctrl_tm: DEPRECATED, PLEASE MOVE TO ._create_ctrl
        :param jnt_tm:
        :param obj_mesh: DEPRECATED, PLEASE MOVE TO ._create_ctrl
        :param follow_mesh: DEPRECATED, PLEASE MOVE TO ._create_ctrl
        :param kwargs:
        :return:
        """
        if self.avar is None:
            raise Exception("Can't build {0}, no avar defined!".format(self))

        super(AvarLogicLinear, self).build(parent=False)

        nomenclature_rig = self.get_nomenclature_rig()

        # Resolve influence matrix
        if jnt_tm is None:
            jnt_tm = self.get_jnt_tm()
        jnt_pos = jnt_tm.translate

        #
        # Build stack
        # The stack resolve the influence final transform relative to it's parent and original bind-pose.
        #
        dag_stack_name = nomenclature_rig.resolve('stack')
        stack = node.Node()
        stack.build(name=dag_stack_name)

        # Create an offset layer that define the starting point of the Avar.
        # It is important that the offset is in this specific node since it will serve as
        # a reference to re-computer the base u and v parameter if the rigger change the
        # size of the surface when the system is build.
        grp_offset_name = nomenclature_rig.resolve('offset')
        self._grp_offset = pymel.createNode('transform', name=grp_offset_name)
        self._grp_offset.rename(grp_offset_name)
        self._grp_offset.setParent(self.grp_rig)
        # layer_offset.setMatrix(jnt_tm)

        # Create a parent layer for constraining.
        # Do not use dual constraint here since it can result in flipping issues.
        grp_parent_name = nomenclature_rig.resolve('parent')
        self._grp_parent = pymel.createNode('transform', name=grp_parent_name)
        self._grp_parent.setParent(self._grp_offset)
        self._grp_parent.rename(grp_parent_name)

        # Move the grp_offset to it's desired position.
        self._grp_offset.setTranslation(jnt_pos)

        # The rest of the stack is built in another function.
        # This allow easier override by sub-classes.
        self._stack = stack
        self.build_stack(stack)
        self._stack.setParent(self._grp_offset)

        # Take the result of the stack and add it on top of the bind-pose and parent group.
        grp_output_name = nomenclature_rig.resolve('output')
        self._grp_output = pymel.createNode('transform', name=grp_output_name)
        self._grp_output.setParent(self._grp_parent)

        attr_get_stack_local_tm = libRigging.create_utility_node(
            'multMatrix',
            matrixIn=(
                self._stack.node.worldMatrix,
                self._grp_offset.worldInverseMatrix
            )
        ).matrixSum
        util_get_stack_local_tm = libRigging.create_utility_node(
            'decomposeMatrix',
            inputMatrix=attr_get_stack_local_tm
        )
        pymel.connectAttr(util_get_stack_local_tm.outputTranslate, self._grp_output.t)
        pymel.connectAttr(util_get_stack_local_tm.outputRotate, self._grp_output.r)
        pymel.connectAttr(util_get_stack_local_tm.outputScale, self._grp_output.s)

        # We connect the joint before creating the controllers.
        # This allow our doritos to work out of the box and allow us to compute their sensibility automatically.
        if self.jnt and constraint:
            pymel.parentConstraint(self._grp_output, self.jnt, maintainOffset=True)
            pymel.scaleConstraint(self._grp_output, self.jnt, maintainOffset=True)

    def parent_to(self, parent):
        pymel.parentConstraint(parent, self._grp_parent, maintainOffset=True)
        pymel.scaleConstraint(parent, self._grp_parent, maintainOffset=True)


def register_plugin():
    return AvarLogicLinear
