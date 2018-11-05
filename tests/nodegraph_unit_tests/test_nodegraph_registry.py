import pymel.core as pymel
from maya import cmds
from omtk_test import omtk_test
from omtk.nodegraph import NodeGraphController, NodeGraphRegistry
from omtk.component import component_registry
from omtk.nodegraph.models import GraphModel
from omtk.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel
from omtk.nodegraph.bindings.session_maya import MayaSession
from omtk.nodegraph.bindings.session_maya_mocked import MockedMayaSession


class BaseDccAgnosticTest(omtk_test.TestCase):
    def setUp(self):
        self.session = MockedMayaSession()
        self.registry = NodeGraphRegistry(session=self.session)



class NodeGraphRegistryCallbackTestCase(omtk_test.NodeGraphTestCase):
    """
    Ensure that the NodeGraphRegistry correctly react to Maya events.
    """
    def setUp(self):
        self.maxDiff = None

        cmds.file(new=True, force=True)

        self.session = MayaSession()
        self.registry = NodeGraphRegistry(session=self.session)
        self.source_model = GraphModel(registry=self.registry)
        self.model = GraphFilterProxyModel(model=self.source_model)
        self.ctrl = NodeGraphController(registry=self.registry, model=self.model)

        self.t1 = pymel.createNode('transform', name='a')
        self.m1 = self.registry.get_node(self.t1)
        self.ctrl.add_node(self.m1)
        self.assertEqual(1, len(self.model.get_nodes()))
        self.assertEqual(1, len(self.registry.get_nodes()))

    def test_delete_dagnode(self):
        """
        Ensure that if a node is deleted by Maya, it is automatically removed from the registry and models.
        """
        pymel.delete(self.t1)  # This should trigger a session callback.

        # Assert that the node was deleted
        self.assertEqual(0, len(self.model.get_nodes()))
        self.assertEqual(0, len(self.registry.get_nodes(safe=False)))

    def test_add_and_remove_port(self):
        """
        Ensure that when a port is added by Maya, it is automatically added on visible nodes.
        Ensure that when a port is removed by Maya, it is automatically removed from visible nodes.
        """
        num_ports = len(self.model.get_ports())
        pymel.addAttr(self.t1, longName='test')
        self.assertGraphPortCountEqual(num_ports + 1)

        self.t1.test.delete()
        self.assertGraphPortCountEqual(num_ports)


class NodeGraphRegistryCompoundCallbackTestCase(omtk_test.NodeGraphTestCase):
    """
    Ensure that the NodeGraphRegistry correctly react to Maya events.
    """
    def setUp(self):
        self.maxDiff = None
        self.session = MayaSession()
        self.registry = NodeGraphRegistry(session=self.session)
        source_model = GraphModel(registry=self.registry)
        self.model = GraphFilterProxyModel(model=source_model)
        self.ctrl = NodeGraphController(registry=self.registry, model=self.model)
        cmds.file(new=True, force=True)

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
