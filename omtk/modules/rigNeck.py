from omtk.modules import rigFK
from omtk.modules import rigTwistbone
from omtk.core.utils import decorator_uiexpose


class CtrlNeck(rigFK.CtrlFk):
    pass


class Neck(rigFK.FK):
    """
    Simple FK setup with twistbone support.
    """

    def __init__(self, *args, **kwarg):
        super(Neck, self).__init__(*args, **kwarg)
        self.create_twist = True
        self.sys_twist = []

    _CLS_CTRL = CtrlNeck
    _CLASS_SYS_TWIST = rigTwistbone.Twistbone
    _NAME_CTRL_MERGE = True  # By default we only expect one controller for the head. (Head_Ctrl > than Head_Head_Ctrl)
    _NAME_CTRL_ENUMERATE = True  # If we find additional influences, we'll use enumeration.

    def build(self, *args, **kwargs):
        super(Neck, self).build(create_grp_rig=True, *args, **kwargs)

        nomenclature_rig = self.get_nomenclature_rig()
        head_jnt = self.rig.get_head_jnt()
        num_twist = len(self.chain_jnt)
        
        # Create twistbone system if needed
        if self.create_twist:
            if head_jnt:
                # If the IK system is a quad, we need to have two twist system
                for i in range(0, num_twist):
                    start_jnt = self.chain[i]
                    end_jnt = self.chain_jnt[i + 1] if i + 1 < len(self.chain_jnt) else head_jnt
                    cur_sys_twist = self.sys_twist[i] if i < len(self.sys_twist) else None
                    if not isinstance(cur_sys_twist, self._CLASS_SYS_TWIST):
                        cur_sys_twist = self._CLASS_SYS_TWIST([start_jnt, end_jnt], rig=self.rig)
                        self.sys_twist.append(cur_sys_twist)
                    # Hack
                    twist_sys_name = start_jnt.name().replace('_' + nomenclature_rig.type_jnt, "Twist")
                    cur_sys_twist.name = '{0}'.format(twist_sys_name)
                    cur_sys_twist.build(num_twist=3, create_bend=True, **kwargs)
            else:
                self.warning("Could not find the head joint. Neck Twist creation will be aborded")

        for sys_twist in self.sys_twist:
            if sys_twist.create_bend:
                sys_twist.grp_anm.setParent(self.grp_anm)
            sys_twist.grp_rig.setParent(self.grp_rig)

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
        num_chain = len(self.chains)

        if num_chain != 1:
            raise Exception("Expected one joint chain, got {0}".format(num_chain))

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