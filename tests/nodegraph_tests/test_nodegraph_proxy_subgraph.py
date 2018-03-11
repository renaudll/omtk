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
        # self.model = GraphFilterProxyModel(filter=self.filter, model=self.model)
        self.model = GraphComponentProxyFilterModel(model=self.model)
        self.ctrl.set_model(self.model)

    def test_compound_creation(self):
        n1 = pymel.createNode('transform', name='n1')
        n2 = pymel.createNode('transform', name='n2')
        u1 = libRigging.create_utility_node(
            'multiplyDivide',
            input1X=n1.translateX,
            name='u1',
        )
        pymel.connectAttr(u1.outputX, n2.translateX)

        model_n1 = self.registry.get_node_from_value(n1)
        model_n2 = self.registry.get_node_from_value(n2)
        model_u1 = self.registry.get_node_from_value(u1)
        self.ctrl.add_node(model_n1)
        self.ctrl.add_node(model_n2)
        self.ctrl.add_node(model_u1)

        self.assertGraphNodeNamesEqual([u'n1', u'n2', u'u1'])

        # Create a subgroup (group nodes)
        component_model = self.ctrl.group_nodes([model_u1])
        self.assertGraphNodeNamesEqual([u'n1', u'n2', u'component00'])
        self.assetGraphConnectionsEqual([
            (u'n1.translateX', u'component00.input1X'),
            (u'component00.outputX', u'n2.translateX'),
        ])

        # Enter the subgrap
        self.ctrl.set_level(component_model)
        self.assertGraphNodeNamesEqual([u'component00:inn', u'u1', u'component00:out'])
        self.assetGraphConnectionsEqual([
            (u'component00:inn.input1X', u'u1.input1X'),
            (u'u1.outputX', u'component00:out.outputX'),
        ])

        # Exit the subgraph
        self.ctrl.set_level(None)
        self.assertGraphNodeNamesEqual([u'n1', u'n2', u'component00'])
        self.assetGraphConnectionsEqual([
            (u'n1.translateX', u'component00.input1X'),
            (u'component00.outputX', u'n2.translateX'),
        ])


if __name__ == '__main__':
    unittest.main()

    # todo: test discovery of nodes in a specific compound space
