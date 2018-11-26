"""
Ensure propre behaviour or the GraphController, GraphRegistry and every related models.
"""
import logging
import unittest
from omtk_test import NodeGraphMockedMayaTestCase
from omtk.nodegraph.models.graph.graph_component_proxy_model import GraphComponentProxyFilterModel

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class NodeGraphSubgraphFilterTestCase(NodeGraphMockedMayaTestCase):
    _cls_proxy_model = GraphComponentProxyFilterModel

    def _register_node(self, node):
        model = self.registry.get_node(node)
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
        n1 = pymel.createNode('transform', name='node')
        n2 = pymel.createNode('transform', name='n2')
        n3 = pymel.createNode('transform', name='n3')
        pymel.connectAttr(n1.t, n2.t)
        pymel.connectAttr(n2.t, n3.t)

        # Register network
        m1 = self.registry.get_node(n1)
        m2 = self.registry.get_node(n2)
        m3 = self.registry.get_node(n3)
        self.ctrl.add_nodes(m1, m2, m3)
        self.assertGraphNodeNamesEqual([u'node', u'n2', u'n3'])
        self.assertGraphConnectionsEqual([
            (u'node.translate', u'n2.translate'),
            (u'n2.translate', u'n3.translate'),
        ])

        # Create a subgroup (group nodes)
        component = self.ctrl.group_nodes([m2])
        self.assertGraphNodeNamesEqual([u'node', u'component1', u'n3'])
        self.assertPortInfo(component, 'translate', is_readable=True, is_writable=True)
        self.assertGraphConnectionsEqual([
            (u'node.translate', u'component1.translate'),
            (u'component1.translate', u'n3.translate'),
        ])

        # Enter the subgrap
        self.ctrl.set_level(component)
        self.assertGraphNodeNamesEqual([u'component1:inn', u'n2', u'component1:out'])
        # self.assertGraphConnectionsEqual

    def test_nested_subgraphs(self):
        """
        Ensure that we are able to navigate between multiple nested subgraphs.
        """
        # Create network
        def _create_transform(name): return pymel.createNode('transform', name=name)
        n1 = _create_transform('node')
        n2 = _create_transform('n2')
        n3 = _create_transform('n3')
        n4 = _create_transform('n4')
        n5 = _create_transform('n5')
        pymel.connectAttr(n1.t, n2.t)
        pymel.connectAttr(n2.t, n3.t)
        pymel.connectAttr(n3.t, n4.t)
        pymel.connectAttr(n4.t, n5.t)

        # Register network
        def _register(n): return self.registry.get_node(n)
        m1 = _register(n1)
        m2 = _register(n2)
        m3 = _register(n3)
        m4 = _register(n4)
        m5 = _register(n5)

        self.ctrl.add_nodes(m1, m2, m3, m4, m5)
        self.assertGraphNodeNamesEqual([u'node', u'n2', u'n3', u'n4', u'n5'])

        # Create a subgroup (group nodes)
        component_1 = self.ctrl.group_nodes([m2, m3, m4])
        self.assertGraphNodeNamesEqual([u'node', u'component1', u'n5'])
        self.assertGraphConnectionsEqual([
            (u'node.translate', u'component1.translate'),
            (u'component1.translate', u'n5.translate'),
        ])

        # Enter the subgrap
        self.ctrl.set_level(component_1)
        self.assertGraphNodeNamesEqual([u'component1:inn', u'n2', u'n3', u'n4', u'component1:out'])
        self.assertGraphConnectionsEqual([
            (u'component1:inn.translate', u'n2.translate'),
            (u'n2.translate', u'n3.translate'),
            (u'n3.translate', u'n4.translate'),
            (u'n4.translate', u'component1:out.translate'),
        ])

        # Create a new component
        component_2 = self.ctrl.group_nodes([m3])
        self.assertGraphNodeNamesEqual([u'component1:inn', u'n2', u'component1:component1', u'n4', u'component1:out'])
        self.assertGraphConnectionsEqual([
            (u'component1:inn.translate', u'n2.translate'),
            (u'n2.translate', u'component1:component1.translate'),
            (u'component1:component1.translate', u'n4.translate'),
            (u'n4.translate', u'component1:out.translate'),
        ])

        # Enter the new component
        self.ctrl.set_level(component_2)
        self.assertGraphNodeNamesEqual([u'component1:component1:inn', u'n3', u'component1:component1:out'])
        self.assertGraphConnectionsEqual([
            (u'component1:component1:inn.translate', u'n3.translate'),
            (u'n3.translate', u'component1:component1:out.translate'),
        ])

        # Exit the new component
        self.ctrl.set_level(component_1)
        self.assertGraphNodeNamesEqual([u'component1:inn', u'n2', u'component1:component1', u'n4', u'component1:out'])
        self.assertGraphConnectionsEqual([
            (u'component1:inn.translate', u'n2.translate'),
            (u'n2.translate', u'component1:component1.translate'),
            (u'component1:component1.translate', u'n4.translate'),
            (u'n4.translate', u'component1:out.translate'),
        ])

        # Return to root level
        self.ctrl.set_level(None)
        self.assertGraphNodeNamesEqual([u'node', u'component1', u'n5'])
        self.assertGraphConnectionsEqual([
            (u'node.translate', u'component1.translate'),
            (u'component1.translate', u'n5.translate'),
        ])


if __name__ == '__main__':
    unittest.main()

    # todo: test discovery of nodes in a specific compound space
