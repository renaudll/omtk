from omtk_test import NodeGraphMockedMayaTestCase
from omtk.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel


class GraphFilterTestCase(NodeGraphMockedMayaTestCase):
    """
    OmtkTestCase that setup a simple graph network.
    GraphModel -> GraphFilterProxyModel
    """
    _cls_proxy_model = GraphFilterProxyModel

    @property
    def model(self):
        """
        :rtype: GraphFilterProxyModel
        """
        return super(GraphFilterTestCase, self).model
