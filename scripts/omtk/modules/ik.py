"""
Logic for the "IK" module
"""
import math
import functools
import collections

from maya import cmds, OpenMaya
import pymel.core as pymel

from omtk.core.ctrl import BaseCtrl
from omtk.core.module import CompoundModule
from omtk.libs import libAttr, libPymel, libPython, libRigging
from omtk.core.compounds import create_compound
from omtk.vendor.omtk_compound.core._factory import create_empty


class CtrlIk(BaseCtrl):
    """
    Base ik ctrl for the IK class. Used to drive ik handle.
    """

    kAttrName_State = "ikFk"  # Attribute string shown in maya

    def create_ctrl(self, *args, **kwargs):
        """
        Create the ctrl node

        :param args: More args passed to the superclass
        :param kwargs: More kwargs passed to the superclass
        :return: The created ctrl node
        """
        return super(CtrlIk, self).create_ctrl(multiplier=1.5, *args, **kwargs)


class CtrlIkSwivel(BaseCtrl):
    """
    Base Ctrl ik swivel class implementation.
    Mostly used to do pole vector on an ik.
    Will create a ctrl with a line to facilitate pole vector visualization.
    """

    def __init__(self):
        super(CtrlIkSwivel, self).__init__()

        self._line_locator = None
        self._line_annotation = None

    def create_ctrl(
        self, refs=None, size=None, line_target=True, offset=None, *args, **kwargs
    ):
        """
        Create the swivel ctrl itself when build node function is called
        :param refs: Reference used to correctly size the ctrl
        :param size: Size of the ctrl
        :param line_target: Bool to tell if we want a line target or not
        :param offset: Offset applied on the ctrl
        :param args: More args passed to the superclass
        :param kwargs: More kwargs passed to the super class
        :return: The created swivel node ctrl
        """
        # Resolve size automatically if refs are provided
        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs
        if size is None and ref is not None:
            size = libRigging.get_recommended_ctrl_size(ref)
        else:
            size = 1.0

        node = super(CtrlIkSwivel, self).create_ctrl(*args, **kwargs)
        make = node.getShape().create.inputs()[0]
        make.radius.set(size * 2)
        make.degree.set(1)
        make.sections.set(4)

        make.radius.set(make.radius.get() * 0.5)
        make.degree.set(1)
        make.sections.set(4)

        return node

    def get_spaceswitch_targets(self, module, *args, **kwargs):
        """
        Add the Hand/Leg IK ctrl by default as a space-switch target to any swivel.
        :param module: The parent module, generally an IK instance.
        :param args: More args passer to the super class
        :param kwargs: More kwargs pass to the super class
        :return: The spaceswitch usable targets and names
        """
        targets, target_names, indexes = super(
            CtrlIkSwivel, self
        ).get_spaceswitch_targets(module, *args, **kwargs)

        # Add the Hand/Foot ctrl
        targets.append(module.ctrl_ik)
        target_names.append(None)
        indexes.append(self.get_bestmatch_index(module.ctrl_ik))

        return targets, target_names, indexes

    def build(self, refs=None, line_target=True, *args, **kwargs):
        """
        Will create the ctrl node and it's line target if needed
        :param refs: The reference used to attach the line target
        :param line_target: Bool to tell if we want a line target
        :param args: More args passed to the super class
        :param kwargs: More kwargs passed to the super class
        :return:
        """
        super(CtrlIkSwivel, self).build(*args, **kwargs)
        assert self.node is not None

        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs

        # Create line
        if line_target and ref:
            # Create a spaceLocator so the annotation can hook itself to it.
            self._line_locator = pymel.spaceLocator()
            locator_shape = self._line_locator.getShape()
            pymel.pointConstraint(ref, self._line_locator)
            self._line_locator.setParent(self.node)
            self._line_locator.hide()

            self._line_annotation = pymel.createNode("annotationShape")
            annotation_transform = self._line_annotation.getParent()
            self._line_annotation.setParent(self.node, relative=True, shape=True)
            pymel.connectAttr(
                locator_shape.worldMatrix,
                self._line_annotation.dagObjectMatrix[0],
                force=True,
            )
            pymel.delete(annotation_transform)

        return self.node


