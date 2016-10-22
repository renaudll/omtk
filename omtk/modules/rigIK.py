import functools
import collections
import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule import Module
from omtk.core.classNode import Node
from omtk.libs import libRigging
from omtk.libs import libAttr
from omtk.libs import libFormula
from omtk.libs import libPymel

class CtrlIk(BaseCtrl):
    """
    Base ik ctrl for the IK class. Used to drive ik handle. Inherit of the base ctrl class
    """
    kAttrName_State = 'ikFk' #Attribute string shown in maya

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


class SoftIkNode(Node):
    """
    Softik implementation class. Inherit of the base node class
    Note that the SoftIkNode is a dagnode so it will be automatically cleaned when the module is un-built.
    """
    def build(self, **kwargs):
        """
        Build function for the softik node
        :return: Nothing
        """
        super(SoftIkNode, self).build(**kwargs)
        formula = libFormula.Formula()
        fn_add_attr = functools.partial(libAttr.addAttr, self.node, hasMinValue=True, hasMaxValue=True)
        formula.inMatrixS = fn_add_attr(longName='inMatrixS', dt='matrix')
        formula.inMatrixE = fn_add_attr(longName='inMatrixE', dt='matrix')
        formula.inRatio = fn_add_attr(longName='inRatio', at='float')
        formula.inStretch = fn_add_attr(longName='inStretch', at='float')
        formula.inChainLength = fn_add_attr(longName='inChainLength', at='float', defaultValue=1.0)

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
        attr_ratio = fn_add_attr(longName='outRatio', at='float')
        pymel.connectAttr(formula.outRatio, attr_ratio)

        attr_stretch = fn_add_attr(longName='outStretch', at='float')
        pymel.connectAttr(formula.outStretch, attr_stretch)


