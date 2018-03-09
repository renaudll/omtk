import unittest

import pymel.core as pymel
from maya import cmds
import omtk_test
from omtk.core import session
from omtk.core.component import Component
from omtk.qt_widgets.nodegraph import NodeGraphController, NodeGraphRegistry
from omtk.qt_widgets.nodegraph.filters.filter_metadata import NodeGraphMetadataFilter
from omtk.qt_widgets.nodegraph.filters.filter_standard import NodeGraphStandardFilter
from omtk.qt_widgets.nodegraph.filters.filter_subgraph import NodeGraphSubgraphFilter
from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphModel
from omtk.qt_widgets.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel


class NodeGraphFilterTest(omtk_test.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.registry = NodeGraphRegistry()
        source_model = NodeGraphModel()
        self.model = GraphFilterProxyModel(model=source_model)
        self.ctrl = NodeGraphController(model=self.model)

        # Create a simple network
        cmds.file(new=True, force=True)
        self.node_1 = pymel.createNode('transform', name='a')
        self.node_2 = pymel.createNode('transform', name='b')
        self.model_1 = self.registry.get_node_from_value(self.node_1)
        self.model_2 = self.registry.get_node_from_value(self.node_2)
        self.ctrl.add_node(self.model_1)
        self.ctrl.add_node(self.model_2)

        # Hack: Force creation of callbacks
        self.model_1.on_added_to_scene()
        self.model_2.on_added_to_scene()

        # # Validate the graph is empty
        self.assertEqual(2, len(self.model.get_nodes()))
        # self.assertEqual(0, len(self.model.get_ports()))

    def test_delete_node(self):
        """
        Ensure that the model update when we delete a node the graph model update itself.
        """
        pymel.delete(self.node_1)
        self.node_1 = None
        self.assertEqual(1, len(self.model.get_nodes()))

