import omtk_test
from maya import cmds
from omtk.nodegraph import NodeGraphRegistry, GraphModel, NodeGraphController
from omtk.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel


class GraphFilterTestCase(omtk_test.NodeGraphTestCase):
    """
    TestCase that setup a simple graph network.
    GraphModel -> GraphFilterProxyModel
    """
    def setUp(self):
        super(GraphFilterTestCase, self).setUp()

        self.registry = NodeGraphRegistry()
        source_model = GraphModel(self.registry)
        self.model = GraphFilterProxyModel(model=source_model)
        self.ctrl = NodeGraphController(self.registry, model=self.model)
        cmds.file(new=True, force=True)

        # Validate the graph is empty
        # self.assertEqual(0, len(self.model.get_nodes()))
        # self.assertEqual(0, len(self.model.get_ports()))
