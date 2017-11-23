from omtk.core import rig
from omtk.nomenclature.snake_case import NomenclatureSnakeCase


class RigStandard(rig.Rig):
    """
    Default OMTK rig.
    """

    def _get_nomenclature_cls(self):
        return NomenclatureSnakeCase


def register_plugin():
    return RigStandard
