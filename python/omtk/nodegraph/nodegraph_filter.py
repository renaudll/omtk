class NodeGraphFilter(object):
    """
    Define filtering rules for a NodeGraphController.
    """
    # For optimisation purpose, you can turn one of theses flags
    # off if you know you are not filtering.
    #
    # For example if you are not filtering nodes, when filtering a port,
    # we won't check if the port is in a node that can be filtered.
    # filter_nodes = True
    # filter_ports = True
    # filter_connections = True

    def __init__(self, model=None):
        self.model = None
        if model:
            self.set_model(model)

    def get_model(self):
        """
        Get the graph affected by the filter.
        :return: A graph
        :rtype: GraphModel
        """
        return self._model

    def set_model(self, model):
        """
        Set the graph affected by the filter.
        :param GraphModel model: The graph to bind
        """
        self._model = model

    def can_show_node(self, node):
        """
        Query a node visibility.
        :param NodeModel node: The node to query.
        :return: True if the node is visible. False otherwise.
        :rtype: bool
        """
        return True

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
        return True

    def can_show_connection(self, connection):
        """

        :param omtk.nodegraph.ConnectionModel connection:
        :return: True if the connect can be shown, False if it is filtered out.
        """
        port_src = connection.get_source()
        if not self.can_show_port(port_src):
            return False

        port_dst = connection.get_destination()
        if not self.can_show_port(port_dst):
            return False

        return True

    def intercept_node(self, node):
        """
        Intercept a node to show something else instead
        :param NodeModel node: The node to intercept
        :return: A node iterator
        :rtype: Generator[NodeModel]
        """
        yield node

    def intercept_port(self, port):
        """
        Intercept a port to show something else instead
        :param PortModel port: The port to intercept
        :return: A port iterator
        :rtype: Generator[PortModel]
        """
        yield port

    def intercept_connection(self, connection):
        """
        Intercept a connection to show something else instead
        :param ConnectionModel connection: The connection to intercept
        :return: A connection iterator
        :rtype: Generator[ConnectionModel]
        """
        yield connection
