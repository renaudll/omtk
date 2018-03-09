"""
Base classes and utility functions to handle unit-testing.
"""
import datetime
import os
import sys
import unittest
from contextlib import contextmanager

import pymel.core as pymel
from maya import cmds
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


#
# Decorators
#


def open_scene(path_local):
    def deco_open(f):
        def f_open(*args, **kwargs):
            m_path_local = path_local  # make mutable

            path = os.path.abspath(os.path.join(os.path.dirname(sys.modules[f.__module__].__file__), m_path_local))
            if not os.path.exists(path):
                raise Exception("File does not exist on disk! {0}".format(path))

            cmds.file(path, open=True, f=True)
            return f(*args, **kwargs)

        return f_open

    return deco_open


def save_on_assert():
    """
    Backup the current scene if an exception is raise. Let the exception propagate afteward.
    """

    def deco(f):
        try:
            f()
        except Exception:
            current_path = cmds.file(q=True, sn=True)
            if current_path:
                dirname = os.path.dirname(current_path)
                basename = os.path.basename(current_path)
                filename, ext = os.path.splitext(basename)

                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
                destination_path = os.path.join(dirname, '{}_{}{}'.format(filename, timestamp, ext))
                print("Saving scene to {}".format(destination_path))
                cmds.file(rename=destination_path)
                cmds.file(save=True, type='mayaAscii')
            raise

    return deco


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
            raise Exception("row #{} {} != {} (dot product {} > epsilon {})".format(i, a_axis, b_axis, diff, r_epsilon))
    # Compare position
    distance = a_pos.distanceTo(b_pos)
    if distance > t_epsilon:
        raise Exception("row #4 {} != {} (distance {} > epsilon {})".format(a_pos, b_pos, distance, t_epsilon))


class TestCase(unittest.TestCase):
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

    def _test_unbuild_rig(self, rig, test_shapes=True):
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
        :return:
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
    def verified_offset(self, objs, offset_tm, pivot_tm=None, **kwargs):
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
            if pivot_tm:
                desired_tm = old_tm * pivot_tm.inverse() * offset_tm * pivot_tm
            else:
                desired_tm = old_tm * offset_tm
            try:
                assertMatrixAlmostEqual(new_tm, desired_tm, **kwargs)
            except Exception, e:
                raise Exception("Invalid transform for {}. {}".format(obj, e))

    def validate_built_rig(self, rig, test_translate=True, test_translate_value=pymel.datatypes.Vector(1, 0, 0),
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
            with self.verified_offset(objs, offset_tm, multiplier=test_translate_value.length()):
                rig.grp_anm.t.set(test_translate_value)
            rig.grp_anm.t.set(0, 0, 0)

        if test_rotate:
            print("Validating rotate...")
            offset_tms_by_rot = (
                ((90, 90, 90),
                 pymel.datatypes.Matrix(
                     0.0, 0.0, -1.0, 0.0,
                     0.0, 1.0, 0.0, 0.0,
                     1.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 1.0
                 )),
                ((180, 0, 0),
                 pymel.datatypes.Matrix(
                     1.0, 0.0, 0.0, 0.0,
                     0.0, -1.0, 0.0, 0.0,
                     0.0, -0.0, -1.0, 0.0,
                     0.0, 0.0, 0.0, 1.0
                 )),
                ((0, 180, 0),
                 pymel.datatypes.Matrix(
                     -1.0, 0.0, -0.0, 0.0,
                     0.0, 1.0, 0.0, 0.0,
                     0.0, 0.0, -1.0, 0.0,
                     0.0, 0.0, 0.0, 1.0
                 )),
                ((0, 0, 180),
                 pymel.datatypes.Matrix(
                     -1.0, 0.0, 0.0, 0.0,
                     -0.0, -1.0, 0.0, 0.0,
                     0.0, 0.0, 1.0, 0.0,
                     0.0, 0.0, 0.0, 1.0
                 )),
            )
            for rot, offset_tm in offset_tms_by_rot:
                with self.verified_offset(objs, offset_tm):
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
            with self.verified_offset(objs, scale_tm, multiplier=test_scale_value):
                rig.grp_anm.globalScale.set(test_scale_value)
            rig.grp_anm.globalScale.set(1.0)


# todo: move this to omtk_test
def _node_to_json(g, n):
    # type: (NodeGraphModel, NodeGraphNodeModel) -> dict
    return {
        # 'name': n.get_name(),
        'ports': [p.get_name() for p in sorted(g.get_node_ports(n))],
    }


# todo: move this to omtk_test
def _graph_to_json(g):
    # type: (NodeGraphModel) -> dict
    return {n.get_name(): _node_to_json(g, n) for n in g.get_nodes()}


# todo: move this to omtk_test
def _get_graph_node_names(g):
    return [n.get_name() for n in g.get_nodes()]


def _get_graph_connections_json(g):
    # type: (NodeGraphModel) -> List[Dict]
    return [(c.get_source().get_path(), c.get_destination().get_path()) for c in g.get_connections()]


class NodeGraphTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super(NodeGraphTestCase, self).__init__(*args, **kwargs)
        self.model = None

    def setUp(self):
        from omtk.qt_widgets.nodegraph import NodeGraphRegistry, NodeGraphModel, GraphFilterProxyModel, NodeGraphController
        self.maxDiff = None
        self.registry = NodeGraphRegistry()
        source_model = NodeGraphModel()
        self.model = GraphFilterProxyModel(model=source_model)
        self.ctrl = NodeGraphController(model=self.model)
        cmds.file(new=True, force=True)

        # Validate the graph is empty
        self.assertEqual(0, len(self.model.get_nodes()))
        self.assertEqual(0, len(self.model.get_ports()))

    def assertGraphNodeCountEqual(self, expected):
        actual = len(self.model.get_nodes())
        self.assertEqual(expected, actual)

    def assertGraphPortCountEqual(self, expected):
        actual = len(self.model.get_ports())
        self.assertEqual(expected, actual)

    def assertGraphConnectionCountEqual(self, expected):
        actual = len(self.model.get_connections())
        self.assertEqual(expected, actual)

    def assertGraphNodeNamesEqual(self, expected):
        actual = _get_graph_node_names(self.model)
        self.assertSetEqual(set(expected), set(actual))

    def assetGraphConnectionsEqual(self, expected):
        actual = _get_graph_connections_json(self.model)
        actual = set(actual)
        expected = set(expected)
        self.assertEqual(expected, actual)

    # todo: move this to omtk_test.NodeGraphTestCase
    def _graph_to_json(self, g):
        # type: (NodeGraphModel) -> dict
        return {n.get_name(): _node_to_json(g, n) for n in g.get_nodes()}
