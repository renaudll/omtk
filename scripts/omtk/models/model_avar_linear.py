import pymel.core as pymel

from omtk.core.compounds import create_compound

from .model_avar_base import AvarInflBaseModel


class AvarLinearModel(AvarInflBaseModel):
    """
    A deformation point on the face that move accordingly to nurbsSurface.
    """

    def _build(self, avar):
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
                "avar": pymel.PyNode(self.compound.input).avar,
                "multLr": self.multiplier_lr,
                "multFb": self.multiplier_fb,
                "multUd": self.multiplier_ud,
            },
        )

        return pymel.Attribute("%s.outputMatrix" % compound.output)
