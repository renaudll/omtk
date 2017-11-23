from omtk import api
from omtk.core.classMacro import BaseMacro


class CalibrateSelectedModulesMacro(BaseMacro):
    def run(self):
        api.calibrate_selected()


def register_plugin():
    return CalibrateSelectedModulesMacro
