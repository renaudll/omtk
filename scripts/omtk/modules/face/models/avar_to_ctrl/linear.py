import pymel.core as pymel

from omtk.modules.face.models.avar_to_ctrl import base
from omtk.core.compounds import create_compound

class ModelCtrlLinear(base.BaseCtrlModel):
    """
    An InteractiveCtrl ctrl is directly constrained on a mesh via a layer_fol.
    To prevent double deformation, the trick is an additional layer
    before the final ctrl that invert the movement.
    For clarity purposes, this is built in the rig so
    the animator don't need to see the whole setup.

    However an InterfactiveCtrl might still have to be callibrated.
    This is necessay to keep the InteractiveCtrl values
    in a specific range (ex: -1 to 1) in any scale.
    The calibration apply non-uniform scaling on
    the ctrl parent to cheat the difference.

    For this reason an InteractiveCtrl is created using the following steps:
    1) Create the setup (using build)
    2) Connecting the doritos ctrl to something
    3) Optionally call .calibrate()
    """

    def __init__(self, *args, **kwargs):
        super(ModelCtrlLinear, self).__init__(*args, **kwargs)

        # The object containing the bind pose of the
        # influence controller by the controller.
        self._grp_bind_infl = None

        # The object containing the desired default position of the ctrl.
        # This can differ from the bind pose of the ctrl mode.
        # For example, the jaw ctrl model will influence a joint
        # inside the head but the controller will be outside.
        self._grp_bind_ctrl = None

        self._attr_inn_parent_tm = None

        self._stack = None

    def _build_compound(self):
        return create_compound(
            "omtk.AvarCtrlLinear",  # TODO: Get our own compound instead of duplicating.
            namespace=self.get_nomenclature().resolve()
        )

    def build(self):
        super(ModelCtrlLinear, self).build()

        # Connect compound inputs
        for attr, value in (
            ("multLr", self.attr_sensitivity_tx),
            ("multFb", self.attr_sensitivity_tx),
            ("multUd", self.attr_sensitivity_tx),
            ("innOffset", self.grp_rig.matrix)
        ):
            pymel.connectAttr(value, "%s.%s" % (self.compound.input, attr))

    def connect_ctrl(self, ctrl):
        self.grp_rig.setMatrix(ctrl.getMatrix(worldSpace=True))

        super(ModelCtrlLinear, self).connect_ctrl(ctrl)

        # Connect compound inputs
        for attr, value in (
            ("ctrlLocalTM", ctrl.matrix),
        ):
            pymel.connectAttr(value, "%s.%s" % (self.compound.input, attr), force=True)
