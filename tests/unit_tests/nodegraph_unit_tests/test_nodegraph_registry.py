from omtk_test import NodeGraphMockedMayaTestCase
from omtk.component import component_registry
from omtk.vendor.mock_maya import MockedCmdsSession


class NodeGraphRegistryCallbackTestCase(NodeGraphMockedMayaTestCase):
    """
    Ensure that the NodeGraphRegistry correctly react to Maya events.
    """
    _cls_controller = None
    _cls_model = None
    _cls_proxy_model = None
    _cls_session_preset = None

    def setUp(self):
        super(NodeGraphRegistryCallbackTestCase, self).setUp()
        self.cmds = MockedCmdsSession(session=self.session)

        self.node = self.session.create_node('transform', name='a')
        self.model_node = self.registry.get_node(self.node)
        self.assertEqual(1, len(self.registry.get_nodes()))

    def _assert_registry_empty(self):
        self._assert_registry_node_empty()
        self._assert_registry_port_empty()
        self._assert_registry_connection_empty()

    def _assert_registry_node_empty(self):
        self.assertFalse(self.registry.nodes)
        self.assertFalse(self.registry.cache_nodes_by_value)

    def _assert_registry_port_empty(self):
        self.assertFalse(self.registry.ports)
        self.assertFalse(self.registry.cache_ports_by_value)
        self.assertFalse(self.registry.cache_ports_by_node)

    def _assert_registry_connection_empty(self):
        self.assertFalse(self.registry.connections)
        self.assertFalse(self.registry.cache_connections_by_port)
        self.assertFalse(self.registry.cache_connection_by_value)

    def test_create_node(self):
        self.assertIn(self.model_node, self.registry.nodes)

    def test_delete_dagnode(self):
        """
        Ensure that if a node is deleted by Maya, it is automatically removed from the REGISTRY_DEFAULT and models.
        """
        self.session.remove_node(self.node)

        # Assert that the node was deleted from model and REGISTRY_DEFAULT
        self._assert_registry_empty()


class NodeGraphRegistryCallbackPortTestCase(NodeGraphRegistryCallbackTestCase):
    def setUp(self):
        super(NodeGraphRegistryCallbackPortTestCase, self).setUp()

        # Build session
        self.port = self.session.create_port(self.node, 'test')

        # Build registry
        self.model_port = self.registry.get_port(self.port)

    def test_create_port(self):
        """
        Ensure that when a port is added by Maya, it is automatically added on visible nodes.
        Ensure that when a port is removed by Maya, it is automatically removed from visible nodes.
        """
        self.assertIn(self.model_port, self.registry.ports)

    def test_remove_port(self):
        self.session.remove_port(self.port)
        self.assertNotIn(self.model_port, self.registry.ports)


class NodeGraphRegistryCallbackConnectionTestCase(NodeGraphRegistryCallbackTestCase):
    def setUp(self):
        super(NodeGraphRegistryCallbackConnectionTestCase, self).setUp()

        # Build session
        self.port_src = self.session.create_port(self.node, 'testSrc')
        self.port_dst = self.session.create_port(self.node, 'testDst')
        self.connection = self.session.create_connection(self.port_src, self.port_dst)

        # Build registry
        self.model_port_src = self.registry.get_port(self.port_src)
        self.model_port_dst = self.registry.get_port(self.port_dst)
        self.model_connection = self.registry.get_connection(self.model_port_src, self.model_port_dst)

    def test_create_connection(self):
        """
        Ensure that when a connection is added to the scene, it is also added to the registry.
        """
        self.assertIn(self.model_connection, self.registry.connections)

    def test_remove_connection(self):
        """
        Ensure that when a connection is removed from the scene, it is also removed from the registry.
        """
        self.session.remove_connection(self.connection)
        self.assertNotIn(self.model_connection, self.registry.connections)

    def test_remove_src_port(self):
        """
        Ensure that when a connection source port is removed from the scene,
        the connection is also removed from the registry.
        """
        self.session.remove_port(self.port_src)
        self.assertNotIn(self.model_port_src, self.registry.ports)
        self.assertIn(self.model_port_dst, self.registry.ports)
        self.assertNotIn(self.model_connection, self.registry.connections)

    def test_remove_dst_port(self):
        """
        Ensure that when a connection source port is removed from the scene,
        the connection is also removed from the registry.
        """
        self.session.remove_port(self.port_dst)
        self.assertIn(self.model_port_src, self.registry.ports)
        self.assertNotIn(self.model_port_dst, self.registry.ports)
        self.assertNotIn(self.model_connection, self.registry.connections)


# TODO: Move the following to the compound proxy model tests
# class NodeGraphRegistryCompoundCallbackTestCase(NodeGraphMockedMayaTestCase):
#     """
#     Ensure that the NodeGraphRegistry correctly react to Maya events.
#     """
#     def setUp(self, *args, **kwargs):
#         super(NodeGraphRegistryCompoundCallbackTestCase, self).setUp(*args, **kwargs)
#         registry = component_registry.get_registry()
#         component_def = registry.get_latest_component_definition_by_name('Float2Float')
#         self.c1 = component_def.instanciate()
#         self.model_node = self.registry.get_node(self.c1)
#         self.ctrl.add_node(self.model_node)
#
#     def test_delete(self):
#         """Ensure that when we delete a compound, it is automatically removed from visible nodes."""
#         self.c1.delete()  # should trigger callbacks
#         self.assertGraphNodeCountEqual(0)
#         self.assertGraphRegistryNodeCountEqual(0)
