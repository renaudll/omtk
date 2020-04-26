"""
Create a locator at the center of the selection.
"""
from omtk.core.macros import BaseMacro
from omtk.libs import libUtils


class CreateLocatorMacro(BaseMacro):
    def run(self):
        libUtils.createLocToCenter()


def register_plugin():
    return CreateLocatorMacro
