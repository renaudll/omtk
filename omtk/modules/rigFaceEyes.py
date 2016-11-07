import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule import Module
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps
from omtk.libs import libRigging

class CtrlEyes(BaseCtrl):
    def __createNode__(self, width=1.0, height=1.0, normal=(0,0,1), *args, **kwargs):
        p1 = [0, height, 0]
        p2 = [width*0.5, height*0.95, 0]
        p3 = [width, 0, 0]
        p4 = [width*0.5, -height*0.95, 0]
        p5 = [0, -height, 0]
        p6 = [-width*0.5, -height*0.95, 0]
        p7 = [-width, 0, 0]
        p8 = [-width*0.5, height*0.95, 0]

        node = pymel.curve(d=2, p=[p1, p2, p3, p4, p5, p6, p7, p8, p1] )
        return node

class CtrlEye(BaseCtrl):
    def __createNode__(self, normal=(0,0,1), *args, **kwargs):
        return super(CtrlEye, self).__createNode__(normal=normal, *args, **kwargs)

class BaseAvarCtrlModel(Module):
    _CLS_CTRL = BaseCtrl
    def __init__(self, *args, **kwargs):
        super(BaseAvarCtrlModel, self).__init__(*args, **kwargs)
        self.ctrl = None

    def get_default_tm_ctrl(self):
        if self.jnt:
            return self.jnt.getMatrix(worldSpace=True)
        raise Exception("Cannot resolve ctrl transformation matrix!")

    # todo: implement correct build method that also create the ctrl.
    def build(self, avar, ctrl_tm=None, ctrl_size=None, **kwargs):
        super(BaseAvarCtrlModel, self).build(**kwargs)

        # Resolve ctrl matrix
        if ctrl_tm is None:
            ctrl_tm = self.get_default_tm_ctrl()

        # Create ctrl
        nomenclature_anm = self.get_nomenclature_anm()
        ctrl_name = nomenclature_anm.resolve()
        self.ctrl = self.init_ctrl(self._CLS_CTRL, self.ctrl)
        self.ctrl.build(name=ctrl_name, size=ctrl_size)
        if ctrl_tm:
            self.ctrl.setMatrix(ctrl_tm)

        self.ctrl.setParent(self.grp_anm)

    def connect(self, avar, ud=True, fb=True, lr=True, yw=True, pt=True, rl=True, sx=True, sy=True, sz=True):
        raise NotImplementedError

