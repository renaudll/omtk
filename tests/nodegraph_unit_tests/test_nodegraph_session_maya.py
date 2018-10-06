import pymel.core as pymel
from maya import cmds
import omtk_test
from omtk.nodegraph import NodeGraphRegistry
from omtk.nodegraph.models import GraphModel
from omtk.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel
from omtk.nodegraph.bindings.session_maya import MayaSession


# TODO: Add test when the node is not visible, we should not add the port/connection


class NodeGraphMayaSessionTestCase(omtk_test.NodeGraphTestCase):
    def setUp(self):
        cmds.file(new=True, force=True)

        self.maxDiff = None
        self.session = MayaSession()
        self.registry = NodeGraphRegistry(session=self.session)
        self.source_model = GraphModel(self.registry)
        self.model = GraphFilterProxyModel(model=self.source_model)

        # Create a simple network
        self.node_1 = pymel.createNode('transform', name='a')
        self.node_2 = pymel.createNode('transform', name='b')
        self.model_1 = self.registry.get_node(self.node_1)
        self.model_2 = self.registry.get_node(self.node_2)

    def test_delete_existing_node(self):
        """Ensure that when a node is deleted in Maya and visible in the graph, it is deleted from the graph."""
        # Add the node to the graph
        self.model.add_node(self.model_1)
        self.assertGraphNodeCountEqual(1)

        # Delete the node from the graph
        pymel.delete(self.node_1)
        self.assertGraphNodeCountEqual(0)

    def test_delete_port(self):
        """Ensure that when a port is deleted in Maya and visible in the graph, it is deleted from the graph."""
        self.model.add_node(self.model_1)
        self.model.add_node(self.model_2)

        # Validate the graph is empty
        self.assertGraphNodeCountEqual(2)

        # Create attribute, ensure it is added to the graph
        ports_count = len(self.model.get_ports())
        pymel.addAttr(self.node_1, longName="test")  # since the node is visible, this will add the port
        self.assertGraphPortCountEqual(ports_count+1)

        # Remove attribute from session, ensure it is removed from the graph
        pymel.deleteAttr(self.node_1, attribute="test")
        self.assertGraphPortCountEqual(ports_count)

    def test_delete_connection(self):
        """Ensure that when a connection is deleted in Maya and visible in the graph, it is deleted from the graph."""
        self.model.add_node(self.model_1)
        self.model.add_node(self.model_2)

        # Validate the graph is empty
        self.assertGraphNodeCountEqual(2)

        pymel.connectAttr(self.node_1.t, self.node_2.t)
        port_src = self.registry.get_port(self.node_1.t)
        port_dst = self.registry.get_port(self.node_2.t)
        connection = self.registry.get_connection(port_src, port_dst)

        self.model.add_connection(connection)
        self.assertGraphConnectionCountEqual(1)

        pymel.disconnectAttr(self.node_1.t, self.node_2.t)
        self.assertGraphConnectionCountEqual(0)
