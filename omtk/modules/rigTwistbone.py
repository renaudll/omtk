import pymel.core as pymel
from maya import cmds
from omtk.classModule import Module
from omtk.classNode import Node
from omtk.libs import libRigging
from omtk.libs import libSkinning
import rigRibbon

class NonRollJoint(Node):
    """
    """
    # TODO: Replace with LookAt method (faster)

    def __init__(self):
        self.ikHandle = self.ikEffector = None

    """
    Used for quaternion extraction.
    """
    def build(self):
        super(NonRollJoint, self).build()

        self.node = pymel.createNode('transform')

        pymel.select(clear=True)
        self.start = pymel.joint() # todo: rename
        self.end = pymel.joint() # todo: rename
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

'''
class NonRollJoint(Module):
    def __init__(self, *args, **kwargs):
        super(NonRollJoint, self).__init__(*args, **kwargs)
        self.nonroll_s = None
        self.nonroll_e = None

    def build(self, rig):
        super(NonRollJoint, self).build(rig, create_grp_anm=False)

        # Create nonroll_s
        nonroll_s_name = nomenclature_rig.resolve('s')
        self.nonroll_s = pymel.createNode('transform', name=nonroll_s_name)
        nonroll_

        # Create nonroll_e
        nonroll_e_name = nomenclature_rig.resolve('e')
        self.nonroll_e = pymel.createNode('transform', name=nonroll_e_name)


        pymel.pointConstraint(self.chain_jnt.start, self.nonroll_s)
        quat_aim = pymel.aimConstraint(self.nonroll_e, self.nonroll_s, maintainOffset=False)
        quat_aim.worldUpType.set(4)  # None

        # Create hyerarchy
        self.nonroll_s.setParent(self.grp_rig)
        self.nonroll_e.setParent(self.grp_rig)

        self.node = pymel.createNode('transform')

        pymel.select(clear=True)
        self.start = pymel.joint() # todo: rename
        self.end = pymel.joint() # todo: rename
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
'''

class RollExtractor(Module):
    """
    Extract the roll in the X axis and expose to in a extractedRoll attribute on self.grp_rig.
    """
    def __init__(self, *args, **kwargs):
        super(RollExtractor, self).__init__(*args, **kwargs)
        self.nonroll_s = None
        self.nonroll_e = None

    def build(self, rig, parent=True, *args, **kwargs):
        super(RollExtractor, self).build(rig, create_grp_anm=False, *args, **kwargs)

        nomenclature_rig = self.get_nomenclature_rig(rig)

        # Create the NonRollJoint and align it to the chain.
        self.nonroll_s = NonRollJoint()
        self.nonroll_s.build()
        self.nonroll_s.rename(nomenclature_rig.resolve('nonroll_s'))
        self.nonroll_s.setMatrix(self.chain_jnt.start.getMatrix(worldSpace=True))
        pymel.pointConstraint(self.chain_jnt.start, self.nonroll_s.start)
        pymel.parentConstraint(self.chain_jnt.start, self.nonroll_s.ikHandle, maintainOffset=True)
        self.nonroll_s.setParent(self.grp_rig)

        # Create extractors
        # Note that the extractor and normally parented to the original joint.
        # For clarity we'll use the grp_ref node.

        grp_ref_name = nomenclature_rig.resolve('ref')
        grp_ref = pymel.createNode('transform', name=grp_ref_name)
        grp_ref.setParent(self.grp_rig)
        pymel.parentConstraint(self.chain_jnt.start, grp_ref)

        extractor_360_name = nomenclature_rig.resolve('extractor360')
        self.roll_extractor = pymel.createNode('transform', name=extractor_360_name)
        self.roll_extractor.setParent(grp_ref)

        self.roll_extractor.t.set(0, 0, 0)
        self.roll_extractor.r.set(0, 0, 0)

        # Create the constraints
        pymel.orientConstraint(self.nonroll_s.start, grp_ref, self.roll_extractor)

        # Note: In favor of simplicity, only joint facing the x axis are supported.
        #attr_extract180 = self.extractor_180.rotateX
        attr_roll_extractor = self.roll_extractor.rotateX
        attr_roll_extractor = libRigging.create_utility_node('multiplyDivide', input1X=attr_roll_extractor, input2X=2.0).outputX

        pymel.addAttr(self.grp_rig, longName='extractedRoll')
        pymel.connectAttr(attr_roll_extractor, self.grp_rig.extractedRoll)
        self.extractedRoll = self.grp_rig.extractedRoll

        # Parent
        if parent and self.parent:
            pymel.parentConstraint(self.parent, self.grp_rig, maintainOffset=True)



