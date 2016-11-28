import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule import Module

class CtrlFk(BaseCtrl):
    def __createNode__(self, *args, **kwargs):
        '''
        if 'shoulder' in name.lower():
            node = libCtrlShapes.create_shape_double_needle(size=size*0.04, normal=(0, 0, 1), *args, **kwargs)
        else:
        '''
        node = super(CtrlFk, self).__createNode__(multiplier=1.1, *args, **kwargs)

        make = next(iter(node.inputs()), None)
        if make:
            # TODO: Multiply radius???
            #make.radius.set(size)
            make.degree.set(1)
            make.sections.set(8)

        return node


class FK(Module):
    """
    A Simple FK with support for multiple hyerarchy.

    Note that there's multiple way to name the ctrls.
    1) Use the inputs as reference ( _NAME_CTRL_ENUMERATE = False )
    ex: (module name is arm_l)
    jnt_upperarm_l -> ctrl_arm_upperarm_l
    jnt_forearm_l  -> ctrl_arm_forearm_l
    2) Use enumeration ( _NAME_CTRL_ENUMERATE = True )
    ex: (module name is arm_l)
    jnt_upperarm_l -> ctrl_arm_01_l
    jnt_forearm_l  -> ctrl_arm_02_l
    ex:
    """
    DEFAULT_NAME_USE_FIRST_INPUT = True
    _NAME_CTRL_ENUMERATE = False  # If set to true, the ctrl will use the module name. Otherwise they will use their associated input name.
    _NAME_CTRL_MERGE = True  # If set to true, it there's only one controller, it will use the name of the module.
    _CLS_CTRL = CtrlFk

    def __init__(self, *args, **kwargs):
        super(FK, self).__init__(*args, **kwargs)
        self.ctrls = []
        self.sw_translate=False
        self.create_spaceswitch = True

    #
    # libSerialization implementation
    #
    def __callbackNetworkPostBuild__(self):
        """
        Cleaning routine automatically called by libSerialization after a network import.
        """
        # Ensure there's no None value in the .ctrls array.
        # This can happen if the rigging delete the stored shape before rebuilding.
        try:
            self.ctrls= filter(None, self.ctrls)
        except (AttributeError, TypeError):
            pass
        super(FK, self).__callbackNetworkPostBuild__()


    def build(self, constraint=True, parent=True, create_grp_anm=True, create_grp_rig=False, *args, **kwargs):
        super(FK, self).build(create_grp_rig=create_grp_rig, *args, **kwargs)
        nomenclature_anm = self.get_nomenclature_anm()

        # Define ctrls
        num_ctrls = 0
        if self.ctrls:
            num_ctrls = len(self.ctrls)
        chain_first_ctrl_idx = 0
        for i, chain in enumerate(self.chains):
            if not self.ctrls or chain_first_ctrl_idx + len(chain) > num_ctrls:
                for input in chain:
                    ctrl = self._CLS_CTRL()
                    self.ctrls.append(ctrl)
                    num_ctrls += 1

            # Create ctrls
            chain_length = len(chain)
            for ctrl_index, input, ctrl in zip(range(chain_length), chain, self.ctrls[chain_first_ctrl_idx:chain_first_ctrl_idx + chain_length]):
                # Resolve ctrl name
                if len(self.jnts) == 1 and self._NAME_CTRL_MERGE:
                    ctrl_name = nomenclature_anm.resolve()
                elif self._NAME_CTRL_ENUMERATE:
                    ctrl_name = nomenclature_anm.resolve('{0:02d}'.format(ctrl_index))
                else:
                    nomenclature = nomenclature_anm + self.rig.nomenclature(input.name())
                    ctrl_name = nomenclature.resolve()

                ctrl.build(name=ctrl_name, refs=input, geometries=self.rig.get_meshes())
                ctrl.setMatrix(input.getMatrix(worldSpace=True))

            if self.create_spaceswitch:
                if self.sw_translate:
                    self.ctrls[chain_first_ctrl_idx].create_spaceswitch(self, self.parent, add_world=True)
                else:
                    self.ctrls[chain_first_ctrl_idx].create_spaceswitch(self, self.parent,
                                                                        skipTranslate=['x', 'y', 'z'], add_world=True)

            self.ctrls[chain_first_ctrl_idx].setParent(self.grp_anm)
            for j in range(chain_first_ctrl_idx + 1, chain_first_ctrl_idx + len(chain)):
                self.ctrls[j].setParent(self.ctrls[j - 1])

            # Connect jnt -> anm
            if constraint is True:
                for inn, ctrl in zip(chain, self.ctrls[chain_first_ctrl_idx:chain_first_ctrl_idx + len(chain)]):
                    pymel.parentConstraint(ctrl, inn)
                    pymel.connectAttr(ctrl.scaleX, inn.scaleX)
                    pymel.connectAttr(ctrl.scaleY, inn.scaleY)
                    pymel.connectAttr(ctrl.scaleZ, inn.scaleZ)

            chain_first_ctrl_idx += len(chain)

        '''
        # Connect to parent
        if parent and self.parent is not None:
            pymel.parentConstraint(self.parent, self.grp_anm, maintainOffset=True)
            #pymel.scaleConstraint(self.parent, self.grp_anm, maintainOffset=True)
        '''



def register_plugin():
    return FK
