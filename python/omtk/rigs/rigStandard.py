from omtk.core import classRig
from omtk.nomenclature.snake_case import NomenclatureSnakeCase


class RigStandard(classRig.Rig):
    """
    Default OMTK rig.
    """

    def _get_nomenclature_cls(self):
        return NomenclatureSnakeCase


def register_plugin():
    return RigStandard
