import collections
import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule import Module
from omtk.libs import libRigging, libCtrlShapes
from omtk.core import constants

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
    """
    DEFAULT_NAME_USE_FIRST_INPUT = True
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

    def build(self, constraint=True, parent=True, create_grp_anm=True, *args, **kwargs):
        super(FK, self).build(create_grp_rig=False, *args, **kwargs)
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
            for input, ctrl in zip(chain, self.ctrls[chain_first_ctrl_idx:chain_first_ctrl_idx + len(chain)]):
                ctrl_nomenclature = nomenclature_anm.rebuild(input.name())
                ctrl_name = ctrl_nomenclature.resolve('fk')
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

class CtrlFkAdd(BaseCtrl):
    def __createNode__(self, size=None, refs=None, *args, **kwargs):
        # Resolve size automatically if refs are provided.
        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs
        if size is None and ref is not None:
            size = libRigging.get_recommended_ctrl_size(ref)
        else:
            size = 1.0

        node = libCtrlShapes.create_shape_needle(size=size, *args, **kwargs)

        return node


class AdditiveFK(FK):
    """
    An AdditiveFK chain is a standard FK chain that have one or many additional controllers to rotate the entire chain.
    """
    _CLASS_CTRL_IK = CtrlFkAdd

    def __init__(self, *args, **kwargs):
        super(AdditiveFK, self).__init__(*args, **kwargs)
        self.num_ctrls = 1
        self.additive_ctrls = []

    def build(self, *args, **kwargs):
        super(AdditiveFK, self).build(*args, **kwargs)

        nomenclature_anm = self.get_nomenclature_anm()

        # Ensure to create the finger ctrl in the good orientation
        if nomenclature_anm.side == self.rig.nomenclature.SIDE_L:
            normal_data = {constants.Axis.x: (1, 0, 0), constants.Axis.y: (0, 1, 0), constants.Axis.z: (0, 0, 1)}
        else:
            normal_data = {constants.Axis.x: (-1, 0, 0), constants.Axis.y: (0, -1, 0), constants.Axis.z: (0, 0, -1)}

        # TODO: Support multiple additive ctrls
        # TODO: Rename
        self.additive_ctrls = filter(None, self.additive_ctrls)
        if not self.additive_ctrls:
            ctrl_add = CtrlFkAdd()
            self.additive_ctrls.append(ctrl_add)
        #HACK - Temp since we don't support multiple ctrl for the moment
        ctrl_add = self.additive_ctrls[0]
        for i, ctrl in enumerate(self.additive_ctrls):
            name = nomenclature_anm.resolve("addFk{0:02d}".format(i))
            ctrl.build(name=name, refs=self.chain.start, normal=normal_data[self.rig._up_axis])
            ctrl.offset.setMatrix(self.chain.start.getMatrix(worldSpace=True))
            ctrl.setParent(self.grp_anm)

        for i, ctrl in enumerate(self.ctrls):
            #HACK Add a new layer if this is the first ctrl to prevent Gimbal lock problems
            if i == 0:
                ctrl.offset = ctrl.append_layer("gimbal")
            attr_rotate_x = libRigging.create_utility_node('addDoubleLinear',
                                                           input1=ctrl.offset.rotateX.get(),
                                                           input2=ctrl_add.rotateX
                                                           ).output
            attr_rotate_y = libRigging.create_utility_node('addDoubleLinear',
                                                           input1=ctrl.offset.rotateY.get(),
                                                           input2=ctrl_add.rotateY
                                                           ).output
            attr_rotate_z = libRigging.create_utility_node('addDoubleLinear',
                                                           input1=ctrl.offset.rotateZ.get(),
                                                           input2=ctrl_add.rotateZ
                                                           ).output
            pymel.connectAttr(attr_rotate_x, ctrl.offset.rotateX)
            pymel.connectAttr(attr_rotate_y, ctrl.offset.rotateY)
            pymel.connectAttr(attr_rotate_z, ctrl.offset.rotateZ)

        # Constraint the fk ctrls in position to the additive fk ctrls
        pymel.pointConstraint(ctrl_add, self.ctrls[0].offset)

    def iter_ctrls(self):
        for ctrl in super(AdditiveFK, self).iter_ctrls():
            yield ctrl
        for ctrl in self.additive_ctrls:
            yield ctrl

def register_plugin():
    return FK
