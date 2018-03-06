import pymel.core as pymel
from omtk.qt_widgets.nodegraph import nodegraph_filter

if False:
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel


class NodeGraphGraphProxyModel(nodegraph_filter.NodeGraphFilter):
    def __init__(self, level=None):
        super(NodeGraphGraphProxyModel, self).__init__()
        self._level = None
        if level:
            self.set_level(level)

    def get_level(self):
        # type: () -> NodeGraphNodeModel
        return self._level

    def set_level(self, level):
        # type: (NodeGraphNodeModel) -> None
        self._level = level

    # --- Implementation

    def can_show_node(self, node):
        # type: (NodeGraphNodeModel) -> bool
        """
        Determine if a node can be shown.
        A node can be shown if it is a children of the current subgraph level (None is root).
        """
        parent = node.get_parent()
        return parent == self._level

    def can_show_port(self, port):
        return True

    def can_show_connection(self, connection):
        # Get the node associated with the connection
        # Even if a connection is between two nodes, only one can have ownership.
        node_model = connection.get_parent()

        if not self.can_show_node(node_model):
            return False

        return super(NodeGraphGraphProxyModel, self).can_show_connection(node_model)
