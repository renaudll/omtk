import pymel.core as pymel
import collections
from omtk.core.classModule import Module
from omtk.core.classCtrl import BaseCtrl
from omtk.modules.rigRibbon import Ribbon
from omtk.libs import libCtrlShapes
from omtk.libs import libRigging
from omtk.libs import libSkinning

class Ctrl_DpSpine_IK(BaseCtrl):
    def __createNode__(self, size=None, multiplier=1.25, refs=None, **kwargs):
        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs
        if size is None and ref is not None:
            size = libRigging.get_recommended_ctrl_size(ref) * multiplier
        else:
            size = 1.0

        node = libCtrlShapes.create_shape_box(size=size, **kwargs)
        return node

class Ctrl_DpSpine_FK(BaseCtrl):
    _DEFAULT_COLOR = 18  # Baby blue

    def __createNode__(self, **kwargs):
        node = super(Ctrl_DpSpine_FK, self).__createNode__(normal=(0,1,0), multiplier=1.25, **kwargs)

        # To match dpSpine, color the shapes individually
        for shape in node.getShapes():
            shape.overrideEnabled.set(1)
            shape.overrideColor.set(self._DEFAULT_COLOR)

        return node

class DpSpine(Module):
    """
    Spine setup similar to dpAutoRig.
    Note that the spline ctrls orientation follow the world axis by default.
    """
    IS_SIDE_SPECIFIC = False
    _CLASS_CTRL_IK = Ctrl_DpSpine_IK
    _CLASS_CTRL_FK = Ctrl_DpSpine_FK

    def __init__(self, *args, **kwargs):
        super(DpSpine, self).__init__(*args, **kwargs)
        self.ctrl_ik_dwn = None
        self.ctrl_ik_upp = None
        self.ctrl_fk_dwn = None
        self.ctrl_fk_mid = None
        self.ctrl_fk_upp = None

        self.jnt_squash_dwn = None
        self.jnt_squash_mid = None
        self.enable_squash = True

    def validate(self, rig):
        super(DpSpine, self).validate()
        if len(self.jnts) != 3:
            raise Exception("DpSpine need exactly 3 joints.")

    def build(self, rig, *args, **kwargs):
        if len(self.chain_jnt) != 3:
            raise Exception("Expected 3 joints. Got {0}.".format(len(self.chain)))

        super(DpSpine, self).build(rig, *args, **kwargs)

        nomenclature_anm = self.get_nomenclature_anm(rig)
        nomenclature_rig = self.get_nomenclature_rig(rig)
        nomenclature_jnt = self.get_nomenclature_jnt(rig)

        #
        # Create ctrls
        #

        jnt_dwn = self.chain_jnt[0]
        jnt_mid = self.chain_jnt[1]
        jnt_upp = self.chain_jnt[2]

        pos_dwn_world = jnt_dwn.getTranslation(space='world')
        pos_mid_world = jnt_mid.getTranslation(space='world')
        pos_upp_world = jnt_upp.getTranslation(space='world')

        # Create IK ctrls
        ctrl_ik_dwn_name = nomenclature_anm.resolve('HipsA')
        if not isinstance(self.ctrl_ik_dwn, self._CLASS_CTRL_IK):
            self.ctrl_ik_dwn = self._CLASS_CTRL_IK()
        self.ctrl_ik_dwn.build(rig, name=ctrl_ik_dwn_name, refs=jnt_dwn)
        self.ctrl_ik_dwn.setTranslation(pos_dwn_world)
        self.ctrl_ik_dwn.setParent(self.grp_anm)

        ctrl_ik_upp_name = nomenclature_anm.resolve('ChestA')
        if not isinstance(self.ctrl_ik_upp, self._CLASS_CTRL_IK):
            self.ctrl_ik_upp = self._CLASS_CTRL_IK()
        self.ctrl_ik_upp.build(rig, name=ctrl_ik_upp_name, refs=jnt_upp)
        self.ctrl_ik_upp.setTranslation(pos_upp_world)
        self.ctrl_ik_upp.setParent(self.ctrl_ik_dwn)

        # Ensure the ctrl_ik_upp pivot is a the middle.
        ctrl_ik_upp_pivot = pos_mid_world - pos_upp_world
        self.ctrl_ik_upp.rotatePivot.set(ctrl_ik_upp_pivot)
        self.ctrl_ik_upp.scalePivot.set(ctrl_ik_upp_pivot)

        # Create FK ctrls
        ctrl_fk_color = 18  # Baby blue

        ctrl_fk_dwn_name = nomenclature_anm.resolve('HipsB')
        if not isinstance(self.ctrl_fk_dwn, self._CLASS_CTRL_FK):
            self.ctrl_fk_dwn = self._CLASS_CTRL_FK()
        self.ctrl_fk_dwn.build(rig, name=ctrl_fk_dwn_name, refs=jnt_dwn)
        self.ctrl_fk_dwn.setTranslation(pos_dwn_world)
        self.ctrl_fk_dwn.setParent(self.ctrl_ik_dwn)

        ctrl_fk_upp_name = nomenclature_anm.resolve('ChestB')
        if not isinstance(self.ctrl_fk_upp, self._CLASS_CTRL_FK):
            self.ctrl_fk_upp = self._CLASS_CTRL_FK()
        self.ctrl_fk_upp.build(rig, name=ctrl_fk_upp_name, refs=jnt_upp)
        self.ctrl_fk_upp.setTranslation(pos_upp_world)
        self.ctrl_fk_upp.setParent(self.ctrl_ik_upp)

        ctrl_fk_mid_name = nomenclature_anm.resolve('Middle1')
        if not isinstance(self.ctrl_fk_mid, self._CLASS_CTRL_FK):
            self.ctrl_fk_mid = self._CLASS_CTRL_FK()
        self.ctrl_fk_mid.build(rig, name=ctrl_fk_mid_name, refs=jnt_mid)
        self.ctrl_fk_mid.setTranslation(pos_mid_world)
        self.ctrl_fk_mid.setParent(self.ctrl_ik_dwn)

        # Ensure the ctrl_fk_mid follow ctrl_ik_upp and ctrl_ik_dwn
        # Note that this is evil, a parentConstraint should never have two targets.
        # HACK: To bypass flip issues, we'll use reference object that have no parent space.
        ref_parent = pymel.createNode('transform', name=nomenclature_rig.resolve('ref'))
        ref_parent.setParent(self.grp_rig)
        pymel.parentConstraint(self.ctrl_fk_dwn, ref_parent)
        ref_s = pymel.createNode('transform', name=nomenclature_rig.resolve('ref_s'))
        pymel.parentConstraint(self.ctrl_fk_upp, ref_s)
        ref_s.setParent(ref_parent)
        ref_e = pymel.createNode('transform', name=nomenclature_rig.resolve('ref_e'))
        pymel.parentConstraint(self.ctrl_fk_dwn, ref_e)
        ref_e.setParent(ref_parent)
        pymel.parentConstraint(ref_s, ref_e, self.ctrl_fk_mid.offset, maintainOffset=True)

        #
        # Create ribbon rig
        #

        sys_ribbon = Ribbon(self.chain_jnt, name=self.name)
        sys_ribbon.build(rig, create_ctrl=False, degree=3)
        sys_ribbon.grp_rig.setParent(self.grp_rig)

        # Constraint the ribbon joints to the ctrls
        pymel.parentConstraint(self.ctrl_fk_dwn, sys_ribbon._ribbon_jnts[0], maintainOffset=True)
        pymel.parentConstraint(self.ctrl_fk_mid, sys_ribbon._ribbon_jnts[1], maintainOffset=True)
        pymel.parentConstraint(self.ctrl_fk_upp, sys_ribbon._ribbon_jnts[2], maintainOffset=True)

        # Ensure the last ribbon chain follow the rotation of the chest ctrl.
        last_jnt = self.chain.end
        last_jnt.rotateX.disconnect()
        last_jnt.rotateY.disconnect()
        last_jnt.rotateZ.disconnect()
        pymel.orientConstraint(ctrl_fk_upp_name, last_jnt, maintainOffset=True)

        #HACK : The rotation of the joint will be an aim constraint instead of the follicle rotation
        #Create intermediate obj to compute the aim constraint
        aim_grp = pymel.createNode("transform")
        aim_grp_name = nomenclature_rig.resolve("aimTarget_grp")
        aim_grp.rename(aim_grp_name)
        aim_grp.setParent(self.grp_rig)
        for i, jnt in enumerate(self.chain_jnt):
            if i < (len(self.chain_jnt) - 1):
                jnt.rotateX.disconnect()
                jnt.rotateY.disconnect()
                jnt.rotateZ.disconnect()

                target = self.ctrl_fk_mid if i == 0 else self.ctrl_fk_upp

                aim_target_off = pymel.createNode("transform")
                aim_target_off_name = nomenclature_rig.resolve("aimTargetOffset" + jnt.name())
                aim_target_off.rename(aim_target_off_name)
                aim_target_off.setParent(aim_grp)
                aim_target_off.setMatrix(jnt.getMatrix(worldSpace=True))
                pymel.parentConstraint(sys_ribbon._follicles[i], aim_target_off, mo=True)

                pymel.aimConstraint(target, jnt, mo=True,
                                    u = (0.0, 1.0, 0.0), wuo=aim_target_off, wu=(0.0, 1.0, 0.0), wut="objectrotation")

        #
        # Configure the squash
        # The standard in omtk is that if something need to stretch or squash, it need to be separated from the main hierarchy.
        #
        #TODO : Keep in network
        if self.enable_squash:
            # Create the squash hierarchy
            jnt_squash_dwn_name = nomenclature_jnt.rebuild(jnt_dwn.name()).resolve('squash')
            self.jnt_squash_dwn = pymel.createNode('joint', name=jnt_squash_dwn_name)
            self.jnt_squash_dwn.setParent(jnt_dwn)
            self.jnt_squash_dwn.t.set(0,0,0)
            self.jnt_squash_dwn.r.set(0,0,0)
            self.jnt_squash_dwn.jointOrientX.set(0)
            self.jnt_squash_dwn.jointOrientY.set(0)
            self.jnt_squash_dwn.jointOrientZ.set(0)

            jnt_squash_mid_name = nomenclature_jnt.rebuild(jnt_mid.name()).resolve('squash')
            self.jnt_squash_mid= pymel.createNode('joint', name=jnt_squash_mid_name)
            self.jnt_squash_mid.setParent(jnt_mid)
            self.jnt_squash_mid.t.set(0,0,0)
            self.jnt_squash_mid.r.set(0,0,0)
            self.jnt_squash_mid.jointOrientX.set(0)
            self.jnt_squash_mid.jointOrientY.set(0)
            self.jnt_squash_mid.jointOrientZ.set(0)

            # Add squash amount attribute
            squash_attr_name = 'squashAmount'
            pymel.addAttr(self.grp_rig, longName=squash_attr_name, defaultValue=1.0)
            attr_squash_amount = self.grp_rig.attr(squash_attr_name)

            # Compute the squash
            attr_stretch_u, attr_stretch_v, node_arc_length = libRigging.create_stretch_attr_from_nurbs_plane(sys_ribbon._ribbon_shape, v=0.5)
            node_arc_length_transform = node_arc_length.getParent()
            node_arc_length_transform .setParent(self.grp_rig)
            attr_squash_raw = libRigging.create_squash_attr_simple(attr_stretch_u)

            # Apply the global uniform scale
            attr_squash_raw_scale = libRigging.create_utility_node('multiplyDivide', input1X=attr_squash_raw, input2X=self.globalScale).outputX

            attr_squash = libRigging.create_utility_node('blendTwoAttr', input=[1.0, attr_squash_raw_scale], attributesBlender=attr_squash_amount).output

            # Apply the squash
            # Note that the squash on the first joint is hardcoded to 80%.
            attr_squash_first_jnt = libRigging.create_utility_node('blendTwoAttr', input=[1.0, attr_squash_raw_scale], attributesBlender=0.8).output
            pymel.connectAttr(attr_squash_first_jnt , self.jnt_squash_dwn.scaleY)
            pymel.connectAttr(attr_squash_first_jnt , self.jnt_squash_dwn.scaleZ)

            pymel.connectAttr(attr_squash , self.jnt_squash_mid.scaleY)
            pymel.connectAttr(attr_squash , self.jnt_squash_mid.scaleZ)

            # Finally, transfer the skin to the squash jnt
            # TODO: Modify the skinCluster connections instead?
            libSkinning.transfer_weights_replace(jnt_dwn, self.jnt_squash_dwn)
            libSkinning.transfer_weights_replace(jnt_mid, self.jnt_squash_mid)

                #Ensure global scale is working correctly
        pymel.connectAttr(self.grp_rig.globalScale, ref_parent.scaleX)
        pymel.connectAttr(self.grp_rig.globalScale, ref_parent.scaleY)
        pymel.connectAttr(self.grp_rig.globalScale, ref_parent.scaleZ)

    def unbuild(self):
        # Restore the original skin and remove the squash joints
        if self.jnt_squash_dwn and self.jnt_squash_dwn.exists():
            jnt_dwn = self.chain_jnt[0]
            libSkinning.transfer_weights_replace(self.jnt_squash_dwn, jnt_dwn)
            pymel.delete(self.jnt_squash_dwn)

        if self.jnt_squash_mid and self.jnt_squash_mid.exists():
            jnt_mid = self.chain_jnt[1]
            libSkinning.transfer_weights_replace(self.jnt_squash_mid, jnt_mid)
            pymel.delete(self.jnt_squash_mid)

        self.jnt_squash_dwn = None
        self.jnt_squash_dwn = None
        super(DpSpine, self).unbuild()

    def get_parent(self, parent):
        if parent == self.chain_jnt[0]:
            return self.ctrl_fk_dwn
        if parent == self.chain_jnt[-1]:
            return self.ctrl_fk_upp

        return super(DpSpine, self).get_parent(parent)

    def get_pin_locations(self):
        if not self.ctrl_fk_upp or not self.ctrl_fk_dwn:
            return ()
        return (
            (self.ctrl_fk_upp.node, 'Chest'),
            (self.ctrl_fk_dwn.node, 'Cog')
        )




