from omtk.core.macro import BaseMacro


class CalibrateSelectedModulesMacro(BaseMacro):
    def run(self):
        from omtk import api
        api.calibrate_selected()


def register_plugin():
    return CalibrateSelectedModulesMacro