class IKStretchModel(CompoundModule):  # TODO: Convert to scripted compound?
    """
    A compound that interact with an IK chain.

    Inputs:
    - start: The ik chain start position
    - end: The ik chain end position
    - length: The ik chain length

    Outputs:
    - end: The ik chain end position
    - stretch: The ik chain stretch, this is applied on the translation

    Here are some implementation examples:
    - None: Standard IK chain without any stretch
    - SimpleStretch: Simple stretch setup based on the distance between the start and end.
    - SoftIK: Complex stretch setup
    - Footroll: Influence the effector
    """

    SHOW_IN_UI = False
    AFFECT_INPUTS = False
    SUPPORT_NO_INPUTS = True
    CREATE_GRP_ANM = False
    CREATE_GRP_RIG = False

    def _build_compound(self):
        inst = create_empty(namespace=self.name)
        libAttr.addAttr(inst.input, longName="start", dataType="double3")
        libAttr.addAttr(inst.input, longName="end", dataType="double3")
        libAttr.addAttr(inst.input, longName="length")
        libAttr.addAttr(inst.output, longName="end", dataType="double3")
        libAttr.addAttr(inst.output, longName="stretch", default=1.0)
        return inst

    def connect_to_ctrl(self, ctrl):
        pass


class SoftIKStretchModel(IKStretchModel):
    """
    Complex stretch model that prevent visual snapping when the leg extend over
    it's length. This is very useful when retargeting animation between characters
    with different proportions.
    """

    def _build_compound(self):
        # Create the network computing the soft ik stretch
        return create_compound("omtk.SoftIkStretch", self.name)

    def connect_to_ctrl(self, ctrl):
        # Create public attributes
        _fn = functools.partial(
            libAttr.addAttr, ctrl, hasMinValue=True, hasMaxValue=True, keyable=True,
        )
        attr_ratio = _fn(
            longName="softIkRatio",
            niceName="SoftIK",
            defaultValue=0,
            minValue=0,
            maxValue=50,
        )
        attr_stretch = _fn(
            longName="stretch",
            niceName="Stretch",
            defaultValue=0,
            minValue=0,
            maxValue=1.0,
        )

        # Convert ratio from percent (user-friendly) to decimal.
        attr_ratio = libRigging.create_utility_node(
            "multiplyDivide", input1X=attr_ratio, input2X=0.01
        ).outputX

        compound_in = pymel.PyNode(self.compound.input)
        attr_compound_ratio = compound_in.ratio
        attr_compount_stretch = compound_in.stretch
        pymel.connectAttr(attr_ratio, attr_compound_ratio)
        pymel.connectAttr(attr_stretch, attr_compount_stretch)


