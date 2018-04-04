import unittest
import omtk_test
import pymel.core as pymel
from maya import cmds
from omtk.qt_widgets.nodegraph import NodeGraphController, NodeGraphRegistry
from omtk.qt_widgets.nodegraph.filters.filter_metadata import NodeGraphMetadataFilter
from omtk.qt_widgets.nodegraph.filters.filter_standard import NodeGraphStandardFilter
from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphModel
from omtk.qt_widgets.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel


# todo: move this to omtk_test.NodeGraphTestCase
def _node_to_json(g, n):
    # type: (NodeGraphModel, NodeGraphNodeModel) -> dict
    return {
        # 'name': n.get_name(),
        'ports': [p.get_name() for p in sorted(g.get_node_ports(n))],
    }


class NodeGraphFilterTest(omtk_test.NodeGraphTestCase):
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
        self.model.expand_node_ports(m1)

        # Validate we see the new node
        self.assertEqual(1, len(self.model.get_nodes()))
        self.assertEqual(219, len(self.model.get_ports()))

        # Apply a filter
        filter_ = NodeGraphStandardFilter()
        self.ctrl.set_filter(filter_)

        # Validate we see the new node with les attributes
        # self.assertEqual(13, len(self.model.get_ports()))
        snapshot = self._graph_to_json(self.model)
        self.assertDictEqual(
            {
                u'a': {
                    'ports': [
                        'hierarchy',
                        u'matrix',
                        u'rotate', u'rotateX', u'rotateY', u'rotateZ',
                        u'scale', u'scaleX', u'scaleY', u'scaleZ',
                        u'translate', u'translateX', u'translateY', u'translateZ',
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
        self.ctrl.expand_node_connections(m1)

        self.assertGraphNodeCountEqual(2)
        self.assertGraphPortCountEqual(439)  # yes that's a lot of ports
        self.assertGraphConnectionCountEqual(2)

        filter_ = NodeGraphStandardFilter()
        filter_.hide_message_attribute_type = True
        self.ctrl.set_filter(filter_)

        self.assertGraphNodeCountEqual(2)
        # self.assertGraphPortCountEqual(221)  # yes that's a lot of ports
        self.assertGraphConnectionCountEqual(1)

        # Plot-twist, change the filter to a filter that only let message attribute pass through.
        filter_ = NodeGraphMetadataFilter()
        self.ctrl.set_filter(filter_)

        self.assertGraphNodeCountEqual(2)
        self.assertGraphConnectionCountEqual(1)

        connection = self.model.get_connections()[0]
        port_src = connection.get_source()
        port_dst = connection.get_destination()
        self.assertEqual('message', port_src.get_metadata().type())
        self.assertEqual('message', port_dst.get_metadata().type())

    def test_unitconversion_filtering(self):
        """
        Ensure NodeGraphStandardFilter hide unitConversion nodes unless explicitly ask to.
        """
        n1 = pymel.createNode('transform', name='a')
        n2 = pymel.createNode('transform', name='b')
        pymel.connectAttr(n1.translateX, n2.rotateX)

        # todo: this should work if we start with no filters, add the node and then change filters?
        filter = NodeGraphStandardFilter()
        self.ctrl.set_filter(filter)

        m1 = self.registry.get_node_from_value(n1)
        m2 = self.registry.get_node_from_value(n2)
        self.ctrl.add_node(m1)
        self.ctrl.add_node(m2)

        self.assertGraphNodeNamesEqual([u'a', u'b'])
        self.assertGraphConnectionsEqual([(u'a.translateX', u'b.rotateX')])

        # However, if you add the unitConversion node explicitly, we want to see it!
        n3 = n1.translateX.outputs()[0]
        m3 = self.registry.get_node_from_value(n3)
        self.ctrl.add_node(m3)

        self.assertGraphNodeNamesEqual([u'a', u'b', u'unitConversion1'])
        self.assertGraphConnectionsEqual([
            (u'a.translateX', u'b.rotateX'),
            (u'a.translateX', u'unitConversion1.input'),
            (u'unitConversion1.output', u'b.rotateX'),
        ])

    def test_existing_unitconversion_filtering(self):
        """
        Ensure NodeGraphStandardFilter hide unitConversion nodes unless explicitly ask to.
        """
        n1 = pymel.createNode('transform', name='a')
        n2 = pymel.createNode('transform', name='b')
        pymel.connectAttr(n1.translateX, n2.rotateX)

        # todo: this should work if we start with no filters, add the node and then change filters?
        filter = NodeGraphStandardFilter()
        self.ctrl.set_filter(filter)

        m1 = self.registry.get_node_from_value(n1)
        m2 = self.registry.get_node_from_value(n2)
        self.ctrl.add_node(m1)
        # self.ctrl.add_node(m2)

        self.assertGraphNodeNamesEqual([u'a', u'b'])
        self.assertGraphConnectionsEqual([(u'a.translateX', u'b.rotateX')])
