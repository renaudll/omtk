from contextlib import contextmanager

from omtk.vendor import libSerialization


def _get_holded_shapes():
    """
    :return: The numbers of shapes connected to anm ctrls in the whole scene.
    """
    shapes = []
    for net in libSerialization.get_networks_from_class('BaseCtrl'):
        if net.hasAttr('shapes'):
            shapes.extend(net.shapes.inputs())
    return shapes


def assertMatrixAlmostEqual(a, b, r_epsilon=0.01, t_epsilon=0.1, multiplier=1.0):
    """
    Raise an exception if two provided pymel.datatypes.Matrix are different depending of the provided parameters.

    :param pymel.datatypes.Matrix a: A matrix
    :param pymel.datatypes.Matrix b: Another matrix
    :param float r_epsilon: How much drift we accept in rotation.
    :param float t_epsilon: How much drift we accept in translation (in cm).
    :param float multiplier: How much scaling have been applied. This will affect t_epsilon and r_epsilon.
    """
    import pymel.core as pymel
    # Adjust epsilon depending of the scale
    t_epsilon *= multiplier

    a_x, a_y, a_z, a_pos = a.data
    b_x, b_y, b_z, b_pos = b.data

    # Compare x, y and z axis.
    for i in range(3):
        a_axis = pymel.datatypes.Vector(a.data[i][0], a.data[i][1], a.data[i][2])
        b_axis = pymel.datatypes.Vector(b.data[i][0], b.data[i][1], b.data[i][2])
        a_axis.normalize()
        b_axis.normalize()
        diff = abs(1.0 - a_axis.dot(b_axis))
        if diff > r_epsilon:
            raise Exception("row #{} {} != {} (dot product {} > epsilon {})".format(i, a_axis, b_axis, diff, r_epsilon))
    # Compare position
    distance = a_pos.distanceTo(b_pos)
    if distance > t_epsilon:
        raise Exception("row #4 {} != {} (distance {} > epsilon {})".format(a_pos, b_pos, distance, t_epsilon))


