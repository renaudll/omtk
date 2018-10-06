from . import graph_model_abstract


class NodeGraphGraphProxyModel(graph_model_abstract.IGraphModel):
    """
    Provides a base class for proxy item models that can do sorting,
    filtering or other data processing tasks on a GraphModel.
    """

    def __init__(self, model=None):
        super(NodeGraphGraphProxyModel, self).__init__()
        self._model = None
        if model:
            self.set_source_model(model)

    def reset(self):
        self._model.reset()
        super(NodeGraphGraphProxyModel, self).reset()

    def get_model(self):
        """
        :return: The graph we are filtering.
        :rtype: GraphModel
        """
        return self._model

    def set_source_model(self, model):
        """
        Set the model to filter by the proxy.
        :param omtk.nodegraph.IGraphModel model:
        """
        # TODO: Is this necessary? Can gc handle it?
        # if self._model:
        #     self._disconnect_model(self._model)

        self._model = model

        self._connect_model(model)

    def _connect_model(self, model):
        """
        Connect a model signal to our internal signals.
        :param omtk.nodegraph.IGraphModel model: The model to connect from
        """
        model.onNodeAdded.connect(self.onNodeAdded.emit)
        model.onNodeRemoved.connect(self.onNodeRemoved.emit)
        model.onNodeMoved.connect(self.onNodeMoved.emit)
        # model.onPortAdded.connect(self.onPortAdded.emit)
        model.onPortAdded.connect(self.on_port_added)
        model.onPortRemoved.connect(self.onPortRemoved.emit)
        model.onConnectionAdded.connect(self.onConnectionAdded.emit)
        model.onConnectionRemoved.connect(self.onConnectionRemoved.emit)
        model.onAboutToBeReset.connect(self.onAboutToBeReset.emit)
        model.onReset.connect(self.onReset.emit)

    def _disconnect_model(self, model):
        """
        Disconnect a model signal to our internal signals.
        :param omtk.nodegraph.IGraphModel model: The model to disconnect from
        """
        model.onNodeAdded.disconnect(self.onNodeAdded)
        model.onNodeRemoved.disconnect(self.onNodeRemoved)
        model.onNodeMoved.disconnect(self.onNodeMoved)
        model.onPortAdded.disconnect(self.onPortAdded)
        model.onPortRemoved.disconnect(self.onPortRemoved)
        model.onConnectionAdded.disconnect(self.onConnectionAdded)
        model.onConnectionRemoved.disconnect(self.onConnectionRemoved)
        model.onAboutToBeReset.disconnect(self.onAboutToBeReset)
        model.onReset.disconnect(self.onReset)

    def on_port_added(self, port):
        # Prevent an undesirable port from being shown if we don't care about it.
        for yielded in self.intercept_port(port):
            self.onPortAdded.emit(yielded)

    # --- Filter methods ---

    def intercept_node(self, node):
        """
        Used to filter nodes from the source graph.
        :param omtk.nodegraph.NodeModel node:
        :return: A node generator
        :rtype: Generator[omtk.nodegraph.NodeModel]
        """
        yield node

    def intercept_port(self, port):
        """
        Used to filter ports from the source graph.
        :param omtk.nodegraph.PortModel port:
        :return: A port generator
        """
        yield port

    def intercept_connection(self, connection):
        """
        Used to filter connections from the source graph.
        :param connection:
        :return: A connection generator
        :rtype: Generator[omtk.nodegraph.ConnectionModel]
        """
        yield

    # --- Abstract methods ---

    def iter_nodes(self):
        for node in self._model.get_nodes():
            # yield node
            for yielded in self.intercept_node(node):
                yield yielded

    # def get_nodes(self):
    #     return list(self.iter_nodes())

    def iter_ports(self):
        for port in self._model.iter_ports():
            # yield port
            for yielded in self.intercept_port(port):
                yield yielded

    # def get_ports(self):
    #     return list(self.iter_ports())

    def iter_connections(self):
        for connection in self._model.iter_connections():
            # yield connection
            for yielded in self.intercept_connection(connection):
                yield yielded

    # def get_connections(self):
    #     return list(self.iter_connections())

    # --- Exploration methods ---

    def iter_node_ports(self, node):
        for port in self._model.iter_node_ports(node):
            for yielded in self.intercept_port(port):
                yield yielded

    # Note: Not needed since iter_port_input_connections() and inter_port_outputs_connections()
    # are already taken care of.

    # def iter_port_connections(self, port):
    #     # type: (PortModel) -> Generator[ConnectionModel]
    #     for connection in self.iter_port_input_connections(port):
    #         yield self.intercept_connection(connection)
    #     for connection in self.iter_port_output_connections(port):
    #         yield self.intercept_connection(connection)

    def iter_port_input_connections(self, port):
        # type: (PortModel) -> List[NodeGraphConnectionModel]
        """
        Control what input connection models are exposed for the provided port model.
        :param model: The destination port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as destination.
        """
        for connection in self._model.iter_port_input_connections(port):
            for yielded in self.intercept_connection(connection):
                yield yielded

    def iter_port_output_connections(self, port):
        """
        Control what output connection models are exposed for the provided port model.
        :param omtk.nodegraph.PortModel port: The source port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as source.
        :rtype: List[omtk.nodegraphPortModel]
        """
        for connection in self._model.iter_port_output_connections(port):
            for yielded in self.intercept_connection(connection):
                yield yielded

    def add_node(self, node, emit=True):
        """
        Add a node to the graph.
        :param GraphModel node: The node to add.
        :param bool emit: If True, the ``onNodeAdded`` Qt Signal will be emitted.
        :rtype: None
        """
        for yielded in self.intercept_node(node):
            self._model.add_node(yielded, emit=emit)

    def remove_node(self, node, emit=True):
        self._model.remove_node(node, emit=emit)

    def is_node_visible(self, node):
        return self._model.is_node_visible(node)

    def get_node_position(self, node):
        return self._model.get_node_position(node)

    def set_node_position(self, node, pos, emit=True):
        self._model.set_node_position(node, pos, emit=emit)

    def add_port(self, port, emit=True):
        # todo: check if we can add port?
        self._model.add_port(port, emit=emit)

    def remove_port(self, port, emit=True):
        self._model.remove_port(port, emit=emit)

    def is_port_visible(self, port):
        return self._model.is_port_visible()

    def is_port_input(self, port):
        return self.get_model().is_port_input(port)

    def is_port_output(self, port):
        return self.get_model().is_port_output(port)

    def add_connection(self, connection, emit=True):
        # todo: check if we can add connection?
        self._model.add_connection(connection, emit=emit)

    def remove_connection(self, connection, emit=True):
        self._model.remove_connection(connection, emit=emit)

    def is_connection_visible(self, connection):
        self._model.is_connection_visible(connection)

    # def expand_node_connections(self, node, inputs=True, outputs=True):
    #     """Redirect any connection expansion to the soure model."""
    #     self._model.expand_node_connections(node, inputs=inputs, outputs=outputs)
    #
    # def expand_port_input_connections(self, port):
    #     """Redirect any connection expansion to the soure model."""
    #     self._model.expand_port_input_connections(port)
    #
    # def expand_port_output_connections(self, port):
    #     """Redirect any connection expansion to the soure model."""
    #     self._model.expand_port_output_connections(port)