# Todo: Support more complex IK limbs (ex: 2 knees)
class IK(CompoundModule):
    """
    Classical IK rig that support stretching and soft-ik.
    This is the base Ik module of the autorig.
    Support a basic 3 bones ik rotate-plane solver
    with the creation of a controller.
    Also used the softik implementation. Inherit of the module class
    to be able to used it in the autorig UI
    """

    AFFECT_INPUTS = True
    SUPPORT_NO_INPUTS = True
    _CLASS_CTRL_IK = CtrlIk  # Ik Ctrl class
    _CLASS_CTRL_SWIVEL = CtrlIkSwivel  # Ik Swivel Ctrl class
    _CLASS_IK_MODEL = SoftIKStretchModel

    def __init__(self, *args, **kwargs):
        super(IK, self).__init__(*args, **kwargs)
        self.ctrl_ik = None
        self.ctrl_swivel = None
        self.ctrl_swivel_quad = None
        self.chain_length = None
        self.swivelDistance = None
        self._sys_stretch = None

    @property
    def sys_stretch(self):
        """
        :return: The module computing the chain stretch.
        :rtype: IKStretchModel
        """
        return self._sys_stretch

    def build(self):
        """
        Build the ik system when needed
        """
        self._sys_stretch = self._CLASS_IK_MODEL.from_instance(
            self, self._sys_stretch, "stretch"
        )

        super(IK, self).build()

        jnt_elbow = self.chain_jnt[1]  # always the second one

        # Compute swivel pos before any operation is done on the bones
        swivel_pos = self.calc_swivel_pos()

        self.ctrl_ik = self._build_ctrl_ik()
        self.ctrl_swivel = self._build_ctrl_swivel(jnt_elbow, swivel_pos)
        self.swivelDistance = self.chain.length()  # Used in ik/fk switch
        self.compound_inputs.length.set(self.swivelDistance)

        self.sys_stretch.connect_to_ctrl(self.ctrl_ik)

        # Connect ctrl ik to the compound
        # TODO: Do not use world matrices
        attr_ctrl_tm = self.ctrl_ik.worldMatrix
        print(self.chain_jnt, self.parent_jnt)
        if self.parent_jnt:
            attr_ctrl_tm = libRigging.create_multiply_matrix(
                [attr_ctrl_tm, self.parent_jnt.worldInverseMatrix]
            )
        pymel.connectAttr(attr_ctrl_tm, self.compound_inputs.effector)

        # Connect ctrl swivel to the compound
        attr_swivel_tm = self.ctrl_swivel.worldMatrix
        if self.parent_jnt:
            attr_swivel_tm = libRigging.create_multiply_matrix(
                [attr_swivel_tm, self.parent_jnt.worldInverseMatrix]
            )
        attr_swivel = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=attr_swivel_tm
        ).outputTranslate
        pymel.connectAttr(attr_swivel, self.compound_inputs.swivel)

        # Constraint
        if self.AFFECT_INPUTS:
            for idx, jnt in enumerate(self.chain):
                attr_out = self.compound_outputs.out[idx]
                libRigging.connect_matrix_to_node(attr_out, jnt)

    def unbuild(self):
        """
        Unbuild the ik system and reset the needed parameters
        :return:
        """
        self.chain_length = None
        self.swivelDistance = None

        super(IK, self).unbuild()

    def iter_ctrls(self):
        for yielded in super(IK, self).iter_ctrls():
            yield yielded
        yield self.ctrl_ik
        yield self.ctrl_swivel
        yield self.ctrl_swivel_quad

    def parent_to(self, parent):
        """
        Parent the system
        :param parent: The node used to parent the system
        :return:
        """

    def _build_compound(self):
        """
        Re-crete the IK3 compound but with a variable number of inputs.
        """
        # TODO: Do we want to still build this dynamically?
        # Would a simple compound do the trick?
        naming = self.get_nomenclature()

        inst = create_empty(namespace=self.name)
        cmds.addAttr(inst.input, longName="bind", dataType="matrix", multi=True)
        cmds.addAttr(inst.input, longName="effector", dataType="matrix")
        cmds.addAttr(inst.input, longName="swivel", dataType="double3")
        cmds.addAttr(inst.input, longName="length")
        cmds.addAttr(inst.output, longName="out", dataType="matrix", multi=True)

        inst_inputs = pymel.PyNode(inst.input)
        inst_output = pymel.PyNode(inst.output)

        attr_bind = inst_inputs.bind
        attr_swivel = inst_inputs.swivel
        attr_start = libRigging.create_utility_node(
            "decomposeMatrix",
            name=naming.resolve("getStartPos"),
            inputMatrix=attr_bind[0],
        ).outputTranslate
        attr_effector = inst_inputs.effector
        attr_out = inst_output.out
        attr_end = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=attr_effector
        ).outputTranslate

        # Connect inputs.bind to original influence matrices
        for idx, jnt in enumerate(self.chain):
            attr_bind[idx].set(jnt.getMatrix())

        # Create joints
        jnts = _create_joint_from_binds(attr_bind, naming)
        jnts.start.setParent(self.grp_rig)

        ctrl_ref = pymel.createNode("transform", parent=self.grp_rig)
        libRigging.connect_matrix_to_node(attr_effector, ctrl_ref)
        pymel.orientConstraint(ctrl_ref, jnts.end)

        # Connect joint to compound output
        for idx, jnt in enumerate(jnts):
            pymel.connectAttr(jnt.matrix, attr_out[idx])

        # Create stretch model
        pymel.connectAttr(inst_inputs.length, self.sys_stretch.compound_inputs.length)
        pymel.connectAttr(attr_start, self.sys_stretch.compound_inputs.start)
        pymel.connectAttr(attr_end, self.sys_stretch.compound_inputs.end)
        attr_stretch = self.sys_stretch.compound_outputs.stretch
        attr_end = self.sys_stretch.compound_outputs.end

        for idx, jnt in enumerate(jnts[1:]):
            util_get_t = libRigging.create_utility_node(
                "multiplyDivide",
                input1X=attr_stretch,
                input1Y=attr_stretch,
                input1Z=attr_stretch,
                input2=jnt.translate.get(),
                name=naming.resolve("getStretch%s" % idx),
            )
            pymel.connectAttr(util_get_t.output, jnt.translate, force=True)

        # Create ik solver
        ik_handle, _ = pymel.ikHandle(
            startJoint=jnts.start, endEffector=jnts.end, solver="ikRPsolver"
        )
        ik_handle.setParent(self.grp_rig)

        # Constraint ik solver
        pymel.connectAttr(attr_end, ik_handle.translate)
        swivel_constraint = _create_swivel_constraint(
            attr_start, attr_swivel, ik_handle
        )
        swivel_constraint.setParent(self.grp_rig)

        return inst

    def calc_swivel_pos(self):
        """
        This function is used to compute a swivel position.
        Can be used for multiple knee setup

        :return: The swivel position computed between the start and end
        :rtype: pymel.datatypes.Vector
        """
        start = self.chain.start.getTranslation(space="world")
        end = self.chain.end.getTranslation(space="world")

        chain_length = 0
        for jnt in self.chain[1:]:
            chain_length += jnt.translate.get().length()

        ratio = self.chain[1].translate.get().length() / chain_length
        pos_swivel_base = (end - start) * ratio + start
        dir_swivel = (
            self.chain[1].getTranslation(space="world") - pos_swivel_base
        ).normal()
        return pos_swivel_base + (dir_swivel * chain_length)

    def _get_ik_ctrl_bound_refs_raycast(self):
        """
        Resolve what objects to use for computing the bound of the ik ctrl.
        Default behavior is to use the hand and any inputs after. (ex: toes)
        :return: An array of pymel.general.PyNode instances.
        """
        return [self.chain[-2]]

    def _build_ctrl_swivel(self, ref, pos, name="swivel", constraint=True, **kwargs):
        """
        Create the swivel ctrl for the ik system

        :param ctrl_swivel: The ctrl used to setup the swivel, create one if needed
        :param ref: Reference object to position the swivel
        :param pos: The computed position of the swivel
        :param ik_handle: The handle to pole vector constraint
        :param name: Part name used to resolve the object rig name
        :param constraint: Do we contraint the ik handle to the swivel ctrl
        :param kwargs: Additionnal parameters
        :return: The created ctrl swivel
        """
        naming = self.get_nomenclature_anm()

        ctrl = self._CLASS_CTRL_SWIVEL.from_instance(self.ctrl_swivel)
        ctrl.build(refs=ref)
        ctrl.setParent(self.grp_anm)
        ctrl.rename(naming.resolve(name))
        ctrl._line_locator.rename(naming.resolve(name + "LineLoc"))
        ctrl._line_annotation.rename(naming.resolve(name + "LineAnn"))
        ctrl.offset.setTranslation(pos, space="world")
        ctrl.create_spaceswitch(self, self.parent_jnt, local_label="World")
        return ctrl

    def _get_ik_ctrl_tms(self):
        """
        Compute the transforms for the ik ctrl.

        :return: The transform for the ctrl offset and the ctrl itself.
        :rtype: tuple[pymel.nodetypes.Matrix, pymel.nodetypes.Matrix]
        """
        inf_tm = self.chain.end.getMatrix(worldSpace=True)
        return inf_tm, inf_tm

    def _get_ik_ctrl_bound_refs_extra(self):
        """
        Resolve what objects to use for computing the bound of the ik ctrl.
        Default behavior is to use the hand and all it's children. (ex: fingers)
        :return: An array of pymel.general.PyNode instances.
        """
        jnt_hand = self.input[self.iCtrlIndex]
        return [jnt_hand] + jnt_hand.getChildren(allDescendents=True)

    def _build_ctrl_ik(self):
        """
        :return: The main ik ctrl
        :rtype: CtrlIk
        """
        naming = self.get_nomenclature_anm()

        # Resolve CtrlIK transform
        ctrl_ik_offset_tm, ctrl_ik_tm = self._get_ik_ctrl_tms()
        ctrl_ik_offset_rot = (
            libPymel.get_rotation_from_matrix(ctrl_ik_offset_tm)
            if ctrl_ik_offset_tm
            else None
        )
        ctrl_ik_rot = (
            libPymel.get_rotation_from_matrix(ctrl_ik_tm) if ctrl_ik_tm else None
        )

        ctrl = self._CLASS_CTRL_IK.from_instance(self.ctrl_ik)
        refs_bound_raycast = self._get_ik_ctrl_bound_refs_raycast()
        refs_bound_extra = self._get_ik_ctrl_bound_refs_extra()
        ctrl.build(
            refs=refs_bound_extra,
            refs_raycast=refs_bound_raycast,
            geometries=self.rig.get_meshes(),
            parent_tm=ctrl_ik_tm,
        )

        ctrl.setParent(self.grp_anm)
        ctrl.rename(naming.resolve())

        # Define CtrlIK transform
        ctrl_ik_t = self.chain.end.getTranslation(space="world")
        ctrl.offset.setTranslation(ctrl_ik_t, space="world")
        if ctrl_ik_offset_rot:
            ctrl.offset.setRotation(ctrl_ik_offset_rot)

        # Create space switch
        ctrl.create_spaceswitch(self, self.parent_jnt, local_label="World")
        if ctrl_ik_rot:
            ctrl.node.setRotation(ctrl_ik_rot, space="world")

        return ctrl

    def _build_stretch(self, attr_start, attr_end, attr_length):
        # Build and connect the IK stretch model
        stretch_model = self._CLASS_IK_MODEL(parent=self)
        stretch_model.build()

        compound_in = pymel.PyNode(stretch_model.compound.input)
        pymel.connectAttr(attr_start, compound_in.start)
        pymel.connectAttr(attr_end, compound_in.end)
        compound_in.length.set(attr_length)

        return stretch_model

    def _get_ik_handle_ref(self):
        return self.ctrl_ik


