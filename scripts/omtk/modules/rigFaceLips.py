import pymel.core as pymel
import functools
from omtk.libs import libAttr
from omtk.libs import libRigging
from omtk.libs import libCtrlShapes
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps

class FaceLips(rigFaceAvarGrps.AvarGrpAreaOnSurface):
    """
    Lips have the same behavior than an AvarGrpUppLow.
    However the lip curl is also connected between the macro avars and the micro avars.

    """
    IS_SIDE_SPECIFIC = False
    SHOW_IN_UI = True

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

    def build(self, rig, **kwargs):
        """
        The Lips rig have additional controllers to open all the upper or lower lips together.
        """
        # Normally the lips are in preDeform.
        # If it is not the case, we'll handle constraining ourself with the head and jaw.
        super(FaceLips, self).build(rig, parent=False, **kwargs)

        # If we are using the lips in the main deformer, we'll do shenanigans with the jaw.
        if not self.preDeform:
            jnt_head = rig.get_head_jnt()
            jnt_jaw = rig.get_jaw_jnt()

            # Hack: To prevent ANY flipping, we'll create an aligned target for the head and the jaw.
            # TODO: Find a cleaner way!
            nomenclature_rig = self.get_nomenclature_rig(rig)

            target_head_name = nomenclature_rig.resolve('targetHead')
            target_head = pymel.createNode('transform', name=target_head_name)
            target_head.setParent(self.grp_rig)
            pymel.parentConstraint(jnt_head, target_head, maintainOffset=True)

            target_jaw_name = nomenclature_rig.resolve('targetJaw')
            target_jaw = pymel.createNode('transform', name=target_jaw_name)
            target_jaw.setParent(self.grp_rig)
            pymel.parentConstraint(jnt_jaw, target_jaw, maintainOffset=True)

            #
            # Create jaw constraints
            #

            for avar in self.avars_upp:
                pymel.parentConstraint(jnt_head, avar._stack._layers[0], maintainOffset=True)

            for avar in self.avars_low:
                pymel.parentConstraint(jnt_jaw, avar._stack._layers[0], maintainOffset=True)

            # Note that since we are using two targets, we need to ensure the parent also follow
            # the face to prevent any accidental flipping.
            for avar in self.avars_corners:
                offset_layer = avar._stack.get_stack_start()
                offset_flip_layer = avar._stack.preprend_layer(name='OffsetNotFlip')

                pymel.parentConstraint(jnt_head, offset_flip_layer, maintainOffset=True)
                pymel.parentConstraint(target_head, target_jaw, offset_layer, maintainOffset=True)
