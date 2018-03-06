from . import graph_model_abstract

if False:
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphModel


class NodeGraphGraphProxyModel(graph_model_abstract.NodeGraphAbstractModel):
    def __init__(self, model=None, filter=None):
        self._model = None
        if model:
            self.set_source_model(model)

    def reset(self):
        return self._model.reset()

    def get_model(self):
        # type: () -> NodeGraphModel
        return self._model

    def set_source_model(self, model):
        # type: (NodeGraphModel) -> None
        if self._model:
            self._model.onNodeAdded.disconnect(self.onNodeAdded)
            self._model.onNodeRemoved.disconnect(self.onNodeRemoved)
            self._model.onNodeMoved.disconnect(self.onNodeMoved)

        self._model = model

        model.onNodeAdded.connect(self.onNodeAdded)
        model.onNodeRemoved.connect(self.onNodeRemoved)
        model.onNodeMoved.connect(self.onNodeMoved)

    def can_show_node(self, node):
        return True

    def can_show_port(self, port):
        return True

    def can_show_connection(self, connection):
        return True

    # --- Abstract methods ---

    def iter_nodes(self):
        for node in self._model.get_nodes():
            if self.can_show_node(node):
                yield node

    def iter_ports(self):
        for port in self._model.iter_ports():
            if self.can_show_port(port):
                yield port

    def iter_node_ports(self, node):
        for port in self._model.iter_node_ports(node):
            if self.can_show_port(port):
                yield port

    def iter_connections(self):
        for connection in self._model.iter_connections():
            if self.can_show_connection(connection):
                yield connection

    def add_node(self, node, emit_signal=False):
        self._model.add_node(node, emit_signal=emit_signal)

    def remove_node(self, node, emit_signal=False):
        self._model.remove_node(node, emit_signal=emit_signal)

    def get_node_position(self, node):
        return self._model.get_node_position(node)

    def set_node_position(self, node, pos, emit_signal=True):
        self._model.set_node_position(node, pos, emit_signal=emit_signal)

    def add_port(self, port, emit_signal=False):
        self._model.add_port(port, emit_signal=emit_signal)

    def remove_port(self, port, emit_signal=False):
        self._model.remove_port(port, emit_signal=emit_signal)

    def add_connection(self, connection, emit_signal=False):
        self._model.add_connection(connection, emit_signal=emit_signal)

    def remove_connection(self, connection, emit_signal=False):
        self._model.remove_connection(connection, emit_signal=emit_signal)

    def expand_node(self, node):
        # type: (NodeGraphNodeModel) -> None
        self._model.expand_node(node)

    def expand_node_ports(self, node, inputs=True, outputs=True):
        # type: (NodeGraphNodeModel, bool, bool) -> None
        self._model.expand_node_ports(node, outputs=True, inputs=True)

    def expand_port_input_connections(self, port_model):
        self._model.expand_port_input_connections(port_model)

    def expand_port_output_connections(self, port_model):
        self._model.expand_port_output_connections(port_model)

    def expand_node_ports(self, node, inputs=True, outputs=True):
        # todo: find a cleaner way?
        # type: (NodeGraphNodeModel, bool, bool) -> None
        for port in self.get_node_ports(node):
            if outputs:
                self.expand_port_output_connections(port)
            if inputs:
                self.expand_port_input_connections(port)

        # Update cache
        self._expanded_nodes_ports.add(node)


