from omtk.core.nomenclature import Nomenclature


class NomenclatureSnakeCase(Nomenclature):
    separator = '_'

    @classmethod
    def split(cls, val):
        return val.split(cls.separator)

    @classmethod
    def join(cls, tokens):
        return cls.separator.join(tokens)


def register_plugin():
    return Nomenclature
