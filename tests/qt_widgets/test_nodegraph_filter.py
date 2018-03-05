import logging
import unittest

import pymel.core as pymel
from omtk.qt_widgets.nodegraph.nodegraph_controller import NodeGraphController
from omtk.qt_widgets.nodegraph.nodegraph_registry import NodeGraphRegistry
from omtk.qt_widgets.nodegraph.filters.widget_filter_base import CustomNodeGraphFilter
from omtk.qt_widgets.nodegraph.models.graph.graph_model import NodeGraphModel
from omtk.qt_widgets.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel
from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel


def _node_to_json(g, n):
    # type: (NodeGraphNodeModel) -> dict
    return {
        # 'name': n.get_name(),
        'ports': [p.get_name() for p in sorted(g.get_node_ports(n))],
    }


def _graph_to_json(g):
    # type: (NodeGraphModel) -> dict
    return {n.get_name(): _node_to_json(g, n) for n in g.get_nodes()}


class NodeGraphFilterTest(unittest.TestCase):
    def test_filter(self):
        """
        Ensure that we are able to:

        - Apply a NodeGraphFilter
        - UnApply a NodeGraphFilter
        """
        registry = NodeGraphRegistry()

        source_model = NodeGraphModel()
        graph = GraphFilterProxyModel(model=source_model)
        ctrl = NodeGraphController(model=graph)

        # Validate the graph is empty
        self.assertEqual(0, len(graph.get_nodes()))
        self.assertEqual(0, len(graph.get_ports()))

        # Configure a basic network
        n1 = pymel.createNode('transform', name='a')
        m1 = registry.get_node_from_value(n1)
        graph.add_node(m1)
        ctrl.expand_node_attributes(m1)

        # Validate we see the new node
        self.assertEqual(1, len(graph.get_nodes()))
        self.assertEqual(228, len(graph.get_ports()))

        # Apply a filter
        filter_ = CustomNodeGraphFilter()
        ctrl.set_filter(filter_)

        # Validate we see the new node with les attributes
        self.assertEqual(14, len(graph.get_ports()))
        snapshot = _graph_to_json(graph)
        self.assertDictEqual(
            snapshot,
            {
                'a': {
                    'ports': [
                        'hierarchy',
                        'matrix',
                        'rotateX',
                        'rotateY',
                        'rotateZ',
                        'scaleX',
                        'scaleY',
                        'scaleZ',
                        'translateX',
                        'translateY',
                        'translateZ',
                        'visibility',
                        'worldMatrix',
                        'worldMatrix[1]'
                    ]
                },
            }
        )

        # Remove the filter
        ctrl.set_filter(None)

        # Validate we see the new node
        self.assertEqual(1, len(graph.get_nodes()))
        self.assertEqual(228, len(graph.get_ports()))
