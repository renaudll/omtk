"""
Logic for the "Limb" module
"""

import collections

from maya import cmds
import pymel.core as pymel

from omtk.core import constants
from omtk.core.module import Module, CompoundModule
from omtk.core.ctrl import BaseCtrl
from omtk.core.utils import ui_expose
from omtk.modules.ik import IK, _create_joint_from_binds
from omtk.modules.fk import FK
from omtk.modules.twistbone import Twistbone
from omtk.libs import libRigging
from omtk.libs import libCtrlShapes
from omtk.libs import libAttr
from omtk.libs import libPython
from omtk.vendor.omtk_compound.core import create_empty


class BaseAttHolder(BaseCtrl):
    def create_ctrl(self, size=None, refs=None, **kwargs):
        # Resolve size automatically if refs are provided.
        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs
        if size is None and ref is not None:
            size = libRigging.get_recommended_ctrl_size(ref)
        else:
            size = 1.0

        node = libCtrlShapes.create_shape_attrholder(size=size, **kwargs)

        # Hide default keyable attributes
        node.t.set(channelBox=False)
        node.r.set(channelBox=False)
        node.s.set(channelBox=False)

        return node


class CtrlElbow(BaseCtrl):
    def create_ctrl(self, size=None, refs=None, *args, **kwargs):
        # Resolve size automatically if refs are provided
        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs
        if size is None and ref is not None:
            size = libRigging.get_recommended_ctrl_size(ref) * 1.25
        else:
            size = 1.0

        return libCtrlShapes.create_shape_cross(size=size, **kwargs)


class LimbFK(FK):
    _FORCE_INPUT_NAME = True
    AFFECT_INPUTS = False

    def build(self, *args, **kwargs):
        super(LimbFK, self).build(*args, **kwargs)

        # Lock X and Y axis on the elbow/knee ctrl
        if self.rig.DEFAULT_UPP_AXIS == constants.Axis.y:
            libAttr.lock_hide_rotation(self.ctrls[1], z=False)
        elif self.rig.DEFAULT_UPP_AXIS == constants.Axis.z:
            libAttr.lock_hide_rotation(self.ctrls[1], y=False)


class LimbIK(IK):
    AFFECT_INPUTS = False


class ElbowBlend(CompoundModule):
    """
    Chain of joints aim constrained to each other.
    This Provide the animator a friendly way of cheating a chain by moving intermediate nodes.
    """

    AFFECT_INPUTS = False
    _CLASS_CTRL = CtrlElbow

    def build(self, **kwargs):
        naming = self.get_nomenclature()
        naming_anm = self.get_nomenclature_anm()

        super(ElbowBlend, self).build(**kwargs)

        # Hack: Position the grp_anm in advance...
        if self.parent_jnt:
            self.grp_anm.setMatrix(self.parent_jnt.getMatrix(worldSpace=True))

        chain_blends = _create_joint_from_binds(
            self.compound_inputs.bind, naming + "blend"
        )
        chain_elbow = _create_joint_from_binds(
            self.compound_inputs.bind, naming + "elbow", connect=False,
            jointOrient=False  # since we are using parentConstraint we need to move rotation out of joint orient
        )
        chain_blends.start.setParent(self.grp_rig)
        chain_elbow.start.setParent(self.grp_rig)

        # Initialize ctrls
        num_ctrls = len(self.chain) - 2
        libPython.resize_list(self.ctrls, num_ctrls)
        self.ctrls = [self._CLASS_CTRL.from_instance(ctrl) for ctrl in self.ctrls]

        pymel.pointConstraint(chain_blends.start, chain_elbow.start)
        pymel.pointConstraint(chain_blends.end, chain_elbow.end)

        # Create elbow ctrl
        for idx, ((blend_prev, blend, blend_next), (elbow_prev, elbow, _)) in enumerate(
            zip(libPython.triplewise(chain_blends), libPython.triplewise(chain_elbow))
        ):
            ctrl_elbow_name = naming_anm.resolve("elbow{:02}".format(idx))
            ctrl_elbow_ref = blend  # jnt_elbow
            ctrl = self.ctrls[idx]
            ctrl.build(refs=ctrl_elbow_ref)
            ctrl.rename(ctrl_elbow_name)
            ctrl.setParent(self.grp_anm)

            attr_ctrl_tm = ctrl.worldMatrix
            if self.parent_jnt:
                attr_ctrl_tm = libRigging.create_multiply_matrix(
                    [attr_ctrl_tm, self.parent_jnt.worldInverseMatrix]
                )

            attr_ctrl_elbow_offset_tm = blend.worldMatrix
            libRigging.connect_matrix_to_node(attr_ctrl_elbow_offset_tm, ctrl.offset)

            ref = pymel.createNode("transform", parent=self.grp_rig)
            libRigging.connect_matrix_to_node(attr_ctrl_tm, ref)

            pymel.pointConstraint(ref, elbow)
            pymel.aimConstraint(
                ref, elbow_prev, worldUpType=2, worldUpObject=blend_prev, maintainOffset=True
            )
            pymel.aimConstraint(
                blend_next, elbow, worldUpType=2, worldUpObject=blend, maintainOffset=True
            )

        # Constraint the last elbow joint on the blend joint at the ctrl index
        pymel.orientConstraint(chain_blends[-1], chain_elbow[-1])

        for idx, blend in enumerate(chain_elbow):
            pymel.connectAttr(blend.matrix, self.compound_outputs.out[idx])

        self._weird_grp_anm_dance()

    def _build_compound(self):
        inst = create_empty()
        cmds.addAttr(inst.input, longName="bind", dataType="matrix", multi=True)
        cmds.addAttr(inst.output, longName="out", dataType="matrix", multi=True)

        attr_bind = pymel.PyNode(inst.input).bind
        for idx, jnt in enumerate(self.chain):
            attr_bind[idx].set(jnt.getMatrix())

        return inst

    def parent_to(self, parent):
        pass  # TODO: JUST REMOVE THIS ALREADY


