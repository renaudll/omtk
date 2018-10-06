import logging

from collections import defaultdict
from omtk.core import manager
from omtk.nodegraph import nodegraph_factory
from omtk.nodegraph.cache import Cache, CacheDefaultDict, NodeCache, PortCache, ConnectionCache
from omtk.vendor.Qt import QtCore

from .models.node import node_base
from .models.port import port_base
from .models.connection import ConnectionModel

log = logging.getLogger(__name__)


class NodeGraphRegistry(QtCore.QObject):  # QObject provide signals
    """
    Link node values to NodeGraph[Node/Port/Connection]Model.

    Qt Signals:
    :signal onNodeDeleted(node): emitted when a node is deleted in Maya.
    :signal onPortAdded(port): emitted when an attribute is created in Maya.
    :signal onPortRemoved(port): emitted when an attribute is removed from Maya.
    :signal onConnectionCreated(port): emitted when a connection is created in Maya.

    Arguments:
    :param ISession session: The DCC session attached to the registry.
           When something change in the DCC session, the registry will be notified.
    """
    onNodeAdded = QtCore.Signal(node_base.NodeModel)
    onNodeDeleted = QtCore.Signal(node_base.NodeModel)
    onPortAdded = QtCore.Signal(port_base.PortModel)
    onPortRemoved = QtCore.Signal(port_base.PortModel)
    onConnectionCreated = QtCore.Signal(port_base.PortModel)
    onConnectionAdded = QtCore.Signal(ConnectionModel)
    onConnectionRemoved = QtCore.Signal(ConnectionModel)

    def __init__(self, session=None):
        super(NodeGraphRegistry, self).__init__()

        self._session = None
        if session:
            self.set_session(session)

        self._nodes = set()
        self._attributes = set()
        self._connections = set()

        # Cache-stuff
        self.cache_nodes_by_value = NodeCache(self)
        self.cache_ports_by_value = PortCache(self)
        self.cache_connection_by_value = ConnectionCache(self)

        self.cache_ports_by_node = CacheDefaultDict(self, set)
        self.cache_connections_by_port = CacheDefaultDict(self, set)

        self._nodes_by_metadata = {}

        # Used so we can invalidate ports when invalidating nodes
        # self._cache_connections_by_port = defaultdict(set)
        # self._cache_ports_by_node = defaultdict(set)
        # self._cache_node_by_port = {}

        self._callback_id_by_node_model = defaultdict(set)
        self._callback_id_node_removed = None

        self._mutex = True  # When False the Registry don't listen to callbacks.

        self.cache_nodes_by_value.onUnregistered.connect(self.on_node_unregistered)
        self.cache_ports_by_value.onUnregistered.connect(self.on_port_unregistered)

    @property
    def session(self):
        """
        :rtype: ISession
        """
        return self._session

    def set_session(self, session):
        """
        Set the DCC session associated with the registry.
        Any events in the session will be fowarded to the registry.
        :param ISession session: The new session associated with the registry.
        """
        old_session = self._session
        if old_session:
            self._disconnect_session(session)
            old_session.remove_callbacks()
            self._session.set_registry(None)

        self._session = session

        session.set_registry(self)
        self._connect_session(session)
        session.add_callbacks()

    def _connect_session(self, session):
        session.nodeAdded.connect(self.onNodeAdded.emit)
        # session.nodeRemoved.connect(self.onNodeDeleted.emit)
        # session.portAdded.connect(self.onPortAdded.emit)
        session.portRemoved.connect(self.onPortRemoved.emit)
        session.connectionAdded.connect(self.onConnectionCreated.emit)
        session.connectionRemoved.connect(self.onConnectionRemoved.emit)

        # Monitor any port deletion
        session.nodeRemoved.connect(self.callback_node_removed)
        session.portAdded.connect(self.callback_port_added)
        session.portRemoved.connect(self.callback_port_removed)
        session.connectionRemoved.connect(self.callback_connection_removed)

    def _disconnect_session(self, session):
        session.nodeAdded.disconnect(self.onNodeAdded.emit)
        # session.nodeRemoved.disconnect(self.onNodeDeleted.emit)
        # session.portAdded.disconnect(self.onPortAdded.emit)
        session.portRemoved.disconnect(self.onPortRemoved.emit)
        session.connectionAdded.disconnect(self.onConnectionCreated.emit)
        session.connectionRemoved.disconnect(self.onConnectionRemoved.emit)

        session.nodeRemoved.disconnect(self.callback_node_removed)
        session.portAdded.connect(self.callback_port_added)
        session.portRemoved.disconnect(self.callback_port_removed)
        session.connectionRemoved.disconnect(self.callback_connection_removed)

    # @decorators.log_info
    def callback_node_removed(self, node):
        """
        :param omtk.nodegraph.NodeModel node:
        :return:
        """
        from omtk.nodegraph.models.node import node_dg

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
                    self._invalidate_node(parent)

        # node.onDeleted.emit(node)
        self.onNodeDeleted.emit(node)  # todo: do we need 2 signals?
        self._invalidate_node(node)

    def callback_port_added(self, key, port):
        """
        Called when a port was created in Maya.
        :param omtk.nodegraph.PortModel port: The created port.
        """
        self.cache_ports_by_value.register(key, port)
        self.onPortAdded.emit(port)

    def callback_port_removed(self, port):
        """
        :param omtk.nodegraph.PorModel port: The port being removed.
        """
        self.cache_ports_by_value.unregister(port)

    def callback_connection_removed(self, connection):
        """
        :param omtk.nodegraph.ConnectionModel connection: The connection being removed.
        """
        self.cache_connection_by_value.unregister(connection)


    @property
    def manager(self):
        return manager.get_session()

    # --- Registration methods ---

    def get_nodes(self, safe=True):
        """
        Return all known nodes.
        :param bool safe: If True (default), a copy of the node registry will be returned to prevent any artifacts.
                          Warning: Disable this only if you known you won't modify the returned value.
        :rtype: List[NodeModel]
        """
        return list(self._nodes) if safe else self._nodes

    def _register_node(self, inst):
        self._nodes.add(inst)

    def _register_attribute(self, inst):
        # TODO: Not used, keep?
        self._attributes.add(inst)

    def _register_connections(self, inst):
        # TODO: Not used, keep?
        self._connections.add(inst)

    # --- Cache clearing method ---

    def _invalidate_node(self, node):
        self.cache_nodes_by_value.unregister(node)

    def on_node_unregistered(self, node):
        ports = self.cache_ports_by_node.get(node)
        for port in ports:
            self._cache_ports_by_node.unregister(port)

    def on_port_unregistered(self, port):
        connections = self._cache_connections_by_port.get(port)
        for connection in connections:
            self._cache_connections_by_port.unregister(connection)

    # --- Access methods ---

    def get_node(self, key):
        """
        Return a OMTK compatible node from an object instance.
        :param object key: An object representable as a node.
        :return: A OMTK node.
        :rtype: NodeModel
        :raise Exception: If value is invalid.
        """
        # Memoize
        try:
            val = self.cache_nodes_by_value.get(key)

        # Fetch and register if necessary
        except LookupError:
            val = self._get_node(key)
            self.cache_nodes_by_value.register(key, val)
        return val

    def _get_node(self, val):
        """
        Return a node representation of the provided value.
        :param object val:
        :return:
        :rtype: NodeModel
        """
        return nodegraph_factory.get_node_from_value(self, val)

    def get_port(self, key):
        """
        Get or create a node from a value.
        :param val: An object representable as a port (str, pymel.Attribute, etc)
        :return: A port
        :rtype: omtk.nodegraph.PortModel
        """
        # Memoize
        try:
            port = self.cache_ports_by_value.get(key)

        # Fetch and register if necessary
        except LookupError:
            port = self._get_port(key)
            self.cache_ports_by_value.register(key, port)

            # Save node <-> port association
            node = port.get_parent()
            self.cache_ports_by_node.register(node, port)

        return port

    def _get_port(self, val):
        """
        Create a port from a value.
        :param val: An object representable as a port (str, pymel.Attribute, etc)
        :return: A port
        :rtype: omtk.nodegraph.PortModel
        """
        inst = nodegraph_factory.get_port_from_value(self, val)
        self._register_attribute(inst)
        return inst

    def get_connection(self, port_src, port_dst):
        """
        Get or create a ``ConnectionModel`` from two ``PortModel``.
        :param port_src: The source port.
        :type model: PortModel
        :param port_dst: The destination port.
        :type model: PortModel
        :return: A ConnectionModel
        :rtype: ConnectionModel
        """
        key = (port_src, port_dst)
        try:
            connection = self.cache_ports_by_value.get(key)
        except LookupError:
            connection = self._get_connection(port_src, port_dst)
            self.cache_ports_by_value.register(key, connection)
            self._register_connections(connection)

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
        # assert(isinstance(port_src, port_base.PortModel))
        # assert(isinstance(port_dst, port_base.PortModel))
        key = (port_src, port_dst)
        inst = nodegraph_factory.get_connection_from_value(self, port_src, port_dst)
        self.cache_connection_by_value.register(key, inst)
        self.cache_connections_by_port.register(port_src, inst)
        self.cache_connections_by_port.register(port_dst, inst)
        self._register_connections(inst)
        return inst
