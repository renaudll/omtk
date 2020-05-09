"""
Simple utility to swap the mesh used by an InteractiveCtrl in case the wrong mesh was used.
"""
from omtk.core.macros import BaseMacro


class CtrlInteractiveSwapMesh(BaseMacro):
    def _iter_ictrl(self):
        from omtk import api
        from omtk.modules import rigFaceAvarGrps
        from omtk.modules import rigFaceAvar
        from omtk.models import model_ctrl_linear

        rig, modules = api._get_modules_from_selection()
        # Build selected modules
        for module in modules:
            if isinstance(module, rigFaceAvarGrps.AvarGrp):
                for avar in module.iter_avars():
                    if (
                        isinstance(avar, rigFaceAvar.AbstractAvar)
                        and avar.model_ctrl
                        and isinstance(
                            avar.model_ctrl, model_ctrl_linear.ModelCtrlLinear
                        )
                    ):
                        yield avar.model_ctrl

    def run(self):
        import pymel.core as pymel
        from omtk.libs import libPymel

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
