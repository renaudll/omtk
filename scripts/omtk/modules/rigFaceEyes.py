"""
Logic for the "FaceEyes" module
"""
import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core import classCtrlModel
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps
from omtk.models.model_avar_linear import AvarLinearModel
from omtk.libs import libRigging


class CtrlEyes(BaseCtrl):
    def create_ctrl(self, width=1.0, height=1.0, normal=(0, 0, 1), *args, **kwargs):
        return pymel.curve(
            d=2,
            p=[
                [0, height, 0],
                [width * 0.5, height * 0.95, 0],
                [width, 0, 0],
                [width * 0.5, -height * 0.95, 0],
                [0, -height, 0],
                [-width * 0.5, -height * 0.95, 0],
                [-width, 0, 0],
                [-width * 0.5, height * 0.95, 0],
                [0, height, 0],
            ],
        )


class CtrlEye(BaseCtrl):
    def create_ctrl(self, normal=(0, 0, 1), *args, **kwargs):
        return super(CtrlEye, self).create_ctrl(normal=normal, *args, **kwargs)


#
# class ModelLookAt(classCtrlModel.BaseCtrlModel):
#     """
#     This controller avars from an object aimConstrained to a ctrl.
#     """
#
#     def connect(
#         self,
#         avar,
#         ud=True,
#         fb=True,
#         lr=True,
#         yw=True,
#         pt=True,
#         rl=True,
#         sx=True,
#         sy=True,
#         sz=True,
#     ):
#         libRigging.connectAttr_withBlendWeighted(self._attr_out_lr, avar.attr_lr)
#         libRigging.connectAttr_withBlendWeighted(self._attr_out_ud, avar.attr_ud)
#         libRigging.connectAttr_withBlendWeighted(self._attr_out_fb, avar.attr_fb)
#         libRigging.connectAttr_withBlendWeighted(self._attr_out_yw, avar.attr_yw)
#         libRigging.connectAttr_withBlendWeighted(self._attr_out_pt, avar.attr_pt)
#         libRigging.connectAttr_withBlendWeighted(self._attr_out_rl, avar.attr_rl)


class AvarEye(rigFaceAvar.Avar):
    CLS_CTRL = CtrlEye
    CLS_MODEL_CTRL = None
    CLS_MODEL_INFL = AvarLinearModel

    def _get_ctrl_tm(self):
        jnt_pos = self.jnt.getTranslation(space="world")
        head_jnt = self.get_head_jnt()
        head_length = self.rig.get_head_length(head_jnt)
        if not head_length:
            pymel.warning(
                "Can't resolve head length! The eyes ctrl location might be erroned."
            )
        offset_z = head_length * 2 if head_length else 0
        return pymel.datatypes.Matrix(
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [jnt_pos.x, jnt_pos.y, jnt_pos.z + offset_z, 1],
        )

    def build(self, ref=None, ref_tm=None, ctrl_tm=None, ctrl_size=1.0, **kwargs):
        super(AvarEye, self).build(ctrl_tm=ctrl_tm, ctrl_size=ctrl_size, **kwargs)

        # Resolve ctrl matrix
        ctrl_tm = ctrl_tm or self._get_ctrl_tm()
        if ctrl_tm:
            self.ctrl.setMatrix(ctrl_tm)

        naming = self.get_nomenclature_rig()

        # Build an aim node in-place for performance
        # This separated node allow the joints to be driven by the avars.
        aim_grp_name = naming.resolve("lookgrp")
        aim_grp = pymel.createNode("transform", name=aim_grp_name)
        aim_grp.setParent(self.grp_rig)

        aim_node_name = naming.resolve("looknode")
        aim_node = pymel.createNode("transform", name=aim_node_name)
        aim_node.setParent(aim_grp)

        aim_grp.setTranslation(self.jnt.getTranslation(space="world"))
        if self.parent_jnt:
            pymel.parentConstraint(self.parent_jnt, aim_grp, maintainOffset=True)

        aim_target_name = naming.resolve("target")
        aim_target = pymel.createNode("transform", name=aim_target_name)
        aim_target.setParent(aim_grp)
        self.target = aim_target  # todo: remove?
        pymel.pointConstraint(self.ctrl, aim_target, maintainOffset=False)

        # Build an upnode for the eyes.
        # Not a fan of upnodes but in this case it's better than guessing joint orient.
        aim_upnode_name = naming.resolve("upnode")

        aim_upnode = pymel.createNode("transform", name=aim_upnode_name)

        aim_upnode.setParent(self.grp_rig)
        pymel.parentConstraint(aim_grp, aim_upnode, maintainOffset=True)

        pymel.aimConstraint(
            aim_target,
            aim_node,
            maintainOffset=True,
            aimVector=(0.0, 0.0, 1.0),
            upVector=(0.0, 1.0, 0.0),
            worldUpObject=aim_upnode,
            worldUpType="object",
        )

        # Position objects
        aim_grp.setTranslation(self.jnt.getTranslation(space="world"))
        jnt_tm = self.jnt.getMatrix(worldSpace=True)
        jnt_pos = jnt_tm.translate
        aim_upnode_pos = pymel.datatypes.Point(0, 1, 0) + jnt_pos
        aim_upnode.setTranslation(aim_upnode_pos, space="world")
        aim_target_pos = pymel.datatypes.Point(0, 0, 1) + jnt_pos
        aim_target.setTranslation(aim_target_pos, space="world")

        # Convert the rotation to avars to additional values can be added.
        util = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=aim_node.matrix
        )
        self._attr_out_lr = util.outputTranslateX
        self._attr_out_ud = util.outputTranslateY
        self._attr_out_fb = util.outputTranslateZ
        self._attr_out_yw = util.outputRotateY
        self._attr_out_pt = util.outputRotateX
        self._attr_out_rl = util.outputRotateZ


