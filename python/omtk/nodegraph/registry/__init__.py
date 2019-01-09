import abc
import logging

from omtk.core import manager
from omtk.nodegraph.cache import NodeCache, PortCache, ConnectionCache, CachedDefaultDict
from omtk.nodegraph.models.connection import ConnectionModel
from omtk.nodegraph.models.node import NodeModel
from omtk.nodegraph.models.port import PortModel
from omtk.nodegraph.signal import Signal

log = logging.getLogger(__name__)


class NodeGraphRegistry(object):  # QObject provide signals
    """
    Link node values to NodeGraph[Node/Port/Connection]Model.

    Qt Signals:
    :signal onNodeAdded(node): Emitted when a node is added in Maya.
    :signal onNodeDeleted(node): Emitted when a node is deleted in Maya.
    :signal onPortAdded(port): Emitted when an attribute is created in Maya.
    :signal onPortRemoved(port): Emitted when an attribute is removed from Maya.
    :signal onConnectionAdded(port): Emitted when a connection is created in Maya.
    :signal onConnectionRemoved(port): Emitted when a connection is removed from Maya.

    Arguments:
    :param ISession session: The DCC session attached to the REGISTRY_DEFAULT.
           When something change in the DCC session, the REGISTRY_DEFAULT will be notified.
    """
    __metaclass__ = abc.ABCMeta
    onNodeAdded = Signal(NodeModel)
    onNodeDeleted = Signal(NodeModel)
    onPortAdded = Signal(PortModel)
    onPortRemoved = Signal(PortModel)
    onConnectionAdded = Signal(ConnectionModel)
    onConnectionRemoved = Signal(ConnectionModel)

    def __init__(self, session=None):
        super(NodeGraphRegistry, self).__init__()

        self._session = None
        if session:
            self.set_session(session)

        self._nodes = set()
        self._attributes = set()
        self._connections = set()

        # Cache-stuff
        self.cache_nodes_by_value = NodeCache()
        self.cache_ports_by_value = PortCache()
        self.cache_ports_by_node = CachedDefaultDict(set)
        self.cache_connections_by_port = CachedDefaultDict(set)
        self.cache_connection_by_value = ConnectionCache()

        # Moved out to remove REGISTRY_DEFAULT references from cache
        self.cache_nodes_by_value.onUnregistered.connect(self.on_node_unregistered)

    def on_node_unregistered(self, node_model):
        self.session.remove_node_callbacks(node_model)

    @property
    def session(self):
        """
        :rtype: ISession
        """
        return self._session

    @property
    def nodes(self):
        """
        Read-only getter for accessing all registered nodes.
        Do not modify the value return as this could lead to artifacts.

        :return: The registered nodes
        :rtype: set(NodeModel)
        """
        return self._nodes

    @property
    def ports(self):
        """
        Read-only getter for accessing all registered ports.
        Do not modify the value return as this could lead to artifacts.

        :return: The registered ports
        :rtype: set(PortModel)
        """
        return self._attributes

    @property
    def connections(self):
        """
        Read-only getter for accessing all registered connections.
        Do not modify the value return as this could lead to artifacts.

        :return: The registered connections
        :rtype: set(ConnectionModel)
        """
        return self._connections

    def set_session(self, session):
        """
        Set the DCC session associated with the REGISTRY_DEFAULT.
        Any events in the session will be forwarded to the REGISTRY_DEFAULT.
        :param ISession session: The new session associated with the REGISTRY_DEFAULT.
        """
        old_session = self._session
        if old_session:
            self._unbind_session(session)
            old_session.remove_callbacks()
            self._session.set_registry(None)

        self._session = session

        session.set_registry(self)
        self._bind_session(session)
        session.add_callbacks()

    def _bind_session(self, session):
        """
        Connect all signals from this session to a registry object signal.

        :param maya_mock.MockedSession session: The registry to connect.
        """
        session.onNodeAdded.connect(self.onNodeAdded.emit)
        session.onNodeRemoved.connect(self.onNodeDeleted.emit)
        session.onPortAdded.connect(self.onPortAdded.emit)
        session.onPortRemoved.connect(self.onPortRemoved.emit)
        session.onConnectionAdded.connect(self.onConnectionAdded.emit)
        session.onConnectionRemoved.connect(self.onConnectionRemoved.emit)

        # Monitor any port deletion
        session.onNodeRemoved.connect(self.callback_node_removed)
        session.onPortAdded.connect(self.callback_port_added)
        session.onPortRemoved.connect(self.callback_port_removed)
        session.onConnectionAdded.connect(self.callback_connection_added)
        session.onConnectionRemoved.connect(self.callback_connection_removed)

    def _unbind_session(self, session):
        """
        Disconnect all signals from this session to a (previously connected) registry object.

        :param omtk.nodegraph.NodeGraphRegistry registry: The registry to disconnect.
        """
        session.nodeAdded.disconnect(self.onNodeAdded.emit)
        session.onNodeRemoved.disconnect(self.onNodeDeleted.emit)
        session.onPortAdded.disconnect(self.onPortAdded.emit)
        session.portRemoved.disconnect(self.onPortRemoved.emit)
        session.connectionRemoved.disconnect(self.onConnectionRemoved.emit)

        session.nodeRemoved.disconnect(self.callback_node_removed)
        session.portAdded.connect(self.callback_port_added)
        session.portRemoved.disconnect(self.callback_port_removed)
        session.connectionAdded.disconnect(self.callback_connection_added)
        session.connectionRemoved.disconnect(self.callback_connection_removed)

    def callback_node_removed(self, node):
        """
        :param omtk.nodegraph.NodeModel node:
        :return:
        """
        from omtk.nodegraph.models._deprecated import node_dg

        log.info("%s was deleted", node)

        # Hack: If the node is part of a compound, ensure that the compound delete
        # itself automatically if there's no more children.
        # This might not be the best way to do, see QUESTIONS.txt 1.1.
        if isinstance(node, node_dg.NodeGraphDgNodeModel):
            parent = node.get_parent()
            if parent:
                parent_children = set(parent.get_children())
                parent_children.remove(node)  # the node is not yet deleted
                if len(parent_children) == 0:
                    self.onNodeDeleted.emit(parent)
                    self._unregister_node(parent)

        # node.onDeleted.emit(node)
        self.onNodeDeleted.emit(node)  # todo: do we need 2 signals?
        self._unregister_node(node)

    def callback_port_added(self, key, port):
        """
        Called when a port is added in a session connected to this registry.

        :param omtk.nodegraph.PortModel port: The created port.
        """
        self.cache_ports_by_value.register(key, port)
        self.onPortAdded.emit(port)

    def callback_port_removed(self, port):
        """
        Called when a port is removed from a session connected to this registry.

        :param omtk.nodegraph.PorModel port: The port being removed.
        """
        self.cache_ports_by_value.unregister(port)

    def callback_connection_added(self, connection):
        """
        Called when a connection is added in a session connected to this registry.

        :param omtk.nodegraph.ConnectionModel connection: The connection being added.
        """
        self.cache_connection_by_value.register(connection.get_source(), connection)
        self.cache_connection_by_value.register(connection.get_destination(), connection)

    def callback_connection_removed(self, connection):
        """
        Called when a connection is removed from a session connected to this registry.

        :param omtk.nodegraph.ConnectionModel connection: The connection being removed.
        """
        self.cache_connection_by_value.unregister(connection)

    # TODO: Deprecate
    @property
    def manager(self):
        return manager.get_session()

    # --- Registration methods ---

    # TODO: replace by nodes?
    def get_nodes(self, safe=True):
        """
        Return all known nodes.
        :param bool safe: If True (default), a copy of the node REGISTRY_DEFAULT will be returned to prevent any artifacts.
                          Warning: Disable this only if you known you won't modify the returned value.
        :rtype: List[NodeModel]
        """
        return list(self._nodes) if safe else self._nodes

    def _register_node(self, node, val):
        """
        Registry a node and it's associated value.

        :param omtk.nodegraph.NodeModel node: The node to registry.
        :param object val: The value associated with the provided node.
        """
        assert isinstance(node, NodeModel)

        log.debug("Registering %s for %s", node, val)

        if node in self._nodes:
            log.debug("Node is already registered. %s", node)
            return

        self._nodes.add(node)
        self.cache_nodes_by_value.register(val, node)

    def _register_port(self, port, val):
        """
        Register a port and it's associated value.

        :param omtk.nodegraph.PortModel port: The port to register
        :param object val: The value associated with the port
        """
        assert isinstance(port, PortModel)

        if port in self._attributes:
            raise Exception("Port is already registered. This is a bug. {}".format(port))

        node = port.get_parent()

        self._attributes.add(port)
        self.cache_ports_by_value.register(val, port)
        self.cache_ports_by_value.register(val, port)
        self.cache_ports_by_node.register(node, port)

    def _register_connections(self, connection, val):
        """
        Register a connection and it's associated value.

        :param ConnectionModel connection: The connection to unregister
        :param object val: The value associated with the connection.
        """
        assert isinstance(connection, ConnectionModel)

        if connection in self._connections:
            raise Exception("Connection is already registered. This is a bug. {}".format(connection))

        port_src = connection.get_source()
        port_dst = connection.get_destination()

        self._connections.add(connection)
        self.cache_connection_by_value.register(val, connection)
        self.cache_connections_by_port.register(port_src, connection)
        self.cache_connections_by_port.register(port_dst, connection)

    # --- Cache clearing method ---

    def _unregister_node(self, node):
        """
        Unregister a node and it's associated value.

        :param NodeModel node: The node to unregister
        """
        self._nodes.discard(node)
        self.cache_nodes_by_value.unregister(node)
        self.cache_ports_by_node.unregister(node)

    def _unregister_port(self, port):
        """
        Unregister a port and it's associated value.

        :param PortModel port: The port to unregister
        """
        node = port.get_parent()

        self._attributes.remove(port)
        self.cache_ports_by_value.unregister(port)
        self.cache_ports_by_node.unregister_val(node, port)

    def _unregister_connection(self, connection):
        """
        Unregister a connection and it's associated value.

        :param ConnectionModel connection: The connection to unregister
        """
        port_src = connection.get_source()
        port_dst = connection.get_destination()

        self._connections.discard(connection)
        self.cache_connection_by_value.unregister((port_src, port_dst))
        self.cache_connections_by_port.unregister_val(port_src, connection)
        self.cache_connections_by_port.unregister_val(port_dst, connection)

    # --- Access methods ---

    def _conform_node_key(self, key):
        """
        Allow us to change the key that will be used to resolve a NodeModel.

        :param object key: The key
        :return: The key to use
        :rtype: object
        """
        return key

    def get_node(self, key):
        """
        Return a OMTK compatible node from an object instance.

        :param object key: An object representable as a node.
        :return: A OMTK node.
        :rtype: NodeModel
        :raise Exception: If value is invalid.
        """
        key = self._conform_node_key(key)

        # Memoize
        try:
            node = self.cache_nodes_by_value.get(key)

        # Fetch and register if necessary
        except LookupError:
            node = self._get_node(key)
            self._register_node(node, key)
        return node

    @abc.abstractmethod
    def _get_node(self, val):
        """
        Return a node representation of the provided value.

        :param object val:
        :return:
        :rtype: NodeModel
        """

    def _conform_port_key(self, key):
        """
        Allow us to change the key that will be used to resolve a NodeModel.

        :param object key: The key
        :return: The key to use
        :rtype: object
        """
        return key

    def get_port(self, key):
        """
        Get or create a node from a value.

        :param object key: An object representable as a port (str, pymel.Attribute, etc)
        :return: A port
        :rtype: omtk.nodegraph.PortModel
        """
        key = self._conform_port_key(key)
        # Memoize
        try:
            port = self.cache_ports_by_value.get(key)

        # Fetch and register if necessary
        except LookupError:
            port = self._get_port(key)
            self._register_port(port, key)
            # Save node <-> port association
            # node = port.get_parent()
            # self.cache_ports_by_node.register(node, port)

        return port

    def get_node_ports(self, node):
        """
        Return all ports associated with a node.

        :param NodeModel node: The node to query.
        :return: A list of ports. List can be empty.
        :rtype: List[PortModel]
        """
        return self.cache_ports_by_node.get(node)

    def get_node_port_by_name(self, node, name):
        """
        Get a port associated to a provided node by it's name.

        :param NodeModel node: A node to query.
        :param str name: The name of the port to query.
        :return: A port or None if no port was found.
        :rtype: PortModel or None
        """
        ports = self.cache_ports_by_node.get(node)
        if not ports:
            return None
        for port in ports:
            if port.get_name() == name:
                return port
        return None

    @abc.abstractmethod
    def _get_port(self, val):
        """
        Create a port from a value.

        :param val: An object representable as a port (str, pymel.Attribute, etc)
        :return: A port
        :rtype: omtk.nodegraph.PortModel
        """

    def get_connection(self, port_src, port_dst):
        """
        Get or create a ``ConnectionModel`` from two ``PortModel``.

        :param PortModel port_src: The source port.
        :param PortModel port_dst: The destination port.
        :return: A ConnectionModel
        :rtype: ConnectionModel
        """
        assert (isinstance(port_src, PortModel))
        assert (isinstance(port_dst, PortModel))

        key = (port_src, port_dst)
        try:
            connection = self.cache_connection_by_value.get(key)
        except LookupError:
            connection = self._get_connection(port_src, port_dst)
            self._register_connections(connection, key)

        return connection

    def _get_connection(self, port_src, port_dst):
        """
        Create a ``ConnectionModel`` from two ``PortModel``.

        :param port_src: The source port.
        :type port_src: PortModel
        :param port_dst: The destination port.
        :type port_dst: PortModel
        :return: A ConnectionModel
        :rtype: ConnectionModel
        """
        from omtk.nodegraph import factory
        # assert(isinstance(port_src, PortModel))
        # assert(isinstance(port_dst, PortModel))
        key = (port_src, port_dst)
        inst = factory.get_connection_from_value(self, port_src, port_dst)
        self.cache_connection_by_value.register(key, inst)

        return inst

    # --- Methods that interact with the DCC ---

    def get_parent(self, node):
        """
        Get a node parent.

        :param omtk.nodegraph.NodeModel node: The node to query
        :return: The node parent. None if node have not parent.
        :rtype: omtk.nodegraph.NodeModel or None
        """
        child_val = self.cache_nodes_by_value.get_key(node)
        parent_val = self._get_parent_impl(child_val)
        if parent_val is None:
            return None
        parent = self.get_node(parent_val)
        return parent

    def get_children(self, node):
        """
        Get a node children.

        :param omtk.nodegraph.NodeModel node: The node to query
        :return: A list of child.
        :rtype: List[omtk.nodegraph.NodeModel]
        """
        parent_val = self.cache_nodes_by_value.get_key(node)
        children_val = self._get_children_impl(parent_val)
        children = [self.get_node(child_val) for child_val in children_val]
        return children

    def parent(self, child, parent):
        """
        Parent a node to another.

        :param omtk.nodegraph.NodeModel child:
        :param omtk.nodegraph.NodeModel parent:
        """
        child_val = self.cache_nodes_by_value.get_key(child)
        parent_val = self.cache_nodes_by_value.get_key(parent)
        self._set_parent_impl(child_val, parent_val)

    def scan_session(self):
        self.scan_nodes()
        self.scan_port_connections()

    def scan_nodes(self):
        self._scan_nodes()

    def scan_node_ports(self, node):
        """
        Query all the ports associated to a provided node in the scene and register them.
        :param NodeModel node: The node to scan
        """
        node_val = self.cache_nodes_by_value.get_key(node)
        self._scan_node_ports(node_val)

    def scan_port_connections(self):
        pass

    # --- Implementation methods

    @abc.abstractmethod
    def _get_parent_impl(self, val):
        """
        Abstract implementation for retrieving a child parent.
        :param object val: A child raw value.
        :return: A parent raw value.
        :rtype: object
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _get_children_impl(self, val):
        """
        Abstract implementation for retrieving a node value children.
        :param object val: A node raw value.
        :return: A list of child values.
        :rtype: List[object]
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _set_parent_impl(self, node, parent):
        """
        :param object node: The node to parent
        :param object parent: The parent
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _scan_nodes(self):
        raise NotImplementedError

    def _scan_node_ports(self, node):
        """
        :param object node: The node to scan
        """
        raise NotImplementedError
