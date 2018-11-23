import omtk_test

from omtk.nodegraph.registry.maya_mocked import MockedSession
# TODO: Add test when the node is not visible, we should not add the port/connection


class NodeGraphMayaSessionTestCase(omtk_test.NodeGraphBaseTestCase):
    _cls_session = MockedSession

    @property
    def session(self):
        """
        rtype: MockedSession
        """
        return super(NodeGraphMayaSessionTestCase, self).session

    def setUp(self):
        super(NodeGraphMayaSessionTestCase, self).setUp()

        # Create a simple network
        self.node_1 = self.session.create_node('transform', name='a')
        self.node_2 = self.session.create_node('transform', name='b')
        self.model_1 = self.registry.get_node(self.node_1)
        self.model_2 = self.registry.get_node(self.node_2)

    def test_delete_existing_node(self):
        """Ensure that when a node is deleted in Maya and visible in the graph, it is deleted from the graph."""
        # Add the node to the graph
        self.model.add_node(self.model_1)
        self.assertGraphNodeCountEqual(1)

        # Delete the node from the graph
        self.session.remove_node(self.node_1)
        self.assertGraphNodeCountEqual(0)

    def test_delete_port(self):
        """Ensure that when a port is deleted in Maya and visible in the graph, it is deleted from the graph."""
        self.model.add_node(self.model_1)
        self.model.add_node(self.model_2)

        # Validate the graph is empty
        self.assertGraphNodeCountEqual(2)

        # Create attribute, ensure it is added to the graph
        ports_count = len(self.model.get_ports())
        # since the node is visible, this will add the port
        port_1 = self.session.create_port(self.node_1, "test")
        self.assertGraphPortCountEqual(ports_count+1)

        # Remove attribute from session, ensure it is removed from the graph
        self.session.remove_port(port_1)
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