class FaceEyes(rigFaceAvarGrps.AvarGrp):
    """
    Look-at setup with avars support.
    """

    CLS_AVAR_MICRO = AvarEye
    IS_SIDE_SPECIFIC = False
    CREATE_MACRO_AVAR_ALL = False
    CREATE_MACRO_AVAR_HORIZONTAL = False
    CREATE_MACRO_AVAR_VERTICAL = False

    def __init__(self, *args, **kwargs):
        """
        Pre-declare here all the used members.
        """
        super(FaceEyes, self).__init__(*args, **kwargs)
        self.ctrl_all = None

    def handle_surface(self):
        pass  # todo: better class schema!

    def get_default_name(self):
        return "Eyes"

    def get_parent_obj(self, **kwargs):
        result = self.get_head_jnt(strict=False)
        return result or super(FaceEyes, self).get_parent_obj(**kwargs)

    def build(self, *args, **kwargs):
        if self.parent_jnt is None:
            raise Exception("Can't build FaceEyes, no parent found!")

        super(FaceEyes, self).build(parent=True, *args, **kwargs)

        nomenclature_anm = self.get_nomenclature_anm()

        # Resolve average position of each ctrls.
        # This is used as the position of the main ctrl.
        ctrl_default_size = 1  # TODO: Compute automatically
        ctrl_pos_average = pymel.datatypes.Vector()
        ctrl_positions = []
        x_min = None
        x_max = None
        y_min = None
        y_max = None
        for avar in self.avars:
            pos = avar.ctrl.getTranslation(space="world")
            ctrl_positions.append(pos)
            ctrl_pos_average += pos
            if x_min is None or pos.x < x_min:
                x_min = pos.x
            if x_max is None or pos.x > x_max:
                x_max = pos.x
            if y_min is None or pos.y < y_min:
                y_min = pos.y
            if y_max is None or pos.y > y_max:
                y_max = pos.y
        ctrl_pos_average /= len(self.jnts)
        width = max(ctrl_default_size, abs(x_max - x_min)) + ctrl_default_size
        height = max(ctrl_default_size, abs(y_max - y_min)) + ctrl_default_size

        # Define main ctrl
        self.ctrl_all = CtrlEyes.from_instance(self.ctrl_all)
        ctrl_all_name = nomenclature_anm.resolve()
        self.ctrl_all.build(width=width, height=height)
        self.ctrl_all.setTranslation(ctrl_pos_average)
        jnt_head = self.get_parent_obj()
        self.ctrl_all.create_spaceswitch(
            self,
            jnt_head,
            add_local=True,
            local_label="Head",
            local_target=jnt_head,
            add_world=True,
        )
        self.ctrl_all.rename(ctrl_all_name)
        self.ctrl_all.setParent(self.grp_anm)

        # Make all eyes ctrls follow the main ctrl
        for avar in self.avars:
            avar.ctrl.setParent(self.ctrl_all)

    def unbuild(self):
        """
        If you are using sub-modules, you might want to clean them here.
        :return:
        """
        super(FaceEyes, self).unbuild()

    def iter_ctrls(self):
        for ctrl in super(FaceEyes, self).iter_ctrls():
            yield ctrl
        yield self.ctrl_all

    def calibrate(self):
        """
        It is not possible to calibrate the eyes since they have no avar on surface.
        This will hide the function from the UI.
        """
        pass


def register_plugin():
    return FaceEyes
