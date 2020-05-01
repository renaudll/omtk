import functools
import collections
import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule import Module
from omtk.libs import libRigging
from omtk.libs import libAttr
from omtk.libs import libPymel
from omtk.core.compounds import create_compound


class CtrlIk(BaseCtrl):
    """
    Base ik ctrl for the IK class. Used to drive ik handle. Inherit of the base ctrl class
    """

    kAttrName_State = "ikFk"  # Attribute string shown in maya

    def __createNode__(self, *args, **kwargs):
        """
        Create the ctrl node

        :param args: More args passed to the superclass
        :param kwargs: More kwargs passed to the superclass
        :return: The created ctrl node
        """
        return super(CtrlIk, self).__createNode__(multiplier=1.5, *args, **kwargs)


class CtrlIkSwivel(BaseCtrl):
    """
    Base Ctrl ik swivel class implementation. Mostly used to do pole vector on an ik. Will create a ctrl with a line
    to facilitate pole vector visualization. Inherit of the base ctrl class
    """

    def __init__(self):
        super(CtrlIkSwivel, self).__init__()

        self._line_locator = None
        self._line_annotation = None

    def __createNode__(
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

        node = super(CtrlIkSwivel, self).__createNode__(*args, **kwargs)
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
        if line_target is True and ref is not None:
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


# Todo: Support more complex IK limbs (ex: 2 knees)
class IK(Module):
    """
    Classical IK rig that support stretching and soft-ik.
    This is the base Ik module of the autorig. Support a basic 3 bones ik rotate-plane solver
    with the creation of a controller. Also used the softik implementation. Inherit of the module class
    to be able to used it in the autorig UI
    """

    _CLASS_CTRL_IK = CtrlIk  # Ik Ctrl class
    _CLASS_CTRL_SWIVEL = CtrlIkSwivel  # Ik Swivel Ctrl class

    def __init__(self, *args, **kwargs):
        super(IK, self).__init__(*args, **kwargs)
        self.iCtrlIndex = 2
        self.ctrl_ik = None
        self.ctrl_swivel = None
        self.ctrl_swivel_quad = None
        self.chain_length = None
        self._chain_ik = None
        self.swivelDistance = None

    def _create_ctrl_ik(self, *args, **kwargs):
        """
        Create an instance of the ik ctrl
        :param args: Args that could be passed to the Ik Ctrl creation
        :param kwargs: Kwargs that could be passed to the Ik Ctrl creation
        :return: The Ik controller
        """
        return self._CLASS_CTRL_IK(*args, **kwargs)

    def calc_swivel_pos(self, start_index=0, end_index=2):
        """
        This function is used to compute a swivel position. Can be used for multiple knee setup
        :param start_index: The start index of the _ik_chain that will be used to compute the swivel pos
        :param end_index: The end index of the _ik_chain that will be used to compute the swivel pos
        :return: The swivel position computed between the start and end
        """
        pos_start = self.chain_jnt[start_index].getTranslation(space="world")
        pos_end = self.chain_jnt[end_index].getTranslation(space="world")

        chain_length = 0
        for i in range(start_index, end_index):
            chain_length += self.chain_jnt[i + 1].t.get().length()

        ratio = self.chain_jnt[start_index + 1].t.get().length() / chain_length
        pos_swivel_base = (pos_end - pos_start) * ratio + pos_start
        dir_swivel = (
            self.chain_jnt[start_index + 1].getTranslation(space="world")
            - pos_swivel_base
        ).normal()
        return pos_swivel_base + (dir_swivel * chain_length)

    def setup_softik(self, ik_handle_to_constraint, stretch_chains):
        """
        Setup the softik system a ik system
        :param ik_handle_to_constraint: A list of ik handles to constraint on the soft-ik network.
        :param stretch_chains: A list of chains to connect the stretch to.
        """
        nomenclature_rig = self.get_nomenclature_rig()

        # Create public attributes
        holder = self.ctrl_ik
        fnAddAttr = functools.partial(
            libAttr.addAttr, holder, hasMinValue=True, hasMaxValue=True, keyable=True
        )
        attInRatio = fnAddAttr(
            longName="softIkRatio",
            niceName="SoftIK",
            defaultValue=0,
            minValue=0,
            maxValue=50,
        )
        attInStretch = fnAddAttr(
            longName="stretch",
            niceName="Stretch",
            defaultValue=0,
            minValue=0,
            maxValue=1.0,
        )

        # Convert ratio from percent (user-friendly) to decimal.
        attInRatio = libRigging.create_utility_node(
            "multiplyDivide", input1X=attInRatio, input2X=0.01
        ).outputX

        # Adjust the original chain length with the global scale modifier
        attLength = libRigging.create_utility_node(
            "multiplyDivide",
            input1X=self.chain_length,
            input2X=self.grp_rig.globalScale,
        ).outputX

        # Create the network computing the soft ik stretch
        soft_ik_network_name = nomenclature_rig.resolve("softik")
        compound = create_compound(
            "omtk.SoftIkStretch",
            soft_ik_network_name,
            inputs={
                "ratio": attInRatio,
                "stretch": attInStretch,
                "start": self._ikChainGrp.worldMatrix,
                "end": self._ik_handle_target.worldMatrix,
                "length": attLength,
            },
        )
        attOutStretch = pymel.Attribute("%s.stretch" % compound.output)
        attOutRatio = pymel.Attribute("%s.ratio" % compound.output)
        attOutRatioInv = libRigging.create_utility_node(
            "reverse", inputX=attOutRatio
        ).outputX

        # TODO: Improve softik ratio when using multiple ik handle.
        # TODO: Not the same ratio will be used depending of the angle
        for handle in ik_handle_to_constraint:
            pointConstraint = pymel.pointConstraint(
                self._ik_handle_target, self._ikChainGrp, handle
            )
            pointConstraint.rename(
                pointConstraint.stripNamespace().replace(
                    "pointConstraint", "softIkConstraint"
                )
            )
            weight_inn, weight_out = pointConstraint.getWeightAliasList()[
                -2:
            ]  # Ensure to get the latest target added
            pymel.connectAttr(attOutRatio, weight_inn)
            pymel.connectAttr(attOutRatioInv, weight_out)

        # Connect stretch
        for stretch_chain in stretch_chains:
            for i in range(1, self.iCtrlIndex + 1):
                obj = stretch_chain[i]
                util_get_t = libRigging.create_utility_node(
                    "multiplyDivide",
                    input1X=attOutStretch,
                    input1Y=attOutStretch,
                    input1Z=attOutStretch,
                    input2=obj.t.get(),
                )
                pymel.connectAttr(util_get_t.outputX, obj.tx, force=True)
                pymel.connectAttr(util_get_t.outputY, obj.ty, force=True)
                pymel.connectAttr(util_get_t.outputZ, obj.tz, force=True)

        compound.explode(
            remove_namespace=True
        )  # TODO: Should be done on the post-build of the rig

    def create_ik_handle(self, solver="ikRPsolver"):
        """
        Create a ik handle for a specific ik setup. Need to be overrided by children class to implement the good behavior
        :return: Return the created ik handle and effector
        """
        # Since the base Ik will always be two bone,
        # we can use the fact that the effector is after the elbow
        start = self._chain_ik[0]
        end = self._chain_ik[self.iCtrlIndex]
        ik_handle, ik_effector = pymel.ikHandle(
            startJoint=start, endEffector=end, solver=solver
        )
        return ik_handle, ik_effector

    def setup_swivel_ctrl(
        self, base_ctrl, ref, pos, ik_handle, name="swivel", constraint=True, **kwargs
    ):
        """
        Create the swivel ctrl for the ik system
        :param base_ctrl: The ctrl used to setup the swivel, create one if needed
        :param ref: Reference object to position the swivel
        :param pos: The computed position of the swivel
        :param ik_handle: The handle to pole vector constraint
        :param name: Part name used to resolve the object rig name
        :param constraint: Do we contraint the ik handle to the swivel ctrl
        :param kwargs: Additionnal parameters
        :return: The created ctrl swivel
        """
        nomenclature_anm = self.get_nomenclature_anm()

        ctrl_swivel = self.init_ctrl(self._CLASS_CTRL_SWIVEL, base_ctrl)
        ctrl_swivel.build(refs=ref)
        ctrl_swivel.setParent(self.grp_anm)
        ctrl_swivel.rename(nomenclature_anm.resolve(name))
        ctrl_swivel._line_locator.rename(nomenclature_anm.resolve(name + "LineLoc"))
        ctrl_swivel._line_annotation.rename(nomenclature_anm.resolve(name + "LineAnn"))
        ctrl_swivel.offset.setTranslation(pos, space="world")
        ctrl_swivel.create_spaceswitch(self, self.parent, local_label="World")

        if constraint:
            # Pole vector contraint the swivel to the ik handle
            pymel.poleVectorConstraint(ctrl_swivel, self._ik_handle)

        return ctrl_swivel

    def _get_ik_ctrl_tms(self):
        """
        Compute the desired rotation for the ik ctrl.
        :return: A two-size tuple containing the transformation matrix for the ctrl offset and the ctrl itself.
        """
        inf_tm = self.input[self.iCtrlIndex].getMatrix(worldSpace=True)
        return inf_tm, inf_tm

    def _get_ik_ctrl_bound_refs_raycast(self):
        """
        Resolve what objects to use for computing the bound of the ik ctrl using raycasts.
        Default behavior is to use the hand and any inputs after. (ex: toes)
        :return: An array of pymel.general.PyNode instances.
        """
        return self.input[self.iCtrlIndex : -1]

    def _get_ik_ctrl_bound_refs_extra(self):
        """
        Resolve what objects to use to expand the bound of the ik ctrl using world-space positions.
        Default behavior is to use the hand and all it's children. (ex: fingers)
        :return: An array of pymel.general.PyNode instances.
        """
        jnt_hand = self.input[self.iCtrlIndex]
        return [jnt_hand] + jnt_hand.getChildren(allDescendents=True)

    def build(
        self,
        constraint=True,
        constraint_handle=True,
        setup_softik=True,
        *args,
        **kwargs
    ):
        """
        Build the ik system when needed
        :param ctrl_ik_orientation: A boolean to define if the ctrl should be zeroed.
        :param constraint: Bool to tell if we constraint the chain_jnt to the system
        :param constraint_handle: Bool to tell if we constraint the ik handle to the ik ctrl
        :param setup_softik: Bool to tell if we setup the soft ik on this system
        :param args: More args passed to the superclass
        :param kwargs: More kwargs passed to the superclass
        :return:
        """
        nomenclature_anm = self.get_nomenclature_anm()
        nomenclature_rig = self.get_nomenclature_rig()

        index_elbow = 1  # The elbow will always be on the second bone
        index_hand = self.iCtrlIndex

        jnt_elbow = self.chain_jnt[index_elbow]
        jnt_hand = self.chain_jnt[index_hand]

        # Compute swivel pos before any operation is done on the bones
        swivel_pos = self.calc_swivel_pos()

        # Create a group for the ik system
        # This group will be parentConstrained to the module parent.
        ikChainGrp_name = nomenclature_rig.resolve("ikChain")
        self._ikChainGrp = pymel.createNode(
            "transform", name=ikChainGrp_name, parent=self.grp_rig
        )
        self._ikChainGrp.setMatrix(
            self.chain.start.getMatrix(worldSpace=True), worldSpace=True
        )

        super(IK, self).build(*args, **kwargs)

        self._ikChainGrp.setParent(self.grp_rig)

        # Duplicate input chain (we don't want to move the hierarchy)
        self._chain_ik = self.chain.duplicate()
        i = 1
        for oIk in self._chain_ik:
            oIk.rename(nomenclature_rig.resolve("{0:02}".format(i)))
            i += 1
        self._chain_ik[0].setParent(
            self.parent
        )  # Trick the IK system (temporary solution)

        obj_e = self._chain_ik[index_hand]

        # Compute chain length
        self.chain_length = libPymel.PyNodeChain(
            self.chain[: self.iCtrlIndex + 1]
        ).length()
        # self.chain_length = self.chain.length()

        # Create ikChain
        self._chain_ik[0].setParent(self._ikChainGrp)
        # Create ikEffector
        ik_solver_name = nomenclature_rig.resolve("ikHandle")
        ik_effector_name = nomenclature_rig.resolve("ikEffector")
        self._ik_handle, _ik_effector = self.create_ik_handle()
        self._ik_handle.rename(ik_solver_name)
        self._ik_handle.setParent(self._ikChainGrp)
        _ik_effector.rename(ik_effector_name)

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

        # Create CtrlIK
        self.ctrl_ik = self.init_ctrl(self._CLASS_CTRL_IK, self.ctrl_ik)

        refs_bound_raycast = self._get_ik_ctrl_bound_refs_raycast()
        refs_bound_extra = self._get_ik_ctrl_bound_refs_extra()
        self.ctrl_ik.build(
            refs=refs_bound_extra,
            refs_raycast=refs_bound_raycast,
            geometries=self.rig.get_meshes(),
            parent_tm=ctrl_ik_tm,
        )  # refs is used by CtrlIkCtrl
        self.ctrl_ik.setParent(self.grp_anm)
        ctrl_ik_name = nomenclature_anm.resolve()
        self.ctrl_ik.rename(ctrl_ik_name)

        # Define CtrlIK transform
        ctrl_ik_t = obj_e.getTranslation(space="world")
        self.ctrl_ik.offset.setTranslation(ctrl_ik_t, space="world")

        if ctrl_ik_offset_rot:
            self.ctrl_ik.offset.setRotation(ctrl_ik_offset_rot)

        # Create space switch
        self.ctrl_ik.create_spaceswitch(self, self.parent, local_label="World")

        if ctrl_ik_rot:
            self.ctrl_ik.node.setRotation(ctrl_ik_rot, space="world")

        # Create the ik_handle_target that will control the ik_handle
        # This is allow us to override what control the main ik_handle
        # Mainly used for the Leg setup
        self._ik_handle_target = pymel.createNode(
            "transform", name=nomenclature_rig.resolve("ikHandleTarget")
        )
        self._ik_handle_target.setParent(self.grp_rig)
        pymel.pointConstraint(self.ctrl_ik, self._ik_handle_target)

        #
        # Create softIk node and connect user accessible attributes to it.
        #
        if setup_softik:
            self.setup_softik([self._ik_handle], [self._chain_ik])

        # Connect global scale
        pymel.connectAttr(self.grp_rig.globalScale, self._ikChainGrp.sx)
        pymel.connectAttr(self.grp_rig.globalScale, self._ikChainGrp.sy)
        pymel.connectAttr(self.grp_rig.globalScale, self._ikChainGrp.sz)

        # Setup swivel
        self.ctrl_swivel = self.setup_swivel_ctrl(
            self.ctrl_swivel, jnt_elbow, swivel_pos, self._ik_handle
        )
        self.swivelDistance = self.chain_length  # Used in ik/fk switch

        # Connect rig -> anm
        if constraint_handle:
            pymel.pointConstraint(self.ctrl_ik, self._ik_handle, maintainOffset=True)
        pymel.orientConstraint(self.ctrl_ik, obj_e, maintainOffset=True)

        if constraint:
            for source, target in zip(self._chain_ik, self.chain):
                pymel.parentConstraint(source, target)

    def unbuild(self):
        """
        Unbuild the ik system and reset the needed parameters
        :return:
        """
        self.chain_length = None
        self._chain_ik = None
        self.swivelDistance = None

        super(IK, self).unbuild()

    def parent_to(self, parent):
        """
        Parent the system
        :param parent: The node used to parent the system
        :return:
        """
        pymel.parentConstraint(parent, self._ikChainGrp, maintainOffset=True)

    def iter_ctrls(self):
        for yielded in super(IK, self).iter_ctrls():
            yield yielded
        yield self.ctrl_ik
        yield self.ctrl_swivel
        yield self.ctrl_swivel_quad


def register_plugin():
    return IK
