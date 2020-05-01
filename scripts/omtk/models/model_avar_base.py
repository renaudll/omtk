import functools

import pymel.core as pymel

from omtk.core import classModule
from omtk.libs import libAttr


class AvarInflBaseModel(classModule.Module):
    """
    A deformation point on the face that move accordingly to nurbsSurface.
    """

    SHOW_IN_UI = False

    _ATTR_NAME_MULT_LR = "multiplierLr"
    _ATTR_NAME_MULT_UD = "multiplierUd"
    _ATTR_NAME_MULT_FB = "multiplierFb"

    default_multiplier_lr = 1.0
    default_multiplier_ud = 1.0
    default_multiplier_fb = 1.0

    support_no_inputs = True

    def __init__(self, *args, **kwargs):
        super(AvarInflBaseModel, self).__init__(*args, **kwargs)

        # An AvarModel will receive the avar values
        self._attr_inn_lr = None
        self._attr_inn_ud = None
        self._attr_inn_fb = None
        self._attr_inn_yw = None
        self._attr_inn_pt = None
        self._attr_inn_rl = None
        self._attr_inn_sx = None
        self._attr_inn_sy = None
        self._attr_inn_sz = None

        # The original transform of the influence
        self._attr_inn_offset_tm = None

        # The output transform of the system
        self._attr_out_tm = None

        # Reference to the object containing the bind pose of the avar.
        self._obj_offset = None

        # How much are we moving around the surface for a specific avar.
        self.multiplier_lr = self.default_multiplier_lr
        self.multiplier_ud = self.default_multiplier_ud
        self.multiplier_fb = self.default_multiplier_fb

    def _create_interface(self):
        fn = functools.partial(libAttr.addAttr, self.grp_rig)
        # Create avar inputs
        self._attr_inn_lr = fn("innAvarLr")
        self._attr_inn_ud = fn("innAvarUd")
        self._attr_inn_fb = fn("innAvarFb")
        self._attr_inn_yw = fn("innAvarYw")
        self._attr_inn_pt = fn("innAvarPt")
        self._attr_inn_rl = fn("innAvarRl")
        self._attr_inn_sx = fn("innAvarSx")
        self._attr_inn_sy = fn("innAvarSy")
        self._attr_inn_sz = fn("innAvarSz")

        self.multiplier_lr = fn("innMultiplierLr", defaultValue=self.multiplier_lr)
        self.multiplier_ud = fn("innMultiplierUd", defaultValue=self.multiplier_ud)
        self.multiplier_fb = fn("innMultiplierFb", defaultValue=self.multiplier_fb)

        self._attr_inn_offset_tm = fn("innOffset", dt="matrix")
        self._attr_out_tm = fn("outTm", dataType="matrix")

    def build(self, **kwargs):
        """
        The dag stack is a chain of transform nodes daisy chained together that computer the final transformation of the influence.
        The decision of using transforms instead of multMatrix nodes is for clarity.
        Note also that because of it's parent (the offset node) the stack relative to the influence original translation.
        """
        super(AvarInflBaseModel, self).build(
            create_grp_anm=False, disconnect_inputs=False, **kwargs
        )

        self._create_interface()
        attr_tm = self._build()
        pymel.connectAttr(attr_tm, self._attr_out_tm)

    def unbuild(self):
        # Cleanup old deprecated properties to prevent invalid pynode warning.
        self.grp_offset = None

        # Save the current uv multipliers.
        # It is very rare that the rigger will tweak this advanced setting manually,
        # however for legacy reasons, it might be useful when upgrading an old rig.
        if (
            isinstance(self.multiplier_lr, pymel.Attribute)
            and self.multiplier_lr.exists()
        ):
            self.multiplier_lr = self.multiplier_lr.get()
        if (
            isinstance(self.multiplier_ud, pymel.Attribute)
            and self.multiplier_ud.exists()
        ):
            self.multiplier_ud = self.multiplier_ud.get()
        if (
            isinstance(self.multiplier_fb, pymel.Attribute)
            and self.multiplier_fb.exists()
        ):
            self.multiplier_fb = self.multiplier_fb.get()

        super(AvarInflBaseModel, self).unbuild()

    def _build(self):
        """
        :return: A matrix pymel.Attribute containing the resulting transform. 
        """
        raise NotImplementedError

    def connect_avar(self, avar):
        pymel.connectAttr(avar.attr_lr, self._attr_inn_lr)
        pymel.connectAttr(avar.attr_ud, self._attr_inn_ud)
        pymel.connectAttr(avar.attr_fb, self._attr_inn_fb)
        pymel.connectAttr(avar.attr_yw, self._attr_inn_yw)
        pymel.connectAttr(avar.attr_pt, self._attr_inn_pt)
        pymel.connectAttr(avar.attr_rl, self._attr_inn_rl)
        pymel.connectAttr(avar.attr_sx, self._attr_inn_sx)
        pymel.connectAttr(avar.attr_sy, self._attr_inn_sy)
        pymel.connectAttr(avar.attr_sz, self._attr_inn_sz)
        pymel.connectAttr(avar.grp_offset.matrix, self._attr_inn_offset_tm)
