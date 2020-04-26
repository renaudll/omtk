from omtk.core.macros import BaseMacro
from omtk.libs import libSkinning


class SkelResetSkinMacro(BaseMacro):
    def run(self):
        libSkinning.reset_selection_skin_cluster()


def register_plugin():
    return SkelResetSkinMacro
