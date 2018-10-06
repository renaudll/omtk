"""
Ensure propre behaviour or the GraphController, GraphRegistry and every related models.
"""
import unittest
import pymel.core as pymel

import omtk_test
from maya import cmds
from omtk.nodegraph import NodeGraphRegistry, GraphModel, NodeGraphController, NodeGraphFilter
from omtk.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel
from omtk.nodegraph.models.node.node_dag import NodeGraphDagNodeModel
from omtk.nodegraph.models.port.port_base import NodeGraphPymelPortModel


class CameraFilter(NodeGraphFilter):
    """
    Show only camera shapes.
    """

    def intercept_node(self, node):
        if not isinstance(node, NodeGraphDagNodeModel):
            return

        pynode = node.get_metadata()
        if not isinstance(pynode, pymel.nodetypes.Camera):
            return

        yield node


class MessageFilter(NodeGraphFilter):
    """
    Show only message type filters.
    """

    def intercept_port(self, port):
        """
        Yield port only if they are named 'message'.
        :param NodeGraphPortModel port: The port to inspect.
        :return: A port generator
        rtype: Generator[NodeGraphPortModel]
        """
        if not isinstance(port, NodeGraphPymelPortModel):
            return

        pyattr = port.get_metadata()
        attr_name = pyattr.longName()
        if attr_name != 'message':
            return

        yield port


class GraphFilterTestCase(omtk_test.NodeGraphTestCase):
    def setUp(self):
        super(GraphFilterTestCase, self).setUp()

        self.registry = NodeGraphRegistry()
        source_model = GraphModel(self.registry)
        self.model = GraphFilterProxyModel(model=source_model)
        self.ctrl = NodeGraphController(self.registry, model=self.model)
        cmds.file(new=True, force=True)

        # Validate the graph is empty
        # self.assertEqual(0, len(self.model.get_nodes()))
        # self.assertEqual(0, len(self.model.get_ports()))


class SimpleNodeGraphFilterTestCase(GraphFilterTestCase):
    """
    Test a simple NodeGraphFilter that only let camera goes through.
    """
    def setUp(self):
        super(SimpleNodeGraphFilterTestCase, self).setUp()

        filter_ = CameraFilter()
        self.model.add_filter(filter_)

    def test_can_show_node(self):
        for pynode in pymel.ls():
            node = self.registry.get_node(pynode)
            print node
            self.ctrl.add_node(node)

        expected = [
            'frontShape',
            'perspShape',
            'topShape',
            'sideShape',
        ]
        self.assertGraphNodeNamesEqual(expected)


class SimpleGraphPortFilterTestCase(GraphFilterTestCase):
    """
    Test a simple NodeGraphFilter that only let message attributes goes throught.
    """
    def setUp(self):
        super(SimpleGraphPortFilterTestCase, self).setUp()

        filter_ = MessageFilter()
        self.model.add_filter(filter_)

    def test_can_shot_port(self):
        pynode = pymel.PyNode('top')
        node = self.registry.get_node(pynode)
        self.model.add_node(node)
        self.assertGraphNodePortNamesEqual(node, ['message'])


if __name__ == '__main__':
    unittest.main()
