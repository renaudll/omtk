import pymel.core as pymel
from classRigPart import RigPart
from classRigNode import RigNode
from omtk.libs import libRigging, libPymel
from rigSplineIK import SplineIK

class NonRollJoint(RigNode):
    def build(self):
        self.node = pymel.createNode('transform')

        pymel.select(clear=True)
        self.start = pymel.joint() # todo: rename
        self.end = pymel.joint() # todo: rename
        self.end.setTranslation([1,0,0])
        pymel.makeIdentity((self.start, self.end), apply=True, r=True)

        self.ikHandle, self.ikEffector = pymel.ikHandle( # todo: rename
            solver='ikRPsolver',
            startJoint=self.start,
            endEffector=self.end)
        self.ikHandle.poleVectorX.set(0)
        self.ikHandle.poleVectorY.set(0)
        self.ikHandle.poleVectorZ.set(0)

        # Set Hyerarchy
        self.start.setParent(self.node)
        self.ikHandle.setParent(self.node)

# Todo: Support more complex IK limbs (ex: 2 knees)
class Twistbone(RigPart):
    def __init__(self, *args, **kwargs):
        super(Twistbone, self).__init__(*args, **kwargs)

    def build(self, _bOrientIkCtrl=True, create_boxes=True, *args, **kwargs):
        super(Twistbone, self).build(create_grp_anm=False, *args, **kwargs)
        jnt_s = self.input[0]
        jnt_e = self.input[1]

        # Create curve from input joints (we'll use maya splineIKEffector for our upnodes.
        num_steps = 2
        self.ikCurve = libRigging.create_nurbsCurve_from_chain(
            jnt_s, jnt_e,
            degree=(2 if num_steps > 2 else 1),
            num_cvs=num_steps)
        pymel.parentConstraint(jnt_s, self.ikCurve, maintainOffset=True) # todo: really?

        # Generate Subjoinbs
        reload(libRigging)
        self.subjnts = libRigging.create_joints_from_chain(jnt_s, jnt_e, 5)

        # Create splineIK
        splineIK = SplineIK(self.subjnts +[self.ikCurve])
        splineIK.bStretch = False # todo: pass it via kwargs
        splineIK.build(create_grp_anm=False)
        self.ikCurve.setParent(splineIK.grp_rig)

        nonroll_1 = NonRollJoint() # todo: remove the need for an input
        nonroll_1.build()
        nonroll_1.rename('nonroll_s')
        jnt_s_parent = jnt_s.getParent()
        nonroll_1.setMatrix(jnt_s.getMatrix(worldSpace=True), worldSpace=True)
        if jnt_s_parent: pymel.parentConstraint(jnt_s_parent, nonroll_1.node, maintainOffset=True)

        pymel.parentConstraint(jnt_s, nonroll_1.ikHandle, maintainOffset=True)

        nonroll_2 = NonRollJoint() # todo: remove the need for an input
        nonroll_2.build()
        nonroll_2.rename('nonroll_e')

        nonroll_2.setMatrix(jnt_s.getMatrix(worldSpace=True), worldSpace=True)
        nonroll_2.setTranslation(jnt_e.getTranslation(space='world'), space='world')
        pymel.parentConstraint(jnt_s, nonroll_2.node, maintainOffset=True)
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
        pymel.connectAttr(upnode_s.xformMatrix, splineIK.ikHandle.dWorldUpMatrix)
        pymel.connectAttr(upnode_e.xformMatrix, splineIK.ikHandle.dWorldUpMatrixEnd)

        # Bonus: Give the twistbones a killer look
        if create_boxes:
            for i in range(len(self.subjnts)-1):
                jnt_inn = self.subjnts[i]
                jnt_out = self.subjnts[i+1]
                libRigging.create_jnt_box(jnt_inn, jnt_out)

    def unbuild(self):
        pass
