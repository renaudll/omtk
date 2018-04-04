"""
Ensure propre behaviour or the GraphController, GraphRegistry and every related models.
"""
import logging
import unittest

import pymel.core as pymel
from maya import cmds
import omtk_test
from omtk.libs import libComponents
from omtk.libs import libRigging
from omtk.qt_widgets.nodegraph.models.graph.graph_component_proxy_model import GraphComponentProxyFilterModel
from omtk.qt_widgets.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel
from omtk.qt_widgets.nodegraph.nodegraph_registry import NodeGraphRegistry
from omtk.qt_widgets.nodegraph.models import NodeGraphModel

log = logging.getLogger('omtk')
log.setLevel(logging.DEBUG)


class NodeGraphSubgraphFilterTestCase(omtk_test.NodeGraphTestCase):
    def setUp(self):
        super(NodeGraphSubgraphFilterTestCase, self).setUp()

        # Add a NodeGraphSubgraphProxyModel
        self.model = GraphComponentProxyFilterModel(model=self.model)
        self.ctrl.set_model(self.model)

    def _register_node(self, node):
        model = self.registry.get_node_from_value(node)
        return model

    def assertPortInfo(self, node, name, is_readable, is_writable):
        def _get_port_by_name(name):
            for port in self.model.iter_node_ports(node):
                if port.get_name() == name:
                    return port
        p = _get_port_by_name(name)
        self.assertEqual(p.is_readable(), is_readable)
        self.assertEqual(p.is_writable(), is_writable)

    def test_io_subgraph(self):
        """
        Ensure that we support subgraphs networks where an attribute is both an input and an output (io).
        """
        # Create network
        n1 = pymel.createNode('transform', name='n1')
        n2 = pymel.createNode('transform', name='n2')
        n3 = pymel.createNode('transform', name='n3')
        pymel.connectAttr(n1.t, n2.t)
        pymel.connectAttr(n2.t, n3.t)

        # Register network
        m1 = self.registry.get_node_from_value(n1)
        m2 = self.registry.get_node_from_value(n2)
        m3 = self.registry.get_node_from_value(n3)
        self.ctrl.add_nodes(m1, m2, m3)
        self.assertGraphNodeNamesEqual([u'n1', u'n2', u'n3'])
        self.assertGraphConnectionsEqual([
            (u'n1.translate', u'n2.translate'),
            (u'n2.translate', u'n3.translate'),
        ])

        # Create a subgroup (group nodes)
        component = self.ctrl.group_nodes([m2])
        self.assertGraphNodeNamesEqual([u'n1', u'component00', u'n3'])
        self.assertPortInfo(component, 'translate', is_readable=True, is_writable=True)
        self.assertGraphConnectionsEqual([
            (u'n1.translate', u'component00.translate'),
            (u'component00.translate', u'n3.translate'),
        ])

        # Enter the subgrap
        self.ctrl.set_level(component)
        self.assertGraphNodeNamesEqual([u'component00:inn', u'n2', u'component00:out'])
        # self.assertGraphConnectionsEqual

    def test_nested_subgraphs(self):
        """
        Ensure that we are able to navigate between multiple nested subgraphs.
        """
        # Create network
        def _create_transform(name): return pymel.createNode('transform', name=name)
        n1 = _create_transform('n1')
        n2 = _create_transform('n2')
        n3 = _create_transform('n3')
        n4 = _create_transform('n4')
        n5 = _create_transform('n5')
        pymel.connectAttr(n1.t, n2.t)
        pymel.connectAttr(n2.t, n3.t)
        pymel.connectAttr(n3.t, n4.t)
        pymel.connectAttr(n4.t, n5.t)

        # Register network
        def _register(n): return self.registry.get_node_from_value(n)
        m1 = _register(n1)
        m2 = _register(n2)
        m3 = _register(n3)
        m4 = _register(n4)
        m5 = _register(n5)

        self.ctrl.add_nodes(m1, m2, m3, m4, m5)
        self.assertGraphNodeNamesEqual([u'n1', u'n2', u'n3', u'n4', u'n5'])

        # Create a subgroup (group nodes)
        component_1 = self.ctrl.group_nodes([m2, m3, m4])
        self.assertGraphNodeNamesEqual([u'n1', u'component00', u'n5'])
        self.assertGraphConnectionsEqual([
            (u'n1.translate', u'component00.translate'),
            (u'component00.translate', u'n5.translate'),
        ])

        # Enter the subgrap
        self.ctrl.set_level(component_1)
        self.assertGraphNodeNamesEqual([u'component00:inn', u'n2', u'n3', u'n4', u'component00:out'])
        self.assertGraphConnectionsEqual([
            (u'component00:inn.translate', u'n2.translate'),
            (u'n2.translate', u'n3.translate'),
            (u'n3.translate', u'n4.translate'),
            (u'n4.translate', u'component00:out.translate'),
        ])

        # Create a new component
        component2 = self.ctrl.group_nodes([m3])
        self.assertGraphNodeNamesEqual([u'component00:inn', u'n2', u'component01', u'n4', u'component00:out'])
        self.assertGraphConnectionsEqual([
            (u'component00:inn.translate', u'n2.translate'),
            (u'n2.translate', u'component01.translate'),
            (u'component01.translate', u'n4.translate'),
            (u'n4.translate', u'component00:out.translate'),
        ])

        # Enter the new component
        self.ctrl.set_level(component2)
        self.assertGraphNodeNamesEqual([u'component01:inn', u'n3', u'component01:out'])
        self.assertGraphConnectionsEqual([
            (u'component01:inn.translate', u'n3.translate'),
            (u'n3.translate', u'component01:out.translate'),
        ])

        # Exit the new component
        self.ctrl.set_level(component_1)
        self.assertGraphNodeNamesEqual([u'component00:inn', u'n2', u'component01', u'n4', u'component00:out'])
        self.assertGraphConnectionsEqual([
            (u'component00:inn.translate', u'n2.translate'),
            (u'n2.translate', u'component01.translate'),
            (u'component01.translate', u'n4.translate'),
            (u'n4.translate', u'component00:out.translate'),
        ])

        # Return to root level
        self.ctrl.set_level(None)
        self.assertGraphNodeNamesEqual([u'n1', u'component00', u'n5'])
        self.assertGraphConnectionsEqual([
            (u'n1.translate', u'component00.translate'),
            (u'component00.translate', u'n5.translate'),
        ])


if __name__ == '__main__':
    unittest.main()

    # todo: test discovery of nodes in a specific compound space
