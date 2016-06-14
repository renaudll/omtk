import pymel.core as pymel
import functools
from omtk.libs import libAttr
from omtk.libs import libRigging
from omtk.libs import libCtrlShapes
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps

class CtrlLipsUpp(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()


class CtrlLipsLow(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()


class FaceLips(rigFaceAvarGrps.AvarGrpUppLow):
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

            for avar in self.avars_upp:
                pymel.parentConstraint(jnt_head, avar._stack._layers[0], maintainOffset=True)

            for avar in self.avars_low:
                pymel.parentConstraint(jnt_jaw, avar._stack._layers[0], maintainOffset=True)

            for avar in self.avars_corners:
                pymel.parentConstraint(jnt_head, jnt_jaw, avar._stack._layers[0], maintainOffset=True)





