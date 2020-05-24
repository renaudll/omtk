"""
Logic for the "Neck" module
"""
from omtk.modules.fk import FK, CtrlFk
from omtk.modules.twistbone import Twistbone
from omtk.core.utils import ui_expose
from omtk.core.exceptions import ValidationError


class CtrlNeck(CtrlFk):
    pass


class Neck(FK):
    """
    Simple FK setup with twistbone support.
    """

    def __init__(self, *args, **kwarg):
        super(Neck, self).__init__(*args, **kwarg)
        self.create_twist = True
        self.sys_twist = None

    _CLS_CTRL = CtrlNeck
    _CLASS_SYS_TWIST = Twistbone
    _NAME_CTRL_MERGE = True  # By default we only expect one controller for the head. (Head_Ctrl > than Head_Head_Ctrl)
    _NAME_CTRL_ENUMERATE = (
        True  # If we find additional influences, we'll use enumeration.
    )

    def build(self, *args, **kwargs):
        super(Neck, self).build(*args, **kwargs)

        # Create twistbone system if needed
        if self.create_twist:
            jnt_s = self.jnt
            jnt_e = self.get_head_jnt()

            twist_nomenclature = self.get_nomenclature().copy()
            twist_nomenclature.add_tokens("bend")

            self.sys_twist = self._CLASS_SYS_TWIST.from_instance(
                self, self.sys_twist, self.name, inputs=[jnt_s, jnt_e],
            )
            self.sys_twist.name = twist_nomenclature.resolve()
            self.sys_twist.build(num_twist=3, create_bend=True)
            if self.sys_twist.grp_anm:
                self.sys_twist.grp_anm.setParent(self.grp_anm)
            self.sys_twist.grp_rig.setParent(self.grp_rig)

    def unbuild(self):
        if self.sys_twist:
            self.sys_twist.unbuild()

        super(Neck, self).unbuild()

    def validate(self):
        """
        Check if the module can be built in it's current state.

        :raises ValidationError: If the module fail to validate.
        """
        super(Neck, self).validate()

        num_jnts = len(self.jnts)
        if num_jnts != 1:
            raise ValidationError("Expected only one influences, got %s" % num_jnts)

        head_jnt = self.get_head_jnt()
        if not head_jnt:
            raise ValidationError("Cannot resolve Head influence from %s" % self.jnt)

    @ui_expose()
    def assign_twist_weights(self):
        """
        Automatically assign twist bone weights.
        """
        for module in self.sys_twist:
            if isinstance(module, Twistbone) and module.is_built():
                module.assign_twist_weights()

    @ui_expose()
    def unassign_twist_weights(self):
        """
        Automatically unassign twist bone weights.
        """
        for module in self.sys_twist:
            if isinstance(module, Twistbone) and module.is_built():
                module.unassign_twist_weights()


def register_plugin():
    """
    Register the plugin. This function is expected by plugin_manager.

    :return: The plugin to register
    :rtype: omtk.core.modules.Module
    """
    return Neck
