import pymel.core as pymel
import functools
from omtk.libs import libAttr
from omtk.libs import libRigging
from omtk.libs import libCtrlShapes
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps

class CtrlLipsUpp(rigFaceAvarGrps.CtrlFaceUpp):
    pass

class CtrlLipsLow(rigFaceAvarGrps.CtrlFaceLow):
    pass

class FaceLips(rigFaceAvarGrps.AvarGrpAreaOnSurface):
    """
    Lips have the same behavior than an AvarGrpUppLow.
    However the lip curl is also connected between the macro avars and the micro avars.

    """
    IS_SIDE_SPECIFIC = False
    SHOW_IN_UI = True
    _CLS_CTRL_UPP = CtrlLipsUpp
    _CLS_CTRL_LOW = CtrlLipsLow

    @property
    def avars_corners(self):
        # TODO: Find a better way
        fnFilter = lambda avar: 'corner' in avar.name.lower()
        return filter(fnFilter, self.avars)

    def get_module_name(self):
        return 'Lip'

    def connect_macro_avar(self, avar_macro, avar_micros):
        for avar_micro in avar_micros:
            libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_ud, avar_micro.attr_ud)
            libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_lr, avar_micro.attr_lr)
            libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_fb, avar_micro.attr_fb)
            libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_pt, avar_micro.attr_pt)

            # Add default FB avars to 'fake' a better lip curl pivot.
            # see: Art of Moving Points page 146
            libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_pt, avar_micro.attr_ud, kv=[0.01, 0.0, -0.01])
            libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_pt, avar_micro.attr_fb, kv=[0.01, 0.0, -0.01])

    def _build_avar_macro_horizontal(self, rig, avar_parent, avar_middle, avar_children, cls_ctrl, connect_ud=False, connect_lr=True, connect_fb=False):
        self.build_abstract_avar(rig, cls_ctrl, avar_parent)

        pos_s = avar_middle.jnt.getTranslation(space='world')
        pos_e = avar_parent.jnt.getTranslation(space='world')

        for avar_child in avar_children:
            # We don't want to connect the middle Avar.
            if avar_child == avar_middle:
                continue

            pos = avar_child.jnt.getTranslation(space='world')

            # Compute the ratio between the middle and the corner.
            # ex: In the lips, we want the lips to stretch when the corner are taken appart.
            ratio = (pos.x - pos_s.x) / (pos_e.x - pos_s.x)
            ratio = max(0, ratio)
            ratio = min(ratio, 1)

            if connect_ud:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_ud, avar_child.attr_ud)
            if connect_lr:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_lr, avar_child.attr_lr,  kv=(-ratio,0.0,ratio))
            if connect_fb:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_fb, avar_child.attr_fb)

    def _build_avar_macro_l(self, rig):
        # Create left avar if necessary
        ref = self.jnt_l_mid
        if self.CREATE_MACRO_AVAR_HORIZONTAL and ref:
            if not self.avar_l:
                self.avar_l = self.create_avar_macro_left(rig, self._CLS_CTRL_LFT, ref)
            self._build_avar_macro_horizontal(rig, self.avar_l, self.get_avar_mid(), self.get_avars_l(), self._CLS_CTRL_LFT, connect_lr=True, connect_ud=False, connect_fb=False)

            # Connect the corner other avars
            avar_l_corner = self.get_avar_l_corner()
            if avar_l_corner:
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_l.attr_ud, avar_l_corner.attr_ud)
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_l.attr_fb, avar_l_corner.attr_fb)

    def _build_avar_macro_r(self, rig):# Create right avar if necessary
        ref = self.jnt_r_mid
        if self.CREATE_MACRO_AVAR_HORIZONTAL and ref:
            # Create l ctrl
            if not self.avar_r:
                self.avar_r = self.create_avar_macro_right(rig, self._CLS_CTRL_RGT, ref)
            self._build_avar_macro_horizontal(rig, self.avar_r, self.get_avar_mid(), self.get_avars_r(), self._CLS_CTRL_RGT, connect_lr=True, connect_ud=False, connect_fb=False)

            avar_r_corner = self.get_avar_r_corner()
            if avar_r_corner:
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_r.attr_ud, avar_r_corner.attr_ud)
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_r.attr_fb, avar_r_corner.attr_fb)

    def _parent_avars(self, rig, parent):
        super(FaceLips, self)._parent_avars(rig, parent)

        # If we are using the lips in the main deformer, we'll do shenanigans with the jaw.
        if not self.preDeform:
            # Resolve the head influence
            jnt_head = self.parent
            #jnt_head = rig.get_head_jnt()

            jnt_jaw = rig.get_jaw_jnt()

            # Hack: To prevent ANY flipping, we'll create an aligned target for the head and the jaw.
            # TODO: Find a cleaner way!
            nomenclature_rig = self.get_nomenclature_rig(rig)

            target_head_name = nomenclature_rig.resolve('targetHead')
            target_head = pymel.createNode('transform', name=target_head_name)
            target_head.setParent(self.grp_rig)
            pymel.parentConstraint(jnt_head, target_head, maintainOffset=True)
            pymel.scaleConstraint(jnt_head, target_head, maintainOffset=True)

            target_jaw_name = nomenclature_rig.resolve('targetJaw')
            target_jaw = pymel.createNode('transform', name=target_jaw_name)
            target_jaw.setParent(self.grp_rig)
            pymel.parentConstraint(jnt_jaw, target_jaw, maintainOffset=True)
            pymel.scaleConstraint(jnt_jaw, target_jaw, maintainOffset=True)


            #
            # Create jaw constraints
            #

            for avar in self.get_avars_upp():
                pymel.parentConstraint(target_head, avar._stack._layers[0], maintainOffset=True)

            for avar in self.get_avars_low():
                pymel.parentConstraint(target_jaw, avar._stack._layers[0], maintainOffset=True)

            # Note that since we are using two targets, we need to ensure the parent also follow
            # the face to prevent any accidental flipping.
            # todo: use a layer AFTER the offset node instead of before...
            for avar in self.avars_corners:
                offset_layer = avar._stack.get_stack_start()
                offset_flip_layer = avar._stack.preprend_layer(name='OffsetNotFlip')

                pymel.parentConstraint(jnt_head, offset_flip_layer, maintainOffset=True)
                pymel.parentConstraint(target_head, target_jaw, offset_layer, maintainOffset=True)

