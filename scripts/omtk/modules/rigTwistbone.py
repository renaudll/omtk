import math

import pymel.core as pymel

from omtk.core.classModule import Module
from omtk.core.utils import decorator_uiexpose
from omtk.libs import libRigging
from omtk.libs import libSkinning
from omtk.libs import libPymel
from omtk.modules.rigRibbon import Ribbon
from omtk.libs import libAttr
from omtk.core.compounds import MANAGER


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

    def build(
        self,
        orient_ik_ctrl=True,
        num_twist=None,
        create_bend=None,
        realign=True,
        *args,
        **kwargs
    ):
        """
        :param orient_ik_ctrl: 
        :param num_twist: 
        :param create_bend: 
        :param realign:
        :param args: 
        :param kwargs: 
        :return: 
        """
        if len(self.chain_jnt) < 2:
            raise Exception(
                "Invalid input count. Expected 2, got {0}. {1}".format(
                    len(self.chain_jnt), self.chain_jnt
                )
            )

        # Support some properties that could be redefined at build time
        if num_twist:
            self.num_twist = num_twist

        if create_bend is not None:
            self.create_bend = create_bend

        # Twistbone is different from other modules as they don't drive their inputs.
        # We modify the kwargs directly so we don't have to expose disconnect_inputs
        # in the function signature.
        kwargs["disconnect_inputs"] = False

        super(Twistbone, self).build(create_grp_anm=self.create_bend, *args, **kwargs)

        top_parent = self.chain[0].getParent()
        jnt_s = self.chain_jnt[0]
        jnt_e = self.chain_jnt[1]

        nomenclature_rig = self.get_nomenclature_rig()
        nomenclature_jnt = self.rig.nomenclature(
            jnt_s.stripNamespace().nodeName(), suffix=self.rig.nomenclature.type_jnt
        )  # Hack: find a better way!

        scalable_grp = pymel.createNode("transform")
        scalable_grp.setParent(self.grp_rig)
        scalable_grp.rename(nomenclature_rig.resolve("scalable"))

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
            self.subjnts = libRigging.create_chain_between_objects(
                jnt_s, jnt_e, self.num_twist
            )
        elif realign:
            # Position the subjnts at equidistance from each others.
            num_subjnts = len(self.subjnts)
            base_tm = jnt_s.getMatrix(worldSpace=True)
            sp = jnt_s.getTranslation(space="world")
            ep = jnt_e.getTranslation(space="world")
            delta = ep - sp
            for i, subjnt in enumerate(self.subjnts):
                ratio = float(i) / (num_subjnts - 1)
                tm = base_tm.copy()
                tm.translate = delta * ratio + sp
                subjnt.setMatrix(tm, worldSpace=True)

        if self.subjnts[0].getParent() != jnt_s:
            self.subjnts[0].setParent(jnt_s)

        driver_grp = pymel.createNode("transform")
        driver_grp.setParent(scalable_grp)
        driver_grp.setMatrix(jnt_s.getMatrix(worldSpace=True), worldSpace=True)
        driver_grp.rename(nomenclature_rig.resolve("driverJnt_grp"))
        pymel.parentConstraint(jnt_s, driver_grp)

        # Create a second chain that will drive the rotation of the skinned joint
        driverjnts = libRigging.create_chain_between_objects(
            jnt_s, jnt_e, self.num_twist
        )

        # Rename the skinning subjnts
        for i, sub_jnt in enumerate(self.subjnts):
            sub_jnt.segmentScaleCompensate.set(0)  # Remove segment scale compensate

            # Right now, we take into consideration that the system will be named Side_SysName(Ex:Upperarm_Twist)
            # nomenclature_inf = nomenclature_jnt.copy()
            # nomenclature_inf.add_tokens('twist', '{0:02d}'.format(i))
            # jnt_name = nomenclature_inf.resolve()
            # jnt_name = nomenclature_jnt.resolve("twist{0:02d}".format(i))
            jnt_name = nomenclature_jnt.resolve("{0:02d}".format(i))
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
            driver_jnt_ref = pymel.createNode("transform")
            driver_jnt_ref.setParent(driver_jnt)
            driver_jnt_ref.setMatrix(
                driver_jnt.getMatrix(worldSpace=True), worldSpace=True
            )
            driver_jnt_ref.rename(driver_name + "_ref")
            driver_refs.append(
                driver_jnt_ref
            )  # Keep them to connect the ref on the subjnts later
            if self.create_bend:
                if i != 0 and i != (
                    len(driverjnts) - 1
                ):  # There will be no ctrl for the first and last twist jnt
                    ctrl_driver = pymel.createNode("transform")
                    ctrl_driver_name = nomenclature_jnt.resolve(
                        "ctrlDriver{0:02d}".format(i)
                    )
                    ctrl_driver.rename(ctrl_driver_name)
                    ctrl_driver.setParent(driver_grp)
                    ctrl_refs.append(ctrl_driver)

        if not self.create_bend:
            # Parent the two extremity of the ribbon to the twist driver associated
            pymel.pointConstraint(jnt_s, driverjnts[0], mo=False)
            pymel.pointConstraint(jnt_e, driverjnts[-1], mo=False)

        mid_idx = math.ceil((self.num_twist / 2.0))
        before_mid_idx = math.floor((self.num_twist / 2.0))
        if self.create_bend:
            # Create Ribbon
            sys_ribbon = self.init_module(Ribbon, None, inputs=self.subjnts)
            sys_ribbon.build(
                create_ctrl=False,
                degree=3,
                num_ctrl=self.num_twist,
                no_subdiv=False,
                rot_fol=False,
            )
            self.ctrls = sys_ribbon.create_ctrls(
                ctrls=self.ctrls,
                no_extremity=True,
                constraint_rot=False,
                refs=self.chain_jnt[1],
            )
            # Point constraint the driver jnt on the ribbon jnt to drive the bending
            for i, driver in enumerate(driverjnts):
                pymel.pointConstraint(sys_ribbon._ribbon_jnts[i], driver, mo=True)
                # Aim constraint the driver to create the bend effect. Skip the middle one if it as one
                # TODO - Find a best way to determine the side
                aim_vec = (
                    [1.0, 0.0, 0.0]
                    if nomenclature_rig.side == nomenclature_rig.SIDE_L
                    else [-1.0, 0.0, 0.0]
                )
                aim_vec_inverse = (
                    [-1.0, 0.0, 0.0]
                    if nomenclature_rig.side == nomenclature_rig.SIDE_L
                    else [1.0, 0.0, 0.0]
                )
                if mid_idx != before_mid_idx and i == (mid_idx - 1):
                    continue
                if i <= mid_idx - 1:
                    pymel.aimConstraint(
                        sys_ribbon._follicles[i + 1],
                        driver,
                        mo=False,
                        wut=2,
                        wuo=jnt_s,
                        aim=aim_vec,
                        u=[0.0, 1.0, 0.0],
                    )
                else:
                    pymel.aimConstraint(
                        sys_ribbon._follicles[i - 1],
                        driver,
                        mo=False,
                        wut=2,
                        wuo=jnt_s,
                        aim=aim_vec_inverse,
                        u=[0.0, 1.0, 0.0],
                    )

            for ctrl, ref in zip(self.ctrls, ctrl_refs):
                # libAttr.lock_hide_rotation(ctrl)
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

        # Create a twist extract component
        # TODO: There are useless unitConversion in the compound, remove them.
        extractor = _create_twist_extractor(
            nomenclature_rig.resolve("extractTwist"), top_parent, jnt_s, jnt_e
        )

        # For now we need to manually inverse the start twist
        # TODO: Adjust compound?
        attr_twist_s = libRigging.create_utility_node(
            "multiplyDivide",
            input1X=pymel.Attribute("%s.outTwistS" % extractor.output),
            input2X=-1,
        ).outputX

        # Connect extracted twist to joints
        _connect_twist(
            attr_twist_s,
            "%s.outTwistE" % extractor.output,
            [driver.rotateX for driver in driver_refs],
        )

        # TODO: Should be done on the post-build of the rig
        extractor.explode(remove_namespace=True)

        # If we created a ribbon, add the controllers twist to the result
        if self.create_bend:
            for ctrl, jnt in zip(self.ctrls, driver_refs[1:-1]):
                libRigging.connectAttr_withBlendWeighted(ctrl.rotateX, jnt.rotateX)
                libRigging.connectAttr_withBlendWeighted(ctrl.rotateY, jnt.rotateY)
                libRigging.connectAttr_withBlendWeighted(ctrl.rotateZ, jnt.rotateZ)

        # Compute the Stretch
        attr_stretch_raw = libRigging.create_stretch_node_between_2_bones(
            jnt_s, jnt_e, self.grp_rig.globalScale
        )
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

        if self.auto_skin:
            self.assign_twist_weights()

    @decorator_uiexpose()
    def assign_twist_weights(self):
        libSkinning.assign_twist_weights(self.chain_jnt.start, self.subjnts)

    @decorator_uiexpose()
    def unassign_twist_weights(self):
        """
        Handle the skin transfert from the subjnts (twists) to the first input. 
        Will be used if the number of twists change between builds
        :return: Nothing
        """
        libSkinning.unassign_twist_weights(self.subjnts, self.chain_jnt.start)

    def get_skinClusters_from_inputs(self):
        skinClusters = set()
        jnts = [
            jnt for jnt in self.chain_jnt if jnt and jnt.exists()
        ]  # Only handle existing objects
        for jnt in jnts:
            for hist in jnt.listHistory(future=True):
                if isinstance(hist, pymel.nodetypes.SkinCluster):
                    skinClusters.add(hist)
        return skinClusters

    def get_skinClusters_from_subjnts(self):
        skinClusters = set()
        jnts = [
            jnt for jnt in self.subjnts if jnt and jnt.exists()
        ]  # Only handle existing objects
        for jnt in jnts:
            for hist in jnt.listHistory(future=True, levels=1):
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
        """
        Unbuild the twist bone
        """

        # Remove twistbones skin
        self.unassign_twist_weights()

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

        """
        # Remove twistbones
        if delete:
            pymel.delete(list(self.subjnts))  # TODO: fix PyNodeChain
            self.subjnts = None
        """


