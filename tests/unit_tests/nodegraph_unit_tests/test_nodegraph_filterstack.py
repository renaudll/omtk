"""
Ensure propre behaviour or the GraphController, GraphRegistry and every related models.
"""
import logging
import unittest

from omtk.nodegraph.filters.filter_standard import NodeGraphStandardFilter
from omtk.nodegraph.models.graph.graph_component_proxy_model import GraphComponentProxyFilterModel
from omtk.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel
from omtk.vendor.mock_maya.decorators import mock_pymel
import omtk_test

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class NodeGraphSubgraphFilterTestCase(omtk_test.NodeGraphMockedMayaTestCase):
    def setUp(self):
        super(NodeGraphSubgraphFilterTestCase, self).setUp()

        # Create filter
        self._filter = NodeGraphStandardFilter()

        # Add a proxy-model to apply user display preferences
        self._proxy_model_filter = GraphFilterProxyModel()
        self._proxy_model_filter.set_source_model(self.model)
        self._proxy_model_filter.set_filter(self._filter)

        # Add a proxy-model to allow encapsulation
        self._proxy_model_subgraph = GraphComponentProxyFilterModel()
        self._proxy_model_subgraph.set_source_model(self._proxy_model_filter)

        self.ctrl.set_ctrl(self._proxy_model_subgraph)

    def test_compound_with_blacklisted_nodes(self):
        """
        """
        # Create network
        with mock_pymel(self.session) as pymel:
            from omtk.libs import libRigging

            n1 = pymel.createNode('transform', name='node')
            n2 = pymel.createNode('transform', name='n2')
            u1 = libRigging.create_utility_node(
                'decomposeMatrix',
                name='n3',
                inputMatrix=n1.matrix,
            )
            pymel.connectAttr(u1.outputTranslate, n2.translate)

        # Register network
        def _register(n): return self.registry.get_node(n)

        m1 = _register(n1)
        m2 = _register(n2)
        m3 = _register(u1)

        # Add the source node, we should not see the decomposeMatrix node.
        self.ctrl.add_nodes(m1, m2, m3)
        self.assertGraphNodeNamesEqual([u'node', u'n2', u'n3'])
        self.assertGraphConnectionsEqual([
            (u'node.matrix', u'n2.translate'),
            (u'node.matrix', u'n3.inputMatrix'),
            (u'n3.outputTranslate', u'n2.translate'),
        ])

        # Create compound
        compound = self.ctrl.group_nodes([m2, m3])
        self.assertGraphNodeNamesEqual([u'node', u'component1'])
        self.assertGraphConnectionsEqual([
            (u'node.matrix', u'component1.inputMatrix'),
        ])

        # Enter compound
        self.ctrl.set_level(compound)
        self.assertGraphNodeNamesEqual([u'component1:inn', u'component1:out', u'n2'])
        self.assertGraphConnectionsEqual([
            (u'component1:inn.inputMatrix', u'n2.translate')
        ])


if __name__ == '__main__':
    unittest.main()

    # todo: test discovery of nodes in a specific compound space
