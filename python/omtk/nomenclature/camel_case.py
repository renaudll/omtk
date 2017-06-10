from .pascal_case import NomenclaturePascalCase


class NomenclatureCamelCase(NomenclaturePascalCase):
    """
    Example Nomenclature definition that use camelCase as separator.
    ex: ['head_ctrl'] -> HeadCtrl
    """

    @classmethod
    def join(cls, tokens):
        result = ''
        i = iter(tokens)
        try:
            result += next(i).lower()
        except StopIteration:
            pass
        for token in i:
            result += token[0].upper() + token[1].lower()
        return result


def register_plugin():
    return NomenclatureCamelCase