# Todo: Support more complex IK limbs (ex: 2 knees)
class Twistbone(Module):
    def __init__(self, *args, **kwargs):
        self.ikCurve = None

        super(Twistbone, self).__init__(*args, **kwargs)

    def build(self, rig, orient_ik_ctrl=True, create_boxes=True, *args, **kwargs):
        if len(self.chain_jnt) < 2:
            raise Exception("Invalid input count. Expected 2, got {0}. {1}".format(len(self.chain_jnt), self.chain_jnt))

        super(Twistbone, self).build(rig, *args, **kwargs)

        nomenclature_rig = self.get_nomenclature_rig(rig)

        jnt_s = self.chain_jnt[0]
        jnt_e = self.chain_jnt[1]

        # Create curve from input joints (we'll use maya splineIKEffector for our upnodes.
        num_steps = 2
        self.ikCurve = libRigging.create_nurbsCurve_from_joints(jnt_s, jnt_e, 2 if num_steps > 2 else 1)
        pymel.parentConstraint(jnt_s, self.ikCurve, maintainOffset=True)

        # Generate Subjoinbs
        self.subjnts = libRigging.create_chain_between_objects(jnt_s, jnt_e, 5)
        self.subjnts.start.setParent(self.chain_jnt.start)

        # Create roll extractors
        # Note that we set parent to False since we extract the roll in worldSpace.
        nonroll_inn = RollExtractor([jnt_s])
        nonroll_inn.build(rig, parent=False)
        nonroll_inn.grp_rig.setParent(self.grp_rig)

        nonroll_out = RollExtractor([jnt_e])
        nonroll_out.build(rig, parent=False)
        nonroll_out.grp_rig.setParent(self.grp_rig)

        # Create the ribbon nurbs plane.
        nurbsSurface = libRigging.create_nurbs_plane_from_joints([self.chain_jnt.start, self.chain_jnt.end], degree=2)
        nurbsSurface.setParent(self.grp_rig)

        # Create the twist deformer and align it to the chain.
        twist_deformer, twist_handle = pymel.nonLinear(type='twist')
        parent_const = pymel.parentConstraint(jnt_s, twist_handle)
        cmds.setAttr('{0}.target[0].targetOffsetRotateZ'.format(parent_const), -90)  # HACK: Bypass pymel bug
        twist_deformer.lowBound.set(0.0)
        twist_deformer.highBound.set(self.chain_jnt.length()/2.0)
        twist_handle.setParent(self.grp_rig)

        pymel.connectAttr(nonroll_inn.extractedRoll, twist_deformer.startAngle)
        pymel.connectAttr(nonroll_out.extractedRoll, twist_deformer.endAngle)

        # Rig Ribbon
        sys_ribbon_inputs = self.subjnts + [nurbsSurface]
        sys_ribbon = rigRibbon.Ribbon(sys_ribbon_inputs)
        sys_ribbon.build(rig, constraint=True)
        sys_ribbon.grp_anm.setParent(self.grp_anm)
        sys_ribbon.grp_rig.setParent(self.grp_rig)

        pymel.delete(sys_ribbon.ctrls[0])
        pymel.delete(sys_ribbon.ctrls[-1])

        jnt_ribbon_inn = sys_ribbon._ribbon_jnts.start
        pymel.parentConstraint(self.chain_jnt.start, jnt_ribbon_inn)

        # Unparent the twistbones so they squash correctly, even in a Game-Engine scenario.
        for jnt in self.subjnts:
            if jnt.getParent() != self.chain_jnt.start:
                jnt.setParent(self.chain_jnt.start)

        # Automatically skin the twistbones
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
                skinCluster.addInfluence(subjnt)

            num_shapes = skinCluster.numOutputConnections()
            for i in range(num_shapes):
                shape = skinCluster.outputShapeAtIndex(i)
                print("Assign skin weights on {0}.".format(shape.name()))
                libSkinning.transfer_weights_from_segments(shape, self.chain_jnt.start, self.subjnts)


        '''
        # Bonus: Give the twistbones a killer look
        if create_boxes:
            for i in range(len(self.subjnts)-1):
                jnt_inn = self.subjnts[i]
                jnt_out = self.subjnts[i+1]
                libRigging.create_jnt_box(jnt_inn, jnt_out)
        '''

    def unbuild(self):
        pass
