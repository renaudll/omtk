import pymel.core as pymel
from classCtrl import BaseCtrl
from classModule import Module
from libs import libRigging, libCtrlShapes


class CtrlFk(BaseCtrl):
    def build(self, size=1, *args, **kwargs):
        super(CtrlFk, self).build(*args, **kwargs)
        make = self.node.getShape().create.inputs()[0]
        make.radius.set(size)
        make.degree.set(1)
        make.sections.set(8)
        return self.node


class FK(Module):
    def __init__(self, *args, **kwargs):
        super(FK, self).__init__(*args, **kwargs)
        self.ctrls = []

    def build(self, constraint=True, parent=True, *args, **kwargs):
        super(FK, self).build(create_grp_rig=False, *args, **kwargs)

        # Create ctrl chain
        self.ctrls = []
        for input in self.input:
            ctrl_name = self.name_anm.resolve('fk')

            ctrl = CtrlFk(name=ctrl_name)
            size = libRigging.get_recommended_ctrl_size(input) * 1.25
            ctrl.build(size=size)
            ctrl.rename(ctrl_name)
            ctrl.setMatrix(input.getMatrix(worldSpace=True))

            self.ctrls.append(ctrl)

        self.ctrls[0].setParent(self.grp_anm)
        for i in range(1, len(self.ctrls)):
            self.ctrls[i].setParent(self.ctrls[i - 1])

        # Connect jnt -> anm
        if constraint is True:
            for inn, ctrl in zip(self.input, self.ctrls):
                pymel.parentConstraint(ctrl, inn)
                pymel.connectAttr(ctrl.scaleX, inn.scaleX)
                pymel.connectAttr(ctrl.scaleY, inn.scaleY)
                pymel.connectAttr(ctrl.scaleZ, inn.scaleZ)

        # Connect to parent
        if parent and self.parent is not None:
            pymel.parentConstraint(self.parent, self.grp_anm, maintainOffset=True)
            pymel.scaleConstraint(self.parent, self.grp_anm, maintainOffset=True)

    def unbuild(self):
        super(FK, self).unbuild()

        self.ctrls = None


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

    def build(self, *args, **kwargs):
        super(AdditiveFK, self).build(*args, **kwargs)

        # TODO: Support multiple additive ctrls
        ctrl_add = CtrlFkAdd()
        ctrl_add.build()
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
