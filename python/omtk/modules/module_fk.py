import logging

from omtk.components_scripted.component_fk import ComponentFk
from omtk.core.ctrl import BaseCtrl
from omtk.core.module import Module
from omtk.libs import libPython
from omtk.libs import libRigging

log = logging.getLogger('omtk')


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
            # make.radius.set(size)
            make.degree.set(1)
            make.sections.set(8)

        return node


class FK(Module):
    DEFAULT_NAME_USE_FIRST_INPUT = True
    _NAME_CTRL_ENUMERATE = False  # If set to true, the ctrl will use the module name. Otherwise they will use their associated input name.
    _NAME_CTRL_MERGE = True  # If set to true, it there's only one controller, it will use the name of the module.
    _CLS_CTRL = CtrlFk

    #
    def __init__(self, *args, **kwargs):
        super(FK, self).__init__(*args, **kwargs)
        self.ctrls = []
        self.sw_translate = False
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
            self.ctrls = filter(None, self.ctrls)
        except (AttributeError, TypeError):
            pass
        super(FK, self).__callbackNetworkPostBuild__()

    def init_ctrls(self):
        nomenclature_anm = self.get_nomenclature_anm()

        # Build ctrls
        libPython.resize_list(self.ctrls, len(self.jnts))
        for i, ctrl in enumerate(self.ctrls):
            self.ctrls[i] = self.init_ctrl(self._CLS_CTRL, ctrl)
            self.ctrls[i].build()

        for i, chain in enumerate(self.chains):
            # Build chain ctrls
            chain_ctrls = []
            for j, jnt in enumerate(chain):
                jnt_index = self.jnts.index(jnt)  # todo: optimize performance by created a map?
                ctrl = self.ctrls[jnt_index]
                chain_ctrls.append(ctrl)

                # Resolve ctrl name.
                # TODO: Validate with multiple chains
                if len(self.jnts) == 1 and self._NAME_CTRL_MERGE:
                    ctrl_name = nomenclature_anm.resolve()
                elif self._NAME_CTRL_ENUMERATE:
                    ctrl_name = nomenclature_anm.resolve('{0:02d}'.format(j))
                else:
                    nomenclature = nomenclature_anm + self.rig.nomenclature(jnt.stripNamespace().nodeName())
                    ctrl_name = nomenclature.resolve()

                ctrl.build(name=ctrl_name, refs=jnt, geometries=self.rig.get_meshes())
                ctrl.setMatrix(jnt.getMatrix(worldSpace=True))

                # Build space-switch for first chain ctrl
                if j == 0:
                    if self.create_spaceswitch:
                        if self.sw_translate:
                            ctrl.create_spaceswitch(self, self.parent, add_world=True)
                        else:
                            ctrl.create_spaceswitch(self, self.parent, skipTranslate=['x', 'y', 'z'],
                                                    add_world=True)

            if chain_ctrls:
                chain_ctrls[0].setParent(self.grp_anm)
                libRigging.create_hyerarchy(chain_ctrls)

    def build(self):
        super(FK, self).build()
        # nomenclature_anm = self.get_nomenclature_anm()

        self.init_ctrls()

        # Connect component
        component = ComponentFk()
        component.build()
        # todo: set chain length?

        component._set_chain_length(len(self.jnts))

        # Store bind pose
        for i, jnt in enumerate(self.jnts):
            component._attr_inn_chain[i].set(jnt.getMatrix(worldSpace=True))


def register_plugin():
    return FK
