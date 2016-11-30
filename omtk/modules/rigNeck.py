from omtk.modules import rigFK
from omtk.modules import rigTwistbone
from omtk.core.utils import decorator_uiexpose
from omtk.libs import libPython

class CtrlNeck(rigFK.CtrlFk):
    pass


class Neck(rigFK.FK):
    """
    Simple FK setup with twistbone support.
    """

    def __init__(self, *args, **kwarg):
        super(Neck, self).__init__(*args, **kwarg)
        self.create_twist = True
        self.sys_twist = None

    _CLS_CTRL = CtrlNeck
    _CLASS_SYS_TWIST = rigTwistbone.Twistbone
    _NAME_CTRL_MERGE = True  # By default we only expect one controller for the head. (Head_Ctrl > than Head_Head_Ctrl)
    _NAME_CTRL_ENUMERATE = True  # If we find additional influences, we'll use enumeration.

    @libPython.memoized_instancemethod
    def _get_head_jnt(self):
        neck_jnt = self.jnt
        head_jnts = self.rig.get_head_jnts()
        for child in neck_jnt.getChildren():
            if child in head_jnts:
                return child

    def build(self, *args, **kwargs):
        super(Neck, self).build(create_grp_rig=True, *args, **kwargs)
        
        # Create twistbone system if needed
        if self.create_twist:
            jnt_s = self.jnt
            jnt_e = self._get_head_jnt()

            twist_nomenclature = self.get_nomenclature().copy()
            twist_nomenclature.add_tokens('bend')

            self.sys_twist = self.init_module(self._CLASS_SYS_TWIST, self.sys_twist, inputs=[jnt_s, jnt_e])
            self.sys_twist.name = twist_nomenclature.resolve()
            self.sys_twist.build(num_twist=3, create_bend=False)
            self.sys_twist.grp_rig.setParent(self.grp_rig)

    def unbuild(self):
        for twist_sys in self.sys_twist:
            twist_sys.unbuild()
            
        super(Neck, self).unbuild()

    def validate(self):
        """
        Allow the ui to know if the module is valid to be builded or not
        :return: True or False depending if it pass the building validation
        """
        super(Neck, self).validate()
        num_jnts = len(self.jnts)

        if num_jnts != 1:
            raise Exception("Expected only one influences, got {}".format(num_jnts))

        head_jnt = self._get_head_jnt()
        if not head_jnt:
            raise Exception("Cannot resolve Head influence from {}".format(self.jnt))

        return True

    @decorator_uiexpose()
    def assign_twist_weights(self):
        for module in self.sys_twist:
            if isinstance(module, rigTwistbone.Twistbone) and module.is_built():
                module.assign_twist_weights()

    @decorator_uiexpose()
    def unassign_twist_weights(self):
        for module in self.sys_twist:
            if isinstance(module, rigTwistbone.Twistbone) and module.is_built():
                module.unassign_twist_weights()


def register_plugin():
    return Neck