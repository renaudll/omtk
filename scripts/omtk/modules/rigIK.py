import functools
import collections
import pymel.core as pymel
from maya import mel
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

    def __init__(self):
        super(CtrlIkSwivel, self).__init__()

        self._line_locator = None
        self._line_annotation = None


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

        return node

    def get_spaceswitch_targets(self, rig, module, *args, **kwargs):
        """
        Add the Hand/Leg IK ctrl by default as a space-switch target to any swivel.
        """
        targets, target_names = super(CtrlIkSwivel, self).get_spaceswitch_targets(rig, module, *args, **kwargs)

        # Add the Hand/Foot ctrl
        targets.append(module.ctrl_ik)
        target_names.append(None)

        return targets, target_names

    def build(self, rig, refs=None, line_target=True, *args, **kwargs):
        super(CtrlIkSwivel, self).build(rig, *args, **kwargs)
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
    _CLASS_CTRL_IK = CtrlIk
    _CLASS_CTRL_SWIVEL = CtrlIkSwivel

    def __init__(self, *args, **kwargs):
        super(IK, self).__init__(*args, **kwargs)
        self.iCtrlIndex = 2
        self.ctrl_ik = None
        self.ctrl_swivel = None
        self.chain_length = None
        self._chain_ik = None
        #self._chain_quad_ik = None
        self._quad_swivel = None
        self._soft_ik_network = None

    def _create_ctrl_ik(self, *args, **kwargs):
        return CtrlIk(*args, **kwargs)

    def calc_swivel_pos(self, start_index=0, end_index=2):
        pos_start = self.chain_jnt[start_index].getTranslation(space='world')
        pos_end = self.chain_jnt[end_index].getTranslation(space='world')

        chain_length = 0
        for i in range(end_index):
            chain_length += self.chain_jnt[i+1].t.get().length()

        ratio = self.chain_jnt[start_index + 1].t.get().length() / chain_length
        pos_swivel_base = (pos_end - pos_start) * ratio + pos_start
        dir_swivel = (self.chain_jnt[start_index + 1].getTranslation(space='world') - pos_swivel_base).normal()
        return pos_swivel_base + (dir_swivel * chain_length)

    def build(self, rig, ctrl_ik_orientation=None, constraint=True, constraint_handle=True, *args, **kwargs):
        nomenclature_anm = self.get_nomenclature_anm(rig)
        nomenclature_rig = self.get_nomenclature_rig(rig)

        if self.iCtrlIndex == 2:
            index_elbow = self.iCtrlIndex - 1
        elif self.iCtrlIndex == 3:
            index_elbow = self.iCtrlIndex - 2
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
        i = 1
        for oInput, oIk, in zip(self.chain_jnt, self._chain_ik):
            oIk.rename(nomenclature_rig.resolve('{0:02}'.format(i)))
            i += 1
        self._chain_ik[0].setParent(self.parent)  # Trick the IK system (temporary solution)

        #We need a second chain for the quadruped setup (spring solver tried setup)
        '''
        if self.iCtrlIndex == 3:
            self._chain_quad_ik = pymel.duplicate(list(self.chain_jnt), renameChildren=True, parentOnly=True)
            i = 1
            for oInput, oIk, in zip(self.chain_jnt, self._chain_quad_ik):
                oIk.rename(nomenclature_rig.resolve('quad{0:02}'.format(i)))
                i += 1
            self._chain_quad_ik[0].setParent(self._chain_ik[0])  #Quad chain is parented to the first joint of the ik chain
        '''


        obj_s = self._chain_ik[0]
        obj_e = self._chain_ik[index_hand]

        # Compute chain length
        self.chain_length = libPymel.PyNodeChain(self.chain[:self.iCtrlIndex+1]).length()
        #self.chain_length = self.chain.length()

        # Compute swivel position
        p3SwivelPos = self.calc_swivel_pos()
        if self.iCtrlIndex == 3:
            quad_swivel_pos = self.calc_swivel_pos(start_index=1, end_index=3)

        # Create ikChain
        obj_s.setParent(self._ikChainGrp)
        #obj_s.setParent(None)

        # Create ikEffector
        ik_solver_name = nomenclature_rig.resolve('ikHandle')
        ik_effector_name = nomenclature_rig.resolve('ikEffector')
        ''' (spring solver tried setup)
        if self.iCtrlIndex == 3:
            mel.eval('ikSpringSolver')
            #The ikSpringSolver cause sometime set it's pole vector computation flipped from the start...
            #but if the solver is not specified correctly, the pole vector setup will cause problem since the first calculation
            #is not fine...
            self._ik_handle, _ik_effector = pymel.ikHandle(startJoint=obj_s, endEffector=obj_e, solver='ikSpringSolver')
            #Switch to the ikSpringSolver
            pymel.ikHandle(self._ik_handle, e=True, solver='ikSpringSolver')
            #Should fix the double transform issue...will see http://juss-usa.blogspot.ca/2010/12/ik-spring-solver.html
            self._ik_handle.splineIkOldStyle.set(True)
        else:
            self._ik_handle, _ik_effector = pymel.ikHandle(startJoint=obj_s, endEffector=obj_e, solver='ikRPsolver')
        '''
        self._ik_handle, _ik_effector = pymel.ikHandle(startJoint=obj_s, endEffector=self._chain_ik[index_hand-1], solver='ikRPsolver')
        self._ik_handle.rename(ik_solver_name)
        self._ik_handle.setParent(self._ikChainGrp)
        _ik_effector.rename(ik_effector_name)

        #We need a second ik solver for the quad chain
        if self.iCtrlIndex == 3:
            ik_solver_quad_name = nomenclature_rig.resolve('quadIkHandle')
            ik_effector_quad_name = nomenclature_rig.resolve('quadIkEffector')
            ''' (spring solver tried setup)
            self._ik_handle_quad, _ik_effector = pymel.ikHandle(startJoint=self._chain_quad_ik[1],
                                                                endEffector=self._chain_quad_ik[self.iCtrlIndex], solver='ikRPsolver')
            '''
            self._ik_handle_quad, _ik_effector = pymel.ikHandle(startJoint=self._chain_ik[1],
                                                                endEffector=obj_e,
                                                                solver='ikRPsolver')
            self._ik_handle_quad.rename(ik_solver_quad_name)
            self._ik_handle_quad.setParent(self._ikChainGrp)
            self._ik_handle.setParent(self._ik_handle_quad)
            _ik_effector.rename(ik_effector_quad_name)

        # Create CtrlIK
        if not isinstance(self.ctrl_ik, self._CLASS_CTRL_IK):
            self.ctrl_ik = self._CLASS_CTRL_IK()
        ctrl_ik_refs = [jnt_hand] + jnt_hand.getChildren(allDescendents=True)
        self.ctrl_ik.build(rig, refs=ctrl_ik_refs, geometries=rig.get_meshes())  # refs is used by CtrlIkCtrl
        self.ctrl_ik.setParent(self.grp_anm)
        ctrl_ik_name = nomenclature_anm.resolve('ik')
        self.ctrl_ik.rename(ctrl_ik_name)
        self.ctrl_ik.offset.setTranslation(obj_e.getTranslation(space='world'), space='world')

        # Set ctrl_ik_orientation
        if ctrl_ik_orientation is None:
            ctrl_ik_orientation = obj_e.getRotation(space='world')
        self.ctrl_ik.offset.setRotation(ctrl_ik_orientation, space='world')

        self.ctrl_ik.create_spaceswitch(rig, self, self.parent, default_name='World')

        # Create CtrlIkSwivel
        if not isinstance(self.ctrl_swivel, self._CLASS_CTRL_SWIVEL):
            self.ctrl_swivel = self._CLASS_CTRL_SWIVEL()
        ctrl_swivel_ref = jnt_elbow
        self.ctrl_swivel.build(rig, refs=ctrl_swivel_ref)
        self.ctrl_swivel.setParent(self.grp_anm)
        self.ctrl_swivel.rename(nomenclature_anm.resolve('swivel'))
        self.ctrl_swivel._line_locator.rename(nomenclature_anm.resolve('swivelLineLoc'))
        self.ctrl_swivel._line_annotation.rename(nomenclature_anm.resolve('swivelLineAnn'))
        self.ctrl_swivel.offset.setTranslation(p3SwivelPos, space='world')
        self.swivelDistance = self.chain_length  # Used in ik/fk switch
        self.ctrl_swivel.create_spaceswitch(rig, self, self.parent, default_name='World')

        #Create another swivel handle node for the quad chain setup
        ''' (spring solver tried setup)
        if self.iCtrlIndex == 3:
            self._quad_swivel = pymel.spaceLocator()
            self._quad_swivel.rename(nomenclature_rig.resolve('quadSwivel'))
            self._quad_swivel.setTranslation(quad_swivel_pos, space='world')
            #self._quad_swivel.hide()
            #Parent it to the second chain ik bone
            self._quad_swivel.setParent(self._chain_ik[1])
        '''

        #
        # Create softIk node and connect user accessible attributes to it.
        #
        oAttHolder = self.ctrl_ik
        fnAddAttr = functools.partial(libAttr.addAttr, hasMinValue=True, hasMaxValue=True)
        if self.iCtrlIndex <= 3:
            attInRatio = fnAddAttr(oAttHolder, longName='softIkRatio', niceName='SoftIK', defaultValue=0, minValue=0,
                                   maxValue=50, k=True)
            attInStretch = fnAddAttr(oAttHolder, longName='stretch', niceName='Stretch', defaultValue=0, minValue=0,
                                     maxValue=1.0, k=True)
            # Adjust the ratio in percentage so animators understand that 0.03 is 3%
            attInRatio = libRigging.create_utility_node('multiplyDivide', input1X=attInRatio, input2X=0.01).outputX

        # Create the ik_handle_target that will control the ik_handle
        # This is allow us to override what control the main ik_handle
        # Mainly used for the Leg setup
        self._ik_handle_target = pymel.createNode('transform', name=nomenclature_rig.resolve('ikHandleTarget'))
        self._ik_handle_target.setParent(self.grp_rig)
        pymel.pointConstraint(self.ctrl_ik, self._ik_handle_target)

        if self.iCtrlIndex <= 3:
            # Create and configure SoftIK solver
            self._soft_ik_network = SoftIkNode()
            self._soft_ik_network.build()
            pymel.connectAttr(attInRatio, self._soft_ik_network.inRatio)
            pymel.connectAttr(attInStretch, self._soft_ik_network.inStretch)
            pymel.connectAttr(self._ikChainGrp.worldMatrix, self._soft_ik_network.inMatrixS)
            pymel.connectAttr(self._ik_handle_target.worldMatrix, self._soft_ik_network.inMatrixE)
            attr_distance = libFormula.parse('distance*globalScale',
                                             distance=self.chain_length,
                                             globalScale=self.grp_rig.globalScale)
            pymel.connectAttr(attr_distance, self._soft_ik_network.inChainLength)

            attOutRatio = self._soft_ik_network.outRatio
            attOutRatioInv = libRigging.create_utility_node('reverse', inputX=self._soft_ik_network.outRatio).outputX
            pymel.select(clear=True)
            ik_to_use = self._ik_handle
            if self.iCtrlIndex == 3:
                ik_to_use = self._ik_handle_quad
            pymel.select(self._ik_handle_target , self._ikChainGrp, ik_to_use)
            pointConstraint = pymel.pointConstraint()
            pointConstraint.rename(pointConstraint.name().replace('pointConstraint', 'softIkConstraint'))
            pymel.select(pointConstraint)
            weight_inn, weight_out = pointConstraint.getWeightAliasList()
            pymel.connectAttr(attOutRatio, weight_inn)
            pymel.connectAttr(attOutRatioInv, weight_out)

            # Connect stretch
            for i in range(1, self.iCtrlIndex+1):
                obj = self._chain_ik[i]
                util_get_t = libRigging.create_utility_node('multiplyDivide',
                                                   input1X=self._soft_ik_network.outStretch,
                                                   input1Y=self._soft_ik_network.outStretch,
                                                   input1Z=self._soft_ik_network.outStretch,
                                                   input2=obj.t.get())
                pymel.connectAttr(util_get_t.outputX, obj.tx, force=True)
                pymel.connectAttr(util_get_t.outputY, obj.ty, force=True)
                pymel.connectAttr(util_get_t.outputZ, obj.tz, force=True)

        # Connect global scale
        pymel.connectAttr(self.grp_rig.globalScale, self._ikChainGrp.sx)
        pymel.connectAttr(self.grp_rig.globalScale, self._ikChainGrp.sy)
        pymel.connectAttr(self.grp_rig.globalScale, self._ikChainGrp.sz)

        # Connect rig -> anm
        if constraint_handle:
            if self.iCtrlIndex == 2:
                pymel.pointConstraint(self.ctrl_ik, self._ik_handle, maintainOffset=True)
            elif self.iCtrlIndex == 3: #Quadruped
                pymel.pointConstraint(self.ctrl_ik, self._ik_handle_quad, maintainOffset=True)
        pymel.orientConstraint(self.ctrl_ik, obj_e, maintainOffset=True)
        pymel.poleVectorConstraint(self.ctrl_swivel, self._ik_handle)

        #If need, constraint the quadruped swivel to it's target
        if self.iCtrlIndex == 3:
            #Pole vector contraint the second ik handle on the first elbox of the first ik handle
            #HACK - Seem to give a cycle dependency warning when done, but it doesn't seem to create any problem...now
            pymel.poleVectorConstraint(self._chain_ik[index_elbow], self._ik_handle_quad)

        '''
        # Connect to parent
        if libPymel.is_valid_PyNode(self.parent):
            pymel.parentConstraint(self.parent, self._ikChainGrp, maintainOffset=True)
        '''

        if constraint:
            for source, target in zip(self._chain_ik, self.chain):
                pymel.parentConstraint(source, target)
            ''' (spring solver tried setup)
            if self.iCtrlIndex == 3:
                for source, target in zip(self._chain_quad_ik, self.chain):
                    pymel.parentConstraint(source, target)
            else:
                for source, target in zip(self._chain_ik, self.chain):
                    pymel.parentConstraint(source, target)
            '''

    def unbuild(self):
        super(IK, self).unbuild()
        #Make sure the soft ik network unbuild correctly
        #self._soft_ik_network.unbuild()

    def parent_to(self, parent):
        pymel.parentConstraint(parent, self._ikChainGrp, maintainOffset=True)


