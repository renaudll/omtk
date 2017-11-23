from omtk import api
from omtk.core.macro import BaseMacro


class UnbuildSelectedModulesMacro(BaseMacro):
    def run(self):
        api.unbuild_selected()


def register_plugin():
    return UnbuildSelectedModulesMacro