# Todo: Support more complex IK limbs (ex: 2 knees)
class IK(Module):
    """
    Classical IK rig that support stretching and soft-ik.
    This is the base Ik module of the autorig. Support a basic 3 bones ik rotate-plane solver
    with the creation of a controller. Also used the softik implementation. Inherit of the module class
    to be able to used it in the autorig UI
    """
    _CLASS_CTRL_IK = CtrlIk #Ik Ctrl class
    _CLASS_CTRL_SWIVEL = CtrlIkSwivel #Ik Swivel Ctrl class

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
            chain_length += self.chain_jnt[i+1].t.get().length()

        ratio = self.chain_jnt[start_index + 1].t.get().length() / chain_length
        pos_swivel_base = (pos_end - pos_start) * ratio + pos_start
        dir_swivel = (self.chain_jnt[start_index + 1].getTranslation(space='world') - pos_swivel_base).normal()
        return pos_swivel_base + (dir_swivel * chain_length)

    def setup_softik(self, ik_handle_to_constraint, stretch_chain):
        """
        Setup the softik system a ik system
        :param ik_handle_to_constraint: The ik handle to constraint on the soft ik network (Can be more than one)
        :param stretch_chain: The chain on which the stretch will be connected
        :return: Nothing
        """
        nomenclature_rig = self.get_nomenclature_rig()

        oAttHolder = self.ctrl_ik
        fnAddAttr = functools.partial(libAttr.addAttr, hasMinValue=True, hasMaxValue=True)
        attInRatio = fnAddAttr(oAttHolder, longName='softIkRatio', niceName='SoftIK', defaultValue=0, minValue=0,
                               maxValue=50, k=True)
        attInStretch = fnAddAttr(oAttHolder, longName='stretch', niceName='Stretch', defaultValue=0, minValue=0,
                                 maxValue=1.0, k=True)
        # Adjust the ratio in percentage so animators understand that 0.03 is 3%
        attInRatio = libRigging.create_utility_node('multiplyDivide', input1X=attInRatio, input2X=0.01).outputX

        # Create and configure SoftIK solver
        soft_ik_network_name = nomenclature_rig.resolve('softik')
        soft_ik_network = SoftIkNode()
        soft_ik_network.build(name=soft_ik_network_name)
        soft_ik_network.setParent(self.grp_rig)

        pymel.connectAttr(attInRatio, soft_ik_network.inRatio)
        pymel.connectAttr(attInStretch, soft_ik_network.inStretch)
        pymel.connectAttr(self._ikChainGrp.worldMatrix, soft_ik_network.inMatrixS)
        pymel.connectAttr(self._ik_handle_target.worldMatrix, soft_ik_network.inMatrixE)
        attr_distance = libFormula.parse('distance*globalScale',
                                         distance=self.chain_length,
                                         globalScale=self.grp_rig.globalScale)
        pymel.connectAttr(attr_distance, soft_ik_network.inChainLength)

        attOutRatio = soft_ik_network.outRatio
        attOutRatioInv = libRigging.create_utility_node('reverse', inputX=soft_ik_network.outRatio).outputX
        #TODO: Improve softik ratio when using multiple ik handle. Not the same ratio will be used depending of the angle
        for handle in ik_handle_to_constraint:
            pointConstraint = pymel.pointConstraint(self._ik_handle_target, self._ikChainGrp, handle)
            pointConstraint.rename(pointConstraint.name().replace('pointConstraint', 'softIkConstraint'))
            weight_inn, weight_out = pointConstraint.getWeightAliasList()[-2:] #Ensure to get the latest target added
            pymel.connectAttr(attOutRatio, weight_inn)
            pymel.connectAttr(attOutRatioInv, weight_out)

        # Connect stretch
        for i in range(1, self.iCtrlIndex+1):
            obj = stretch_chain[i]
            util_get_t = libRigging.create_utility_node('multiplyDivide',
                                               input1X=soft_ik_network.outStretch,
                                               input1Y=soft_ik_network.outStretch,
                                               input1Z=soft_ik_network.outStretch,
                                               input2=obj.t.get())
            pymel.connectAttr(util_get_t.outputX, obj.tx, force=True)
            pymel.connectAttr(util_get_t.outputY, obj.ty, force=True)
            pymel.connectAttr(util_get_t.outputZ, obj.tz, force=True)
        
        return soft_ik_network

    def create_ik_handle(self, solver='ikRPsolver'):
        """
        Create a ik handle for a specific ik setup. Need to be overrided by children class to implement the good behavior
        :return: Return the created ik handle and effector
        """
        #Since the base Ik will always be two bone, we can use the fact that the effector is after the elbow
        start = self._chain_ik[0]
        end = self._chain_ik[self.iCtrlIndex]
        ik_handle, ik_effector = pymel.ikHandle(startJoint=start, endEffector=end,
                                                       solver=solver)
        return ik_handle, ik_effector

    def setup_swivel_ctrl(self, base_ctrl, ref, pos, ik_handle, name='swivel', constraint=True, **kwargs):
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

        ctrl_swivel = base_ctrl
        if not isinstance(base_ctrl, self._CLASS_CTRL_SWIVEL):
            ctrl_swivel = self._CLASS_CTRL_SWIVEL()
        ctrl_swivel.build(refs=ref)
        ctrl_swivel.setParent(self.grp_anm)
        ctrl_swivel.rename(nomenclature_anm.resolve(name))
        ctrl_swivel._line_locator.rename(nomenclature_anm.resolve(name+'LineLoc'))
        ctrl_swivel._line_annotation.rename(nomenclature_anm.resolve(name+'LineAnn'))
        ctrl_swivel.offset.setTranslation(pos, space='world')
        ctrl_swivel.create_spaceswitch(self, self.parent, default_name='World')

        if constraint:
            #Pole vector contraint the swivel to the ik handle
            pymel.poleVectorConstraint(ctrl_swivel, self._ik_handle)

        return ctrl_swivel

    def build(self, ctrl_ik_orientation=None, constraint=True, constraint_handle=True, setup_softik=True, *args, **kwargs):
        """
        Build the ik system when needed
        :param ctrl_ik_orientation: The ik ctrl orientation override
        :param constraint: Bool to tell if we constraint the chain_jnt to the system
        :param constraint_handle: Bool to tell if we constraint the ik handle to the ik ctrl
        :param setup_softik: Bool to tell if we setup the soft ik on this system
        :param args: More args passed to the superclass
        :param kwargs: More kwargs passed to the superclass
        :return:
        """
        nomenclature_anm = self.get_nomenclature_anm()
        nomenclature_rig = self.get_nomenclature_rig()

        index_elbow = 1 #The elbow will always be on the second bone
        index_hand = self.iCtrlIndex

        jnt_elbow = self.chain_jnt[index_elbow]
        jnt_hand = self.chain_jnt[index_hand]

        #Compute swivel pos before any operation is done on the bones
        swivel_pos = self.calc_swivel_pos()

        # Create a group for the ik system
        # This group will be parentConstrained to the module parent.
        ikChainGrp_name = nomenclature_rig.resolve('ikChain')
        self._ikChainGrp = pymel.createNode('transform', name=ikChainGrp_name, parent=self.grp_rig)
        self._ikChainGrp.setMatrix(self.chain.start.getMatrix(worldSpace=True), worldSpace=True)

        super(IK, self).build(*args, **kwargs)

        self._ikChainGrp.setParent(self.grp_rig)

        # Duplicate input chain (we don't want to move the hierarchy)
        #self._chain_ik = pymel.duplicate(list(self.chain_jnt), renameChildren=True, parentOnly=True)
        self._chain_ik = self.chain.duplicate()
        i = 1
        for oIk in self._chain_ik:
            oIk.rename(nomenclature_rig.resolve('{0:02}'.format(i)))
            i += 1
        self._chain_ik[0].setParent(self.parent)  # Trick the IK system (temporary solution)

        obj_e = self._chain_ik[index_hand]

        # Compute chain length
        self.chain_length = libPymel.PyNodeChain(self.chain[:self.iCtrlIndex+1]).length()
        #self.chain_length = self.chain.length()

        # Create ikChain
        self._chain_ik[0].setParent(self._ikChainGrp)
        # Create ikEffector
        ik_solver_name = nomenclature_rig.resolve('ikHandle')
        ik_effector_name = nomenclature_rig.resolve('ikEffector')
        self._ik_handle, _ik_effector = self.create_ik_handle()
        self._ik_handle.rename(ik_solver_name)
        self._ik_handle.setParent(self._ikChainGrp)
        _ik_effector.rename(ik_effector_name)

        # Create CtrlIK
        if not isinstance(self.ctrl_ik, self._CLASS_CTRL_IK):
            self.ctrl_ik = self._CLASS_CTRL_IK()
        ctrl_ik_refs = [jnt_hand] + jnt_hand.getChildren(allDescendents=True)
        self.ctrl_ik.build(refs=ctrl_ik_refs, geometries=self.rig.get_meshes())  # refs is used by CtrlIkCtrl
        self.ctrl_ik.setParent(self.grp_anm)
        ctrl_ik_name = nomenclature_anm.resolve('ik')
        self.ctrl_ik.rename(ctrl_ik_name)
        self.ctrl_ik.offset.setTranslation(obj_e.getTranslation(space='world'), space='world')

        # Set ctrl_ik_orientation
        if ctrl_ik_orientation is None:
            ctrl_ik_orientation = obj_e.getRotation(space='world')
        self.ctrl_ik.offset.setRotation(ctrl_ik_orientation, space='world')

        self.ctrl_ik.create_spaceswitch(self, self.parent, default_name='World')

        # Create the ik_handle_target that will control the ik_handle
        # This is allow us to override what control the main ik_handle
        # Mainly used for the Leg setup
        self._ik_handle_target = pymel.createNode('transform', name=nomenclature_rig.resolve('ikHandleTarget'))
        self._ik_handle_target.setParent(self.grp_rig)
        pymel.pointConstraint(self.ctrl_ik, self._ik_handle_target)

        #
        # Create softIk node and connect user accessible attributes to it.
        #
        if setup_softik:
            self.setup_softik([self._ik_handle], self._chain_ik)

        # Connect global scale
        pymel.connectAttr(self.grp_rig.globalScale, self._ikChainGrp.sx)
        pymel.connectAttr(self.grp_rig.globalScale, self._ikChainGrp.sy)
        pymel.connectAttr(self.grp_rig.globalScale, self._ikChainGrp.sz)

        #Setup swivel
        self.ctrl_swivel = self.setup_swivel_ctrl(self.ctrl_swivel, jnt_elbow, swivel_pos, self._ik_handle)
        self.swivelDistance = self.chain_length  # Used in ik/fk switch
        #pymel.poleVectorConstraint(flip_swivel_ref, self._ik_handle)

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
        for ctrl in super(IK, self).iter_ctrls():
            yield ctrl
        yield self.ctrl_ik
        yield self.ctrl_swivel
        yield self.ctrl_swivel_quad


def register_plugin():
    return IK
