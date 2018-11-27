import itertools
import logging
import string

from omtk.nodegraph.bindings.base import ISession
from omtk.nodegraph.cache import CachedDefaultDict
from omtk.nodegraph.signal import Signal
from omtk.vendor.mock_maya.base import MockedConnection
from omtk.vendor.mock_maya.base import MockedNode
from omtk.vendor.mock_maya.base import MockedPort

log = logging.getLogger(__name__)


class MockedSession(ISession):
    """
    Maya mock that try to match pymel symbols.

    :param conf: The configuration of the session. (registered node types)
    If nothing is provided the default configuration will be used.
    """
    nodeAdded = Signal(MockedNode)
    nodeRemoved = Signal(MockedNode)
    portAdded = Signal(MockedPort)
    portRemoved = Signal(MockedPort)
    connectionAdded = Signal(MockedConnection)
    connectionRemoved = Signal(MockedConnection)

    def __init__(self, preset=None):
        super(MockedSession, self).__init__()
        self.nodes = set()
        self.ports = set()
        self.connections = set()
        self.selection = set()
        self.ports_by_node = CachedDefaultDict(set)
        self.presets = preset

    # --- Public methods

    def exists(self, dagpath):
        return bool(self.get_node_by_match(dagpath, strict=False))

    def _unique_name(self, prefix):
        for i in itertools.count(1):
            name = "{}{}".format(prefix, i)
            if not self.exists(name):
                return name

    def get_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def get_node_by_match(self, pattern, strict=True):
        for node in self.nodes:
            if node._match(pattern):
                return node
        if strict:
            raise ValueError("No object matches name: {}".format(pattern))
        return None

    def get_port_by_match(self, pattern):
        for port in self.ports:
            if port._match(pattern):
                return port
        return None

    def get_connection_by_ports(self, src, dst):
        """
        Get an existing connection from two ports

        :param MockedPort src: The source port
        :param MockedPort dst: The destination port
        :return: An existing connection. None otherwise.
        :rtype: MockedConnection or None
        """
        return next((conn for conn in self.connections if conn.src is src and conn.dst is dst), None)

    def create_node(self, node_type, name=None, emit=True):
        """
        Create a new node in the scene.

        :param str node_type: The type of the node.
        :param str name: The name of the node.
        :param bool emit: If True, the `portAdded` signal will be emmited.
        :return: The created node
        :rtype: MockedNode
        """
        # TODO: cmds.createNode("locator") -> "locatorShape"
        if name and not self.exists(name):
            pass
        else:
            prefix = name if name else node_type
            prefix = prefix.rstrip(string.digits)
            name = self._unique_name(prefix)

        node = MockedNode(self, node_type, name)
        self.nodes.add(node)

        if emit:
            signal = self.nodeAdded
            log.debug("%s emited with %s", signal, node)
            signal.emit(node)

        # Add port from configuration if needed
        if self.presets:
            preset = self.presets.get(node_type)
            if preset:
                preset.apply(self, node)

        return node

    def remove_node(self, node, emit=True):
        """
        Remove a node from the graph.
        :param node:
        :param bool emit: If True, the `portAdded` signal will be emmited.
        """
        # Remove any port that where used by the node.
        ports = [port for port in self.ports if port.node is node]
        for port in ports:
            self.remove_port(port, emit=emit)

        if emit:
            self.nodeRemoved.emit(node)

        self.nodes.remove(node)

    def create_port(self, node, name, emit=True, **kwargs):
        """
        Create a new port in the scene.

        :param MockedNode node: The port parent node
        :param name: The name of the port
        :return: The create port
        :rtype: MockedPort
        """
        port = MockedPort(node, name, **kwargs)
        self.ports_by_node.get(node).add(port)
        self.ports.add(port)
        if emit:
            self.portAdded.emit(port)
        return port

    def remove_port(self, port, emit=True):
        """
        Remove a port from the graph.
        :param port:
        :param emit:
        :return:
        """
        # Remove any connection that used the port
        connections = [conn for conn in self.connections if conn.src is port or conn.dst is port]
        for conn in connections:
            self.remove_connection(conn, emit=emit)

        if emit:
            self.portRemoved.emit(port)

        self.ports.remove(port)

    def remove_node_port(self, node, name, emit=True):
        """
        :param MockedNode node:
        :param name:
        :param emit:
        :return:
        """
        port = self.get_node_port_by_name(node, name)
        self.remove_port(port, emit=emit)

    def create_connection(self, port_src, port_dst, emit=True):
        """
        Create a new connection in the scene.

        :param port_in:
        :param port_out:
        :param bool emit: If True, the `connectionAdded` signal will be emitted.
        :return:
        """
        connection = MockedConnection(port_src, port_dst)
        self.connections.add(connection)
        if emit:
            self.connectionAdded.emit(connection)
        return connection

    def remove_connection(self, connection, emit=True):
        """
        Remove an existing connection from the scene.

        :param connection:
        :param bool emit: If True, the `connectionRemoved` signal will be emitted.
        :return:
        """
        if emit:
            self.connectionRemoved.emit(connection)
        self.connections.remove(connection)

    # Node methods

    def get_selection(self):
        return self.selection

    # Port methods

    def get_node_port_by_name(self, node, name):
        """
        Retreive a port from a node and a port name.
        :param MockedNode node: The node to query.
        :param str name: The desired port name.
        :return: A port matching the requirements. None if nothing is found.
        :rtype MockedPort or None
        """
        assert(isinstance(node, MockedNode))
        assert(isinstance(name, basestring))

        for port in self.ports_by_node.get(node):
            if port.name == name:
                return port
        return None

    def port_is_source(self, port):
        """
        Resolve if the provided port is the source of a connection.
        :param MockedPort port: The port to query.
        :return: True if the port is the source of a connection. False otherwise.
        :rtype: bool
        """
        return any(connection.src is port for connection in self.connections)

    def port_is_destination(self, port):
        """
        Resolve if the provided port if the destination of a connection.
        :param MockedPort port: The port to query.
        :return: True if the port is the destination of a connection. False otherwise.
        :rtype: bool
        """
        return any(connection.dst is port for connection in self.connections)

    def get_port_input_connections(self, port):
        """
        Retrieve the connections that use the provided port as destination.
        :param MockedPort port: The port to query.
        :return: A set of mocked connections
        :rtype: Set[MockedConnection]
        """
        return {connection for connection in self.connections if connection.dst is port}

    def get_port_output_connections(self, port):
        """
        Retrieve the connections that use the provided port as destination.
        :param MockedPort port: The port to query.
        :return: A set of mocked connections
        :rtype: Set[MockedConnection]
        """
        return {connection for connection in self.connections if connection.dst is port}

    def get_port_inputs(self, port):
        """
        Retrieve all port that take part in a connection where the provided port is the destination.
        :param MockedPort port: The port to query.
        :return: A set of mocked ports.
        :rtype: Set[MockedPort]
        """
        return {connection.src for connection in self.get_port_input_connections(port)}

    def get_port_outputs(self, port):
        """
        Retrieve all port that take part in a connection where the provided port is the source.
        :param MockedPort port: The port to query.
        :return: A set of mocked ports.
        :rtype: Set[MockedPort]
        """
        return {connection.dst for connection in self.get_port_output_connections(port)}
