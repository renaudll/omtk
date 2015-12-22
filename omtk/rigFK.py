import pymel.core as pymel
from className import Name
from classCtrl import BaseCtrl
from classModule import Module

class CtrlFk(BaseCtrl):
    def build(self, *args, **kwargs):
        super(CtrlFk, self).build(*args, **kwargs)
        make = self.node.getShape().create.inputs()[0]
        make.radius.set(5)
        make.degree.set(1)
        make.sections.set(6)
        return self.node

class FK(Module):
    def __init__(self, *args, **kwargs):
        super(FK, self).__init__(*args, **kwargs)
        self.ctrls = []

    def build(self, constraint=True, *args, **kwargs):
        super(FK, self).build(create_grp_rig=False, *args, **kwargs)

        # Create ctrl chain
        self.ctrls = []
        for input in self.input:
            ctrl_name = self.name_anm.resolve('fk')
            ctrl = CtrlFk(name=ctrl_name, create=True)
            ctrl.offset.setMatrix(input.getMatrix(worldSpace=True))
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
        if self.parent is not None:
            pymel.parentConstraint(self.parent, self.grp_anm, maintainOffset=True)
            pymel.scaleConstraint(self.parent, self.grp_anm, maintainOffset=True)


    def unbuild(self, *args, **kwargs):
        super(FK, self).unbuild(*args, **kwargs)

        self.ctrls = None
