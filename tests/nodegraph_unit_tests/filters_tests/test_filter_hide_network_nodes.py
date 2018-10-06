"""
Ensure propre behaviour or the GraphController, GraphRegistry and every related models.
"""
import unittest

import pymel.core as pymel
from omtk.nodegraph.filters.filter_hide_network_nodes import NodeGraphMetadataFilter
from omtk.libs import libAttr

from .base import GraphFilterTestCase


class HideNetworkNodesFilterTestCase(GraphFilterTestCase):
    """
    Test a simple NodeGraphFilter that only let camera goes through.
    """

    def setUp(self):
        super(HideNetworkNodesFilterTestCase, self).setUp()

        filter_ = NodeGraphMetadataFilter()
        self.model.add_filter(filter_)

    def assertGraphIsEmpty(self):
        self.assertGraphNodeCountEqual(0)
        self.assertGraphPortCountEqual(0)
        self.assertGraphConnectionCountEqual(0)

    def test_node_visibility(self):
        """Ensure that adding a network node to the graph don't add anything."""
        pynode = pymel.createNode('network')
        node = self.registry.get_node(pynode)

        self.assertGraphIsEmpty()
        self.model.add_node(node)
        self.assertGraphIsEmpty()

    def test_port_visibility(self):
        """Ensure that adding a network node port to the graph don't add anything."""
        pynode = pymel.createNode('network')
        attr = libAttr.addAttr(pynode, 'test')
        port = self.registry.get_port(attr)

        self.assertGraphIsEmpty()
        self.model.add_port(port)
        self.assertGraphIsEmpty()

    def test_connection_source_visibility(self):
        """Ensure that adding a connection from a network node to the graph don't add anything."""
        pynode_src = pymel.createNode('network')
        pynode_dst = pymel.createNode('transform')
        pymel.addAttr(pynode_dst, longName='test', at='message')
        pymel.connectAttr(pynode_src.message, pynode_dst.test)
        connection = self.registry.get_connection(pynode_src, pynode_dst)

        self.assertGraphIsEmpty()
        self.model.add_connection(connection)
        # self.assertGraphNodeCountEqual(1)  # node will be added but empty
        # self.assertGraphPortCountEqual(0)
        self.assertGraphConnectionCountEqual(0)


if __name__ == '__main__':
    unittest.main()
