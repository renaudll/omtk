import pymel.core as pymel
from omtk.classModule import Module
from omtk.classNode import Node
from omtk.libs import libRigging
from omtk.libs import libSkinning
from omtk.modules.rigSplineIK import SplineIK
import re


class NonRollJoint(Node):

    def __init__(self):
        self.ikHandle = self.ikEffector = None

    """
    Used for quaternion extraction.
    """
    def build(self):
        self.node = pymel.createNode('transform')

        pymel.select(clear=True)
        self.start = pymel.joint() # todo: really the best name ?
        pymel.rename(self.start, "Nonroll_Start_Jnt")
        self.end = pymel.joint() # todo: really the best name ?
        pymel.rename(self.end, "Nonroll_End_Jnt")
        self.end.setTranslation([1,0,0])
        pymel.makeIdentity((self.start, self.end), apply=True, r=True)

        self.ikHandle, self.ikEffector = pymel.ikHandle(
            solver='ikRPsolver',
            startJoint=self.start,
            endEffector=self.end)
        self.ikHandle.poleVectorX.set(0)
        self.ikHandle.poleVectorY.set(0)
        self.ikHandle.poleVectorZ.set(0)

        # Set Hierarchy
        self.start.setParent(self.node)
        self.ikHandle.setParent(self.node)


