import pymel.core as pymel
from classNameMap import NameMap
from classRigCtrl import RigCtrl
from classRigPart import RigPart

class CtrlFk(RigCtrl):
    def build(self, *args, **kwargs):
        super(CtrlFk, self).build(*args, **kwargs)
        make = self.node.getShape().create.inputs()[0]
        make.radius.set(5)
        make.degree.set(1)
        make.sections.set(6)
        return self.node

class FK(RigPart):
    def __init__(self, *args, **kwargs):
        super(FK, self).__init__(*args, **kwargs)
        self.ctrls = []

    def build(self, constraint=True, *args, **kwargs):
        super(FK, self).build(create_grp_rig=False, *args, **kwargs)

        # Create ctrl chain
        self.ctrls = []
        for input in self.input:
            #ctrl_name = self._namemap_anm.Serialize('fk')
            ctrl_name = NameMap(input).Serialize('fk', _sType='anm')
            ctrl = CtrlFk(name=ctrl_name, create=True)
            ctrl.offset.setMatrix(input.getMatrix(worldSpace=True))
            self.ctrls.append(ctrl)

        self.ctrls[0].setParent(self.grp_anm)
        for i in range(1, len(self.ctrls)):
            self.ctrls[i].setParent(self.ctrls[i - 1])

        # Connect jnt -> anm
        if constraint is True:
            for input, ctrl in zip(self.input, self.ctrls):
                pymel.parentConstraint(ctrl, input)
                pymel.connectAttr(ctrl.s, input.s)

        # Connect to parent
        if self._oParent is not None:
            pymel.parentConstraint(self._oParent, self.grp_anm, maintainOffset=True)


    def unbuild(self, *args, **kwargs):
        super(FK, self).unbuild(*args, **kwargs)

        self.ctrls = None
