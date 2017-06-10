import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule2 import Module2
from omtk.libs import libPython
from omtk.libs import libRigging


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


class FK2(Module2):
    DEFAULT_NAME_USE_FIRST_INPUT = True
    _NAME_CTRL_ENUMERATE = False  # If set to true, the ctrl will use the module name. Otherwise they will use their associated input name.
    _NAME_CTRL_MERGE = True  # If set to true, it there's only one controller, it will use the name of the module.
    _CLS_CTRL = CtrlFk

    def __init__(self, *args, **kwargs):
        super(FK2, self).__init__(*args, **kwargs)
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
        super(FK2, self).__callbackNetworkPostBuild__()

    def build(self, constraint=True, parent=True, create_grp_anm=True, create_grp_rig=False, *args, **kwargs):
        super(FK2, self).build(create_grp_rig=create_grp_rig, *args, **kwargs)

        # Store bind pose
        for i, jnt in enumerate(self.jnts):
            self.grp_inn.innInfWorld[i].set(jnt.getMatrix(worldSpace=True))

        # Build ctrls
        libPython.resize_list(self.ctrls, len(self.jnts))
        for i, ctrl in enumerate(self.ctrls):
            self.ctrls[i] = self.init_ctrl(self._CLS_CTRL, ctrl)
            self.ctrls[i].build()

        #libRigging.create_hyerarchy(self.ctrls)  # todo: return 'Chain' object?

        for ctrl, bind_tm in zip(self.ctrls, self.grp_inn.innInfWorld):
            tm = libRigging.create_utility_node(
                'multMatrix',
                matrixIn=(
                    bind_tm,
                    self.grp_hook.matrix
                )
            ).matrixSum

            decompose = libRigging.create_utility_node(
                'decomposeMatrix',
                inputMatrix=tm
            )

            pymel.connectAttr(decompose.outputTranslate, ctrl.offset.translate)
            pymel.connectAttr(decompose.outputRotate, ctrl.offset.rotate)
            pymel.connectAttr(decompose.outputScale, ctrl.offset.scale)

        for i, (ctrl, jnt, bind_tm) in enumerate(zip(self.ctrls, self.jnts, self.grp_inn.innInfWorld)):
            attr_dst = self.grp_out.outInfWorld[i]

            tm = libRigging.create_utility_node(
                'multMatrix',
                matrixIn=(
                    bind_tm,
                    ctrl.matrix
                )
            ).matrixSum
            pymel.connectAttr(tm, attr_dst)

            tm = libRigging.create_utility_node(
                'multMatrix',
                matrixIn=(
                    attr_dst,
                    jnt.worldInverseMatrix,
                )
            ).matrixSum

            decompose = libRigging.create_utility_node(
                'decomposeMatrix',
                inputMatrix=tm
            )

            pymel.connectAttr(decompose.outputTranslate, jnt.translate)
            pymel.connectAttr(decompose.outputRotate, jnt.rotate)
            pymel.connectAttr(decompose.outputScale, jnt.scale)


        # for i, chain in enumerate(self.chains):
        #     # Build chain ctrls
        #     chain_ctrls = []
        #     for j, jnt in enumerate(chain):
        #         jnt_index = self.jnts.index(jnt)  # todo: optimize performance by created a map?
        #         ctrl = self.ctrls[jnt_index]
        #         chain_ctrls.append(ctrl)
        #
        #         # Resolve ctrl name.
        #         # TODO: Validate with multiple chains
        #         if len(self.jnts) == 1 and self._NAME_CTRL_MERGE:
        #             ctrl_name = nomenclature_anm.resolve()
        #         elif self._NAME_CTRL_ENUMERATE:
        #             ctrl_name = nomenclature_anm.resolve('{0:02d}'.format(j))
        #         else:
        #             nomenclature = nomenclature_anm + self.rig.nomenclature(jnt.stripNamespace().nodeName())
        #             ctrl_name = nomenclature.resolve()
        #
        #         ctrl.build(name=ctrl_name, refs=jnt, geometries=self.rig.get_meshes())
        #         ctrl.setMatrix(jnt.getMatrix(worldSpace=True))
        #
        #         # Build space-switch for first chain ctrl
        #         if j == 0:
        #             if self.create_spaceswitch:
        #                 if self.sw_translate:
        #                     ctrl.create_spaceswitch(self, self.parent, add_world=True)
        #                 else:
        #                     ctrl.create_spaceswitch(self, self.parent, skipTranslate=['x', 'y', 'z'], add_world=True)

        #     if chain_ctrls:
        #         chain_ctrls[0].setParent(self.grp_anm)
        #         libRigging.create_hyerarchy(chain_ctrls)
        #
        # # Constraint jnts to ctrls if necessary
        # if constraint is True:
        #     for jnt, ctrl in zip(self.jnts, self.ctrls):
        #         pymel.parentConstraint(ctrl, jnt, maintainOffset=True)
        #         pymel.connectAttr(ctrl.scaleX, jnt.scaleX)
        #         pymel.connectAttr(ctrl.scaleY, jnt.scaleY)
        #         pymel.connectAttr(ctrl.scaleZ, jnt.scaleZ)


def register_plugin():
    return FK2
