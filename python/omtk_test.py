"""
Base classes and utility functions to handle unit-testing.
"""
import unittest
from contextlib import contextmanager

import pymel.core as pymel
from maya import cmds
from omtk.vendor import libSerialization
from omtk.nodegraph import NodeGraphRegistry, GraphModel, GraphFilterProxyModel, NodeGraphController


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

def assertMatrixAlmostEqual(a, b, r_epsilon=0.01, t_epsilon=0.1, multiplier=1.0):
    """
    Raise an exception if two provided pymel.datatypes.Matrix are different depending of the provided parameters.

    :param pymel.datatypes.Matrix a: A matrix
    :param pymel.datatypes.Matrix b: Another matrix
    :param float r_epsilon: How much drift we accept in rotation.
    :param float t_epsilon: How much drift we accept in translation (in cm).
    :param float multiplier: How much scaling have been applied. This will affect t_epsilon and r_epsilon.
    """
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
        :param Dict[str,object] kwargs: Any additional arguments will be fowarded to assetMatrixAlmostEqual.
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
            with self.context_assertMatrixOffset(objs, offset_tm, multiplier=test_translate_value.length()):
                rig.grp_anm.t.set(test_translate_value)
            rig.grp_anm.t.set(0, 0, 0)

        if test_rotate:
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



class NodeGraphTestCase(TestCase):
    """
    Base TestCase for testing the interaction between:
    - NodeGraphView
    - NodeGraphRegistry
    - NodeGraphModel
    """
    def __init__(self, *args, **kwargs):
        super(NodeGraphTestCase, self).__init__(*args, **kwargs)
        self.model = None

    def setUp(self):

        cmds.file(new=True, force=True)
        self.maxDiff = None
        self.registry = NodeGraphRegistry()
        source_model = GraphModel(self.registry)
        self.model = GraphFilterProxyModel(model=source_model)
        self.ctrl = NodeGraphController(self.registry, model=self.model)

        # Validate the graph is empty
        self.assertEqual(0, len(self.model.get_nodes()))
        self.assertEqual(0, len(self.model.get_ports()))

    def assertGraphNodeCountEqual(self, expected):
        """
        Ensure that the number of nodes in the graph match the provided count.

        :param int expected: The expected node counts in the graph.
        :raise Exception: If the number of nodes in the graph is incorrect.
        """
        actual = len(self.model.get_nodes())
        self.assertEqual(expected, actual)

    def assertGraphRegistryNodeCountEqual(self, expected):
        """
        Ensure that the number of registered nodes match the provided count.

        :param int expected: The expected node count in the registry.
        :raise Exception: If the number of nodes in the registry is incorrect.

        """
        actual = len(self.registry._nodes)
        self.assertEqual(expected, actual)

    def assertGraphPortCountEqual(self, expected):
        """
        Ensure that the number of ports visible in the graph match the expected count.

        :param int expected: The expected port count in the graph.
        :raise Exception: If the number of ports visible in the graph is incorrect.
        """
        actual = len(self.model.get_ports())
        self.assertEqual(expected, actual)

    def assertGraphNodePortNamesEqual(self, node, expected):
        """
        Ensure that all the current ports in a provided nodes match.

        :param omtk.nodegraph.NodeModel node: The node to retreive the port from.
        :param List[str] expected: A sorted list of names to match
        :raise Exception: If the name of any port don't match the expected value.
        """
        ports = self.model.get_node_ports(node)
        actual = sorted(port.get_name() for port in ports)
        self.assertEqual(expected, actual)

    def assertGraphConnectionCountEqual(self, expected):
        """
        Validate the the number of visible connections in the graph.

        :param int expected: The expected number of connections in the graph.
        :raise Exception: If the number of connections in the graph is unexpected.
        """
        actual = len(self.model.get_connections())
        self.assertEqual(expected, actual)

    def assertGraphNodeNamesEqual(self, expected):
        """
        Validate the name of all the graph nodes.

        :param List[str] expected: A sorted list of all the graph node names.
        :raise Exception: If any node name don't match the expected value.
        """
        nodes = self.model.get_nodes()
        actual = sorted([node.get_name() for node in nodes])
        self.assertSetEqual(set(expected), set(actual))

    def assertGraphConnectionsEqual(self, expected):
        """
        Validate the number of connections in the graph.
        :param List[Tuple(str, str)] expected: A list of 2-tuple describing connection in the graph.
        """
        connections = self.model.get_connections()
        actual = [connection.dump() for connection in connections]

        # Using set for comparison as we don't want the ordering to be taken in account.
        self.assertEqual(set(expected), set(actual))
