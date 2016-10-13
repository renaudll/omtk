import pymel.core as pymel

from omtk.libs import libRigging
from omtk.libs import libPython
from omtk.libs import libAttr
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

    def validate(self):
        """
        If we are using the preDeform flag, we will need to validate that we can find the Jaw influence!
        """
        super(FaceLips, self).validate()

        if not self.preDeform:
            if self.rig.get_jaw_jnt(strict=False) is None:
                raise Exception("Can't resolve jaw. Please create a Jaw module.")

    def get_avars_corners(self):
        # todo: move upper?
        fnFilter = lambda avar: 'corner' in avar.name.lower()
        result = filter(fnFilter, self.avars)

        if self.avar_l:
            result.append(self.avar_l)
        if self.avar_r:
            result.append(self.avar_r)

        return result

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

    def _build_avar_macro_horizontal(self, avar_parent, avar_middle, avar_children, cls_ctrl, connect_ud=False, connect_lr=True, connect_fb=False):
        self._build_avar_macro(cls_ctrl, avar_parent)

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

    def _build_avar_macro_l(self):
        # Create left avar if necessary
        ref = self.get_jnt_l_mid()
        if self.CREATE_MACRO_AVAR_HORIZONTAL and ref:
            if not self.avar_l:
                self.avar_l = self.create_avar_macro_left(self._CLS_CTRL_LFT, ref)
            self._build_avar_macro_horizontal(self.avar_l, self.get_avar_mid(), self.get_avars_l(), self._CLS_CTRL_LFT, connect_lr=True, connect_ud=False, connect_fb=False)

            # Connect the corner other avars
            avar_l_corner = self.get_avar_l_corner()
            if avar_l_corner:
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_l.attr_ud, avar_l_corner.attr_ud)
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_l.attr_fb, avar_l_corner.attr_fb)

    def _build_avar_macro_r(self):# Create right avar if necessary
        ref = self.get_jnt_r_mid()
        if self.CREATE_MACRO_AVAR_HORIZONTAL and ref:
            # Create l ctrl
            if not self.avar_r:
                self.avar_r = self.create_avar_macro_right(self._CLS_CTRL_RGT, ref)
            self._build_avar_macro_horizontal(self.avar_r, self.get_avar_mid(), self.get_avars_r(), self._CLS_CTRL_RGT, connect_lr=True, connect_ud=False, connect_fb=False)

            avar_r_corner = self.get_avar_r_corner()
            if avar_r_corner:
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_r.attr_ud, avar_r_corner.attr_ud)
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_r.attr_fb, avar_r_corner.attr_fb)

    @libPython.memoized
    def _get_mouth_width(self):
        min_x = max_x = 0
        for avar in self.get_avars_corners():
            x = avar._grp_offset.tx.get()
            min_x = min(min_x, x)
            max_x = max(max_x, x)
        return max_x - min_x

    def _create_extractor(self, avar, default_ratio, target_head, target_jaw):
        """
        Create an attribute on the avar grp_rig to contain the ratio.
        Note that this ratio is preserved when un-building/building.
        """
        attr_ratio = libAttr.addAttr(avar.grp_rig, longName='influenceJaw')
        attr_ratio.showInChannelBox(True)
        attr_ratio.set(default_ratio)  # TODO: Define the ratio
        attr_ratio_inv = libRigging.create_utility_node('plusMinusAverage', operation=2, input1D=[1.0, attr_ratio]).output1D

        nomenclature_rig = avar.get_nomenclature_rig()
        grp_parent = avar._grp_parent
        grp_parent_pos = grp_parent.getTranslation(space='world')  # grp_offset is always in world coordinates

        grp_ref_name = nomenclature_rig.resolve('jawRef' + avar.name)
        grp_ref = pymel.createNode('transform', name=grp_ref_name)
        grp_ref.t.set(grp_parent_pos)
        grp_ref.setParent(avar.grp_rig)

        # Create constraints
        constraint_pr = pymel.parentConstraint(target_head, target_jaw, grp_ref, maintainOffset=True)
        constraint_s = pymel.scaleConstraint(target_head, target_jaw, grp_ref)
        weight_pr_head, weight_pr_jaw = constraint_pr.getWeightAliasList()
        weight_s_head, weight_s_jaw = constraint_s.getWeightAliasList()
        pymel.connectAttr(attr_ratio, weight_pr_jaw)
        pymel.connectAttr(attr_ratio, weight_s_jaw)
        pymel.connectAttr(attr_ratio_inv, weight_pr_head)
        pymel.connectAttr(attr_ratio_inv, weight_s_head)

        # Extract deformation delta
        attr_delta_tm = libRigging.create_utility_node('multMatrix', matrixIn=[
            grp_ref.worldMatrix,
            grp_parent.worldInverseMatrix
        ]).matrixSum

        util_delta_decompose = libRigging.create_utility_node('decomposeMatrix', inputMatrix=attr_delta_tm)

        # Connect to the stack
        # Note that we want the
        stack = avar._stack
        layer_jaw_r = stack.prepend_layer(name='jawRotate')
        layer_jaw_t = stack.prepend_layer(name='jawTranslate')

        pymel.connectAttr(util_delta_decompose.outputTranslate, layer_jaw_t.t)
        pymel.connectAttr(util_delta_decompose.outputRotate, layer_jaw_r.r)

    def build(self, **kwargs):
        super(FaceLips, self).build(**kwargs)

        if not self.preDeform:
            # Resolve the head influence
            jnt_head = self.parent
            if not jnt_head:
                self.error("Failed parenting avars, no head influence found!")
                return

            jnt_jaw = self.rig.get_jaw_jnt()
            if not jnt_jaw:
                self.error("Failed parenting avars, no jaw influence found!")
                return

            nomenclature_rig = self.get_nomenclature_rig()

            # Note #2: A common target for the head
            target_head_name = nomenclature_rig.resolve('targetHead')
            target_head = pymel.createNode('transform', name=target_head_name)
            target_head.setTranslation(jnt_head.getTranslation(space='world'))
            target_head.setParent(self.grp_rig)
            pymel.parentConstraint(jnt_head, target_head, maintainOffset=True)
            pymel.scaleConstraint(jnt_head, target_head, maintainOffset=True)

            # Note #3: A common target for the jaw
            target_jaw_name = nomenclature_rig.resolve('targetJaw')
            target_jaw = pymel.createNode('transform', name=target_jaw_name)
            target_jaw.setTranslation(jnt_jaw.getTranslation(space='world'))
            target_jaw.setParent(self.grp_rig)
            pymel.parentConstraint(jnt_jaw, target_jaw, maintainOffset=True)
            pymel.scaleConstraint(jnt_jaw, target_jaw, maintainOffset=True)

            # For each avars, create an extractor node and extract the delta from the bind pose.
            # We'll then feed this into the stack layers.
            mouth_width = self._get_mouth_width()
            for avar in self.get_avars_corners():
                self._create_extractor(avar, 0.5, target_head, target_jaw)

            for avar in self.get_avars_upp():
                avar_pos_x = avar._grp_offset.tx.get()
                ratio = abs(avar_pos_x / mouth_width)
                ratio = max(min(ratio, 1.0), 0.0)  # keep ratio in range
                ratio = 1.0 - libRigging.interp_football(ratio)  # apply football shape
                self._create_extractor(avar, ratio, target_head, target_jaw)

            for avar in self.get_avars_low():
                avar_pos_x = avar._grp_offset.tx.get()
                ratio = abs(avar_pos_x / mouth_width)
                ratio = max(min(ratio, 1.0), 0.0)  # keep ratio in range
                ratio = libRigging.interp_football(ratio)  # apply football shape
                self._create_extractor(avar, ratio, target_head, target_jaw)
