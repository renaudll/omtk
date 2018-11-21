from omtk_test import NodeGraphMockedMayaTestCase
from omtk.component import component_registry
from omtk.vendor.mock_maya import MockedCmdsSession


class NodeGraphRegistryCallbackTestCase(NodeGraphMockedMayaTestCase):
    """
    Ensure that the NodeGraphRegistry correctly react to Maya events.
    """
    def setUp(self):
        super(NodeGraphRegistryCallbackTestCase, self).setUp()
        self.cmds = MockedCmdsSession(session=self.session)

        self.n1 = self.session.create_node('transform', name='a')
        self.m1 = self.registry.get_node(self.n1)
        self.ctrl.add_node(self.m1)
        self.assertEqual(1, len(self.model.get_nodes()))
        self.assertEqual(1, len(self.registry.get_nodes()))

    def test_delete_dagnode(self):
        """
        Ensure that if a node is deleted by Maya, it is automatically removed from the registry and models.
        """
        self.session.remove_node(self.n1)

        # Assert that the node was deleted from model and registry
        self.assertEqual(0, len(self.model.get_nodes()))
        self.assertEqual(0, len(self.registry.get_nodes(safe=False)))

    def test_add_and_remove_port(self):
        """
        Ensure that when a port is added by Maya, it is automatically added on visible nodes.
        Ensure that when a port is removed by Maya, it is automatically removed from visible nodes.
        """
        num_ports = len(self.model.get_ports())
        p = self.session.create_port(self.n1, 'test')
        self.assertGraphPortCountEqual(num_ports + 1)

        self.session.remove_port(p)
        self.assertGraphPortCountEqual(num_ports)


class NodeGraphRegistryCompoundCallbackTestCase(NodeGraphMockedMayaTestCase):
    """
    Ensure that the NodeGraphRegistry correctly react to Maya events.
    """
    def setUp(self, *args, **kwargs):
        super(NodeGraphRegistryCompoundCallbackTestCase, self).setUp(*args, **kwargs)
        registry = component_registry.get_registry()
        component_def = registry.get_latest_component_definition_by_name('Float2Float')
        self.c1 = component_def.instanciate()
        self.m1 = self.registry.get_node(self.c1)
        self.ctrl.add_node(self.m1)

    def test_delete(self):
        """Ensure that when we delete a compound, it is automatically removed from visible nodes."""
        self.c1.delete()  # should trigger callbacks
        self.assertGraphNodeCountEqual(0)
        self.assertGraphRegistryNodeCountEqual(0)
