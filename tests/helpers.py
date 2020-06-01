"""
Helper methods for easier testing.
"""
import os
import json
import sys
import tempfile
from contextlib import contextmanager

from maya import cmds
import pymel.core as pymel
from pymel.core.datatypes import Matrix

from omtk.vendor import libSerialization


def _get_holded_shapes():
    """
    :return: The numbers of shapes connected to anm ctrls in the whole scene.
    """
    shapes = []
    for net in libSerialization.get_networks_from_class("BaseCtrl"):
        if net.hasAttr("shapes"):
            shapes.extend(net.shapes.inputs())
    return shapes


def open_scene(path_local):
    def deco_open(f):
        def f_open(*args, **kwargs):
            m_path_local = path_local  # make mutable

            path = os.path.abspath(
                os.path.join(
                    os.path.dirname(sys.modules[f.__module__].__file__), m_path_local
                )
            )
            if not os.path.exists(path):
                raise Exception("File does not exist on disk! {0}".format(path))

            cmds.file(path, open=True, f=True)
            return f(*args, **kwargs)

        return f_open

    return deco_open


def assertMatrixAlmostEqual(a, b, r_epsilon=0.01, t_epsilon=0.1, multiplier=1.0):
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
            raise AssertionError(
                "%s != %s (dot product %s > epsilon %s)"
                % (a_axis, b_axis, diff, r_epsilon)
            )
    # Compare position
    distance = a_pos.distanceTo(b_pos)
    if distance > t_epsilon:
        raise AssertionError(
            "Position %s != %s (distance %s > epsilon %s)"
            % (a_pos, b_pos, distance, t_epsilon)
        )


@contextmanager
def verified_offset(objs, offset_tm, **kwargs):
    """
    Context that store the world matrix of provided object.
    An offset matrix is also provided that will be used to determine the desired world matrix of the objects.
    If when leaving the context the matrices don't match, an Exeption is raised.
    Use this function to test for scaling issue, flipping and double transformation.
    :param objs:
    :param offset_tm:
    :param kwargs:
    """
    # Store the base matrices
    old_tms = [obj.getMatrix(worldSpace=True) for obj in objs]
    yield True
    # Verify the matrices matches
    for obj, old_tm in zip(objs, old_tms):
        new_tm = obj.getMatrix(worldSpace=True)
        desired_tm = old_tm * offset_tm
        try:
            assertMatrixAlmostEqual(new_tm, desired_tm, **kwargs)
        except Exception as error:
            raise Exception("Invalid transform for %s. %s" % (obj, error))


def assert_match_pose(data, dump=True):
    """
    :param data: A dict of matrix by name
    :type data: dict[str, pymel.datatypes.Matrix]
    """
    try:
        for obj_name, expected in data.items():
            if not cmds.objExists(obj_name):
                raise AssertionError("Transform %r don't exist" % obj_name)
            obj = pymel.PyNode(obj_name)
            actual = obj.getMatrix(worldSpace=True)
            try:
                assertMatrixAlmostEqual(actual, expected)
            except AssertionError as error:
                raise AssertionError(
                    "Invalid transform for %s: %s." % (obj_name, error)
                )
    except AssertionError as error:
        if not dump:
            raise

        # Save expected transforms visually
        for obj_name, expected in data.items():
            ref = pymel.spaceLocator(name="EXPECTED_%s" % obj_name)
            ref.setMatrix(expected)
            pymel.color(
                ref, rgb=(1, 0, 0)
            )  # TODO: Different color depending on the state

        # Save the scene in it's current state for further debuggin
        path = tempfile.mktemp(suffix=".ma")
        cmds.file(rename=path)
        cmds.file(save=True, type="mayaAscii")
        raise AssertionError("%s Scene was dumped here: %r" % (error, path))


def assert_match_pose_from_file(path):
    """
    :param str path: Path to a saved pose
    :raises AssertionError: If the pose don't match
    """
    with open(path) as fp:
        data = json.load(fp)
        data = {key: Matrix(val) for key, val in data.items()}
    assert_match_pose(data)


