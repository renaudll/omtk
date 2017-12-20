from omtk import api
from omtk.core.macro import BaseMacro


class BuildSelectedModulesMacro(BaseMacro):
    def run(self):
        api.build_selected()


def register_plugin():
    return BuildSelectedModulesMacro