def _create_swivel_constraint(attr_start, attr_swivel, ik_handle):
    """
    Helper method that create a poleVectorConstraint object with minimal attributes.

    :param attr_start: The IK chain start position
    :param attr_swivel: The IK chain swivel position
    :param ik_handle: The IK handle to constraint
    """
    node = pymel.createNode("poleVectorConstraint")
    pymel.connectAttr(attr_swivel, node.target[0].targetTranslate)
    pymel.connectAttr(attr_start, node.constraintRotatePivot)
    pymel.connectAttr(node.constraintTranslate, ik_handle.poleVector)
    return node


def _create_joint_from_binds(attr_bind, naming, connect=True, jointOrient=True):
    """
    Create a joint chain from a list of matrix attributes.
    """
    # TODO: Move to a shared location?
    # Ensure selection is clear so we don't accidentally parent our joint to something.
    pymel.select(clear=True)
    jnts = []
    for idx, attr_tm in enumerate(attr_bind):
        jnt = pymel.joint(name=naming.resolve(str(idx)))

        if connect:
            util = libRigging.create_utility_node(
                "decomposeMatrix", inputMatrix=attr_tm
            )
            pymel.connectAttr(util.outputTranslate, jnt.translate)
            if jointOrient:
                pymel.connectAttr(util.outputRotate, jnt.jointOrient)
            else:
                pymel.connectAttr(util.outputRotate, jnt.rotate)
        else:
            tm = attr_tm.get()
            jnt.translate.set(tm.translate)
            rotation = libPymel.get_rotation_from_matrix(tm).asEulerRotation()
            rotation = [
                math.degrees(rotation.x),
                math.degrees(rotation.y),
                math.degrees(rotation.z),
            ]

            if jointOrient:
                jnt.jointOrient.set(rotation)
            else:
                jnt.rotate.set(rotation)
        jnts.append(jnt)
    for parent, child in libPython.pairwise(jnts):
        child.setParent(parent)
    return libPymel.PyNodeChain(jnts)


def register_plugin():
    """
    Register the plugin. This function is expected by plugin_manager.

    :return: The plugin to register
    :rtype: omtk.core.modules.Module
    """
    return IK