class ModelLookAt(BaseAvarCtrlModel):
    """
    This controller avars from an object aimConstrained to a ctrl.
    """
    _CLS_CTRL = BaseCtrl

    def __init__(self, *args, **kwargs):
        super(ModelLookAt, self).__init__(*args, **kwargs)

        self._attr_out_lr = None
        self._attr_out_ud = None
        self._attr_out_fb = None
        self._attr_out_yw = None
        self._attr_out_pt = None
        self._attr_out_rl = None

    def get_default_tm_ctrl(self):
        """
        Find the chin location. This is the preffered location for the jaw doritos.
        """
        jnt_pos = self.jnt.getTranslation(space='world')
        head_length = self.rig.get_head_length()
        if not head_length:
            pymel.warning("Can't resolve head length! The eyes ctrl location might be erroned.")
        offset_z = head_length * 2 if head_length else 0
        return pymel.datatypes.Matrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            jnt_pos.x,
            jnt_pos.y,
            jnt_pos.z + offset_z
        )

    def build(self, avar, ref=None, ref_tm=None,  ctrl_tm=None, ctrl_size=None, **kwargs):
        super(ModelLookAt, self).build(avar, ctrl_tm=ctrl_tm, ctrl_size=ctrl_size, **kwargs)

        nomenclature_rig = self.get_nomenclature_rig()

        # Build an aim node in-place for performance
        # This separated node allow the joints to be driven by the avars.
        aim_grp_name = nomenclature_rig.resolve('lookgrp')
        aim_grp = pymel.createNode('transform', name=aim_grp_name)
        aim_grp.setParent(self.grp_rig)

        aim_node_name = nomenclature_rig.resolve('looknode')
        aim_node = pymel.createNode('transform', name=aim_node_name)
        aim_node.setParent(aim_grp)

        aim_target_name = nomenclature_rig.resolve('target')
        aim_target = pymel.createNode('transform', name=aim_target_name)
        aim_target.setParent(aim_grp)
        self.target = aim_target  # todo: remove?
        pymel.pointConstraint(self.ctrl, aim_target, maintainOffset=False)

        # Build an upnode for the eyes.
        # I'm not a fan of upnodes but in this case it's better to guessing the joint orient.
        aim_upnode_name = nomenclature_rig.resolve('upnode')

        aim_upnode = pymel.createNode('transform', name=aim_upnode_name)
        #
        aim_upnode.setParent(self.grp_rig)
        pymel.parentConstraint(aim_grp, aim_upnode, maintainOffset=True)

        pymel.aimConstraint(aim_target, aim_node,
                            maintainOffset=False,
                            aimVector=(0.0, 0.0, 1.0),
                            upVector=(0.0, 1.0, 0.0),
                            worldUpObject=aim_upnode,
                            worldUpType='object'
                            )

        # Position objects
        aim_grp.setTranslation(self.jnt.getTranslation(space='world'))
        # aim_grp.setParent(self._grp_offset)  # todo: add begin , end property
        # aim_grp.t.set(0, 0, 0)
        # aim_grp.r.set(0, 0, 0)
        jnt_tm = self.jnt.getMatrix(worldSpace=True)
        jnt_pos = jnt_tm.translate
        aim_upnode_pos = pymel.datatypes.Point(0, 1, 0) + jnt_pos
        aim_upnode.setTranslation(aim_upnode_pos, space='world')
        aim_target_pos = pymel.datatypes.Point(0, 0, 1) + jnt_pos
        aim_target.setTranslation(aim_target_pos, space='world')

        # pymel.parentConstraint(aim_node, stack, maintainOffset=True)

        # Convert the rotation to avars to additional values can be added.
        util_decomposeMatrix = libRigging.create_utility_node('decomposeMatrix', inputMatrix=aim_node.matrix)

        self._attr_out_lr = util_decomposeMatrix.outputTranslateX
        self._attr_out_ud = util_decomposeMatrix.outputTranslateY
        self._attr_out_fb = util_decomposeMatrix.outputTranslateZ
        self._attr_out_yw = util_decomposeMatrix.outputRotateY
        self._attr_out_pt = util_decomposeMatrix.outputRotateX
        self._attr_out_rl = util_decomposeMatrix.outputRotateZ

    def connect(self, avar, ud=True, fb=True, lr=True, yw=True, pt=True, rl=True, sx=True, sy=True, sz=True):
        libRigging.connectAttr_withBlendWeighted(self._attr_out_lr, avar.attr_lr)
        libRigging.connectAttr_withBlendWeighted(self._attr_out_ud, avar.attr_ud)
        libRigging.connectAttr_withBlendWeighted(self._attr_out_fb, avar.attr_fb)
        libRigging.connectAttr_withBlendWeighted(self._attr_out_yw, avar.attr_yw)
        libRigging.connectAttr_withBlendWeighted(self._attr_out_pt, avar.attr_pt)
        libRigging.connectAttr_withBlendWeighted(self._attr_out_rl, avar.attr_rl)

class FaceEyes(rigFaceAvarGrps.AvarGrp):
    """
    Look-at setup with avars support.
    """
    IS_SIDE_SPECIFIC = False
    SHOW_IN_UI = True
    _CLS_MODEL_CTRL_MICRO = ModelLookAt
    _CLS_CTRL_MICRO = CtrlEye

    def __init__(self, *args, **kwargs):
        """
        Pre-declare here all the used members.
        """
        super(FaceEyes, self).__init__(*args, **kwargs)
        self.ctrl_all = None

    def handle_surface(self):
        pass  # todo: better class schema!

    def get_module_name(self):
        return 'Eyes'

    def build(self, *args, **kwargs):
        if self.parent is None:
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
            pos = avar.ctrl.getTranslation(space='world')
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
        if not isinstance(self.ctrl_all, CtrlEyes):
            self.ctrl_all = CtrlEyes()
        ctrl_all_name = nomenclature_anm.resolve()
        self.ctrl_all.build(width=width, height=height)
        self.ctrl_all.setTranslation(ctrl_pos_average)
        self.ctrl_all.create_spaceswitch(self, self.parent, add_default=True, default_name='Head', add_world=True)
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