# Todo: Support more complex IK limbs (ex: 2 knees)
class Twistbone(Module):
    def __init__(self, *args, **kwargs):
        self.ikCurve = None

        super(Twistbone, self).__init__(*args, **kwargs)

    def build(self, rig, orient_ik_ctrl=True, create_boxes=True, *args, **kwargs):
        if len(self.chain_jnt) < 2:
            raise Exception("Invalid input count. Expected 2, got {0}. {1}".format(len(self.chain_jnt), self.chain_jnt))

        super(Twistbone, self).build(rig, create_grp_anm=False, *args, **kwargs)

        nomenclature_rig = self.get_nomenclature_rig(rig)
        nomenclature_jnt = self.get_nomenclature_jnt(rig)

        jnt_s = self.chain_jnt[0]
        jnt_e = self.chain_jnt[1]

        # Create curve from input joints (we'll use maya splineIKEffector for our upnodes.
        num_steps = 2
        self.ikCurve = libRigging.create_nurbsCurve_from_joints(jnt_s, jnt_e, 2 if num_steps > 2 else 1)
        pymel.parentConstraint(jnt_s, self.ikCurve, maintainOffset=True)

        # Generate Subjoints
        self.subjnts = libRigging.create_chain_between_objects(jnt_s, jnt_e, 4)

        #TODO : Use the nomeclature system to name the bones
        for i, sub_jnt in enumerate(self.subjnts):
            #Right now, we take into consideration that the system will be named Side_SysName(Ex:Upperarm_Twist)
            jnt_name = nomenclature_jnt.resolve("twist{0:02d}".format(i))
            sub_jnt.rename(jnt_name)

        # Create splineIK
        #Do not connect the stretch to prevent scaling problem
        #TODO : If a stretch system exist on the input, we need to find a way to connect it to the twist system
        splineIK = SplineIK(self.subjnts +[self.ikCurve])
        splineIK.bStretch = False
        splineIK.build(rig, create_grp_anm=False, stretch=False)
        self.ikCurve.setParent(splineIK.grp_rig)

        nonroll_1 = NonRollJoint()
        nonroll_1.build()
        nonroll_1.rename(nomenclature_rig.resolve('nonroll_s'))
        jnt_s_parent = jnt_s.getParent()
        nonroll_1.setMatrix(jnt_s.getMatrix(worldSpace=True), worldSpace=True)
        if jnt_s_parent:
            pymel.parentConstraint(jnt_s_parent, nonroll_1.node, maintainOffset=True, skipTranslate=['x', 'y', 'z'])
            pymel.pointConstraint(jnt_s, nonroll_1.node)

        pymel.parentConstraint(jnt_s, nonroll_1.ikHandle, maintainOffset=True)

        nonroll_2 = NonRollJoint()
        nonroll_2.build()
        nonroll_2.rename(nomenclature_rig.resolve('nonroll_e'))

        nonroll_2.setMatrix(jnt_s.getMatrix(worldSpace=True), worldSpace=True)
        nonroll_2.setTranslation(jnt_e.getTranslation(space='world'), space='world')
        pymel.parentConstraint(jnt_s, nonroll_2.node, maintainOffset=True, skipTranslate=['x', 'y', 'z'])
        pymel.pointConstraint(jnt_e, nonroll_2.node)
        pymel.parentConstraint(jnt_e, nonroll_2.ikHandle, maintainOffset=True)

        twist_info = pymel.createNode('transform')
        twist_info.rename('twist_info')
        twist_info.setMatrix(nonroll_2.start.getMatrix(worldSpace=True), worldSpace=True)
        twist_info.setParent(nonroll_2.start)
        pymel.aimConstraint(nonroll_2.end, twist_info, worldUpType=2, worldUpObject=jnt_e)

        ref_end = pymel.createNode('transform')
        ref_end.rename('ref_end')
        ref_end.setMatrix(nonroll_2.getMatrix(worldSpace=True), worldSpace=True)
        ref_end.setParent(nonroll_2.node)
        pymel.connectAttr(twist_info.rotate, ref_end.rotate)

        # Create the upnodes
        upnode_s = pymel.createNode('transform', name='upnode_s')
        upnode_s.setMatrix(jnt_s.getMatrix(worldSpace=True))
        upnode_e = pymel.createNode('transform', name='upnode_e')
        upnode_e.setMatrix(jnt_s.getMatrix(worldSpace=True), worldSpace=True)
        upnode_e.setTranslation(jnt_e.getTranslation(space='world'), space='world')

        pymel.parentConstraint(nonroll_1.start, upnode_s)
        pymel.parentConstraint(ref_end, upnode_e)

        # Cleanup
        nonroll_1.setParent(self.grp_rig)
        nonroll_2.setParent(self.grp_rig)
        upnode_s.setParent(self.grp_rig)
        upnode_e.setParent(self.grp_rig)
        splineIK.grp_rig.setParent(self.grp_rig)

        # Configure splineIK upnodes parameters
        splineIK.ikHandle.dTwistControlEnable.set(1)
        splineIK.ikHandle.dWorldUpType.set(4) # Object Rotation Up (Start End)
        #TODO : Find a better way to define the foward axis than the side string
        if nomenclature_rig.get_side() == 'r':
            splineIK.ikHandle.dForwardAxis.set(1)
            #splineIK.ikHandle.dWorldUpAxis.set(1)
        pymel.connectAttr(upnode_s.xformMatrix, splineIK.ikHandle.dWorldUpMatrix)
        pymel.connectAttr(upnode_e.xformMatrix, splineIK.ikHandle.dWorldUpMatrixEnd)

        #Compute the Stretch
        attr_stretch_raw = libRigging.create_stretch_node_between_2_bones(jnt_s, jnt_e)

        #Adjust with the global scale
        attr_stretch = libRigging.create_utility_node('multiplyDivide',
                                                           input1X=self.grp_rig.globalScale,
                                                            input2X=attr_stretch_raw,
                                                            operation=1
                                                           ).outputX

        #pymel.connectAttr(attr_stretch, attr_stretch_raw.input2X)

        #The distance between the twist bones is the same
        '''
        stretch_value = libRigging.create_utility_node('multiplyDivide',
                                   input1X=stretch_factor.outputX,
                                    input2X=self.subjnts[1].translateX.get(),
                                    operation=1
                                   ).outputX


        #Connect stretch
        for i in range(1, len(self.subjnts)):
            pymel.connectAttr(stretch_value, self.subjnts[i].translateX)
        '''
        for subjnt in self.subjnts[:-1]:
            pymel.connectAttr(attr_stretch, subjnt.scaleX)

        #Connect global scale
        pymel.connectAttr(self.grp_rig.globalScale, self.grp_rig.scaleX)
        pymel.connectAttr(self.grp_rig.globalScale, self.grp_rig.scaleY)
        pymel.connectAttr(self.grp_rig.globalScale, self.grp_rig.scaleZ)

        # Unparent the twistbones so they squash correctly, even in a Game-Engine scenario.
        if self.subjnts[0].getParent() != self.chain_jnt.start:
            self.subjnts[0].setParent(self.chain_jnt.start)

        skinClusters = set()
        for jnt in self.chain_jnt:
            for hist in jnt.listHistory(future=True):
                if isinstance(hist, pymel.nodetypes.SkinCluster):
                    skinClusters.add(hist)

        for skinCluster in skinClusters:
            # Ensure the source joint is in the skinCluster influences
            influenceObjects = skinCluster.influenceObjects()
            if self.chain_jnt.start not in influenceObjects:
                continue

            # Add new joints as influence.
            for subjnt in self.subjnts:
                skinCluster.addInfluence(subjnt, lockWeights=True, weight=0.0)

        # TODO : Automatically skin the twistbones
        '''
            num_shapes = skinCluster.numOutputConnections()
            for i in range(num_shapes):
                shape = skinCluster.outputShapeAtIndex(i)
                print("Assign skin weights on {0}.".format(shape.name()))
                libSkinning.transfer_weights_from_segments(shape, self.chain_jnt.start, self.subjnts)
        '''

        '''
        # Bonus: Give the twistbones a killer look
        if create_boxes:
            for i in range(len(self.subjnts)-1):
                jnt_inn = self.subjnts[i]
                jnt_out = self.subjnts[i+1]
                libRigging.create_jnt_box(jnt_inn, jnt_out)
        '''