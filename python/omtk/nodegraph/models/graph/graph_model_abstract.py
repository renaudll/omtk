import abc
import logging

from omtk.vendor.Qt import QtCore
from omtk.nodegraph.models.node import NodeModel
from omtk.nodegraph.models.port import PortModel
from omtk.nodegraph.models.connection import ConnectionModel
from omtk.nodegraph.signal import Signal


log = logging.getLogger('omtk.nodegraph')


class IGraphModel(object):

    """
    Define a nodal network from various NodeGraph[Node/Port/Connection]Model instances.
    Subgraphs and filters can be implemented by feeding a NodeGraphRegistry through a NodeGraphProxyModel.
    NodeGraphRegistry are consumed
    """
    # __metaclass__ = abc.ABCMeta

    # Signal emitted when a node is added in the model.
    onNodeAdded = Signal(NodeModel)

    # Signal emitted when a node is removed from the model.
    onNodeRemoved = Signal(NodeModel)

    # Signal emitted when a node position change.
    onNodeMoved = Signal(NodeModel, QtCore.QPointF)

    # Signal emitted when a node port is added in the model.
    onPortAdded = Signal(PortModel)

    # Signal emitted when a node port is removed from the model.
    onPortRemoved = Signal(PortModel)

    # Signal emitted when a port connection is added in the model.
    onConnectionAdded = Signal(ConnectionModel)

    # Signal emitted when a port connection is removed from the model.
    onConnectionRemoved = Signal(ConnectionModel)

    # Signal emitted before the model internal state has been invalidated.
    onAboutToBeReset = Signal()

    # Signal emitted after the model internal state has been invalidated.
    onReset = Signal()

    def __init__(self, registry):
        super(IGraphModel, self).__init__()
        self._registry = None
        self.set_registry(registry)

    @property
    def registry(self):
        """
        Getter for the REGISTRY_DEFAULT.
        :return: The REGISTRY_DEFAULT
        :rtype: omtk.nodegraph.NodeGraphRegistry
        """
        return self._registry

    def get_registry(self):
        """
        Return the REGISTRY_DEFAULT associated with the graph.
        The REGISTRY_DEFAULT is the interface to any DCC application like Maya.
        :return:
        :rtype omtk.nodegraph.NodeGraphRegistry
        """
        return self._registry

    def set_registry(self, registry):
        """
        The the REGISTRY_DEFAULT associated with the graph.
        The REGISTRY_DEFAULT is the interface to any DCC application like Maya.
        :param NodeGraphRegistry registry: The graph new REGISTRY_DEFAULT.
        """
        self._registry = registry

    @abc.abstractmethod
    def reset(self):
        # type: () -> None
        """"""
        self.onAboutToBeReset.emit()
        self.onReset.emit()

    def dump(self):
        nodes = sorted(node.get_name() for node in self.get_nodes())
        ports = sorted(port.get_path() for port in self.get_ports())
        connections = sorted(connection.dump() for connection in self.get_connections())

        return {
            "nodes": nodes,
            "ports": ports,
            "connections": connections,
        }

    # --- Node methods ---

    @abc.abstractmethod
    def iter_nodes(self):
        """
        Yield all the nodes visible in the graph.
        :return: A generator that yield NodeModel instances.
        :rtype: Generator[omtk.nodegraph.NodeModel]
        """

    def get_nodes(self):
        """
        Return all node visible in the graph.
        :return: A list of NodeModel instances.
        :rtype: List[omtk.nodegraph.NodeModel]
        """
        return list(self.iter_nodes())

    @abc.abstractmethod
    def add_node(self, node, emit=False):  # TODO: Why emit if False?
        """
        Add a node to the graph.
        :param NodeModel node: A NodeModel instance.
        :param bool emit: If True, the onNodeAdded signal will emitted.
        """

    @abc.abstractmethod
    def add_all_nodes(self, emit=True):
        """
        Ensure that all registered nodes are in the graph.
        :param bool emit: If True, the `onNodeAdded` signal will be emitted.
        """

    @abc.abstractmethod
    def remove_node(self, node, emit=False):  # TODO: Why emit if False?
        """
        Remove a node from the graph.
        :param omtk.nodegraph.NodeModel node: The node to remove.
        :param bool emit: If True, the Qt Signal ``onNodeRemoved`` will be emitted.
        """

    @abc.abstractmethod
    def is_node_visible(self, node):
        """
        Query a node visibility in the graph.
        :param omtk.nodegraph.NodeModel node: The node to inspect.
        :return: True if the node is visible. False otherwise.
        :rtype: bool
        """

    @abc.abstractmethod
    def get_node_position(self, node):
        """
        Query a node position in the graph.
        :param omtk.nodegraph.NodeModelnode: The node to inspect.
        :return: The node position in the graph.
        :rtype: QtCOre.QRectF
        """

    @abc.abstractmethod
    def set_node_position(self, node, pos, emit=True):
        """
        Change a node position in the graph.
        :param omtk.nodegraph.NodeModel node: The node to move. 
        :param QtCore.QRectF pos: The new position of the node. 
        :param emit: If True, the ``onNodeMoved`` Qt Signal will be emitted.
        """

    # --- Port methods ---

    @abc.abstractmethod
    def iter_ports(self):
        """
        Iterate through all the ports in the graph.
        :return: A port generator
        :rtype: Generator[PortModel]
        """
        return
        yield

    def get_ports(self):
        """
        Return all node visible in the graph.
        :return: A list of port
        :rtype: List[PortModel]
        """
        return list(self.iter_ports())

    @abc.abstractmethod
    def add_port(self, port, emit=False):
        """
        Add a port to the graph.
        :param PortModel port: The port to add
        :param bool emit: If True, the `onPortAdded` signal will be emitted.
        """

    @abc.abstractmethod
    def remove_port(self, port, emit=False):
        """
        Remove a port from the graph.
        :param PortModel port: The port to remove
        :param emit: If True, the `onPortRemoved` signal will be emitted.
        """

    @abc.abstractmethod
    def is_port_visible(self, port):
        """
        Determine if a port is visible.
        :param PortModel port: The port to query
        :return: True if the port is visible. False otherwise.
        :rtype: bool
        """

    # --- Connection methods ---

    @abc.abstractmethod
    def iter_connections(self):
        """
        Iterate through all graph connections.
        :return: A connection generator
        :rtype Generator[ConnectionModel]
        """

    @abc.abstractmethod
    def get_connections(self):
        """
        Get all the graph connections.
        :return: A list of connections
        :rtype: List[ConnectionModel]
        """
        return list(self.iter_connections())

    @abc.abstractmethod
    def add_connection(self, connection, emit=False):
        """
        Add a connection to the graph.
        :param ConnectionModel connection: The connection to add
        :param bool emit: If True, the `onConnectionAdded` signal will be emitted.
        """

    @abc.abstractmethod
    def remove_connection(self, connection, emit=False):
        """
        Remove a connection from the graph.
        :param ConnectionModel connection: The connection to remove
        :param bool emit: If True, the `onConnectionRemoved` signal will be emitted.
        """

    @abc.abstractmethod
    def is_connection_visible(self, connection):
        """
        Determine if a connection is visible.
        :param ConnectionModel connection: The connection to query.
        :return: True if the connection is visible. False otherwise.
        :rtype: bool
        """

    # --- Exploration methods that add nothing to the graph ---

    def iter_node_ports(self, node):
        """
        Yield all ports inside a node model. This don't add the port into the graph.
        :param node: A NodeModel instance.
        :return: A generator that yield PortModel.
        :rtype: Generator[PortModel]
        """
        return
        yield

    def get_node_ports(self, node):
        # type: (NodeModel) -> List[PortModel]
        return list(self.iter_node_ports(node))

    def iter_node_input_connections(self, node):
        """
        Iterate through all connection where the destination is a port of the provided node.
        :param node: The node which is the destination of the connection we want.
        :type node: NodeModel
        :return: Generator[ConnectionModel]
        """
        for port in self.iter_node_ports(node):
            for connection in self.iter_port_input_connections(port):
                yield connection

    def get_node_input_connections(self, node):
        return list(self.iter_node_input_connections(node))

    def iter_node_output_connections(self, node):
        """
        Iterate through all connections where the source is a port of the provided node.
        :param node: The node which is the source of the connection we want.
        :type node: NodeModel
        :return: Generator[ConnectionModel]
        """
        for port in self.iter_node_ports(node):
            for connection in self.iter_port_output_connections(port):
                yield connection

    def get_node_output_connections(self, node):
        return list(self.iter_node_output_connections(node))

    def iter_port_connections(self, port):
        # type: (PortModel) -> Generator[ConnectionModel]
        for connection in self.iter_port_input_connections(port):
            yield connection
        for connection in self.iter_port_output_connections(port):
            yield connection

    def get_port_connections(self, port):
        return list(self.iter_port_connections(port))

    def iter_port_input_connections(self, port):
        # type: (PortModel) -> list[ConnectionModel]
        """
        Control what input connection models are exposed for the provided port model.
        :param port: The destination port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as destination.
        """
        for connection in port.get_input_connections():
            yield connection

    def get_port_input_connections(self, port):
        return list(self.iter_port_input_connections(port))  # cannot memoize a generator

    def iter_port_output_connections(self, port):
        # type: (PortModel) -> List[PortModel]
        """
        Control what output connection models are exposed for the provided port model.
        :param port: The source port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as source.
        """
        for connection in port.get_output_connections():
            yield connection

    def get_port_output_connections(self, port):
        return list(self.iter_port_output_connections(port))  # cannot memoize a generator

    def iter_node_connections(self, node, inputs=True, outputs=True):
        # type: (NodeModel, bool, bool) -> Generator[ConnectionModel]
        for port in self.iter_node_ports(node):
            if outputs:
                for connection in self.iter_port_output_connections(port):
                    yield connection
            if inputs:
                for connection in self.iter_port_input_connections(port):
                    yield connection

    # --- Utility methods ---
    def expand_node_ports(self, node):
        """
        Show all available attributes for a PyFlowgraph Node.
        Add it in the pool if it didn't previously exist.
        :param NodeModel node: The node to scan.
        """
        for port in sorted(self.iter_node_ports(node)):
            self.add_port(port, emit=True)

    def expand_node_connections(self, node, inputs=True, outputs=True):
        for port in self.iter_node_ports(node):
            if inputs:
                for connection in self.iter_port_input_connections(port):
                    self.add_connection(connection)
            if outputs:
                for connection in self.iter_port_output_connections(port):
                    self.add_connection(connection)

    def expand_port_input_connections(self, port):
        # type: (PortModel) -> None
        for connection in self.iter_port_input_connections(port):
            self.add_connection(connection)

    def expand_port_output_connections(self, port):
        # type: (PortModel) -> None
        for connection in self.iter_port_output_connections(port):
            self.add_connection(connection)

    # --- Filtering methods ---
    # do we want these?

    def intercept_node(self, node):
        yield node

    def intercept_port(self, port):
        yield port

    def intercept_connection(self, connection):
        yield connection

    def is_port_input(self, port):
        # type: (PortModel) -> bool
        return port.is_writable()

    def is_port_output(self, port):
        # type: (PortModel) -> bool
        return port.is_readable()