def validate_built_rig(
    rig,
    test_translate=True,
    translate=pymel.datatypes.Vector(1, 0, 0),
    test_rotate=True,
    test_scale=True,
    test_scale_value=2.0,
):
    """
    Build a specific rig and verify the following:
    - Is the rig scaling correctly?

    :param rig: The rig to scale.
    :param test_translate: If True, the rig will be verified for translation.
    :param translate: The value to use when testing the translation.
    :param test_scale: If True, the rig will be verified for scaling.
    :param test_scale_value: The value to use when testing the scale.
    """
    influences = rig.get_influences(key=lambda x: isinstance(x, pymel.nodetypes.Joint))
    ctrls = rig.get_ctrls()
    objs = influences + ctrls

    # Ensure the rig translate correctly.
    if test_translate:
        print("Validating translate...")
        offset_tm = pymel.datatypes.Matrix(
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [translate.x, translate.y, translate.z, 1.0,],
        )
        with verified_offset(objs, offset_tm, multiplier=translate.length()):
            rig.grp_anm.t.set(translate)
        rig.grp_anm.t.set(0, 0, 0)

    if test_rotate:
        print("Validating rotate...")
        offset_tms_by_rot = (
            (
                (90, 90, 90),
                pymel.datatypes.Matrix(
                    [0.0, 0.0, -1.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                ),
            ),
            (
                (180, 0, 0),
                pymel.datatypes.Matrix(
                    [1.0, 0.0, 0.0, 0.0],
                    [0.0, -1.0, 0.0, 0.0],
                    [0.0, -0.0, -1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                ),
            ),
            (
                (0, 180, 0),
                pymel.datatypes.Matrix(
                    [-1.0, 0.0, -0.0, 0.0],
                    [0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, -1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                ),
            ),
            (
                (0, 0, 180),
                pymel.datatypes.Matrix(
                    [-1.0, 0.0, 0.0, 0.0],
                    [-0.0, -1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                ),
            ),
        )
        for rot, offset_tm in offset_tms_by_rot:
            with verified_offset(objs, offset_tm):
                rig.grp_anm.r.set(rot)
            rig.grp_anm.r.set(0, 0, 0)

    # Ensure we the rig scale correctly.
    if test_scale:
        print("Validating scale...")
        m = test_scale_value
        scale_tm = pymel.datatypes.Matrix(
            [m, 0, 0, 0], [0, m, 0, 0], [0, 0, m, 0], [0, 0, 0, 1]
        )
        with verified_offset(objs, scale_tm, multiplier=test_scale_value):
            rig.grp_anm.globalScale.set(test_scale_value)
        rig.grp_anm.globalScale.set(1.0)


def test_build_rig(rig, **kwargs):
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
    validate_built_rig(rig, **kwargs)


def test_unbuild_rig(rig):
    """
    Unbuild a specific rig and verify the following:
    - Do we have extra or missing ctrl shapes after building?

    :param rig: The rig to unbuild.
    """
    num_holder_shapes_before = len(_get_holded_shapes())
    rig.unbuild()
    num_holder_shapes_after = len(_get_holded_shapes())
    assert num_holder_shapes_before == num_holder_shapes_after


def build_unbuild_build_all(**kwargs):
    """
    Build/Unbuild/Build all the rig in the scene and check for the following errors:
    - Is there junk shapes remaining? This could be a sign that we didn't cleanup correctly.

    :return:
    """
    import omtk

    num_holder_shapes_before = len(_get_holded_shapes())

    rigs = omtk.find()
    for rig in rigs:
        test_build_rig(rig, **kwargs)
        test_unbuild_rig(rig)
        test_build_rig(rig, **kwargs)

    # Ensure no shapes are left after a rebuild.
    num_holder_shapes_after = len(_get_holded_shapes())
    assert num_holder_shapes_before == num_holder_shapes_after
