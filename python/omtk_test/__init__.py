"""
Base classes and utility functions to handle unit-testing.
"""
import unittest

from omtk.nodegraph import GraphModel, GraphFilterProxyModel, NodeGraphController
from omtk.nodegraph.registry.base import NodeGraphRegistry


#
# Decorators
#

class TestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.maxDiff = None

        super(TestCase, self).__init__(*args, **kwargs)

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


class NodeGraphBaseTestCase(TestCase):
    """
    Base TestCase for testing the interaction between:
    - NodeGraphView
    - NodeGraphRegistry
    - NodeGraphModel
    """
    _cls_registry = NodeGraphRegistry

    def __init__(self, *args, **kwargs):
        super(NodeGraphBaseTestCase, self).__init__(*args, **kwargs)
        self.model = None

    def setUp(self):
        from maya import cmds
        cmds.file(new=True, force=True)
        self.maxDiff = None
        self.registry = self._cls_registry()
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

    def assertGraphEquals(self, expected):
        graph = self.model.dump()
        self.assertEqual(expected, graph)


