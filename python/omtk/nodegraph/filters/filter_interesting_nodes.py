from omtk.core import preferences
from omtk.nodegraph import NodeGraphFilter


class InterestingNodePortFilter(NodeGraphFilter):
    """
    Filter than only let node and port juged as "interesting" through.
    """

    # def __init__(self, model=None):
    #     self.model = None
    #     if model:
    #         self.set_model(model)
    #
    #     self.hide_libserialization_network = False

    def _is_node_interesting(self, node):
        # Some DagNode types might be blacklisted.
        from omtk.nodegraph.models._deprecated import node_dg
        # todo: move to filter_standard

        if isinstance(node, node_dg.NodeGraphDgNodeModel):
            blacklist = preferences.get_preferences().get_nodegraph_blacklisted_nodetypes()
            node = node.get_metadata()
            nodetype = node.type()
            if nodetype in blacklist:
                return False
        return True

    def can_show_node(self, node):
        """
        Query if a node should be displayed.
        :param omtk.nodegraph.NodeModel node: The node to query.
        :return: True if the node should be displayed.
        :rtype: bool
        """
        return node.is_interesting()

    def can_show_port(self, port):
        """
        Check if a port is displayable according to the filter.
        The default behavior is to check if the port is considered "interesting".
        :param PortModel port: The port to inspect.
        :return: True if we can display this port.
        :rtype: bool
        """
        node = port.get_parent()
        if not self.can_show_node(node):
            return False

        if not port.is_interesting():
            return False
        
        return super(InterestingNodePortFilter, self).can_show_port(port)

    # def can_show_connection(self, connection):
    #     return True

    # def intercept_node(self, node):
    #     """
    #     Intercept a node to show something else instead
    #     :param NodeModel node: The node to intercept
    #     :return: A node iterator
    #     :rtype: Generator[NodeModel]
    #     """
    #     yield node
    #
    # def intercept_port(self, port):
    #     """
    #     Intercept a port to show something else instead
    #     :param PortModel port: The port to intercept
    #     :return: A port iterator
    #     :rtype: Generator[PortModel]
    #     """
    #     yield port
    #
    # def intercept_connection(self, connection):
    #     """
    #     Intercept a connection to show something else instead
    #     :param ConnectionModel connection: The connection to intercept
    #     :return: A connection iterator
    #     :rtype: Generator[ConnectionModel]
    #     """
    #     """Intercept a connection to show something else instead."""
    #     yield connection
