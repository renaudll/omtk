import re
from omtk.core.classNomenclature import Nomenclature


class NomenclaturePascalCase(Nomenclature):
    """
    Example Nomenclature definition that use PascalCase as separator.
    """

    @classmethod
    def split(cls, val):
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', val)
        # todo: validate each tokens first letter?
        return [m.group(0) for m in matches]

    @classmethod
    def join(cls, tokens):
        result = ''
        for token in tokens:
            result += token[0].upper() + tokens[0:].lower()
        return result


def register_plugin():
    return NomenclaturePascalCase
