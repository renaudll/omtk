import collections

import pymel.core as pymel
from omtk.components_scripted.component_ik import ComponentIk
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classDagBuilder import DagBuilder
from omtk.core.classModule import Module
from omtk.core.classEntityAction import EntityAction
from omtk.libs import libAttr
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libRigging


class CtrlIk(BaseCtrl):
    """
    Base libs ctrl for the IK class. Used to drive libs handle. Inherit of the base ctrl class
    """
    kAttrName_State = 'ikFk'  # Attribute string shown in maya

    def __createNode__(self, *args, **kwargs):
        """
        Create the ctrl node itself
        :param args: More args passed to the superclass
        :param kwargs: More kwargs passed to the superclass
        :return: The created ctrl node
        """
        return super(CtrlIk, self).__createNode__(multiplier=1.5, *args, **kwargs)


class CtrlIkSwivel(BaseCtrl):
    """
    Base Ctrl libs swivel class implementation. Mostly used to do pole vector on an libs. Will create a ctrl with a line
    to facilitate pole vector visualization. Inherit of the base ctrl class
    """

    def __init__(self):
        super(CtrlIkSwivel, self).__init__()

        self._line_locator = None
        self._line_annotation = None

    def __createNode__(self, refs=None, size=None, line_target=True, offset=None, *args, **kwargs):
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
        targets, target_names, indexes = super(CtrlIkSwivel, self).get_spaceswitch_targets(module, *args, **kwargs)

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
        assert (self.node is not None)

        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs

        # Create line
        if line_target is True and ref is not None:
            # Create a spaceLocator so the annotation can hook itself to it.
            self._line_locator = pymel.spaceLocator()
            locator_shape = self._line_locator.getShape()
            pymel.pointConstraint(ref, self._line_locator)
            self._line_locator.setParent(self.node)
            self._line_locator.hide()

            self._line_annotation = pymel.createNode('annotationShape')
            annotation_transform = self._line_annotation.getParent()
            self._line_annotation.setParent(self.node, relative=True, shape=True)
            pymel.connectAttr(locator_shape.worldMatrix, self._line_annotation.dagObjectMatrix[0], force=True)
            pymel.delete(annotation_transform)

        return self.node


def _get_chain_length_from_local_tms(tms):
    """
    :param tms: A list of matrix pymel.Attribute representing local matrices.
    :return: A float3 pymel.Attribute.
    """
    i = iter(tms)
    next(i)  # skip first influence
    distances = [
        libRigging.create_utility_node(
            'distanceBetween',
            inMatrix1=attr_parent_tm,
            inMatrix2=attr_child_tm
        ).distance
        for attr_parent_tm, attr_child_tm in libPython.pairwise(tms)
        ]

    return libRigging.create_utility_node(
        'plusMinusAverage',
        input1D=distances
    ).output1D


def _create_joints_from_local_tms(tms):
    def _fn(tms):
        pymel.select(clear=True)
        prev = None
        for tm in tms:
            jnt = pymel.joint()

            # Hack: We don't use segmentScaleCompensate and never will...
            jnt.segmentScaleCompensate.set(False)
            jnt.inverseScale.disconnect()

            if prev:
                jnt.setParent(prev)
            prev = jnt

            u = libRigging.create_utility_node(
                'decomposeMatrix',
                inputMatrix=tm
            )
            # Note: We connect leaf (translateX) attributes instead of their parent (translate) for a reason.
            # Otherwise this will create weird updates with the ikEffector which seem to affect the parent attribute.
            pymel.connectAttr(u.outputTranslateX, jnt.translateX)
            pymel.connectAttr(u.outputTranslateY, jnt.translateY)
            pymel.connectAttr(u.outputTranslateZ, jnt.translateZ)
            pymel.connectAttr(u.outputRotateX, jnt.rotateX)
            pymel.connectAttr(u.outputRotateY, jnt.rotateY)
            pymel.connectAttr(u.outputRotateZ, jnt.rotateZ)
            pymel.connectAttr(u.outputScaleX, jnt.scaleX)
            pymel.connectAttr(u.outputScaleY, jnt.scaleY)
            pymel.connectAttr(u.outputScaleZ, jnt.scaleZ)
            yield jnt

    return list(_fn(tms))


