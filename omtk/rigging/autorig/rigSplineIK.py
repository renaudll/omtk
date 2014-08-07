import math
import pymel.core as pymel
from classRigPart import RigPart
from omtk.libs import libRigging, libPymel, libPython, libFormula

# Todo: Support more complex IK limbs (ex: 2 knees)
class SplineIK(RigPart):
    def __init__(self, *args, **kwargs):
        super(SplineIK, self).__init__(*args, **kwargs)
        self.bStretch = True
        self.iCtrlIndex = 2

    def _post_setattr_inputs(self):
        super(SplineIK, self)._post_setattr_inputs()
        self._joints = [input for input in self.input if libPymel.isinstance_of_transform(input, pymel.nodetypes.Joint)]
        self._curves = [input for input in self.input if libPymel.isinstance_of_shape(input, pymel.nodetypes.CurveShape)]

    def build(self,  *args, **kwargs):
        assert(len(self._joints) > 1) # need at least 2 jnts
        assert(len(self._curves) > 0)

        super(SplineIK, self).build(*args, **kwargs)

        # todo: handle multiple curves?
        curve = self._curves[0]
        curveShape = next((shape for shape in curve.getShapes() if isinstance(shape, pymel.nodetypes.NurbsCurve)), None)

        # create splineik effector
        # todo: search for additional options
        name_kEffector = self._pNameMapRig.Serialize('ikEffector')
        self.ikEffector = pymel.ikHandle(
            solver="ikSplineSolver",
            curve=curve,
            startJoint=self._joints[0],
            endEffector=self._joints[-1],
            createCurve=False,
            name=name_kEffector,
            parentCurve=False,
            snapCurve=False)

        # Create stretch
        # Todo: use shape instead of transform as curve input?
        curveLength = libRigging.CreateUtilityNode('curveInfo', inputCurve=curveShape.worldSpace).arcLength
        self.stretch_att = libRigging.CreateUtilityNode('multiplyDivide', operation=2, input1X=curveLength, input2X=curveLength.get()).outputX

        # Create squash
        num_joints = len(self._joints)
        squash_atts = [libFormula.parse("1 / (e^(x^2))", e=math.e, x=self.stretch_att) for i in libPython.frange(0, 1, 1.0/num_joints)]

        # Connect stretch/squash
        # Todo: Find correct axis orient
        for jnt, squash in zip(self._joints, squash_atts):
            pymel.connectAttr(self.stretch_att, jnt.sx)
            pymel.connectAttr(squash, jnt.sy)
            pymel.connectAttr(squash, jnt.sz)

        # Todo: Connect to parent?
