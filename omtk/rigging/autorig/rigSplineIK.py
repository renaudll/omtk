import math
import pymel.core as pymel
from classRigCtrl import RigCtrl
from classRigPart import RigPart
from omtk.libs import libRigging, libAttr, libPymel, libPython
from omtk.rigging import formulaParser

# Todo: Support more complex IK limbs (ex: 2 knees)
class SplineIK(RigPart):
    def __init__(self, *args, **kwargs):
        super(SplineIK, self).__init__(*args, **kwargs)
        self.bStretch = True
        self.iCtrlIndex = 2

    def _post_setattr_inputs(self):
        super(SplineIK, self)._post_setattr_inputs()
        self._joints = [input for input in self.inputs if libPymel.isinstance_of_transform(input)]
        self._curves = [input for input in self.inputs if libPymel.isinstance_of_shape(input, pymel.nodetypes.CurveShape)]
        assert(len(self._joints) > 0)
        assert(len(self._curves) > 0)

    def build(self,  *args, **kwargs):
        super(SplineIK, self).build(*args, **kwargs)

        # create splineik effector
        # todo: search for additional options
        name_kEffector = self._pNameMapRig.Serialize('ikEffector')
        self.ikEffector = pymel.ikHandle(
            solver="ikSplineSolver",
            createCurve=False,
            freezeJoints=True,
            name=name_kEffector,
            parentCurve=False,
            snapCurve=False)

        # Create stretch
        # Todo: use shape instead of transform as curve input?
        curveShape = next((shape for shape in self._curves[0] if isinstance(shape, pymel.nodetypes.NurbsCurve)), None)
        self.stretch_att = libRigging.CreateUtilityNode('curveInfo', inputCurve=curveShape).arcLength

        # Create squash
        num_joints = len(self._joints)
        squash_atts = [formulaParser.parse("1 / (e^(x^2))", e=math.e, x=stretch) for i in libPython.frange(0, 1, 1.0/num_joints)]

        # Connect stretch/squash
        # Todo: Find correct axis orient
        for jnt, squash in zip(self._joints, squash_atts):
            pymel.connectAttr(self.stretch_att, jnt.sx)
            pymel.connectAttr(squash, jnt.sy)
            pymel.connectAttr(squash, jnt.sy)

        # Todo: Connect to parent?
