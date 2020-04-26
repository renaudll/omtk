import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule import Module
from omtk.libs import libPython
from omtk.libs import libRigging


class CtrlFk(BaseCtrl):
    def __createNode__(self, *args, **kwargs):
        """
        if 'shoulder' in name.lower():
            node = libCtrlShapes.create_shape_double_needle(size=size*0.04, normal=(0, 0, 1), *args, **kwargs)
        else:
        """
        node = super(CtrlFk, self).__createNode__(multiplier=1.1, *args, **kwargs)

        make = next(iter(node.inputs()), None)
        if make:
            # TODO: Multiply radius???
            # make.radius.set(size)
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
    _NAME_CTRL_ENUMERATE = False  # If set to true, the ctrl will use the module name.
    _FORCE_INPUT_NAME = (
        False  # Force using the name of the input in the name of the ctrl
    )
    # Otherwise they will use their associated input name.
    _CLS_CTRL = CtrlFk

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

    def build(
        self,
        constraint=True,
        parent=True,
        create_grp_anm=True,
        create_grp_rig=False,
        *args,
        **kwargs
    ):
        super(FK, self).build(create_grp_rig=create_grp_rig, *args, **kwargs)
        nomenclature_anm = self.get_nomenclature_anm()
        nomenclature_rig = self.get_nomenclature_rig()

        # Initialize ctrls
        libPython.resize_list(self.ctrls, len(self.jnts))
        for i, ctrl in enumerate(self.ctrls):
            self.ctrls[i] = self.init_ctrl(self._CLS_CTRL, ctrl)

        for i, chain in enumerate(self.chains):
            # Build chain ctrls
            chain_ctrls = []
            for j, jnt in enumerate(chain):
                jnt_index = self.jnts.index(
                    jnt
                )  # todo: optimize performance by created a map?
                ctrl = self.ctrls[jnt_index]
                chain_ctrls.append(ctrl)

                # Resolve ctrl name.
                # TODO: Validate with multiple chains
                nomenclature = nomenclature_anm + self.rig.nomenclature(
                    jnt.stripNamespace().nodeName()
                )
                if not self._FORCE_INPUT_NAME:
                    if len(self.jnts) == 1 and len(self.chains) == 1:
                        ctrl_name = nomenclature_anm.resolve()
                    elif len(self.chains) == 1 or self._NAME_CTRL_ENUMERATE:
                        ctrl_name = nomenclature_anm.resolve("{0:02d}".format(j))
                    else:
                        ctrl_name = nomenclature.resolve()
                else:
                    ctrl_name = nomenclature.resolve()

                ctrl.build(name=ctrl_name, refs=jnt, geometries=self.rig.get_meshes())
                ctrl.setMatrix(jnt.getMatrix(worldSpace=True))

                # Build space-switch for first chain ctrl
                if j == 0:
                    if self.create_spaceswitch:
                        if self.sw_translate:
                            ctrl.create_spaceswitch(self, self.parent, add_world=True)
                        else:
                            ctrl.create_spaceswitch(
                                self,
                                self.parent,
                                skipTranslate=["x", "y", "z"],
                                add_world=True,
                            )

            if chain_ctrls:
                chain_ctrls[0].setParent(self.grp_anm)
                libRigging.create_hyerarchy(chain_ctrls)

        # Constraint jnts to ctrls if necessary
        if constraint is True:
            for jnt, ctrl in zip(self.jnts, self.ctrls):
                pymel.parentConstraint(ctrl, jnt, maintainOffset=True)
                pymel.connectAttr(ctrl.scaleX, jnt.scaleX)
                pymel.connectAttr(ctrl.scaleY, jnt.scaleY)
                pymel.connectAttr(ctrl.scaleZ, jnt.scaleZ)


def register_plugin():
    return FK
