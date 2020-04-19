from omtk.core import api
from omtk.core.macros import BaseMacro


class CalibrateSelectedModulesMacro(BaseMacro):
    def run(self):
        api.calibrate_selected()


def register_plugin():
    return CalibrateSelectedModulesMacro
