from omtk.core.macro import BaseMacro


class BuildSelectedModulesMacro(BaseMacro):
    def run(self):
        from omtk import api
        api.build_selected()


def register_plugin():
    return BuildSelectedModulesMacro