def _create_twist_extractor(name, parent, start, end):
    """
    Create a network that extract two twist values between two joints.
    :param str name: Name of the network.
    :param parent: Optional parent or the first joint
    :param start: The first joint
    :param end: The last joint
    :return: A compound
    """
    extractor = MANAGER.create_compound(name="omtk.TwistExtractor", namespace=name)
    extractor_inn = pymel.PyNode(extractor.input)
    # TODO: Will bind pose be preserved on file save?
    # TODO: The worldMatrix attribute will bypass global scaling, is this okay?
    extractor_inn.bind1.set(
        parent.getMatrix(worldSpace=True) if parent else pymel.datatypes.Matrix()
    )
    extractor_inn.bind2.set(start.getMatrix(worldSpace=True))
    extractor_inn.bind3.set(end.getMatrix(worldSpace=True))
    if parent:
        pymel.connectAttr(parent.worldMatrix, extractor_inn.inn1)
    pymel.connectAttr(start.worldMatrix, extractor_inn.inn2)
    pymel.connectAttr(end.worldMatrix, extractor_inn.inn3)
    return extractor


def _connect_twist(start, end, attrs):
    """
    Linearly interpolate two values and connect it to multiple attributes.

    :param start: The start value. Used as is for attr 0
    :type start: str or pymel.Attribute
    :param end: The end value. Used as is for attr n
    :type end: str or pymel.Attribute
    :param attrs: A list of attributes to connect to.
    """
    pymel.connectAttr(start, attrs[0])

    # Use a blendWeighted for each intermediate attributes.
    length = len(attrs[1:-1])
    for i, attr in enumerate(attrs[1:-1]):
        weight = (1.0 / (length + 1)) * (length - i)
        libRigging.connectAttrs_withBlendWeighted(
            [start, end], attr, weights=[weight, 1.0 - weight]
        )

    pymel.connectAttr(end, attrs[-1])


def register_plugin():
    return Twistbone
