"""
Session class which hold informations about current nodes, ports and connections.
"""
import collections
import itertools
import logging
import re
import string

import six

from . import naming
from .connection import MockedConnection
from .constants import (
    SHAPE_CLASS,
    DEFAULT_PREFIX_BY_SHAPE_TYPE,
    CONVERSION_FACTOR_BY_TYPE,
    IMPOSSIBLE_CONNECTIONS,
)
from .naming import (
    pattern_to_regex,
    conform_node_name,
    is_valid_node_name,
)
from .node import MockedNode
from .port import MockedPort
from .schema import MockedSessionSchema
from .signal import Signal

LOG = logging.getLogger(__name__)


class MockedSession(collections.MutableMapping):  # pylint: disable=too-many-public-methods
    """
    Collection of nodes, ports and connections.

    :param schema: The schema to use for the session. Optional
    :type schema: maya_mock.MockedSessionSchema or None
    """

    onNodeAdded = Signal(MockedNode)
    onNodeRemoved = Signal(MockedNode)
    onPortAdded = Signal(MockedPort)
    onPortRemoved = Signal(MockedPort)
    onConnectionAdded = Signal(MockedConnection)
    onConnectionRemoved = Signal(MockedConnection)

    def __init__(self, schema=None):
        super(MockedSession, self).__init__()
        self.nodes = set()
        self.namespaces = set()
        self.ports = set()
        self.connections = set()
        self.selection = set()
        self.ports_by_node = collections.defaultdict(set)
        self.schema = schema

        if schema:
            if not isinstance(schema, MockedSessionSchema):
                raise ValueError("Unexpected schema type for %s" % schema)
            for name, type_ in schema.default_state.items():
                self.create_node(type_, name)

    def __str__(self):
        return "<MockedSession %s nodes>" % len(self)

    def __iter__(self):
        return iter(self.nodes)

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, item):
        port = self.get_port_by_match(item)
        if port:
            return port

        node = self.get_node_by_match(item)
        if node:
            return node

        raise KeyError("Found no node or port matching %r" % item)

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError

    # --- Public methods

    def node_exist(self, dagpath):
        """
        Determine if dagpath match an existing node or not.

        :param str dagpath: A dagpath to match.
        :param parent: If provided, the dagpath will be resolved relative to this node.
        :type parent: MockedNode or None
        :return: True if the dagpath match an existing object. False otherwise.
        :rtype: bool
        """
        return bool(self.get_node_by_match(dagpath, strict=False))

    def _unique_name(self, prefix, parent=None):
        """
        Resolve a unique name from a provided base suffix.

        :param str prefix:
        :param MockedNode parent:
        :return:
        """
        counter = itertools.count(1)
        while True:
            name = "{}{}".format(prefix, next(counter))
            dagpath = naming.join(parent.dagpath, name) if parent else "|" + name
            if is_valid_node_name(name) and not self.node_exist(dagpath):
                return name

    def get_node_by_name(self, name):
        """
        Retrieve a node by it's name.
        Note that multiple nodes can have the same name.

        :param str name: The name of the MockedNode.
        :return: A node or None if no match was found.
        :rtype: MockedNode or None
        """
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def get_nodes_by_match(self, pattern, strict=True):
        """
        :param str pattern: The pattern to match.
        :param bool strict: If True, a ValueError will be raised if no node are found.
        :return: A node or None if no match was found.
        :rtype: MockedNode or None
        :raise ValueError: If no node are found matching provided pattern AND strict is True.
        """
        result = sorted(self.iter_node_by_match(pattern))
        if strict and not result:
            raise ValueError("No object matches name: {}".format(pattern))
        return result

    def is_pattern_clashing(self, node, pattern):
        """
        Determine if the MEL repr of a node clash with another node dagpath.

        :param node:
        :param pattern:
        :return: True if provided pattern match with another node that provided. False otherwise.
        :rtype: bool
        """
        matches = self.iter_node_by_match(pattern)
        for guess in matches:
            if guess is not node:
                return True
        return False

    def get_node_by_match(self, pattern, **kwargs):
        """
        Retrieve a node by matching it' against a provided pattern.
        Note that multiple nodes can match the same pattern.

        """
        return next(iter(self.get_nodes_by_match(pattern, **kwargs)), None)

    def iter_node_by_match(self, pattern):
        """
        Yield all the node which dagpath match the provided pattern.

        :param pattern: The node we want the MEL representation.
        :return: A node generator
        :rtype: Generator[MockedNode]
        """
        regex = pattern_to_regex(pattern)

        for node in self.nodes:
            if re.match(regex, node.dagpath):
                yield node

    def get_port_by_match(self, pattern):
        """
        Retrieve a port by matching it against a provided pattern.
        Note that multiple ports can match a same pattern.

        :param str pattern: The pattern to match.
        :return: A port or None if no match was found.
        :rtype: MockedPort or None
        """
        for port in self.ports:
            if port.match(pattern):
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
        return next(
            (conn for conn in self.connections if conn.src is src and conn.dst is dst), None,
        )

    @staticmethod
    def warning(msg):
        """
        Print a warning message.
        Similar to cmds.warning

        :param str msg: The message to display
        """
        print("Warning: %s" % msg)

    def create_node(self, node_type, name=None, parent=None, emit=True):
        """
        Create a new node in the scene.

        :param str node_type: The type of the node.
        :param str name: The name of the node.
        :param parent: The parent of the node if applicable.
        :type parent: MockedNode or None
        :param bool emit: If True, the `onPortAdded` signal will be emitted.
        :return: The created node
        :rtype: MockedNode
        """
        is_shape_type = node_type in SHAPE_CLASS

        # Validate if the provided name if any is valid.
        # Remove any characters from name.
        # Start by removing any invalid characters from the name.
        if name:
            name_conformed = conform_node_name(name)
            if name != name_conformed:
                self.warning("Removing invalid characters from name.")
                name = name_conformed

        # Handle the case where the resulting name is empty
        # which can happen if invalid characters are found.
        # ex: cmds.createNode('transform', name='0')
        if name == "":
            raise RuntimeError(u"New name has no legal characters.\n")

        # If name is not provided, we'll name the object automatically
        if not name:
            # If node is a shape, add 'Shape' before the number.
            if node_type in SHAPE_CLASS:
                name = "%sShape" % DEFAULT_PREFIX_BY_SHAPE_TYPE.get(node_type, node_type)
            # Otherwise, name the node against it's type.
            else:
                name = node_type

            name = self._unique_name(name, parent=parent)
        else:
            # Next, if the name is invalid or clash with another node dagpath,
            # we'll need to add a number suffix.
            dagpath = "%s|%s" % (parent.dagpath, name) if parent else "|" + name
            if not is_valid_node_name(name) or self.node_exist(dagpath):
                name = name.rstrip(string.digits)
                name = self._unique_name(name, parent=parent)

        # If we are sure that we can create the node and it is a shape, create it's transform first.
        if is_shape_type:
            transform_name_prefix = DEFAULT_PREFIX_BY_SHAPE_TYPE.get(node_type, node_type)
            transform_name = self._unique_name(transform_name_prefix)
            parent = self.create_node("transform", name=transform_name)

        node = MockedNode(self, node_type, name, parent=parent)
        if emit:
            signal = self.onNodeAdded
            LOG.debug("%s emitted with %s", signal, node)
            signal.emit(node)
        self.nodes.add(node)

        # Add port from configuration if needed
        if self.schema:
            node_def = self.schema.get(node_type)
            if node_def:
                node_def.apply(self, node)

        return node

    def remove_node(self, node, emit=True):
        """
        Remove a node from the graph.
        :param node:
        :param bool emit: If True, the `onPortAdded` signal will be emitted.
        """
        # Remove any port that where used by the node.
        ports = [port for port in self.ports if port.node is node]
        for port in ports:
            self.remove_port(port, emit=emit)

        if emit:
            self.onNodeRemoved.emit(node)

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
        self.ports_by_node[node].add(port)
        self.ports.add(port)
        if emit:
            self.onPortAdded.emit(port)
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
            self.onPortRemoved.emit(port)

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

    def create_connection(self, src, dst, emit=True):
        """
        Create a new connection in the scene.

        :param MockedPort src: The connection source port.
        :param MockedPort dst: The connection destination port.
        :param bool emit: If True, the `onConnectionAdded` signal will be emitted.
        :return: A connection
        :rtype: MockedConnection
        """
        # TODO: What do we return if multiple connections are created?
        assert src.type
        assert dst.type
        key = src.type, dst.type

        if key in IMPOSSIBLE_CONNECTIONS:
            msg = "The attribute %r cannot be connected to %r." % (src.dagpath, dst.dagpath,)
            raise RuntimeError(msg)

        # When connecting some port types together, Maya can create a unitConversion node.
        factor = CONVERSION_FACTOR_BY_TYPE.get((src.type, dst.type))
        if factor:
            node_conversion = self.create_node("unitConversion")
            port_input = self.get_node_port_by_name(node_conversion, "input")
            port_output = self.get_node_port_by_name(node_conversion, "output")
            port_factor = self.get_node_port_by_name(node_conversion, "conversionFactor")
            port_factor.value = factor
            self.create_connection(src, port_input)
            self.create_connection(port_output, dst)
            return None

        connection = MockedConnection(src, dst)
        self.connections.add(connection)
        if emit:
            self.onConnectionAdded.emit(connection)
        return connection

    def remove_connection(self, connection, emit=True):
        """
        Remove an existing connection from the scene.

        :param connection:
        :param bool emit: If True, the `onConnectionRemoved` signal will be emitted.
        :return:
        """
        if emit:
            self.onConnectionRemoved.emit(connection)
        self.connections.remove(connection)

    # Port methods

    def get_node_port_by_name(self, node, name):
        """
        Retrive a port from a node and a port name.

        :param MockedNode node: The node to namespace.
        :param str name: The desired port name.
        :return: A port matching the requirements. None if nothing is found.
        :rtype: MockedPort or None
        """
        assert isinstance(node, MockedNode)
        assert isinstance(name, six.string_types)

        for port in self.ports_by_node.get(node, ()):
            if port.name == name:
                return port
            if port.short_name == name:
                return port
            if port.nice_name == name:
                return port
        return None

    def port_is_source(self, port):
        """
        Resolve if the provided port is the source of a connection.
        :param MockedPort port: The port to namespace.
        :return: True if the port is the source of a connection. False otherwise.
        :rtype: bool
        """
        return any(connection.src is port for connection in self.connections)

    def port_is_destination(self, port):
        """
        Resolve if the provided port if the destination of a connection.
        :param MockedPort port: The port to namespace.
        :return: True if the port is the destination of a connection. False otherwise.
        :rtype: bool
        """
        return any(connection.dst is port for connection in self.connections)

    def get_port_input_connections(self, port):
        """
        Retrieve the connections that use the provided port as destination.
        :param MockedPort port: The port to namespace.
        :return: A set of mocked connections
        :rtype: Set[MockedConnection]
        """
        return {connection for connection in self.connections if connection.dst is port}

    def get_port_output_connections(self, port):
        """
        Retrieve the connections that use the provided port as destination.
        :param MockedPort port: The port to namespace.
        :return: A set of mocked connections
        :rtype: Set[MockedConnection]
        """
        return {connection for connection in self.connections if connection.src is port}

    def get_port_inputs(self, port):
        """
        Retrieve all port that take part in a connection where the provided port is the destination.
        :param MockedPort port: The port to namespace.
        :return: A set of mocked ports.
        :rtype: Set[MockedPort]
        """
        return {connection.src for connection in self.get_port_input_connections(port)}

    def get_port_outputs(self, port):
        """
        Retrieve all port that take part in a connection where the provided port is the source.
        :param MockedPort port: The port to namespace.
        :return: A set of mocked ports.
        :rtype: Set[MockedPort]
        """
        return {connection.dst for connection in self.get_port_output_connections(port)}
