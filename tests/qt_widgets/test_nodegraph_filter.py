import unittest

import pymel.core as pymel
from maya import cmds

from omtk.qt_widgets.nodegraph.nodegraph_controller import NodeGraphController
from omtk.qt_widgets.nodegraph.nodegraph_registry import NodeGraphRegistry
from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphModel
from omtk.qt_widgets.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel
from omtk.qt_widgets.nodegraph.filters.filter_standard import NodeGraphStandardFilter
from omtk.qt_widgets.nodegraph.filters.filter_metadata import NodeGraphMetadataFilter


def _node_to_json(g, n):
    # type: (NodeGraphModel, NodeGraphNodeModel) -> dict
    return {
        # 'name': n.get_name(),
        'ports': [p.get_name() for p in sorted(g.get_node_ports(n))],
    }


def _graph_to_json(g):
    # type: (NodeGraphModel) -> dict
    return {n.get_name(): _node_to_json(g, n) for n in g.get_nodes()}


class NodeGraphFilterTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff=None
        self.registry = NodeGraphRegistry()
        source_model = NodeGraphModel()
        self.model = GraphFilterProxyModel(model=source_model)
        self.ctrl = NodeGraphController(model=self.model)
        cmds.file(new=True, force=True)

        # Validate the graph is empty
        self.assertEqual(0, len(self.model.get_nodes()))
        self.assertEqual(0, len(self.model.get_ports()))

    def test_port_filtering(self):
        """
        Ensure that we are able to:
        - Apply a NodeGraphFilter
        - UnApply a NodeGraphFilter
        """
        # Configure a basic network
        n1 = pymel.createNode('transform', name='a')
        m1 = self.registry.get_node_from_value(n1)

        self.model.add_node(m1)
        self.ctrl.expand_node_attributes(m1)

        # Validate we see the new node
        self.assertEqual(1, len(self.model.get_nodes()))
        self.assertEqual(219, len(self.model.get_ports()))

        # Apply a filter
        filter_ = NodeGraphStandardFilter()
        self.ctrl.set_filter(filter_)

        # Validate we see the new node with les attributes
        # self.assertEqual(13, len(self.model.get_ports()))
        snapshot = _graph_to_json(self.model)
        self.assertDictEqual(
            {
                u'a': {
                    'ports': [
                        'hierarchy',
                        u'matrix',
                        u'rotateX', u'rotateY', u'rotateZ',
                        u'scaleX', u'scaleY', u'scaleZ',
                        u'translateX', u'translateY', u'translateZ',
                        u'visibility',
                        u'worldMatrix'
                    ]
                },
            },
            snapshot
        )

        # Remove the filter
        self.ctrl.set_filter(None)  # attributes are changing here, wtf...

        # Validate we see the new node
        self.assertEqual(1, len(self.model.get_nodes()))
        self.assertEqual(225, len(self.model.get_ports()))

    def test_connection_filtering(self):
        """
        Ensure we are able to ignore connections like non-message.
        :return:
        """
        n1 = pymel.createNode('transform', name='a')
        n2 = pymel.createNode('transform', name='b')
        pymel.addAttr(n2, longName='test', at='message')
        pymel.connectAttr(n1.translate, n2.translate)  # float3 -> float3
        pymel.connectAttr(n1.message, n2.test)  # message -> message

        m1 = self.registry.get_node_from_value(n1)
        m2 = self.registry.get_node_from_value(n2)
        self.model.add_node(m1)
        self.model.add_node(m2)
        self.ctrl.expand_node_ports(m1)

        self.assertEqual(2, len(self.model.get_nodes()))
        self.assertEqual(221, len(self.model.get_ports()))  # yes that's a lot of ports
        self.assertEqual(2, len(self.model.get_connections()))

        filter_ = NodeGraphStandardFilter()
        filter_.hide_message_attribute_type = True
        self.ctrl.set_filter(filter_)

        self.assertEqual(2, len(self.model.get_nodes()))
        # self.assertEqual(457, len(self.model.get_ports()))  # yes that's a lot of ports
        self.assertEqual(1, len(self.model.get_connections()))

        # # Plot-twist, change the filter to a filter that only let message attribute pass through.
        filter_ = NodeGraphMetadataFilter()
        self.ctrl.set_filter(filter_)

        self.assertEqual(2, len(self.model.get_nodes()))
        self.assertEqual(1, len(self.model.get_connections()))

        connection = self.model.get_connections()[0]
        port_src = connection.get_source()
        port_dst = connection.get_destination()
        self.assertEqual('message', port_src.get_metadata().type())
        self.assertEqual('message', port_dst.get_metadata().type())



# todo: test subgraph filter
# todo: test decomposeMatrix filter
# todo: test libSerialization filter?