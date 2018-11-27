"""
Base classes and utility functions to handle unit-testing.
"""
import unittest

from omtk.nodegraph import GraphModel, GraphFilterProxyModel
from omtk.nodegraph.bindings.base import ISession
from omtk.nodegraph.registry.base import NodeGraphRegistry
from omtk.nodegraph.registry.maya_mocked import MockedMayaRegistry
from omtk.nodegraph.registry.maya_mocked import MockedSession
from omtk.vendor.mock_maya.cmds.session import MockedCmdsSession
from omtk.vendor.mock_maya.pymel.session import MockedPymelSession
from omtk.vendor.mock_maya.base.presets import REGISTRY_DEFAULT


class OmtkTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.maxDiff = None

        super(OmtkTestCase, self).__init__(*args, **kwargs)


class NodeGraphBaseTestCase(OmtkTestCase):
    """
    Base OmtkTestCase for testing the interaction between:
    - NodeGraphView
    - NodeGraphRegistry
    - NodeGraphModel
    """
    _cls_session = None
    _cls_registry = NodeGraphRegistry
    _cls_model = GraphModel
    _cls_proxy_model = None
    _cls_controller = None

    def _create_session(self):
        return self._cls_session() if self._cls_session else None

    def setUp(self):
        super(NodeGraphBaseTestCase, self).setUp()

        self._session = self._create_session()
        self._registry = self._cls_registry(session=self.session)
        self.source_model = self._cls_model(registry=self.registry) if self._cls_model else None
        self.model = self._cls_proxy_model(registry=self.registry, model=self.source_model) if self._cls_proxy_model else self.source_model
        self.ctrl = self._cls_controller(registry=self.registry, model=self.model) if self._cls_controller else None

        # By default, expose cmds or pymel mock if needed
        if self._cls_session:
            self.cmds = MockedCmdsSession(session=self.session)
            self.pymel = MockedPymelSession(session=self.session)

        # Validate the graph is empty
        if self.model:
            self.assertEqual(0, len(self.model.get_nodes()))
            self.assertEqual(0, len(self.model.get_ports()))

    @property
    def session(self):
        """
        Getter for the sesion
        :return: The session
        :rtype: ISession
        """
        return self._session

    @property
    def registry(self):
        """
        Getter for the REGISTRY_DEFAULT
        :return: The REGISTRY_DEFAULT
        :rtype omtk.nodegraph.NodeGraphRegistry
        """
        return self._registry

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

        :param int expected: The expected node count in the REGISTRY_DEFAULT.
        :raise Exception: If the number of nodes in the REGISTRY_DEFAULT is incorrect.

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
        # self.assertEqual(len(expected), len(actual))  # in case some item where are duplicated

    def assertGraphConnectionsEqual(self, expected):
        """
        Validate the number of connections in the graph.
        :param List[Tuple(str, str)] expected: A list of 2-tuple describing connection in the graph.
        """
        connections = self.model.get_connections()
        actual = [connection.dump() for connection in connections]

        # Using set for comparison as we don't want the ordering to be taken in account.
        self.assertSetEqual(set(expected), set(actual))
        self.assertEqual(len(expected), len(actual))  # in case some item where are duplicated

    def assertGraphEquals(self, expected):
        graph = self.model.dump()
        self.assertEqual(expected, graph)


class NodeGraphMockedMayaTestCase(NodeGraphBaseTestCase):
    _cls_session = MockedSession
    _cls_session_preset = REGISTRY_DEFAULT  # This one is an object instead of a class???
    _cls_registry = MockedMayaRegistry

    def _create_session(self):
        return self._cls_session(preset=self._session_preset) if self._cls_session else None

    def setUp(self):
        self._session_preset = self._cls_session_preset if self._cls_session_preset else None

        super(NodeGraphMockedMayaTestCase, self).setUp()

    @property
    def session(self):
        """
        :rtype: MockedSession
        """
        return super(NodeGraphMockedMayaTestCase, self).session

    @property
    def registry(self):
        """
        :rtype: MockedMayaRegistry
        """
        return super(NodeGraphMockedMayaTestCase, self).registry


class NodeGraphMockedMayaFilterTestCase(NodeGraphMockedMayaTestCase):
    """
    Base class for a TestCase that test a NodeGraph filter under a mocked maya environment.
    """
    _cls_proxy_model = GraphFilterProxyModel
    _cls_filter = None

    def _create_filter(self):
        return self._cls_filter()

    def setUp(self):
        super(NodeGraphMockedMayaFilterTestCase, self).setUp()

        self.filter = self._create_filter()
        self.model.set_filter(self.filter)
