from omtk import api
from omtk.core.macro import BaseMacro


class CalibrateSelectedModulesMacro(BaseMacro):
    def run(self):
        api.calibrate_selected()


def register_plugin():
    return CalibrateSelectedModulesMacro
