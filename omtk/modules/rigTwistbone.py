import pymel.core as pymel

from omtk.core.classModule import Module
from omtk.core.classNode import Node
from omtk.core.utils import decorator_uiexpose
from omtk.libs import libRigging
from omtk.libs import libSkinning
from omtk.libs import libPymel
from omtk.modules.rigRibbon import Ribbon
from omtk.libs import libAttr
import math


class NonRollJoint(Node):
    """
    This class will create a node that work as the Non-RollJoint of Victor Vinyals to prevent any
    other axis to rotate on twists.
    """

    def __init__(self, *args, **kwargs):
        super(NonRollJoint, self).__init__(*args, **kwargs)
        self.ikHandle = None
        self.start = None
        self.end = None
        self.twist_extractor = None

    """
    Used for quaternion extraction.
    """
    def build(self, extract_world_up, name=None, *args, **kwargs):
        super(NonRollJoint, self).build(name=name, *args, **kwargs)

        pymel.select(clear=True)
        self.start = pymel.joint()
        self.end = pymel.joint()
        self.end.setTranslation([1,0,0])
        pymel.makeIdentity((self.start, self.end), apply=True, r=True)

        self.ikHandle, ikEffector = pymel.ikHandle(
            solver='ikRPsolver',
            startJoint=self.start,
            endEffector=self.end)
        self.ikHandle.poleVectorX.set(0)
        self.ikHandle.poleVectorY.set(0)
        self.ikHandle.poleVectorZ.set(0)

        # Name stuff, if no nomenclature, cry, node will be named by the base class
        start_name = name + "_jntStart"
        end_name = name + "_jntEnd"
        ik_handle_name = name + "_ikHandle"
        ik_effector_name = name + "_ikEffector"
        twist_extract_name = name + "_twistExtractor"

        self.start.rename(start_name)
        self.end.rename(end_name)
        self.ikHandle.rename(ik_handle_name)
        ikEffector.rename(ik_effector_name)

        # Create the extract node for the twist information
        self.twist_extractor = pymel.createNode('transform')
        self.twist_extractor.rename(twist_extract_name)
        self.twist_extractor.setMatrix(self.start.getMatrix(worldSpace=True), worldSpace=True)
        self.twist_extractor.setParent(self.start)
        pymel.aimConstraint(self.end, self.twist_extractor, worldUpType=2, worldUpObject=extract_world_up)

        # Set Hierarchy
        self.start.setParent(self.node)
        self.ikHandle.setParent(self.node)