class NodeGraphMayaRigTestCase():
    def _test_unbuild_rig(self, rig):
        """
        Unbuild a specific rig and verify the following:
        - Do we have extra or missing ctrl shapes after building?

        :param rig: The rig to unbuild.
        :param test_shapes: If True, the number of shape before and after will be checked.
        """
        num_holder_shapes_before = len(_get_holded_shapes())
        rig.unbuild()
        num_holder_shapes_after = len(_get_holded_shapes())
        self.assertEqual(num_holder_shapes_before, num_holder_shapes_after)

    def _build_unbuild_build_all(self, **kwargs):
        """
        Build/Unbuild/Build all the rig in the scene and check for the following errors:
        - Is there junk shapes remaining? This could be a sign that we didn't cleanup correctly.
        """
        import omtk

        num_holder_shapes_before = len(_get_holded_shapes())

        rigs = omtk.find()
        for rig in rigs:
            self._test_build_rig(rig, **kwargs)
            self._test_unbuild_rig(rig)
            self._test_build_rig(rig, **kwargs)

        # Ensure no shapes are left after a rebuild.
        num_holder_shapes_after = len(_get_holded_shapes())
        self.assertEqual(num_holder_shapes_before, num_holder_shapes_after)

    @contextmanager
    def context_assertMatrixOffset(self, objs, offset_tm, pivot_tm=None, **kwargs):
        """
        Context that store the world matrix of provided object.
        An offset matrix is also provided that will be used to determine the desired world matrix of the objects.
        If when leaving the context the matrices don't match, an Exeption is raised.
        Use this function to test for scaling issue, flipping and double transformation.

        :param List[pymel.PyNode] objs:
        :param pymel.datatypes.Matrix offset_tm:
        :param Dict[str,object] kwargs: Any additional arguments will be forwarded to assetMatrixAlmostEqual.
        """

        # Store the base matrices
        old_tms = [obj.getMatrix(worldSpace=True) for obj in objs]
        yield True
        # Verify the matrices matches
        for obj, old_tm in zip(objs, old_tms):
            new_tm = obj.getMatrix(worldSpace=True)
            if pivot_tm:
                desired_tm = old_tm * pivot_tm.inverse() * offset_tm * pivot_tm
            else:
                desired_tm = old_tm * offset_tm
            try:
                assertMatrixAlmostEqual(new_tm, desired_tm, **kwargs)
            except Exception, e:
                raise Exception("Invalid transform for {}. {}".format(obj, e))

    def validate_built_rig(self, rig, test_translate=True, test_translate_value=None,
                           test_rotate=True, test_scale=True, test_scale_value=2.0):
        """
        Build a specific rig and verify the following:
        - Is the rig scaling correctly?

        :param rig: The rig to scale.
        :param test_translate: If True, the rig will be verified for translation.
        :param test_translate_value: The value to use when testing the translation.
        :param test_scale: If True, the rig will be verified for scaling.
        :param test_scale_value: The value to use when testing the scale.
        """
        import pymel.core as pymel

        if test_translate_value is None:
            test_translate_value = pymel.datatypes.Vector(1, 0, 0)

        influences = rig.get_influences(key=lambda x: isinstance(x, pymel.nodetypes.Joint))
        ctrls = rig.get_ctrls()
        objs = influences + ctrls

        # Ensure the rig translate correctly.
        if test_translate:
            print("Validating translate...")
            offset_tm = pymel.datatypes.Matrix(
                1, 0, 0, 0,
                0, 1, 0, 0,
                0, 0, 1, 0,
                test_translate_value.x, test_translate_value.y, test_translate_value.z, 1.0
            )
            with self.context_assertMatrixOffset(objs, offset_tm, multiplier=test_translate_value.length()):
                rig.grp_anm.t.set(test_translate_value)
            rig.grp_anm.t.set(0, 0, 0)

        if test_rotate:
            offset_tms_by_rot = (
                (
                    (90, 90, 90),
                    pymel.datatypes.Matrix(  # -z, y, x
                        0.0, 0.0, -1.0, 0.0,
                        0.0, 1.0, 0.0, 0.0,
                        1.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 1.0
                    )
                ),
                (
                    (180, 0, 0),
                    pymel.datatypes.Matrix(  # x, -y, -z
                        1.0, 0.0, 0.0, 0.0,
                        0.0, -1.0, 0.0, 0.0,
                        0.0, -0.0, -1.0, 0.0,
                        0.0, 0.0, 0.0, 1.0
                    )
                ),
                (
                    (0, 180, 0),
                    pymel.datatypes.Matrix(  # -x, y ,-z
                        -1.0, 0.0, -0.0, 0.0,
                        0.0, 1.0, 0.0, 0.0,
                        0.0, 0.0, -1.0, 0.0,
                        0.0, 0.0, 0.0, 1.0
                    )
                ),
                (
                    (0, 0, 180),
                    pymel.datatypes.Matrix(  # -x, -y, z
                        -1.0, 0.0, 0.0, 0.0,
                        -0.0, -1.0, 0.0, 0.0,
                        0.0, 0.0, 1.0, 0.0,
                        0.0, 0.0, 0.0, 1.0
                    )
                ),
            )

            for rot, offset_tm in offset_tms_by_rot:
                with self.context_assertMatrixOffset(objs, offset_tm):
                    rig.grp_anm.r.set(rot)
                rig.grp_anm.r.set(0, 0, 0)

        # Ensure we the rig scale correctly.
        if test_scale:
            print("Validating scale...")
            m = test_scale_value
            scale_tm = pymel.datatypes.Matrix(
                m, 0, 0, 0,
                0, m, 0, 0,
                0, 0, m, 0,
                0, 0, 0, 1
            )
            with self.context_assertMatrixOffset(objs, scale_tm, multiplier=test_scale_value):
                rig.grp_anm.globalScale.set(test_scale_value)
            rig.grp_anm.globalScale.set(1.0)

    def _test_build_rig(self, rig, **kwargs):
        """
        Build a specific rig and verify the following:
        - Is the rig scaling correctly?

        :param rig: The rig to scale.
        :param test_translate: If True, the rig will be verified for translation.
        :param test_translate_value: The value to use when testing the translation.
        :param test_scale: If True, the rig will be verified for scaling.
        :param test_scale_value: The value to use when testing the scale.
        """
        rig.build(strict=True)
        self.validate_built_rig(rig, **kwargs)
