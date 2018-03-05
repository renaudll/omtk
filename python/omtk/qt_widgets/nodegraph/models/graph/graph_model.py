import abc
import logging
from collections import defaultdict

from omtk.vendor.Qt import QtCore

from . import graph_model_abstract

log = logging.getLogger('omtk.nodegraph')

# for type hinting
if False:
    from omtk.qt_widgets.nodegraph.models.node.node_base import NodeGraphNodeModel
    from omtk.qt_widgets.nodegraph.nodegraph_connection_model import NodeGraphConnectionModel
    from omtk.qt_widgets.nodegraph.port_model import NodeGraphPortModel


class NodeGraphModel(graph_model_abstract.NodeGraphAbstractModel):
    """
    Define a nodal network from various NodeGraph[Node/Port/Connection]Model instances.
    Subgraphs and filters can be implemented by feeding a NodeGraphRegistry through a NodeGraphProxyModel.
    NodeGraphRegistry are consumed
    """

    # onNodeAdded = QtCore.Signal(nodegraph_node_model_base.NodeGraphNodeModel)
    # onNodeRemoved = QtCore.Signal(nodegraph_node_model_base.NodeGraphNodeModel)
    # onNodeMoved = QtCore.Signal(nodegraph_node_model_base.NodeGraphNodeModel, QtCore.QPointF)
    # onPortAdded = QtCore.Signal(nodegraph_port_model.NodeGraphPortModel)
    # onPortRemoved = QtCore.Signal(nodegraph_port_model.NodeGraphPortModel)
    # onConnectionAdded = QtCore.Signal(nodegraph_connection_model.NodeGraphConnectionModel)
    # onConnectionRemoved = QtCore.Signal(nodegraph_connection_model.NodeGraphConnectionModel)

    def __init__(self):
        super(NodeGraphModel, self).__init__()  # initialize Qt signals

        self._nodes = set()
        self._ports = set()
        self._connections = set()
        self._pos_by_node = {}  # (k is a NodeGraphNodeModel, v is a QRectF).

        self._nodes_by_port = defaultdict(set)
        self._ports_by_nodes = defaultdict(set)

        self._ports_by_connection = defaultdict(set)
        self._connections_by_port = defaultdict(set)

    def reset(self):
        for node in list(self.get_nodes()):  # hack: prevent change during iteration
            self.remove_node(node, emit_signal=False)

        # gc check
        assert not self._nodes
        assert not self._ports
        assert not self._connections
        assert not self._pos_by_node
        assert not self._nodes_by_port
        assert not self._ports_by_nodes
        assert not self._ports_by_connection
        assert not self._connections_by_port

    # --- Node methods ---

    def get_nodes(self):
        # type: () -> List[NodeGraphNodeModel]
        return self._nodes

    def iter_nodes(self):
        return iter(self._nodes)

    def add_node(self, node, emit_signal=False):
        # type: (NodeGraphNodeModel, bool) -> None
        self._nodes.add(node)
        self._pos_by_node[node] = QtCore.QPointF(0.0, 0.0)  # todo: handle automatic positioning
        if emit_signal:
            self.onNodeAdded.emit(node)

    def remove_node(self, node, emit_signal=False):
        # type: (NodeGraphNodeModel, bool) -> None
        self._nodes.remove(node)
        self._pos_by_node.pop(node)

        # Remove node ports
        for port in list(self._ports_by_nodes[node]):  # hack: prevent change during iteration
            self.remove_port(port, emit_signal=emit_signal)
        self._ports_by_nodes.pop(node)

        if emit_signal:
            self.onNodeRemoved.emit(node)

    def get_node_position(self, node):
        # type: (NodeGraphNodeModel) -> None
        return self._pos_by_node[node]

    def set_node_position(self, node, pos, emit_signal=True):
        # type: (NodeGraphNodeModel, QtCore.QRectF, bool) -> None
        self._pos_by_node[node] = pos

        if emit_signal:
            self.onNodeMoved.emit(node, pos)

    # --- Port methods ---

    def get_ports(self):
        # todo: optimize?
        result = []
        for node in self.get_nodes():
            for port in node.iter_ports():
                result.append(port)
        return result
        # return self._ports

    def get_node_ports(self, node):
        return self._ports_by_nodes[node]

    def add_port(self, port, emit_signal=False):
        # type: (NodeGraphPortModel, bool) -> None
        self._ports.add(port)

        # Remove port connections
        node = port.get_parent()
        self._ports_by_nodes[node].add(port)
        self._nodes_by_port[port].add(node)

        if emit_signal:
            self.onPortAdded.emit(port)

    def remove_port(self, port, emit_signal=False):
        # type: (NodeGraphPortModel, bool) -> None
        self._ports.remove(port)

        # Remove port connections
        for connection in self._connections_by_port[port]:
            self.remove_connection(connection, emit_signal=emit_signal)
        self._connections_by_port.pop(port)

        # Update cache
        for node in self._nodes_by_port[port]:
            self._ports_by_nodes[node].remove(port)
        self._nodes_by_port.pop(port)

        if emit_signal:
            self.onPortRemoved.emit(port)

    # --- Connection methods ---

    def iter_connections(self):
        return iter(self._connections)

    def get_connections(self):
        return self._connections

    def add_connection(self, connection, emit_signal=False):
        # type: (NodeGraphConnectionModel, bool) -> None
        self._connections.add(connection)

        # Update cache
        port_src = connection.get_source()
        port_dst = connection.get_destination()
        self._connections_by_port[port_src].add(connection)
        self._connections_by_port[port_dst].add(connection)
        self._ports_by_connection[connection].add(port_src)
        self._ports_by_connection[connection].add(port_dst)

        if emit_signal:
            self.onPortAdded.emit(connection)

    def remove_connection(self, connection, emit_signal=False):
        # type: (NodeGraphConnectionModel, bool) -> None
        self._connections.remove(connection)

        # Update cache
        for port in self._ports_by_connection[connection]:
            self._connections_by_port[port].remove(connection)
        self._ports_by_connection.pop(connection)

        if emit_signal:
            self.onPortRemoved.emit(connection)

    # --- Exploration methods ---

    def iter_ports(self):
        for node in self.iter_nodes():
            for port in node.get_ports():
                yield port

    # --- clean this

    def expand_node_attributes(self, node):
        # type: (NodeGraphNodeModel) -> None
        """
        Show all available attributes for a PyFlowgraph Node.
        Add it in the pool if it didn't previously exist.
        :return:
        """
        for port in sorted(self.iter_ports(node)):
            self.add_port(port)
            # self.get_port_widget(port_model)

    def expand_node_connections(self, node_model, expand_downstream=True, expand_upstream=True):
        # type: (NodeGraphNodeModel) -> None
        if expand_upstream:
            for port_model in node_model.get_connected_output_attributes(self):
                self.expand_port_output_connections(port_model)
        if expand_downstream:
            for port_model in node_model.get_connected_input_attributes(self):
                self.expand_port_input_connections(port_model)

    def expand_port_input_connections(self, port_model):
        for connection_model in self.get_port_input_connections(port_model):
            self.get_connection_widget(connection_model)

    def expand_port_output_connections(self, port_model):
        for connection_model in self.get_port_output_connections(port_model):
            self.get_connection_widget(connection_model)
