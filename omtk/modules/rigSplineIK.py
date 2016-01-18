import math
import pymel.core as pymel
from omtk.classModule import Module
from omtk.libs import libRigging, libPymel, libPython, libFormula

# Todo: Support more complex IK limbs (ex: 2 knees)
class SplineIK(Module):
    def __init__(self, *args, **kwargs):
        super(SplineIK, self).__init__(*args, **kwargs)
        self.bStretch = True
        self.iCtrlIndex = 2
        self.ikEffector = None
        self.ikHandle = None


    def build(self, rig, stretch=True, squash=False, *args, **kwargs):
        # TODO: Use self.chain_jnt
        self._joints = [input for input in self.input if libPymel.isinstance_of_transform(input, pymel.nodetypes.Joint)]
        self._curves = [input for input in self.input if libPymel.isinstance_of_shape(input, pymel.nodetypes.CurveShape)]

        if len(self._joints) < 2:
            raise Exception("Can't build SplineIK. Expected at least two joints, got {0}".format(self._joints))
        if len(self._curves) < 1:
            raise Exception("Can't build SplineIK. Expected at least one nurbsCurve, got {0}".format(self._curves))

        super(SplineIK, self).build(rig, segmentScaleCompensate=True, *args, **kwargs)

        nomenclature_rig = self.get_nomenclature_rig(rig)

        # todo: handle multiple curves?
        curve = next(iter(self._curves), None)
        curve_shape = next((shape for shape in curve.getShapes() if isinstance(shape, pymel.nodetypes.NurbsCurve)), None)

        # Create ik solver
        solver_name = nomenclature_rig.resolve('ikEffector')
        self.ikHandle, self.ikEffector = pymel.ikHandle(
            solver="ikSplineSolver",
            curve=curve,
            startJoint=self._joints[0],
            endEffector=self._joints[-1],
            createCurve=False,
            name=solver_name,
            parentCurve=False,
            snapCurve=False)
        self.ikHandle.setParent(self.grp_rig)

        # Create stretch
        # Todo: use shape instead of transform as curve input?
        if stretch:
            stretch_attr = libRigging.create_strech_attr_from_curve(curve_shape)
            for jnt in self._joints:
                pymel.connectAttr(stretch_attr, jnt.sx, force=True)

            # Create squash
            if squash:
                num_joints = len(self._joints)
                squash_attrs = libRigging.create_squash_atts(stretch_attr, num_joints)
                # Todo: Find correct axis orient
                for jnt, squash in zip(self._joints, squash_attrs):
                    pymel.connectAttr(squash, jnt.sy, force=True)
                    pymel.connectAttr(squash, jnt.sz, force=True)


    def unbuild(self, **kwargs):
        # hack: the ikEffector is parented to the bone chain and need to be deleted manually
        if libPymel.is_valid_PyNode(self.ikEffector):
            pymel.delete(self.ikEffector)

        super(SplineIK, self).unbuild(**kwargs)