class Limb(Module):
    """
    Generic IK/FK setup. Twistbones are included.
    """

    kAttrName_State = "fkIk"  # The name of the IK/FK attribute
    _CLASS_SYS_IK = LimbIK
    _CLASS_SYS_FK = LimbFK
    _CLASS_SYS_ELBOW = ElbowBlend
    _CLASS_CTRL_ATTR = BaseAttHolder
    _CLASS_SYS_TWIST = Twistbone

    def __init__(self, *args, **kwargs):
        super(Limb, self).__init__(*args, **kwargs)
        self.sysIK = None  # type: IK
        self.sysFK = None  # type: FK
        self.sysElbow = None  # type: ElbowBlend
        self.sys_twist = []  # type: List[Twistbone]
        self.create_twist = True
        self.ctrl_elbow = None
        self.attState = None
        self.offset_ctrl_ik = None
        self.ctrl_attrs = None
        self.STATE_IK = 1.0
        self.STATE_FK = 0.0

    def build(self, *args, **kwargs):
        self.sysIK = self._CLASS_SYS_IK.from_instance(
            self, self.sysIK, "ik", inputs=self.chain_jnt,
        )

        self.sysFK = self._CLASS_SYS_FK.from_instance(
            self, self.sysFK, "fk", inputs=self.chain_jnt,
        )

        self.sysElbow = self._CLASS_SYS_ELBOW.from_instance(
            self, self.sysElbow, "elbow", inputs=self.chain_jnt
        )

        # Create twist bones
        if self.create_twist:
            num_twist_sys = self.sysIK.iCtrlIndex
            # Ensure the twist bone list have the proper size
            libPython.resize_list(self.sys_twist, num_twist_sys)

            # If the IK system is a quad, we need to have two twist system
            self.sys_twist = [
                self._CLASS_SYS_TWIST.from_instance(
                    self, sys_twist, "twist%s" % i, inputs=self.chain_jnt[i : (i + 2)],
                )
                for i, sys_twist in enumerate(self.sys_twist)
            ]
        else:
            self.sys_twist = []

        super(Limb, self).build(*args, **kwargs)

        naming_anm = self.get_nomenclature_anm()
        naming = self.get_nomenclature_rig()

        # Store the offset between the ik ctrl and it's joint equivalent.
        # Useful when they don't match for example on a leg setup.
        self.offset_ctrl_ik = (
            self.sysIK.ctrl_ik.getMatrix(worldSpace=True)
            * self.chain.end.getMatrix(worldSpace=True).inverse()
        )

        # Add attributes to the attribute holder.
        # Add ikFk state attribute on the grp_rig.
        # This is currently controlled by self.ctrl_attrs.
        pymel.addAttr(
            self.grp_rig,
            longName=self.kAttrName_State,
            hasMinValue=True,
            hasMaxValue=True,
            minValue=0,
            maxValue=1,
            defaultValue=1,
            k=True,
        )
        attr_ik_weight = self.grp_rig.attr(self.kAttrName_State)
        attr_fk_weight = libRigging.create_utility_node(
            "reverse", inputX=attr_ik_weight
        ).outputX

        # Create attribute holder (this is where the IK/FK attribute will be stored)
        # Note that this is production specific and
        # should be defined in a sub-class implementation.
        jnt_hand = self.chain_jnt[self.sysIK.iCtrlIndex]
        ctrl_attrs_name = naming_anm.resolve("atts")
        if not isinstance(self.ctrl_attrs, self._CLASS_CTRL_ATTR):
            self.ctrl_attrs = self._CLASS_CTRL_ATTR()
        self.ctrl_attrs.build(name=ctrl_attrs_name, refs=jnt_hand)
        self.ctrl_attrs.setParent(self.grp_anm)
        pymel.parentConstraint(jnt_hand, self.ctrl_attrs.offset)

        pymel.addAttr(
            self.ctrl_attrs,
            longName=self.kAttrName_State,
            hasMinValue=True,
            hasMaxValue=True,
            minValue=0,
            maxValue=1,
            defaultValue=1,
            k=True,
        )
        pymel.connectAttr(
            self.ctrl_attrs.attr(self.kAttrName_State),
            self.grp_rig.attr(self.kAttrName_State),
        )

        # Create a chain for blending ikChain and fkChain
        binds = [jnt.getMatrix() for jnt in self.chain_jnt]
        chain_blend = _create_joint_from_binds(binds, naming)
        chain_blend[0].setParent(self.grp_rig)

        ik_compound_out = pymel.PyNode(self.sysIK.compound.output)
        fk_compound_out = pymel.PyNode(self.sysFK.compound.output)
        for blend, attr_ik_tm, attr_fk_tm in zip(
            chain_blend, ik_compound_out.out, fk_compound_out.out
        ):
            attr_tm = libRigging.create_blend_two_matrix(
                attr_ik_tm, attr_fk_tm, attr_ik_weight
            )
            libRigging.connect_matrix_to_node(
                attr_tm, blend, rotate=False, jointOrient=True
            )

        for idx, (blend, jnt) in enumerate(zip(chain_blend, self.chain_jnt)):
            pymel.connectAttr(blend.matrix, self.sysElbow.compound_inputs.bind[idx])
            libRigging.connect_matrix_to_node(
                self.sysElbow.compound_outputs.out[idx], jnt
            )

        # Connect visibility
        pymel.connectAttr(attr_ik_weight, self.sysIK.grp_anm.visibility)
        pymel.connectAttr(attr_fk_weight, self.sysFK.grp_anm.visibility)

        self.attState = attr_ik_weight  # Expose state

    def unbuild(self):
        super(Limb, self).unbuild()

        self.attState = None

    def parent_to(self, parent):
        # Do nothing as everything is handled by the sysIK and sysFK modules.
        pass

    #
    # Functions called for IK/FK switch (animation tools)
    #

    def snap_ik_to_fk(self):
        """
        Match the IK chain from the FK chain.
        """
        # Position ikCtrl
        ctrl_ik_tm = self.chain_jnt[self.sysIK.iCtrlIndex].getMatrix(worldSpace=True)
        self.sysIK.ctrl_ik.node.setMatrix(
            self.offset_ctrl_ik * ctrl_ik_tm, worldSpace=True
        )

        # Position swivel
        pos_s = self.sysFK.ctrls[0].getTranslation(space="world")
        pos_m = self.sysFK.ctrls[self.sysIK.iCtrlIndex - 1].getTranslation(
            space="world"
        )
        pos_e = self.sysFK.ctrls[self.sysIK.iCtrlIndex].getTranslation(space="world")

        length_start = pos_m.distanceTo(pos_s)
        length_end = pos_m.distanceTo(pos_e)
        length_ratio = length_start / (length_start + length_end)

        pos_middle = (pos_e - pos_s) * length_ratio + pos_s
        dir_swivel = pos_m - pos_middle
        dir_swivel.normalize()
        pos_swivel = (dir_swivel * self.sysIK.swivelDistance) + pos_middle
        self.sysIK.ctrl_swivel.node.setTranslation(pos_swivel, space="world")

    def snap_fk_to_ik(self):
        """
        Match the FK chain from the IK chain.
        """
        for ctrl, jnt in zip(self.sysFK.ctrls, self.chain_jnt):
            ctrl.node.setMatrix(jnt.getMatrix(worldSpace=True), worldSpace=True)

    def switch_to_ik(self):
        """
        Snap the IK chain to the FK chain and switch mode to IK.
        """
        self.snap_ik_to_fk()
        attr_state = libAttr.get_settable_attr(self.attState)
        if attr_state:
            attr_state.set(self.STATE_IK)

    def switch_to_fk(self):
        """
        Snap the FK chain to the IK chain and switch mode to FK.
        """
        self.snap_fk_to_ik()
        attr_state = libAttr.get_settable_attr(self.attState)
        if attr_state:
            attr_state.set(self.STATE_FK)

    def iter_ctrls(self):
        for ctrl in super(Limb, self).iter_ctrls():
            yield ctrl
        if self.sysIK:
            for ctrl in self.sysIK.iter_ctrls():
                yield ctrl
        if self.sysFK:
            for ctrl in self.sysFK.iter_ctrls():
                yield ctrl
        yield self.ctrl_attrs
        yield self.ctrl_elbow

    @ui_expose()
    def assign_twist_weights(self):
        for module in self.sys_twist:
            if module.__class__.__name__ == self._CLASS_SYS_TWIST.__name__:
                module.assign_twist_weights()

    @ui_expose()
    def unassign_twist_weights(self):
        for module in self.sys_twist:
            if module.__class__.__name__ == self._CLASS_SYS_TWIST.__name__:
                module.unassign_twist_weights()


def register_plugin():
    """
    Register the plugin. This function is expected by plugin_manager.

    :return: The plugin to register
    :rtype: omtk.core.modules.Module
    """
    return Limb
