from omtk.core import preferences
from omtk.qt_widgets.widget_nodegraph import nodegraph_node_model_dagnode


class NodeGraphControllerFilter(object):
    """
    Define filtering rules for a NodeGraphController.
    """
    def __init__(self, controller):
        self._controller = controller

    def can_show_node(self, node_model):
        # type: (NodeGraphNodeModel) -> bool
        # Some DagNode types might be blacklisted.
        if isinstance(node_model, nodegraph_node_model_dagnode.NodeGraphDagNodeModel):
            blacklist = preferences.get_preferences().get_nodegraph_blacklisted_nodetypes()
            node = node_model.get_metadata()
            nodetype = node.type()
            if nodetype in blacklist:
                return False
        return True

    def can_show_port(self, port_model):
        # type: (NodeGraphPortModel) -> bool
        """
        Check if a port is displayable according to the filter.
        The default behavior is to check if the port is considered "interesting".
        :param port_model: The port to inspect.
        :return: True if we can display this port.
        """
        return port_model.is_interesting()

    def can_show_connection(self, connection_model):
        # type: (NodeGraphConnectionModel) -> bool
        return True