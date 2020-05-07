from omtk.core import classCtrlModel


class ModelCtrlLinear(classCtrlModel.BaseCtrlModel):
    """
    An InteractiveCtrl ctrl is directly constrained on a mesh via a layer_fol.
    To prevent double deformation, the trick is an additional layer before the final ctrl that invert the movement.
    For clarity purposes, this is built in the rig so the animator don't need to see the whole setup.

    However an InterfactiveCtrl might still have to be callibrated.
    This is necessay to keep the InteractiveCtrl values in a specific range (ex: -1 to 1) in any scale.
    The calibration apply non-uniform scaling on the ctrl parent to cheat the difference.

    For this reason an InteractiveCtrl is created using the following steps:
    1) Create the setup (using build)
    2) Connecting the doritos ctrl to something
    3) Optionally call .calibrate()
    """

    _ATTR_NAME_SENSITIVITY_TX = "sensitivityX"
    _ATTR_NAME_SENSITIVITY_TY = "sensitivityY"
    _ATTR_NAME_SENSITIVITY_TZ = "sensitivityZ"

    def __init__(self, *args, **kwargs):
        super(ModelCtrlLinear, self).__init__(*args, **kwargs)
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None

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

    def parent_to(self, parent):
        """
        Bypass default parent mecanism since it is computer internally.
        """
        pass

    def build(self, ctrl,):
        # todo: get rid of the u_coods, v_coods etc, we should rely on the bind
        super(ModelCtrlLinear, self).build(ctrl)

        # TODO: Implement

        # naming = self.get_nomenclature_rig()
        #
        # # For now we'll just do a constraint, but we'll want more that than soon...
        # pymel.connectAttr(ctrl.offset)
