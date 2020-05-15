"""
Simple utility to swap the mesh used by an InteractiveCtrl in case the wrong mesh was used.
"""
import pymel.core as pymel

from omtk.libs import libPymel
from omtk.core import api
from omtk.core.macros import BaseMacro
from omtk.modules.face.avar_grp import AvarGrp
from omtk.modules.face.avar import AbstractAvar
from omtk.modules.face.models.avar_to_ctrl.linear import ModelCtrlLinear


class CtrlInteractiveSwapMesh(BaseMacro):
    def _iter_ictrl(self):
        _, modules = api.get_modules_from_selection()
        # Build selected modules
        for module in modules:
            if isinstance(module, AvarGrp):
                for avar in module.iter_avars():
                    if (
                        isinstance(avar, AbstractAvar)
                        and avar.model_ctrl
                        and isinstance(avar.model_ctrl, ModelCtrlLinear)
                    ):
                        yield avar.model_ctrl

    def run(self):
        mesh = next(
            (
                obj
                for obj in pymel.selected()
                if libPymel.isinstance_of_shape(obj, cls=pymel.nodetypes.Mesh)
            ),
            None,
        )
        if not mesh:
            pymel.warning("Please select a mesh to follow.")
            return

        for ctrl_model in self._iter_ictrl():
            ctrl_model.swap_mesh(mesh)


def register_plugin():
    return CtrlInteractiveSwapMesh
