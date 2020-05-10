import pymel.core as pymel

from omtk.core.compounds import create_compound

from .model_avar_base import AvarInflBaseModel


class AvarLinearModel(AvarInflBaseModel):
    """
    A deformation point on the face that move accordingly to nurbsSurface.
    """

    SHOW_IN_UI = False

    _ATTR_NAME_MULT_LR = "multiplierLr"
    _ATTR_NAME_MULT_UD = "multiplierUd"
    _ATTR_NAME_MULT_FB = "multiplierFb"

    def _build(self, avar, bind_tm):
        """
        :param avar: Avar that provide our input values
        :type avar: omtk.modules.rigFaceAvar.AbstractAvar
        :return: A matrix attribute that give us our influence final world pos
        :rtype: pymel.Attribute
        """
        compound = create_compound(
            "omtk.AvarInflLinear",
            namespace=self.get_nomenclature().resolve(),
            inputs={
                "innAvarFb": avar.attr_fb,
                "innAvarLr": avar.attr_lr,
                "innAvarPt": avar.attr_pt,
                "innAvarRl": avar.attr_rl,
                "innAvarSx": avar.attr_sx,
                "innAvarSy": avar.attr_sy,
                "innAvarSz": avar.attr_sz,
                "innAvarUd": avar.attr_ud,
                "innAvarYw": avar.attr_yw,
                "multLr": self.multiplier_lr,
                "multFb": self.multiplier_fb,
                "multUd": self.multiplier_ud,
                "innOffset": bind_tm,
            },
        )

        return pymel.Attribute("%s.outputMatrix" % compound.output)