# Todo: Support more complex IK limbs (ex: 2 knees)
class IK(Module):
    """
    Classical IK rig that support stretching and soft-libs.
    This is the base Ik module of the autorig. Support a basic 3 bones libs rotate-plane solver
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

    def validate(self):
        super(IK, self).validate()

        # Ensure our chain is not zero-length
        length = self._get_chain_length()
        if length < 0.0001:
            raise Exception("Chain is too short! Got {0}".format(length))

    def _create_ctrl_ik(self, *args, **kwargs):
        """
        Create an instance of the libs ctrl
        :param args: Args that could be passed to the Ik Ctrl creation
        :param kwargs: Kwargs that could be passed to the Ik Ctrl creation
        :return: The Ik controller
        """
        return self._CLASS_CTRL_IK(*args, **kwargs)

    @libPython.memoized_instancemethod
    def _get_chain_length(self, start_index=0, end_index=2):
        # todo: replace with a libPymel.PyNodeChain?
        chain_length = 0
        for i in range(start_index, end_index):
            chain_length += self.chain_jnt[i + 1].t.get().length()
        return chain_length

    def calc_swivel_pos(self, start_index=0, end_index=2):
        """
        This function is used to compute a swivel position. Can be used for multiple knee setup
        :param start_index: The start index of the _ik_chain that will be used to compute the swivel pos
        :param end_index: The end index of the _ik_chain that will be used to compute the swivel pos
        :return: The swivel position computed between the start and end
        """
        pos_start = self.chain_jnt[start_index].getTranslation(space='world')
        pos_end = self.chain_jnt[end_index].getTranslation(space='world')

        chain_length = self._get_chain_length(start_index=start_index, end_index=end_index)

        ratio = self.chain_jnt[start_index + 1].t.get().length() / chain_length
        pos_swivel_base = (pos_end - pos_start) * ratio + pos_start
        dir_swivel = (self.chain_jnt[start_index + 1].getTranslation(space='world') - pos_swivel_base).normal()
        return pos_swivel_base + (dir_swivel * chain_length)

    def create_ctrl_ik(self):
        nomenclature_anm = self.get_nomenclature_anm()
        obj_e = self.input[-1]

        # Resolve CtrlIK transform
        ctrl_ik_offset_tm, ctrl_ik_tm = self._get_ik_ctrl_tms()
        ctrl_ik_offset_rot = libPymel.get_rotation_from_matrix(ctrl_ik_offset_tm) if ctrl_ik_offset_tm else None
        ctrl_ik_rot = libPymel.get_rotation_from_matrix(ctrl_ik_tm) if ctrl_ik_tm else None

        # Create CtrlIK
        self.ctrl_ik = self.init_ctrl(self._CLASS_CTRL_IK, self.ctrl_ik)
        refs_bound_raycast = self._get_ik_ctrl_bound_refs_raycast()
        refs_bound_extra = self._get_ik_ctrl_bound_refs_extra()
        self.ctrl_ik.build(
            refs=refs_bound_extra,
            refs_raycast=refs_bound_raycast,
            geometries=self.rig.get_meshes(),
            parent_tm=ctrl_ik_tm
        )  # refs is used by CtrlIkCtrl
        self.ctrl_ik.setParent(self.grp_anm)
        self.ctrl_ik_name = nomenclature_anm.resolve()
        self.ctrl_ik.rename(self.ctrl_ik_name)

        # Define CtrlIK transform
        self.ctrl_ik_t = obj_e.getTranslation(space='world')
        self.ctrl_ik.offset.setTranslation(self.ctrl_ik_t, space='world')

        if ctrl_ik_offset_rot:
            self.ctrl_ik.offset.setRotation(ctrl_ik_offset_rot)

        # Create space switch
        self.ctrl_ik.create_spaceswitch(self, self.parent, local_label='World')

        if ctrl_ik_rot:
            self.ctrl_ik.node.setRotation(ctrl_ik_rot, space='world')

    def create_ctrl_swivel(self, ref, name='swivel', **kwargs):
        '''
        Create the swivel ctrl for the libs system
        :param base_ctrl: The ctrl used to setup the swivel, create one if needed
        :param ref: Reference object to position the swivel
        :param pos: The computed position of the swivel
        :param ik_handle: The handle to pole vector constraint
        :param name: Part name used to resolve the object rig name
        :param constraint: Do we contraint the libs handle to the swivel ctrl
        :param kwargs: Additionnal parameters
        :return: The created ctrl swivel
        '''
        nomenclature_anm = self.get_nomenclature_anm()
        pos = self.calc_swivel_pos()

        self.ctrl_swivel = self.init_ctrl(self._CLASS_CTRL_SWIVEL, self.ctrl_swivel)
        self.ctrl_swivel.build(refs=ref)
        self.ctrl_swivel.setParent(self.grp_anm)
        self.ctrl_swivel.rename(nomenclature_anm.resolve(name))
        self.ctrl_swivel._line_locator.rename(nomenclature_anm.resolve(name + 'LineLoc'))
        self.ctrl_swivel._line_annotation.rename(nomenclature_anm.resolve(name + 'LineAnn'))
        self.ctrl_swivel.offset.setTranslation(pos, space='world')
        self.ctrl_swivel.create_spaceswitch(self, self.parent, local_label='World')

    def _get_ik_ctrl_tms(self):
        """
        Compute the desired rotation for the libs ctrl.
        :return: A two-size tuple containing the transformation matrix for the ctrl offset and the ctrl itself.
        """
        inf_tm = self.input[self.iCtrlIndex].getMatrix(worldSpace=True)
        return inf_tm, inf_tm

    def _get_ik_ctrl_bound_refs_raycast(self):
        """
        Resolve what objects to use for computing the bound of the libs ctrl using raycasts.
        Default behavior is to use the hand and any inputs after. (ex: toes)
        :return: An array of pymel.general.PyNode instances.
        """
        return self.input[self.iCtrlIndex:-1]

    def _get_ik_ctrl_bound_refs_extra(self):
        """
        Resolve what objects to use to expand the bound of the libs ctrl using world-space positions.
        Default behavior is to use the hand and all it's children. (ex: fingers)
        :return: An array of pymel.general.PyNode instances.
        """
        jnt_hand = self.input[self.iCtrlIndex]
        return [jnt_hand] + jnt_hand.getChildren(allDescendents=True)

    def initialize_inputs(self):
        outputs = [
            pymel.joint(name='upperarm', position=[0, 0, 0]),
            pymel.joint(name='forearm', position=[0, -1, 1]),
            pymel.joint(name='hand', position=[0, -2, 0])
        ]
        self.input = outputs

    def build(self, *args, **kwargs):
        """
        Build the libs system when needed
        :param ctrl_ik_orientation: A boolean to define if the ctrl should be zeroed.
        :param constraint: Bool to tell if we constraint the chain_jnt to the system
        :param constraint_handle: Bool to tell if we constraint the libs handle to the libs ctrl
        :param setup_softik: Bool to tell if we setup the soft libs on this system
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


        # Create a group for the libs system
        # This group will be parentConstrained to the module parent.

        super(IK, self).build(*args, **kwargs)

        self.create_ctrl_ik()
        self.create_ctrl_swivel(jnt_elbow)

        # Add stretch and soft_ik attributes on ctrl_ik
        holder = self.ctrl_ik
        attr_soft_amount = libAttr.addAttr(
            holder,
            longName='softIkRatio', niceName='SoftIK',
            defaultValue=0,
            minValue=0, maxValue=50,
            hasMinValue=True, hasMaxValue=True,
            k=True,
        )

        attr_stretch_amount = libAttr.addAttr(
            holder,
            longName='stretch', niceName='Stretch',
            defaultValue=0,
            minValue=0, maxValue=1.0,
            hasMinValue=True, hasMaxValue=True,
            k=True,
        )

        self.swivelDistance = self.chain_length,  # used in ik/fk switch

        builder = DagBuilder()

        from omtk.libs import libComponents
        component = libComponents.create_component(
            ComponentIk,
            bindPoses=[obj.worldMatrix for obj in self.input],
            ikCtrlEndPos=self.ctrl_ik.worldMatrix,
            swivelPos=builder.get_world_translate(self.ctrl_swivel),
            softik=attr_soft_amount,
            stretch=attr_stretch_amount,

        )
        component.grp_dag.setParent(self.grp_rig)

        # more eleguant?
        for source, target in zip(component._attr_out_matrices, self.chain):
            builder.constraint_obj_to_tm(target, source, compensate_parent=True)

        self.components.append(component)  # todo: implement add_component?

    def unbuild(self):
        """
        Unbuild the libs system and reset the needed parameters
        :return:
        """
        self.swivelDistance = None

        super(IK, self).unbuild()

        # def parent_to(self, parent):
        """
        Parent the system
        :param parent: The node used to parent the system
        :return:
        """
        # pymel.parentConstraint(parent, self._ikChainGrp, maintainOffset=True)

    def iter_ctrls(self):
        for ctrl in super(IK, self).iter_ctrls():
            yield ctrl
        yield self.ctrl_ik
        yield self.ctrl_swivel
        yield self.ctrl_swivel_quad

    def iter_actions(self):
        for action in super(IK, self).iter_actions():
            yield action
        yield ActionCreateInfluences(self)


class ActionCreateInfluences(EntityAction):
    """
    Create influences in case no influences was provided.
    todo: maybe move it to module?
    """

    def get_name(self):
        return 'Create Influences'

    def execute(self):
        self.component.init_influences()

        # def iter_flags(self):
        #     for flag in super(ActionCreateInfluences, self).iter_flags():
        #         yield flag
        #     yield constants.ComponentActionFlags.trigger_network_export


def register_plugin():
    return IK
