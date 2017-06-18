import collections

import pymel.core as pymel
from omtk.core.classComponent import Component
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classDagBuilder import DagBuilder
from omtk.core.classModule import Module
from omtk.libs import libAttr
from omtk.libs import libFormula
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libRigging

from omtk import constants


def _get_vector_from_axis(axis):
    if axis == constants.Axis.x:
        return pymel.datatypes.Vector.xAxis
    if axis == constants.Axis.y:
        return pymel.datatypes.Vector.yAxis
    if axis == constants.Axis.z:
        return pymel.datatypes.Vector.zAxis
    raise IOError("Unexpected constant. Expected X, Y, or Z. Got {}".format(axis))


class CtrlIk(BaseCtrl):
    """
    Base ik ctrl for the IK class. Used to drive ik handle. Inherit of the base ctrl class
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
    Base Ctrl ik swivel class implementation. Mostly used to do pole vector on an ik. Will create a ctrl with a line
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


class ComponentSoftIk(Component):
    """
    Softik implementation class.

    inputs:
    - inMatrixS: The world matrix of the arm start.
    - inMatrixE: The world matrix of the arm end.
    - inRatio: The amount to soft ik to use.
    - inStretch: The amount of stretch to use.
    - inChainLength: A float representing the length of the Arm.

    outputs:
    - outRatio: A float representing ???
    - outStretch: A float representing a stretch multiplier. ???

    todos:
    - Add support for n-length chain. Soft-IK might not trigger earlier on 4+ length chain
    depending on the smalest angles.
    """

    def __init__(self, **kwargs):
        super(ComponentSoftIk, self).__init__(**kwargs)

        # Pre-define protected input attributes for scripted usage.
        self._attr_inn_matrix_s = None
        self._attr_inn_matrix_e = None
        self._attr_inn_ratio = None
        self._attr_inn_stretch = None
        self._attr_inn_length = None

        # Pre-define protected output attributes for scripted usage.
        self._attr_out_ratio = None
        self._attr_out_stretch = None

    def build(self, **kwargs):
        """
        Build function for the softik node
        :return: Nothing
        """
        super(ComponentSoftIk, self).build(**kwargs)
        formula = libFormula.Formula()

        # Create input attributes
        self._attr_inn_matrix_s = self.add_input_attr('inMatrixS', dt='matrix')
        self._attr_inn_matrix_e = self.add_input_attr('inMatrixE', dt='matrix')
        self._attr_inn_ratio = self.add_input_attr('inRatio', at='float')
        self._attr_inn_stretch = self.add_input_attr('inStretch', at='float')
        self._attr_inn_length = self.add_input_attr('inChainLength', at='float', defaultValue=1.0)

        # Create output attributes
        self._attr_out_ratio = self.add_output_attr('outRatio', at='float')
        self._attr_out_stretch = self.add_output_attr('outStretch', at='float')

        # Generate network using libFormula since we are fancy peoples
        formula.inMatrixS = self._attr_inn_matrix_s
        formula.inMatrixE = self._attr_inn_matrix_e
        formula.inRatio = self._attr_inn_ratio
        formula.inStretch = self._attr_inn_stretch
        formula.inChainLength = self._attr_inn_length

        # inDistance is the distance between the start of the chain and the ikCtrl
        formula.inDistance = "inMatrixS~inMatrixE"
        # distanceSoft is the distance before distanceMax where the softIK kick in.
        # ex: For a chain of length 10.0 with a ratio of 0.1, the distanceSoft will be 1.0.
        formula.distanceSoft = "inChainLength*inRatio"
        # distanceSafe is the distance where there's no softIK.
        # ex: For a chain of length 10.0 with a ratio of 0.1, the distanceSafe will be 9.0.
        formula.distanceSafe = "inChainLength-distanceSoft"
        # This represent the soft-ik state
        # When the soft-ik kick in, the value is 0.0.
        # When the stretch kick in, the value is 1.0.
        # |-----------|-----------|----------|
        # -1          0.0         1.0         +++
        # -dBase      dSafe       dMax
        # Hack: Prevent potential division by zero.
        # Originally we were using a condition, however in Maya 2016+ in Parallel or Serial evaluation mode, this
        # somehow evalated the division even when the condition was False.
        formula.distanceSoftClamped = libRigging.create_utility_node('clamp',
                                                                     inputR=formula.distanceSoft,
                                                                     minR=0.0001,
                                                                     maxR=999
                                                                     ).outputR
        formula.deltaSafeSoft = "(inDistance-distanceSafe)/distanceSoftClamped"

        # outDistanceSoft is the desired ikEffector distance from the chain start after aplying the soft-ik
        # If there's no stretch, this will be directly applied to the ikEffector.
        # If there's stretch, this will be used to compute the amount of stretch needed to reach the ikCtrl
        # while preserving the shape.
        formula.outDistanceSoft = "(distanceSoft*(1-(e^(deltaSafeSoft*-1))))+distanceSafe"

        # Affect ikEffector distance only where inDistance if bigger than distanceSafe.
        formula.outDistance = libRigging.create_utility_node('condition',
                                                             operation=2,
                                                             firstTerm=formula.deltaSafeSoft,
                                                             secondTerm=0.0,
                                                             colorIfTrueR=formula.outDistanceSoft,
                                                             colorIfFalseR=formula.inDistance
                                                             ).outColorR
        # Affect ikEffector when we're not using stretching
        formula.outDistance = libRigging.create_utility_node('blendTwoAttr',
                                                             input=[formula.outDistance, formula.inDistance],
                                                             attributesBlender=formula.inStretch).output

        #
        # Handle Stretching
        #

        # If we're using softIk AND stretchIk, we'll use the outRatioSoft to stretch the joints enough so
        # that the ikEffector reach the ikCtrl.
        formula.outStretch = "inDistance/outDistanceSoft"

        # Apply the softIK only AFTER the distanceSafe
        formula.outStretch = libRigging.create_utility_node('condition',
                                                            operation=2,
                                                            firstTerm=formula.inDistance,
                                                            secondTerm=formula.distanceSafe,
                                                            colorIfTrueR=formula.outStretch,
                                                            colorIfFalseR=1.0
                                                            ).outColorR

        # Apply stretching only if inStretch is ON
        formula.outStretch = libRigging.create_utility_node('blendTwoAttr',
                                                            input=[1.0, formula.outStretch],
                                                            attributesBlender=formula.inStretch).output

        #
        # Connect outRatio and outStretch to our softIkNode
        #
        # fnAddAttr(longName='outTranslation', dt='float3')
        formula.outRatio = "outDistance/inDistance"
        pymel.connectAttr(formula.outRatio, self._attr_out_ratio)
        pymel.connectAttr(formula.outStretch, self._attr_out_stretch)


class ComponentIkBuilder(DagBuilder):
    def __init__(self, attr_chain_bind, attr_hook, attr_ctrl_tm, attr_swivel_pos, attr_stretch_amount,
                 attr_softik_amount):
        super(ComponentIkBuilder, self).__init__()

        # Internal variables
        self._jnts = None
        self._attr_chain_length = None
        self._grp_ik_handle = None
        self._grp_ik_effector = None
        self._local_tms = None

        # Pre-define inputs for scripted usage.
        self.attr_inn_chain_tms = attr_chain_bind
        self.attr_inn_hook = attr_hook
        self.attr_inn_ctrl_tm = attr_ctrl_tm
        self.attr_inn_swivel_pos = attr_swivel_pos
        self.attr_inn_start_pos = None
        self.attr_inn_end_pos = None
        self.attr_inn_stretch_amount = attr_stretch_amount
        self.attr_inn_softik_amount = attr_softik_amount
        self.attr_out_chain = None

    def create_ik_handle(self, obj_s, obj_e, solver_type='ikRPsolver'):
        """
        Create a ik handle for a specific ik setup. Need to be overrided by children class to implement the good behavior
        :return: Return the created ik handle and effector
        """
        ik_handle, ik_effector = pymel.ikHandle(
            startJoint=obj_s,
            endEffector=obj_e,
            solver=solver_type
        )
        return ik_handle, ik_effector

    def setup_softik(self):
        """
        Setup the softik system a ik system
        :param ik_handle_to_constraint: A list of ik handles to constraint on the soft-ik network.
        :param stretch_chains: A list of chains to connect the stretch to.
        :return: Nothing
        """
        solver = ComponentSoftIk(name='softik')
        solver.build()

        # Connect component inputs
        tm_s = self.attr_inn_chain_tms[0]
        tm_e = self.attr_inn_chain_tms[2]  # todo: find a way of using -1?
        pymel.connectAttr(tm_s, solver._attr_inn_matrix_s)
        pymel.connectAttr(tm_e, solver._attr_inn_matrix_e)
        pymel.connectAttr(self.attr_inn_softik_amount, solver._attr_inn_ratio)
        pymel.connectAttr(self.attr_inn_stretch_amount, solver._attr_inn_stretch)
        pymel.connectAttr(self._attr_chain_length, solver._attr_inn_length)

        # Connect component outputs

        # The softIK affect the position of the ikEffector.
        # Normally this position is always at the end of the chain, however the ikSolver
        # can change this when it's being activated.

        attr_current_s_tm = self.create_utility_node(
            'multMatrix',
            matrixIn=(
                self.attr_inn_chain_tms[0],
                self.attr_inn_hook
            )
        ).matrixSum
        util_decompose_current_s = self.create_utility_node(
            'decomposeMatrix',
            inputMatrix=attr_current_s_tm
        )
        attr_current_s_pos = util_decompose_current_s.outputTranslate

        # todo: use decorator?
        attr_current_e_pos = self.create_utility_node(
            'decomposeMatrix',
            inputMatrix=self.attr_inn_ctrl_tm
        ).outputTranslate

        attr_ik_handle_pos = self.create_utility_node(
            'blendColors',
            color1=attr_current_e_pos,
            color2=attr_current_s_pos,
            blender=solver._attr_out_ratio
        ).output
        pymel.connectAttr(attr_ik_handle_pos, self._grp_ik_handle.translate)

        # Connect stretch
        for bind_tm, obj in zip(self._local_tms, self._jnts):
            util_get_t = libRigging.create_utility_node(
                'multiplyDivide',
                input1X=solver._attr_out_stretch,
                input1Y=solver._attr_out_stretch,
                input1Z=solver._attr_out_stretch,
                input2=self.create_utility_node(
                    'decomposeMatrix',
                    inputMatrix=bind_tm
                ).outputTranslate
            )
            pymel.connectAttr(util_get_t.output, obj.translate, force=True)

        return [jnt.worldMatrix for jnt in self._jnts]

    def build(self, grp_dag, nomenclature=None):
        # todo: how do we handle the nomenclature?
        # solution: we do not, this is all in a single level.

        ####

        #
        # Resolve the length of the arm
        #
        self._local_tms = self.get_chain_tms(self.attr_inn_chain_tms)

        self._attr_chain_length = _get_chain_length_from_local_tms(self._local_tms)

        #
        # Vanilla maya ikSolver node need joints for computation...
        #
        self._jnts = _create_joints_from_local_tms(self._local_tms)
        self._jnts[0].setParent(grp_dag)

        # Create ikChain
        self._grp_ik_handle, self._grp_ik_effector = self.create_ik_handle(
            self._jnts[0],
            self._jnts[-1]
        )
        self._grp_ik_handle.rename('handle')
        self._grp_ik_effector.rename('effector')
        self._grp_ik_handle.setParent(grp_dag)

        #
        # Create softIk node and connect user accessible attributes to it.
        #
        self.setup_softik()

        # Setup swivel
        self.grp_swivel = pymel.createNode('transform', name='swivel', parent=grp_dag)
        pymel.connectAttr(self.attr_inn_swivel_pos, self.grp_swivel.translate)
        pymel.poleVectorConstraint(self.grp_swivel, self._grp_ik_handle)

        return [jnt.worldMatrix for jnt in self._jnts]


class ComponentIk(Component):
    """
    A scripted component that allow the generation of multi-joint IK system.
    This also include stretching and soft-ik.

    inputs:
    - bindPoses: A list of world matrices representing the bind pose of the influence chain.
    - ikCtrlEndPos: A world vector for the position of the end effector.
    - ikCtrlSwivelPos: A world vector fot eh position of the swivel controller.

    outputs:
    - out: A list of world matrices of the same size than bindPoses for the output influences.
    """
    need_grp_dag = True

    def __init__(self, **kwargs):
        super(ComponentIk, self).__init__(**kwargs)

        # Pre-define inputs for scripted usage.
        self._attr_inn_chain = None
        self._attr_inn_hook_tm = None
        self._attr_ctrl_tm = None
        self._attr_ctrl_swivel_pos = None
        self._attr_inn_stretch = None
        self._attr_inn_softik = None
        self._attr_out_matrices = None

    def _create_io(self):
        self._attr_inn_chain = self.add_input_attr('bindPoses', dt='matrix', multi=True)
        self._attr_inn_hook_tm = self.add_input_attr('hook', at='matrix')
        self._attr_ctrl_tm = self.add_input_attr('ikCtrlEndPos', at='matrix')
        self._attr_ctrl_swivel_pos = self.add_input_attr('swivelPos', dt='double3')  # translate datatype
        self._attr_inn_stretch = self.add_input_attr('stretch', at='float')
        self._attr_inn_softik = self.add_input_attr('softik', at='float')
        self._attr_out_matrices = self.add_output_attr('out', at='matrix', multi=True)

        # hack for now
        for i in xrange(3):
            self._attr_inn_chain[i].set(pymel.datatypes.Matrix())

        # hack for now
        for i in xrange(3):
            self._attr_out_matrices[i].set(pymel.datatypes.Matrix())

    def build(self):
        super(ComponentIk, self).build()
        self._create_io()
        builder = ComponentIkBuilder(
            attr_chain_bind=self._attr_inn_chain,
            attr_hook=self._attr_inn_hook_tm,
            attr_ctrl_tm=self._attr_ctrl_tm,
            attr_swivel_pos=self._attr_ctrl_swivel_pos,
            attr_stretch_amount=self._attr_inn_stretch,
            attr_softik_amount=self._attr_inn_softik
        )

        attr_out_chain = builder.build(self.grp_dag)
        for attr_src, attr_dst in zip(attr_out_chain, self._attr_out_matrices):
            pymel.connectAttr(attr_src, attr_dst)


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
        pos_start = self.chain_jnt[start_index].getTranslation(space='world')
        pos_end = self.chain_jnt[end_index].getTranslation(space='world')

        chain_length = 0
        for i in range(start_index, end_index):
            chain_length += self.chain_jnt[i + 1].t.get().length()

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
        Create the swivel ctrl for the ik system
        :param base_ctrl: The ctrl used to setup the swivel, create one if needed
        :param ref: Reference object to position the swivel
        :param pos: The computed position of the swivel
        :param ik_handle: The handle to pole vector constraint
        :param name: Part name used to resolve the object rig name
        :param constraint: Do we contraint the ik handle to the swivel ctrl
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
        return self.input[self.iCtrlIndex:-1]

    def _get_ik_ctrl_bound_refs_extra(self):
        """
        Resolve what objects to use to expand the bound of the ik ctrl using world-space positions.
        Default behavior is to use the hand and all it's children. (ex: fingers)
        :return: An array of pymel.general.PyNode instances.
        """
        jnt_hand = self.input[self.iCtrlIndex]
        return [jnt_hand] + jnt_hand.getChildren(allDescendents=True)

    def build(self, *args, **kwargs):
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


        # Create a group for the ik system
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

        builder = DagBuilder()

        solver = ComponentIk()
        solver.build()
        solver.grp_dag.setParent(self.grp_rig)

        # Connect inputs
        for i, jnt in enumerate(self.input):
            solver._attr_inn_chain[i].set(jnt.worldMatrix.get())
            # pymel.connectAttr(jnt.worldMatrix, solver._attr_inn_chain[i])

        pymel.connectAttr(self.ctrl_ik.worldMatrix, solver._attr_ctrl_tm)
        pymel.connectAttr(builder.get_world_translate(self.ctrl_swivel), solver._attr_ctrl_swivel_pos)
        pymel.connectAttr(attr_soft_amount, solver._attr_inn_softik)
        pymel.connectAttr(attr_stretch_amount, solver._attr_inn_stretch)

        self.swivelDistance = self.chain_length  # Used in ik/fk switch

        for source, target in zip(solver._attr_out_matrices, self.chain):
            # u = libRigging.create_utility_node(
            #     'decomposeMatrix',
            #     inputMatrix=source
            # )
            # pymel.connectAttr(u.outputTranslate, target.translate)
            # pymel.connectAttr(u.outputRotate, target.rotate)
            # pymel.connectAttr(u.outputScale, target.scale)
            builder.constraint_obj_to_tm(target, source, compensate_parent=True)


    def unbuild(self):
        """
        Unbuild the ik system and reset the needed parameters
        :return:
        """
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
        for ctrl in super(IK, self).iter_ctrls():
            yield ctrl
        yield self.ctrl_ik
        yield self.ctrl_swivel
        yield self.ctrl_swivel_quad


def register_plugin():
    return IK
