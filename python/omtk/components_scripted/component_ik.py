import collections

import pymel.core as pymel
from omtk.core.classComponent import ComponentScripted
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classDagBuilder import DagBuilder
from omtk.core.classModule import Module
from omtk.libs import libAttr
from omtk.libs import libFormula
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libRigging

from omtk import constants


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


class ComponentSoftIk(ComponentScripted):
    """
    Softik implementation class.

    inputs:
    - inMatrixS: The world matrix of the arm start.
    - inMatrixE: The world matrix of the arm end.
    - inRatio: The amount to soft libs to use.
    - inStretch: The amount of stretch to use.
    - inChainLength: A float representing the length of the Arm.

    outputs:
    - outRatio: A float representing ???
    - outStretch: A float representing a stretch multiplier. ???

    todos:
    - Add support for n-length chain. Soft-IK might not trigger earlier on 4+ length chain
    depending on the smalest angles.
    """
    component_name = '_SoftIkSolver'
    component_id = constants.BuiltInComponentIds.IkSoftSolver

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
        # This represent the soft-libs state
        # When the soft-libs kick in, the value is 0.0.
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

        # outDistanceSoft is the desired ikEffector distance from the chain start after aplying the soft-libs
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
        Create a libs handle for a specific libs setup. Need to be overrided by children class to implement the good behavior
        :return: Return the created libs handle and effector
        """
        ik_handle, ik_effector = pymel.ikHandle(
            startJoint=obj_s,
            endEffector=obj_e,
            solver=solver_type
        )
        return ik_handle, ik_effector

    def setup_softik(self):
        """
        Setup the softik system a libs system
        :param ik_handle_to_constraint: A list of libs handles to constraint on the soft-libs network.
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


class ComponentIk(ComponentScripted):
    """
    A scripted component that allow the generation of multi-joint IK system.
    This also include stretching and soft-libs.

    inputs:
    - bindPoses: A list of world matrices representing the bind pose of the influence chain.
    - ikCtrlEndPos: A world vector for the position of the end effector.
    - ikCtrlSwivelPos: A world vector fot eh position of the swivel controller.

    outputs:
    - out: A list of world matrices of the same size than bindPoses for the output influences.
    """
    need_grp_dag = True
    component_name = 'IK'
    component_id = constants.BuiltInComponentIds.Ik

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


def register_plugin():
    return ComponentIk
