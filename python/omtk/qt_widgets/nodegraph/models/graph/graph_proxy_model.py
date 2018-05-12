from . import graph_model_abstract

if False:
    from typing import Generator
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphModel


class NodeGraphGraphProxyModel(graph_model_abstract.NodeGraphAbstractModel):
    """
    Provides a base class for proxy item models that can do sorting,
    filtering or other data processing tasks on a NodeGraphModel.
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
        # type: () -> NodeGraphModel
        return self._model

    def set_source_model(self, model):
        # type: (NodeGraphModel) -> None
        if self._model:
            self._model.onNodeAdded.disconnect(self.onNodeAdded)
            self._model.onNodeRemoved.disconnect(self.onNodeRemoved)
            self._model.onNodeMoved.disconnect(self.onNodeMoved)
            self._model.onPortAdded.disconnect(self.onPortAdded)
            self._model.onPortRemoved.disconnect(self.onPortRemoved)
            self._model.onConnectionAdded.disconnect(self.onConnectionAdded)
            self._model.onConnectionRemoved.disconnect(self.onConnectionRemoved)
            self._model.onAboutToBeReset.disconnect(self.onAboutToBeReset)
            self._model.onReset.disconnect(self.onReset)

        self._model = model

        model.onNodeAdded.connect(self.onNodeAdded.emit)
        model.onNodeRemoved.connect(self.onNodeRemoved.emit)
        model.onNodeMoved.connect(self.onNodeMoved.emit)
        model.onPortAdded.connect(self.onPortAdded.emit)
        model.onPortRemoved.connect(self.onPortRemoved.emit)
        model.onConnectionAdded.connect(self.onConnectionAdded.emit)
        model.onConnectionRemoved.connect(self.onConnectionRemoved.emit)
        model.onAboutToBeReset.connect(self.onAboutToBeReset.emit)
        model.onReset.connect(self.onReset.emit)

    # --- Filter methods ---

    def intercept_node(self, node):
        yield node

    def intercept_port(self, port):
        yield port

    def intercept_connection(self, connection):
        yield

    # --- Abstract methods ---

    def iter_nodes(self):
        for node in self._model.get_nodes():
            yield node
            # for yielded in self.intercept_node(node):
            #     yield yielded

    def iter_ports(self):
        for port in self._model.iter_ports():
            yield port
            # for yielded in self.intercept_port(port):
            #     yield yielded

    def iter_connections(self):
        for connection in self._model.iter_connections():
            yield connection
            # for yielded in self.intercept_connection(connection):
            #     yield yielded

    # --- Exploration methods ---

    def iter_node_ports(self, node):
        for port in self._model.iter_node_ports(node):
            for yielded in self.intercept_port(port):
                yield yielded

    # Note: Not needed since iter_port_input_connections() and inter_port_outputs_connections()
    # are already taken care of.

    # def iter_port_connections(self, port):
    #     # type: (NodeGraphPortModel) -> Generator[NodeGraphConnectionModel]
    #     for connection in self.iter_port_input_connections(port):
    #         yield self.intercept_connection(connection)
    #     for connection in self.iter_port_output_connections(port):
    #         yield self.intercept_connection(connection)

    def iter_port_input_connections(self, port):
        # type: (NodeGraphPortModel) -> List[NodeGraphConnectionModel]
        """
        Control what input connection models are exposed for the provided port model.
        :param model: The destination port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as destination.
        """
        for connection in self._model.iter_port_input_connections(port):
            for yielded in self.intercept_connection(connection):
                yield yielded

    def iter_port_output_connections(self, port):
        # type: (NodeGraphPortModel) -> List[NodeGraphPortModel]
        """
        Control what output connection models are exposed for the provided port model.
        :param port: The source port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as source.
        """
        for connection in self._model.iter_port_output_connections(port):
            for yielded in self.intercept_connection(connection):
                yield yielded

    def add_node(self, node, emit_signal=True):
        for yielded in self.intercept_node(node):
            self._model.add_node(yielded, emit_signal=emit_signal)

    def remove_node(self, node, emit_signal=True):
        self._model.remove_node(node, emit_signal=emit_signal)

    def is_node_visible(self, node):
        return self._model.is_node_visible(node)

    def get_node_position(self, node):
        return self._model.get_node_position(node)

    def set_node_position(self, node, pos, emit_signal=True):
        self._model.set_node_position(node, pos, emit_signal=emit_signal)

    def add_port(self, port, emit_signal=True):
        # todo: check if we can add port?
        self._model.add_port(port, emit_signal=emit_signal)

    def remove_port(self, port, emit_signal=True):
        self._model.remove_port(port, emit_signal=emit_signal)

    def is_port_visible(self, port):
        return self._model.is_port_visible()

    def is_port_input(self, port):
        return self.get_model().is_port_input(port)

    def is_port_output(self, port):
        return self.get_model().is_port_output(port)

    def add_connection(self, connection, emit_signal=True):
        # todo: check if we can add connection?
        self._model.add_connection(connection, emit_signal=emit_signal)

    def remove_connection(self, connection, emit_signal=True):
        self._model.remove_connection(connection, emit_signal=emit_signal)

    def is_connection_visible(self, connection):
        self._model.is_connection_visible(connection)
