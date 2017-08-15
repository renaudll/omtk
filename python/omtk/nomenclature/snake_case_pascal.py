from .snake_case import NomenclatureSnakeCase


class NomenclatureSnakePascalCase(NomenclatureSnakeCase):
    """
    Nomenclature that use the Pascal_Snake_Case syntax.
    ex: ['head_ctrl'] -> Head_Ctrl
    """

    @classmethod
    def join(cls, tokens):
        return cls.separator.join(
            token.title() for token in tokens
        )


def register_plugin():
    return NomenclatureSnakePascalCase
