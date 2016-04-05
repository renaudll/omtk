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
    kAttrName_State = 'ikFk'

    def __createNode__(self, *args, **kwargs):
        return super(CtrlIk, self).__createNode__(multiplier=1.5, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(CtrlIk, self).__init__(*args, **kwargs)
        self.m_attState = None

    def build(self, *args, **kwargs):
        super(CtrlIk, self).build(*args, **kwargs)
        assert (self.node is not None)
        pymel.addAttr(self.node, longName=self.kAttrName_State)
        self.m_attState = getattr(self.node, self.kAttrName_State)
        return self.node

    def unbuild(self, *args, **kwargs):
        super(CtrlIk, self).unbuild(*args, **kwargs)
        self.m_attState = None


class CtrlIkSwivel(BaseCtrl):

    def __createNode__(self, refs=None, size=None, line_target=True, offset=None, *args, **kwargs):
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

        # Create line
        if line_target is True:
            # Create a spaceLocator so the annotation can hook itself to it.
            locator_transform = pymel.spaceLocator()
            locator_shape = locator_transform.getShape()
            pymel.pointConstraint(ref, locator_transform)
            locator_transform.setParent(node)
            locator_transform.hide()

            annotation_shape = pymel.createNode('annotationShape')
            annotation_transform = annotation_shape.getParent()
            annotation_shape.setParent(node, relative=True, shape=True)
            pymel.connectAttr(locator_shape.worldMatrix, annotation_shape.dagObjectMatrix[0], force=True)
            pymel.delete(annotation_transform)

        return node

    def build(self, line_target=False, *args, **kwargs):
        super(CtrlIkSwivel, self).build(*args, **kwargs)
        assert (self.node is not None)

        # Create line
        if line_target is True:
            ctrl_shape = self.node.getShape()
            line_shape = pymel.createNode('annotationShape')
            line_transform = line_shape.getParent()
            pymel.connectAttr(ctrl_shape.worldMatrix, line_shape.dagObjectMatrix[0], force=True)
            line_transform.setParent(self.offset)
            pymel.pointConstraint(line_target, line_transform)

        return self.node


class SoftIkNode(Node):
    def __createNode__(self, *args, **kwargs):
        return pymel.createNode('network')

    def build(self):
        super(SoftIkNode, self).build()
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
        formula.deltaSafeSoft = "(inDistance-distanceSafe)/distanceSoft"
        # Hack: Prevent potential division by zero when soft-ik is desactivated
        formula.deltaSafeSoft = libRigging.create_utility_node('condition',
                                                               firstTerm=formula.distanceSoft,
                                                               secondTerm=0.0,
                                                               colorIfTrueR=0.0,
                                                               colorIfFalseR=formula.deltaSafeSoft
                                                               ).outColorR

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
    _CLASS_CTRL_IK = CtrlIk
    _CLASS_CTRL_SWIVEL = CtrlIkSwivel

    def __init__(self, *args, **kwargs):
        super(IK, self).__init__(*args, **kwargs)
        self.iCtrlIndex = 2
        self.ctrl_ik = None
        self.ctrl_swivel = None
        self.chain_length = None
        self._chain_ik = None

    def _create_ctrl_ik(self, *args, **kwargs):
        return CtrlIk(*args, **kwargs)

    def calc_swivel_pos(self):
        pos_start = self.chain_jnt[0].getTranslation(space='world')
        pos_end = self.chain_jnt[self.iCtrlIndex].getTranslation(space='world')

        chain_length = 0
        for i in range(self.iCtrlIndex):
            chain_length += self.chain_jnt[i+1].t.get().length()

        ratio = self.chain_jnt[1].t.get().length() / chain_length
        pos_swivel_base = (pos_end - pos_start) * ratio + pos_start
        dir_swivel = (self.chain_jnt[1].getTranslation(space='world') - pos_swivel_base).normal()
        return pos_swivel_base + (dir_swivel * chain_length)

    def build(self, rig, ctrl_ik_orientation=None, constraint=False, *args, **kwargs):
        nomenclature_anm = self.get_nomenclature_anm(rig)
        nomenclature_rig = self.get_nomenclature_rig(rig)

        index_elbow = self.iCtrlIndex - 1
        index_hand = self.iCtrlIndex

        jnt_elbow = self.chain_jnt[index_elbow]
        jnt_hand = self.chain_jnt[index_hand]

        # Create a group for the ik system
        # This group will be parentConstrained to the module parent.
        ikChainGrp_name = nomenclature_rig.resolve('ikChain')
        self._ikChainGrp = pymel.createNode('transform', name=ikChainGrp_name, parent=self.grp_rig)
        self._ikChainGrp.setMatrix(self.chain.start.getMatrix(worldSpace=True), worldSpace=True)

        super(IK, self).build(rig, *args, **kwargs)

        self._ikChainGrp.setParent(self.grp_rig)

        # Duplicate input chain (we don't want to move the hierarchy)
        # Todo: implement a duplicate method in omtk.libs.libPymel.PyNodeChain
        # Create ikChain and fkChain
        self._chain_ik = pymel.duplicate(list(self.chain_jnt), renameChildren=True, parentOnly=True)
        for oInput, oIk, in zip(self.chain_jnt, self._chain_ik):
            oIk.rename(nomenclature_rig.resolve('ik'))
        self._chain_ik[0].setParent(self.parent)  # Trick the IK system (temporary solution)


        obj_s = self._chain_ik[0]
        obj_e = self._chain_ik[index_hand]

        # Compute chain length
        self.chain_length = libPymel.PyNodeChain(self.chain[:self.iCtrlIndex+1]).length()
        #self.chain_length = self.chain.length()

        # Compute swivel position
        p3SwivelPos = self.calc_swivel_pos()

        # Create ikChain
        obj_s.setParent(self._ikChainGrp)

        # Create ikEffector
        ik_solver_name = nomenclature_rig.resolve('ikHandle')
        ik_effector_name = nomenclature_rig.resolve('ikEffector')
        self._ik_handle, _ik_effector = pymel.ikHandle(startJoint=obj_s, endEffector=obj_e, solver='ikRPsolver')
        self._ik_handle.rename(ik_solver_name)
        self._ik_handle.setParent(self._ikChainGrp)
        _ik_effector.rename(ik_effector_name)

        # Create CtrlIK
        if not isinstance(self.ctrl_ik, self._CLASS_CTRL_IK):
            self.ctrl_ik = self._CLASS_CTRL_IK()
        ctrl_ik_refs = [jnt_hand] + jnt_hand.getChildren(allDescendents=True)
        self.ctrl_ik.build(refs=ctrl_ik_refs)  # refs is used by CtrlIkCtrl
        self.ctrl_ik.setParent(self.grp_anm)
        ctrl_ik_name = nomenclature_anm.resolve('ik')
        self.ctrl_ik.rename(ctrl_ik_name)
        self.ctrl_ik.offset.setTranslation(obj_e.getTranslation(space='world'), space='world')

        # Set ctrl_ik_orientation
        if ctrl_ik_orientation is None:
            ctrl_ik_orientation = obj_e.getRotation(space='world')
        self.ctrl_ik.offset.setRotation(ctrl_ik_orientation, space='world')

        # Create CtrlIkSwivel
        if not isinstance(self.ctrl_swivel, self._CLASS_CTRL_SWIVEL):
            self.ctrl_swivel = self._CLASS_CTRL_SWIVEL()
        ctrl_swivel_ref = jnt_elbow
        self.ctrl_swivel.build(refs=ctrl_swivel_ref)
        self.ctrl_swivel.setParent(self.grp_anm)
        self.ctrl_swivel.rename(nomenclature_anm.resolve('swivel'))
        self.ctrl_swivel.offset.setTranslation(p3SwivelPos, space='world')
        self.swivelDistance = self.chain_length  # Used in ik/fk switch

        #
        # Create softIk node and connect user accessible attributes to it.
        #
        oAttHolder = self.ctrl_ik
        fnAddAttr = functools.partial(libAttr.addAttr, hasMinValue=True, hasMaxValue=True)
        attInRatio = fnAddAttr(oAttHolder, longName='softIkRatio', niceName='SoftIK', defaultValue=0, minValue=0,
                               maxValue=50, k=True)
        attInStretch = fnAddAttr(oAttHolder, longName='stretch', niceName='Stretch', defaultValue=0, minValue=0,
                                 maxValue=1.0, k=True)

        # Adjust the ratio in percentage so animators understand that 0.03 is 3%
        attInRatio = libRigging.create_utility_node('multiplyDivide', input1X=attInRatio, input2X=0.01).outputX

        # Create and configure SoftIK solver
        rig_softIkNetwork = SoftIkNode()
        rig_softIkNetwork.build()
        pymel.connectAttr(attInRatio, rig_softIkNetwork.inRatio)
        pymel.connectAttr(attInStretch, rig_softIkNetwork.inStretch)
        pymel.connectAttr(self._ikChainGrp.worldMatrix, rig_softIkNetwork.inMatrixS)
        pymel.connectAttr(self.ctrl_ik.worldMatrix, rig_softIkNetwork.inMatrixE)
        attr_distance = libFormula.parse('distance*globalScale',
                                         distance=self.chain_length,
                                         globalScale=self.grp_rig.globalScale)
        pymel.connectAttr(attr_distance, rig_softIkNetwork.inChainLength)

        # Constraint effector
        # Note that we create an ikHandleTarget node so that we can hijack the system later.
        # For example if we are building a Leg and want to footroll to influence the ikHandle.
        self._ik_handle_target = pymel.createNode('transform', name=nomenclature_rig.resolve('ikHandleTarget'))
        self._ik_handle_target.setParent(self.grp_rig)
        pymel.pointConstraint(self.ctrl_ik, self._ik_handle_target)
        attOutRatio = rig_softIkNetwork.outRatio
        attOutRatioInv = libRigging.create_utility_node('reverse', inputX=rig_softIkNetwork.outRatio).outputX
        pymel.select(clear=True)
        pymel.select(self._ik_handle_target , self._ikChainGrp, self._ik_handle)
        pointConstraint = pymel.pointConstraint()
        pointConstraint.rename(pointConstraint.name().replace('pointConstraint', 'softIkConstraint'))
        pymel.select(pointConstraint)
        weight_inn, weight_out = pointConstraint.getWeightAliasList()
        pymel.connectAttr(attOutRatio, weight_inn)
        pymel.connectAttr(attOutRatioInv, weight_out)

        # Connect global scale
        pymel.connectAttr(self.grp_rig.globalScale, self._ikChainGrp.sx)
        pymel.connectAttr(self.grp_rig.globalScale, self._ikChainGrp.sy)
        pymel.connectAttr(self.grp_rig.globalScale, self._ikChainGrp.sz)

        # Connect stretch
        for i in range(1, self.iCtrlIndex+1):
            obj = self._chain_ik[i]
            util_get_t = libRigging.create_utility_node('multiplyDivide',
                                               input1X=rig_softIkNetwork.outStretch,
                                               input1Y=rig_softIkNetwork.outStretch,
                                               input1Z=rig_softIkNetwork.outStretch,
                                               input2=obj.t.get())
            pymel.connectAttr(util_get_t.outputX, obj.tx, force=True)
            pymel.connectAttr(util_get_t.outputY, obj.ty, force=True)
            pymel.connectAttr(util_get_t.outputZ, obj.tz, force=True)

        # Connect rig -> anm
        pymel.orientConstraint(self.ctrl_ik, obj_e, maintainOffset=True)
        pymel.poleVectorConstraint(self.ctrl_swivel, self._ik_handle)

        '''
        # Connect to parent
        if libPymel.is_valid_PyNode(self.parent):
            pymel.parentConstraint(self.parent, self._ikChainGrp, maintainOffset=True)
        '''

        if constraint:
            for source, target in zip(self._chain_ik, self.chain):
                pymel.parentConstraint(source, target)


    def parent_to(self, parent):
        pymel.parentConstraint(parent, self._ikChainGrp, maintainOffset=True)


