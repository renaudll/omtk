from omtk.nodegraph.filters.filter_intermediate_nodes import IntermediateNodeFilter
from omtk.nodegraph.filters.filter_standard import NodeGraphStandardFilter
from pymel import core as pymel

from base import GraphFilterTestCase


class NodeGraphFilterIntermediateTest(GraphFilterTestCase):
    # def setUp(self):
    #     super(NodeGraphFilterIntermediateTest, self).setUp()

        # filter_ = IntermediateNodeFilter()
        # self.model.add_filter(filter_)

    def test_unitconversion_filtering(self):
        """
        Ensure NodeGraphStandardFilter hide unitConversion nodes unless explicitly ask to.
        """
        n1 = pymel.createNode('transform', name='a')
        n2 = pymel.createNode('transform', name='b')
        pymel.connectAttr(n1.translateX, n2.rotateX)

        # todo: this should work if we start with no filters, add the node and then change filters?
        filter = IntermediateNodeFilter()
        self.ctrl.set_filter(filter)

        m1 = self.registry.get_node(n1)
        m2 = self.registry.get_node(n2)
        self.ctrl.add_node(m1)
        self.ctrl.add_node(m2)

        self.assertGraphNodeNamesEqual([u'a', u'b'])
        self.assertGraphConnectionsEqual([(u'a.translateX', u'b.rotateX')])

        # However, if you add the unitConversion node explicitly, we want to see it!
        n3 = n1.translateX.outputs()[0]
        m3 = self.registry.get_node(n3)
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
        filter = IntermediateNodeFilter()
        self.ctrl.set_filter(filter)

        m1 = self.registry.get_node(n1)
        m2 = self.registry.get_node(n2)
        self.ctrl.add_node(m1)
        # self.ctrl.add_node_callbacks(m2)

        self.assertGraphNodeNamesEqual([u'a', u'b'])
        self.assertGraphConnectionsEqual([(u'a.translateX', u'b.rotateX')])