class Twistbone(Module):
    """
    Bi-directional twistbone setup on a ribbon.
    """
    DEFAULT_NAME_USE_FIRST_INPUT = True

    def __init__(self, *args, **kwargs):
        self.ikCurve = None
        self.subjnts = []
        self.auto_skin = True
        self.create_bend = True
        self._sys_ribbon = None
        self.num_twist = 3

        super(Twistbone, self).__init__(*args, **kwargs)

    def build(self, orient_ik_ctrl=True, num_twist=None, create_bend=None, realign=True, *args, **kwargs):
        if len(self.chain_jnt) < 2:
            raise Exception("Invalid input count. Expected 2, got {0}. {1}".format(len(self.chain_jnt), self.chain_jnt))

        # Support some properties that could be redefined at build time
        if num_twist:
            self.num_twist = num_twist

        if create_bend:
            self.create_bend = create_bend

        super(Twistbone, self).build(create_grp_anm=self.create_bend, *args, **kwargs)

        nomenclature_rig = self.get_nomenclature_rig()
        nomenclature_jnt = self.get_nomenclature_jnt()

        top_parent = self.chain[0].getParent()
        jnt_s = self.chain_jnt[0]
        jnt_e = self.chain_jnt[1]

        scalable_grp = pymel.createNode('transform')
        scalable_grp.setParent(self.grp_rig)
        scalable_grp.rename(nomenclature_rig.resolve('scalable'))

        # Handle case where the number of twist change. The skin will be lost
        if self.subjnts and len(self.subjnts) != self.num_twist:
            self.unassign_twist_weights()
            pymel.delete(self.subjnts)
            self.subjnts = []
            # Also invalidate ctrls
            self.ctrls = []
        # Generate Subjoints if necessary, they will be use as the skinned one and will be drived by the ribbon and
        # driver chain
        if not self.subjnts:
            self.subjnts = libRigging.create_chain_between_objects(jnt_s, jnt_e, self.num_twist)
        elif realign:
            # Position the subjnts at equidistance from each others.
            num_subjnts = len(self.subjnts)
            base_tm = jnt_s.getMatrix(worldSpace=True)
            sp = jnt_s.getTranslation(space='world')
            ep = jnt_e.getTranslation(space='world')
            delta = ep - sp
            for i, subjnt in enumerate(self.subjnts):
                ratio = float(i) / (num_subjnts-1)
                tm = base_tm.copy()
                tm.translate = delta * ratio + sp
                subjnt.setMatrix(tm, worldSpace=True)

        self.subjnts[0].setParent(jnt_s)

        driver_grp = pymel.createNode('transform')
        driver_grp.setParent(scalable_grp)
        driver_grp.setMatrix(jnt_s.getMatrix(worldSpace=True), worldSpace=True)
        driver_grp.rename(nomenclature_rig.resolve('driverJnt_grp'))
        pymel.parentConstraint(jnt_s, driver_grp)

        # Create a second chain that will drive the rotation of the skinned joint
        driverjnts = libRigging.create_chain_between_objects(jnt_s, jnt_e, self.num_twist)

        # Rename the skinning subjnts
        for i, sub_jnt in enumerate(self.subjnts):
            sub_jnt.segmentScaleCompensate.set(0)  # Remove segment scale compensate
            # Right now, we take into consideration that the system will be named Side_SysName(Ex:Upperarm_Twist)
            jnt_name = nomenclature_jnt.resolve("twist{0:02d}".format(i))
            sub_jnt.rename(jnt_name)

        driver_refs = []
        ctrl_refs = []  # Will be used to drive the ctrl when stretch append
        for i, driver_jnt in enumerate(driverjnts):
            driver_jnt.segmentScaleCompensate.set(0)  # Remove segment scale compensate
            driver_name = nomenclature_jnt.resolve("twistDriver{0:02d}".format(i))
            driver_jnt.rename(driver_name)
            # Parent all driver joint to the driver group and ensure 0 rotation
            driver_jnt.setParent(driver_grp)
            driver_jnt.rotate.set(0, 0, 0)
            driver_jnt.jointOrient.set(0, 0, 0)
            # Create a transform that will drive the twist data
            driver_jnt_ref = pymel.createNode('transform')
            driver_jnt_ref.setParent(driver_jnt)
            driver_jnt_ref.setMatrix(driver_jnt.getMatrix(worldSpace=True), worldSpace=True)
            driver_jnt_ref.rename(driver_name + '_ref')
            driver_refs.append(driver_jnt_ref) # Keep them to connect the ref on the subjnts later
            if self.create_bend:
                if i != 0 and i != (len(driverjnts) - 1):  # There will be no ctrl for the first and last twist jnt
                    ctrl_driver = pymel.createNode("transform")
                    ctrl_driver_name = nomenclature_jnt.resolve("ctrlDriver{0:02d}".format(i))
                    ctrl_driver.rename(ctrl_driver_name)
                    ctrl_driver.setParent(driver_grp)
                    ctrl_refs.append(ctrl_driver)

        if not self.create_bend:
            # Parent the two extremity of the ribbon to the twist driver associated
            pymel.pointConstraint(jnt_s, driverjnts[0], mo=False)
            pymel.pointConstraint(jnt_e, driverjnts[-1], mo=False)

        mid_idx = math.ceil((self.num_twist/2.0))
        before_mid_idx = math.floor((self.num_twist/2.0))
        if self.create_bend:
            # Create Ribbon
            sys_ribbon = Ribbon(self.subjnts, name=nomenclature_rig.resolve("bendRibbon"), rig=self.rig)
            sys_ribbon.build(create_ctrl=False, degree=3, num_ctrl=self.num_twist, no_subdiv=False, rot_fol=False)
            self.ctrls = sys_ribbon.create_ctrls(ctrls=self.ctrls, no_extremity=True,
                                                 constraint_rot=False, refs=self.chain_jnt[1])
            # Point constraint the driver jnt on the ribbon jnt to drive the bending
            for i, driver in enumerate(driverjnts):
                pymel.pointConstraint(sys_ribbon._ribbon_jnts[i], driver, mo=True)
                # Aim constraint the driver to create the bend effect. Skip the middle one if it as one
                # TODO - Find a best way to determine the side
                aim_vec = [1.0, 0.0, 0.0] if nomenclature_rig.side == nomenclature_rig.SIDE_L else [-1.0, 0.0, 0.0]
                aim_vec_inverse = [-1.0, 0.0, 0.0] if nomenclature_rig.side == nomenclature_rig.SIDE_L else [1.0, 0.0, 0.0]
                if mid_idx != before_mid_idx and i == (mid_idx - 1):
                    continue
                if i <= mid_idx - 1:
                    pymel.aimConstraint(sys_ribbon._follicles[i + 1], driver,
                                        mo=False, wut=2, wuo=jnt_s, aim=aim_vec, u=[0.0, 1.0, 0.0])
                else:
                    pymel.aimConstraint(sys_ribbon._follicles[i - 1], driver,
                                        mo=False, wut=2, wuo=jnt_s, aim=aim_vec_inverse, u=[0.0, 1.0, 0.0])
            for ctrl, ref in zip(self.ctrls, ctrl_refs):
                #libAttr.lock_hide_rotation(ctrl)
                libAttr.lock_hide_scale(ctrl)
                ctrl.setParent(self.grp_anm)
                pymel.parentConstraint(ref, ctrl.offset, mo=True)
            # We don't want the ribbon to scale with the system since it will follow with it's bone
            sys_ribbon.grp_rig.setParent(self.grp_rig)
            # Ensure that the ribbon jnts are following the start jnt correctly
            pymel.parentConstraint(jnt_s, sys_ribbon.ribbon_chain_grp, mo=True)
            # Parent the two extremity of the ribbon to the twist driver associated
            pymel.pointConstraint(jnt_s, sys_ribbon._ribbon_jnts[0], mo=False)
            pymel.pointConstraint(jnt_e, sys_ribbon._ribbon_jnts[-1], mo=False)

        # Create the first non roll system
        nonroll_sys_start = NonRollJoint()
        nonroll_sys_start.build(jnt_s, name=nomenclature_rig.resolve("nonrollStart"))
        nonroll_sys_start.setMatrix(jnt_s.getMatrix(worldSpace=True), worldSpace=True)
        if top_parent:
            pymel.orientConstraint(top_parent, nonroll_sys_start.node, maintainOffset=True)
            pymel.pointConstraint(jnt_s, nonroll_sys_start.node)
        pymel.parentConstraint(jnt_s, nonroll_sys_start.ikHandle, maintainOffset=True)

        # Create the second non-roll system
        nonroll_sys_end = NonRollJoint()
        nonroll_sys_end.build(jnt_e, name=nomenclature_rig.resolve("nonrollEnd"))
        nonroll_sys_end.setMatrix(jnt_e.getMatrix(worldSpace=True), worldSpace=True)
        # nonroll_sys_end.setTranslation(jnt_e.getTranslation(space='world'), space='world')
        pymel.orientConstraint(jnt_s, nonroll_sys_end.node, maintainOffset=True)
        pymel.pointConstraint(jnt_e, nonroll_sys_end.node)
        pymel.parentConstraint(jnt_e, nonroll_sys_end.ikHandle, maintainOffset=True)

        # Setup twist extraction using the two non-roll twist extractor
        # The start ref will be connected as inverted to prevent it to twist
        mdl_reverse_rotx_start = pymel.createNode("multDoubleLinear")
        pymel.connectAttr(nonroll_sys_start.twist_extractor.rotateX, mdl_reverse_rotx_start.input1)
        mdl_reverse_rotx_start.input2.set(-1.0)
        pymel.connectAttr(mdl_reverse_rotx_start.output, driver_refs[0].rotateX)

        # The last ref will be directly be connected
        pymel.connectAttr(nonroll_sys_end.twist_extractor.rotateX, driver_refs[-1].rotateX)

        # Finally, compute the twist value for the middle twists joints, also connect the ctrl rotation in the system
        # for more control
        twist_split_len = len(driver_refs[1:-1])
        for i, ref in enumerate(driver_refs[1:-1]):
            blend_w_node = pymel.createNode("blendWeighted")
            pymel.connectAttr(mdl_reverse_rotx_start.output, blend_w_node.input[0])
            pymel.connectAttr(nonroll_sys_end.twist_extractor.rotateX, blend_w_node.input[1])
            # Compute the weight of each twist in the system
            weight_start = (1.0 / (twist_split_len + 1)) * (twist_split_len - i)
            weight_end = 1.0 - weight_start
            blend_w_node.weight[0].set(weight_start)
            blend_w_node.weight[1].set(weight_end)
            blend_w_node.weight[2].set(1.0)
            pymel.connectAttr(blend_w_node.output, ref.rotateX)
            if self.create_bend:
                pymel.connectAttr(self.ctrls[i].rotateX, blend_w_node.input[2])
                pymel.connectAttr(self.ctrls[i].rotateY, ref.rotateY)
                pymel.connectAttr(self.ctrls[i].rotateZ, ref.rotateZ)

        # Cleanup
        nonroll_sys_start.setParent(scalable_grp)
        nonroll_sys_end.setParent(scalable_grp)

        # Compute the Stretch
        attr_stretch_raw = libRigging.create_stretch_node_between_2_bones(jnt_s, jnt_e, self.grp_rig.globalScale)
        pymel.connectAttr(attr_stretch_raw, driver_grp.scaleX)

        # Connect global scale
        pymel.connectAttr(self.grp_rig.globalScale, scalable_grp.scaleX)
        pymel.connectAttr(self.grp_rig.globalScale, scalable_grp.scaleY)
        pymel.connectAttr(self.grp_rig.globalScale, scalable_grp.scaleZ)

        for driver_ref, jnt in zip(driver_refs, self.subjnts):
            # If we have the bend, just orient constraint cause the subjnt are constrained to the follicle of the ribbon
            if self.create_bend:
                pymel.orientConstraint(driver_ref, jnt, mo=False)
            else:
                pymel.parentConstraint(driver_ref, jnt, mo=False)
            '''
            pymel.connectAttr(driver_ref.scaleX, jnt.scaleX)
            pymel.connectAttr(driver_ref.scaleY, jnt.scaleY)
            pymel.connectAttr(driver_ref.scaleZ, jnt.scaleZ)
            '''

        if self.auto_skin:
            self.assign_twist_weights()

    @decorator_uiexpose()
    def assign_twist_weights(self):
        skin_deformers = self.get_skinClusters_from_inputs()

        for skin_deformer in skin_deformers:
            # Ensure the source joint is in the skinCluster influences
            influenceObjects = skin_deformer.influenceObjects()
            if self.chain_jnt.start not in influenceObjects:
                continue

            # Add new joints as influence.
            for subjnt in self.subjnts:
                if subjnt in influenceObjects:
                    continue
                skin_deformer.addInfluence(subjnt, lockWeights=True, weight=0.0)
                subjnt.lockInfluenceWeights.set(False)

        for mesh in self.get_farest_affected_meshes():
            self.info("{1} --> Assign skin weights on {0}.".format(mesh.name(), self.name))
            # Transfer weight, note that since we use force_straight line, the influence
            # don't necessaryy need to be in their bind pose.
            libSkinning.transfer_weights_from_segments(mesh, self.chain_jnt.start, self.subjnts, force_straight_line=True)

    @decorator_uiexpose()
    def unassign_twist_weights(self):
        """
        Handle the skin transfert from the subjnts (twists) to the first input. Will be used if the number of twists
        change between builds
        :return: Nothing
        """
        for skin_deformer in self.get_skinClusters_from_subjnts():
            # Ensure that the start joint is in the skin cluster
            influenceObjects = skin_deformer.influenceObjects()
            if self.chain_jnt.start not in influenceObjects:
                skin_deformer.addInfluence(self.chain_jnt.start, lockWeights=True, weight=0.0)
                self.chain_jnt.start.lockInfluenceWeights.set(False)

            # Ensure subjnts are transfert correctly
            to_transfer = []
            for subjnt in self.subjnts:
                if subjnt in influenceObjects:
                    to_transfer.append(subjnt)
            libSkinning.transfer_weights(skin_deformer, to_transfer, self.chain_jnt.start)

    def get_skinClusters_from_inputs(self):
        skinClusters = set()
        for jnt in self.chain_jnt:
            for hist in jnt.listHistory(future=True):
                if isinstance(hist, pymel.nodetypes.SkinCluster):
                    skinClusters.add(hist)
        return skinClusters

    def get_skinClusters_from_subjnts(self):
        skinClusters = set()
        if self.subjnts:
            for jnt in self.subjnts:
                for hist in jnt.listHistory(future=True):
                    if isinstance(hist, pymel.nodetypes.SkinCluster):
                        skinClusters.add(hist)
        return skinClusters

    def get_farest_affected_meshes(self):
        results = set()
        for jnt in self.jnts:
            mesh = self.rig.get_farest_affected_mesh(jnt)
            if mesh:
                results.add(mesh)
        return results

    def unbuild(self, delete=True):
        '''
        Unbuild the twist bone
        '''

        '''
        # Remove twistbones skin
        for mesh in self.get_farest_affected_mesh():
            libSkinning.transfer_weights(mesh, self.subjnts, self.jnt)
        '''
        # React if the user deleted some twist influences.
        self.subjnts = filter(libPymel.is_valid_PyNode, self.subjnts)

        # Remove scaling from the subjnts before unbuilding, otherwise scale issue will occur.
        for jnt in self.subjnts:
            pymel.disconnectAttr(jnt.tx)
            pymel.disconnectAttr(jnt.ty)
            pymel.disconnectAttr(jnt.tz)
            pymel.disconnectAttr(jnt.rx)
            pymel.disconnectAttr(jnt.ry)
            pymel.disconnectAttr(jnt.rz)
            pymel.disconnectAttr(jnt.sx)
            pymel.disconnectAttr(jnt.sy)
            pymel.disconnectAttr(jnt.sz)

        # Don't disconnect input attribute when unbuilding twist bones
        super(Twistbone, self).unbuild(disconnect_attr=False)

        self.start = None
        self.end = None

        '''
        # Remove twistbones
        if delete:
            pymel.delete(list(self.subjnts))  # TODO: fix PyNodeChain
            self.subjnts = None
        '''

def register_plugin():
    return Twistbone
