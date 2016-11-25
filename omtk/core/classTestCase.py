import unittest

import pymel.core as pymel

import libSerialization
from . import api as omtk

class TestCase(unittest.TestCase):
    def __get_holded_shapes(self):
        """
        Return the shapes that are in 'limbo' and wait to be used on a re-build.
        """
        shapes = []
        for net in libSerialization.get_networks_from_class('BaseCtrl'):
            if net.hasAttr('shapes'):
                shapes.extend(net.shapes.inputs())
        return shapes

    def assertMatrixAlmostEqual(self, a, b, r_epsilon=0.01, t_epsilon=0.1, multiplier=1.0):
        """
        Compare two pymel.datatypes.Matrix and assert if they are too far away.
        :param a: A pymel.datatypes.Matrix instance.
        :param b: A pymel.datatypes.Matrix instance.
        :param r_epsilon: How much drift we accept in rotation.
        :param t_epsilon: How much drift we accept in translation (in cm).
        :param multiplier: How much scaling have been applied. This will affect t_epsilon and r_epsilon.
        """
        # Apply multiplier on epsilon
        # This is necessary since if we're scaling 10 times, we expect 5 times more imprecision that if we're scaling 2 times.
        t_epsilon *= multiplier
        r_epsilon *= multiplier

        a_x, a_y, a_z, a_pos = a.data
        b_x, b_y, b_z, b_pos = b.data
        # Compare axises
        for axis_a, axis_b in zip((a_x, a_y, a_z), (b_x, b_y, b_z)):
            distance = axis_a.distanceTo(axis_b)
            if distance > r_epsilon:
                raise Exception("{} != {} (distance {} > epsilon {})".format(axis_a, axis_b, distance, r_epsilon))
        # Compare position
        distance = a_pos.distanceTo(b_pos)
        if distance > t_epsilon:
           raise Exception("{} != {} (distance {} > epsilon {})".format(a_pos, b_pos, distance, t_epsilon))

    def _test_unbuilt_rig(self, scale_value=2.0):
        # Ensure a rig exist in the scene.
        rigs = omtk.find()
        self.assertGreater(len(rigs), 0)

        for rig in rigs:
            num_holder_shapes_before = len(self.__get_holded_shapes())
            influences = rig.get_influences(key=lambda x: isinstance(x, pymel.nodetypes.Joint))
            old_influence_tms = [influence.getMatrix(worldSpace=True) for influence in influences]

            rig.build(strict=True)

            # Ensure we the rig scale correctly.
            rig.grp_anm.globalScale.set(scale_value)
            m = scale_value
            scale_tm = pymel.datatypes.Matrix(
                m, 0, 0, 0,
                0, m, 0, 0,
                0, 0, m, 0,
                0, 0, 0, 1
            )
            for influence, old_tm in zip(influences, old_influence_tms):
                new_tm = influence.getMatrix(worldSpace=True)
                desired_tm = old_tm * scale_tm
                try:
                    self.assertMatrixAlmostEqual(new_tm, desired_tm, multiplier=scale_value)
                except Exception, e:
                    raise Exception("Invalid scaling for {}. \nExpected:\n{}\nGot: \n{}\n{}".format(
                        influence, desired_tm, new_tm, e.message
                    ))

            rig.unbuild()
            rig.build(strict=True)

            # Ensure no shapes are left after a rebuild.
            num_holder_shapes_after = len(self.__get_holded_shapes())
            self.assertEqual(num_holder_shapes_before, num_holder_shapes_after)

    def _test_built_rig(self, rig):
        rig.unbuild_all()
        rig.build_all(strict=True)