import pymel.core as pymel
from omtk.classCtrl import BaseCtrl
from omtk.classModule import Module
from omtk.libs import libRigging, libCtrlShapes


class CtrlFk(BaseCtrl):
    def __createNode__(self, size=1, *args, **kwargs):
        '''
        if 'shoulder' in name.lower():
            node = libCtrlShapes.create_shape_double_needle(size=size*0.04, normal=(0, 0, 1), *args, **kwargs)
        else:
        '''

        node, make = libCtrlShapes.create_shape_circle(size=size, *args, **kwargs)
        make.radius.set(size)
        make.degree.set(1)
        make.sections.set(8)

        return node


class FK(Module):
    def __init__(self, *args, **kwargs):
        super(FK, self).__init__(*args, **kwargs)
        self.ctrls = None

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

    def build(self, rig, constraint=True, parent=True, *args, **kwargs):
        super(FK, self).build(rig, create_grp_rig=False, *args, **kwargs)

        nomenclature_anm = self.get_nomenclature_anm(rig)

        # Define ctrls
        if not self.ctrls:
            self.ctrls = []
            for input in self.chain_jnt:
                ctrl = CtrlFk()
                self.ctrls.append(ctrl)

        # Create ctrls
        for input, ctrl in zip(self.chain_jnt, self.ctrls):
            ctrl_nomenclature = nomenclature_anm.copy(input.name())
            ctrl_name = ctrl_nomenclature.resolve('fk')
            size = libRigging.get_recommended_ctrl_size(input) * 1.25
            ctrl.build(size=size, name=ctrl_name)
            ctrl.setMatrix(input.getMatrix(worldSpace=True))


        self.ctrls[0].setParent(self.grp_anm)
        for i in range(1, len(self.ctrls)):
            self.ctrls[i].setParent(self.ctrls[i - 1])

        # Connect jnt -> anm
        if constraint is True:
            for inn, ctrl in zip(self.chain_jnt, self.ctrls):
                pymel.parentConstraint(ctrl, inn)
                pymel.connectAttr(ctrl.scaleX, inn.scaleX)
                pymel.connectAttr(ctrl.scaleY, inn.scaleY)
                pymel.connectAttr(ctrl.scaleZ, inn.scaleZ)

        '''
        # Connect to parent
        if parent and self.parent is not None:
            pymel.parentConstraint(self.parent, self.grp_anm, maintainOffset=True)
            #pymel.scaleConstraint(self.parent, self.grp_anm, maintainOffset=True)
        '''

    def unbuild(self):
        super(FK, self).unbuild()


class CtrlFkAdd(BaseCtrl):
    def __createNode__(self, *args, **kwargs):
        return libCtrlShapes.create_shape_needle(*args, **kwargs)


class AdditiveFK(FK):
    """
    An AdditiveFK chain is a standard FK chain that have one or many additional controllers to rotate the entire chain.
    """
    def __init__(self, *args, **kwargs):
        super(AdditiveFK, self).__init__(*args, **kwargs)
        self.num_ctrls = 1
        self.additive_ctrls = []

    def build(self, rig, *args, **kwargs):
        super(AdditiveFK, self).build(rig, *args, **kwargs)

        # TODO: Support multiple additive ctrls
        ctrl_add_size = libRigging.get_recommended_ctrl_size(self.chain.start)

        ctrl_add = CtrlFkAdd()
        ctrl_add.build(size=ctrl_add_size)
        ctrl_add.setMatrix(self.chain.start.getMatrix(worldSpace=True))
        ctrl_add.setParent(self.grp_anm)
        self.additive_ctrls.append(ctrl_add)

        for ctrl in self.ctrls:
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

    def unbuild(self):
        self.additive_ctrls = None
        super(AdditiveFK, self).unbuild()
