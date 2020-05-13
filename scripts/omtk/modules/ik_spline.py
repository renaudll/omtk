"""
Logic for the "SplineIK" module
"""
import pymel.core as pymel

from omtk.core.module import Module
from omtk.libs import libRigging, libPymel


# Todo: Support more complex IK limbs (ex: 2 knees)
class SplineIK(Module):
    """
    Generic ik setup on a spline.
    """

    def __init__(self, *args, **kwargs):
        super(SplineIK, self).__init__(*args, **kwargs)
        self.bStretch = True
        self.iCtrlIndex = 2
        self.ikEffector = None
        self.ikHandle = None

    def build(self, stretch=True, squash=False, *args, **kwargs):
        # TODO: Use self.chain_jnt
        self._joints = [
            input
            for input in self.input
            if libPymel.isinstance_of_transform(input, pymel.nodetypes.Joint)
        ]
        self._curves = [
            input
            for input in self.input
            if libPymel.isinstance_of_shape(input, pymel.nodetypes.CurveShape)
        ]

        if len(self._joints) < 2:
            raise Exception(
                "Can't build SplineIK. Expected at least two joints, got %s"
                % self._joints
            )
        if len(self._curves) < 1:
            raise Exception(
                "Can't build SplineIK. Expected at least one nurbsCurve, got %s"
                % self._curves
            )

        super(SplineIK, self).build(*args, **kwargs)

        nomenclature_rig = self.get_nomenclature_rig()

        # todo: handle multiple curves?
        curve = next(iter(self._curves), None)
        curve_shape = next(
            (
                shape
                for shape in curve.getShapes()
                if isinstance(shape, pymel.nodetypes.NurbsCurve)
            ),
            None,
        )

        # Create ik solver
        handle_name = nomenclature_rig.resolve("ikHandle")
        eff_name = nomenclature_rig.resolve("ikEffector")
        self.ikHandle, self.ikEffector = pymel.ikHandle(
            solver="ikSplineSolver",
            curve=curve,
            startJoint=self._joints[0],
            endEffector=self._joints[-1],
            createCurve=False,
            name=handle_name,
            parentCurve=False,
            snapCurve=False,
        )
        self.ikHandle.setParent(self.grp_rig)
        self.ikEffector.rename(eff_name)

        # Create stretch
        # Todo: use shape instead of transform as curve input?
        if stretch:
            stretch_attr = _create_strech_attr_from_curve(curve_shape)
            for jnt in self._joints:
                pymel.connectAttr(stretch_attr, jnt.sx, force=True)

            # Create squash
            if squash:
                num_joints = len(self._joints)
                squash_attrs = _create_squash_atts(stretch_attr, num_joints)
                # Todo: Find correct axis orient
                for jnt, squash in zip(self._joints, squash_attrs):
                    pymel.connectAttr(squash, jnt.sy, force=True)
                    pymel.connectAttr(squash, jnt.sz, force=True)

    def unbuild(self):
        # hack: the ikEffector is parented to the bone chain and need to be deleted manually
        if libPymel.is_valid_PyNode(self.ikEffector):
            pymel.delete(self.ikEffector)

        super(SplineIK, self).unbuild()


def _create_strech_attr_from_curve(curve_shape):
    curveLength = libRigging.create_utility_node(
        "curveInfo", inputCurve=curve_shape.worldSpace
    ).arcLength
    return libRigging.create_utility_node(
        "multiplyDivide", operation=2, input1X=curveLength, input2X=curveLength.get()
    ).outputX


def _create_squash_atts(attr_stretch, samples):
    """
    Create attributes resolving a curve using the following formula.
    s^(e^(x^2)))
    see: http://www.wolframalpha.com/input/?i=%28x%5E2-1%29*-1
    :param attr_stretch: # The stretch attribute.
    :param samples: Number of samples to resolve.
    """
    if not isinstance(attr_stretch, pymel.Attribute):
        raise IOError(
            "Expected pymel Attribute, got %s (%s)" % (attr_stretch, type(attr_stretch))
        )

    attr_stretch_inv = libRigging.create_utility_node(
        "multiplyDivide", operation=2, input1X=1.0, input2X=attr_stretch
    ).outputX

    return_vals = []
    for i in range(samples):
        pos = float(i) / (samples - 1) * 2.0 - 1.0

        # Blend between no squash and full squash using a bell curve.
        # 0 = Maximum Squash
        # 1 = No Squash
        # see see: http://www.wolframalpha.com/input/?i=%28x%5E2-1%29*-1
        blend = libRigging.create_utility_node(
            "multiplyDivide", operation=3, input1X=pos, input2X=2
        ).outputX
        attr_squash = libRigging.create_utility_node(
            "blendTwoAttr", input=[attr_stretch_inv, 1], attributesBlender=blend
        )

        return_vals.append(attr_squash)
    return return_vals


def register_plugin():
    return SplineIK
