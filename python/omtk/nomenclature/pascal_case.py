import re
from omtk.core.nomenclature import Nomenclature


class NomenclaturePascalCase(Nomenclature):
    """
    Example Nomenclature definition that use PascalCase as separator.
    """

    @classmethod
    def split(cls, val):
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', val)
        # todo: validate each tokens first letter?
        return [m.group(0).lower() for m in matches]

    @classmethod
    def join(cls, tokens):
        result = ''
        for token in tokens:
            result += token.title()
        return result


def register_plugin():
    return NomenclaturePascalCase
