from omtk_test import omtk_test
import pymel.core as pymel
from omtk.nodegraph.filters.filter_hide_message_ports import NodeGraphMetadataFilter
from omtk.nodegraph.filters.filter_standard import NodeGraphStandardFilter


class NodeGraphFilterStandardTest(omtk_test.NodeGraphTestCase):
    def setUp(self):
        super(NodeGraphFilterStandardTest, self).setUp()

        filter_ = NodeGraphStandardFilter()
        self.ctrl.set_filter(filter_)

    def test_on_off(self):
        n1 = pymel.createNode('transform', name='a')
        m1 = self.registry.get_node(n1)
        self.model.add_node(m1)

        self.assertEqual(1, len(self.model.get_nodes()))
        self.assertEqual(219, len(self.model.get_ports()))

        self.ctrl.set_filter(None)  # attributes are changing here, wtf...

        # Validate we see the new node
        self.assertEqual(1, len(self.model.get_nodes()))
        self.assertEqual(225, len(self.model.get_ports()))

    def assertGraphEqual(self, expected):
        actual = self.model.dump()
        self.assertDictEqual(expected, actual)

    def test_port_filtering(self):
        """
        Ensure that we are able to:
        - Apply a NodeGraphFilter
        - UnApply a NodeGraphFilter
        """
        # Configure a basic network
        n1 = pymel.createNode('transform', name='a')
        m1 = self.registry.get_node(n1)

        self.model.add_node(m1)
        self.model.expand_node_ports(m1)

        self.assertGraphEqual({
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
        })


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

        m1 = self.registry.get_node(n1)
        m2 = self.registry.get_node(n2)
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
