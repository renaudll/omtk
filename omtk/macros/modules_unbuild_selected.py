from omtk.core import api
from omtk.core.macros import BaseMacro


class UnbuildSelectedModulesMacro(BaseMacro):
    def run(self):
        api.unbuild_selected()


def register_plugin():
    return UnbuildSelectedModulesMacro
