from omtk.core.macro import BaseMacro


class UnbuildSelectedModulesMacro(BaseMacro):
    def run(self):
        from omtk import api
        api.unbuild_selected()


def register_plugin():
    return UnbuildSelectedModulesMacro
