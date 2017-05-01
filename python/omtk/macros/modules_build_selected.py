from omtk.core import api
from omtk.core.macros import BaseMacro


class BuildSelectedModulesMacro(BaseMacro):
    def run(self):
        api.build_selected()


def register_plugin():
    return BuildSelectedModulesMacro
