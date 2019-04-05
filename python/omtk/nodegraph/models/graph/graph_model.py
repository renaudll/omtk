import logging
from collections import defaultdict

import omtk
from omtk.libs import libPython
from omtk.nodegraph.models.graph import igraph
from omtk.nodegraph.models.node import NodeModel
from omtk.vendor.Qt import QtCore

log = logging.getLogger('omtk.nodegraph')


class GraphModel(igraph.IGraphModel):
    """
    A Graph is a network of nodes (NodeModel).
    Nodes have ports (PortModel).
    Nodes can be connected via connections(ConnectionModel).

    A GraphModel provide the complete node graph in a single data type.
    This ease the development of proxy models like the GraphComponentProxyFilterModel.
    Subgraphs and filters can be implemented by feeding a NodeGraphRegistry through a NodeGraphProxyModel.
    NodeGraphRegistry are consumed
    """

    def __init__(self, registry):
        super(GraphModel, self).__init__(registry)  # initialize Qt signals

        self._nodes = set()
        self._ports = set()
        self._connections = set()
        self._pos_by_node = {}  # (k is a NodeModel, v is a QRectF).

        self._nodes_by_port = defaultdict(set)
        self._ports_by_nodes = defaultdict(set)

        self._ports_by_connection = defaultdict(set)
        self._connections_by_port = defaultdict(set)

        self.set_registry(registry)

    def reset(self, emit=True):
        """
        Clear the graph of any nodes, ports and connections.
        :param emit: If True, the ``onAboutToBeReset`` and ``onReset`` Qt Signal will be emitted.
        """
        if emit:
            self.onAboutToBeReset.emit()

        for node in list(self.get_nodes()):  # hack: prevent change during iteration
            self.remove_node(node, emit=False)

        # TODO: remove this, they should get cleaned by themself
        self._nodes = set()
        self._ports = set()
        self._connections = set()

        # gc check
        assert not self._nodes
        assert not self._ports
        assert not self._connections
        assert not self._pos_by_node
        assert not self._nodes_by_port
        assert not self._ports_by_nodes
        assert not self._ports_by_connection
        assert not self._connections_by_port

        if emit:
            self.onReset.emit()

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
        if self._registry:
            self._unregister_registry(self._registry)

        if registry:
            self._register_registry(registry)

        self._registry = registry

    def _connect_registry(self, registry):
        """

        :param omtk.nodegraph.NodeGraphRegistry registry: The graph registered to connection from this session.
        """
        registry.onNodeDeleted.connect(self.on_node_unexpectedly_deleted)
        # component_registry.onPortAdded.connect(self.on_attribute_unexpectedly_added)
        registry.onPortRemoved.connect(self.on_attribute_unexpectedly_removed)
        # component_registry.onConnectionAdded.connect(self.on_connection_unexpectedly_added)
        registry.onConnectionRemoved.connect(self.on_connection_unexpectedly_removed)

    def _register_registry(self, registry):
        """
        Add callbacks to a REGISTRY_DEFAULT Qt Signal so we can intercept it.
        :param NodeGraphRegistry registry: The REGISTRY_DEFAULT to connect.
        """
        registry.onNodeDeleted.connect(self.on_node_unexpectedly_deleted)
        # component_registry.onPortAdded.connect(self.on_attribute_unexpectedly_added)
        registry.onPortRemoved.connect(self.on_attribute_unexpectedly_removed)
        # component_registry.onConnectionAdded.connect(self.on_connection_unexpectedly_added)
        registry.onConnectionRemoved.connect(self.on_connection_unexpectedly_removed)

        # REGISTRY_DEFAULT.onNodeDeleted.connect(self.onNodeRemoved.emit)

    def _unregister_registry(self, registry):
        """
        Remove callbacks from a REGISTRY_DEFAULT Qt Signal.
        """
        registry.onNodeDeleted.disconnect(self.on_node_unexpectedly_deleted)
        # component_registry.onPortAdded.disconnect(self.on_attribute_unexpectedly_added)
        registry.onPortRemoved.disconnect(self.on_attribute_unexpectedly_removed)
        # component_registry.onConnectionAdded.connect(self.on_connection_unexpectedly_added)
        registry.onConnectionRemoved.disconnect(self.on_connection_unexpectedly_removed)

        # REGISTRY_DEFAULT.onNodeDeleted.disconnect(self.onNodeRemoved.emit)

    # --- Node methods ---

    def iter_nodes(self):
        """
        Iterate through all the known nodes.
        :return: A node generator.
        :rtype: Generator[NodeModel]
        """
        return iter(self._nodes)

    def get_nodes(self):
        """
        Return all known nodes.
        :return: A list of nodes.
        :rtype: List[NodeModel]
        """
        return self._nodes

    def add_node(self, node, emit=True, expand=False):
        """
        Add a node to the graph.
        :param omtk.nodegraph.NodeModel node: The node to add.
        :param bool emit: If True, the ``onNodeAdded`` Qt Signal will be emitted.
        :rtype: None
        """
        assert isinstance(node, NodeModel)
        if node in self._nodes:
            return

        pos = self.get_available_position(node)

        self._register_node(node, pos)
        if emit:
            self.onNodeAdded.emit(node)

        self.set_node_position(node, pos)

        if expand:
            self.expand_node_ports(node)
            self.expand_node_connections(node)

    def _register_node(self, node, pos=None):
        """
        Add a node to the REGISTRY_DEFAULT.
        If the node is already registered, nothing happen.
        :param GraphModel node: The node to register.
        :param QtCore.QPointF pos: The position of the node. Optional.
        """
        self._nodes.add(node)
        self._pos_by_node[node] = pos  # todo: handle automatic positioning

    def remove_node(self, node, emit=False):
        """
        Remove a node from the graph.
        :param NodeModel node: The node to remove.
        :param bool emit: If True, the ``onNodeRemoved`` Qt Signal will be emmited.
        :return:
        """
        if not self.is_node_visible(node):
            log.debug("Cannot remove Node {0}. Node is not in view.".format(node))
        else:
            self._unregister_node(node, emit)

        if emit:
            self.onNodeRemoved.emit(node)

    def _unregister_node(self, node, emit=True):
        """
        Remove a node from the REGISTRY_DEFAULT.
        :param node: The node to unregister.
        """
        self._nodes.remove(node)
        self._pos_by_node.pop(node)
        # Remove node ports
        ports = list(self._ports_by_nodes[node])
        for port in ports:
            self.remove_port(port, emit=emit)  # we expect the user to know we're removing the port?
        self._ports_by_nodes.pop(node)

    def is_node_visible(self, node):
        """
        Query a node visibility in the graph.
        :param NodeModel node: The node to inspect.
        :return: True if the node is visible in the graph. False otherwise.
        :rtype: bool
        """
        return node in self._nodes

    def get_node_position(self, node):
        """
        Query a node position in the graph.
        :param NodeModel node: The node to inspect.
        :return: The node position in the graph.
        :rtype: QtCore.QRectF
        """
        return self._pos_by_node[node]

    def set_node_position(self, node, pos, emit=True):
        """
        Set the node position in the graph.
        :param NodeModel node: The node to position.
        :param pos: The position to set.
        :param emit: If True the ``onNodeMoved`` Qt Signal will be emitted.
        """
        self._pos_by_node[node] = pos

        assert isinstance(node, NodeModel)
        node.set_position(pos)

        if emit:
            self.onNodeMoved.emit(node, pos)

    # --- Port methods ---

    @property
    def ports(self):
        """
        Mutable accessor to the ports.
        :return: A set of ports.
        :rtype: set(PortModel)
        """
        return self._ports

    def iter_ports(self):
        """
        Iterate through all the known ports.
        :return: A port generator.
        :rtype: Generator[PortModel]
        """
        for port in iter(self._ports):
            yield port

    def get_ports(self):
        """
        Return all known ports.
        :return: A set of ports.
        :rtype: Set[PortModel]
        """
        return self._ports

    def iter_node_ports(self, node):
        """
        Iterate through a node ports.
        :param node: The node to iterate through.
        :return: A port generator.
        :rtype: Iterator[PortModel]
        """
        return iter(self.get_node_ports(node))

    def get_node_ports(self, node):
        """
        Provide all registered ports associated to a node.
        :param NodeModel node: The node to inspect.
        :return: A list of ports.
        :rtype: List[PortModel]
        """
        return self.registry.cache_ports_by_node.get(node) or []

    def add_port(self, port, emit=True):
        """
        Add a port to the graph.
        :param PortModel port: The port to add.
        :param bool emit: If True, the Qt Signal ``onPortAdded`` will be emitted.
        """
        if port in self._ports:
            return

        self._ports.add(port)

        node = port.get_parent()
        if not node in self._nodes:
            self.add_node(node)

        node._register_port(port)
        self._ports_by_nodes[node].add(port)
        self._nodes_by_port[port].add(node)

        if emit:
            self.onPortAdded.emit(port)

    def remove_port(self, port, emit=True):
        """
        Remove a port from the graph.
        No nothing if the port don't exist.

        :param port: The port to remove.
        :param emit: If True, the Qt Signal ``onPortRemoved`` will be emitted.
        """
        # Remove port connections
        for connection in list(self._connections_by_port[port]):  # hack: prevent change during iteration
            self.remove_connection(connection, emit=emit)
        self._connections_by_port.pop(port)

        # Update cache
        self._unregister_port(port)

        if emit:
            self.onPortRemoved.emit(port)

    def _unregister_port(self, port):
        """
        Remove a port from the internal REGISTRY_DEFAULT.
        :param PortModel port: The port to unregister.
        """
        if port not in self._ports:
            log.warning("Cannot unregister an unregistered port. %s", port)
            return

        self._ports.remove(port)
        for node in self._nodes_by_port[port]:
            self._ports_by_nodes[node].remove(port)
        self._nodes_by_port.pop(port)

    def is_port_visible(self, port):
        """
        Query a port visibility.
        :param PortModel port: The port to inspect.
        :return: True if the port is visible. False otherwise.
        :type: bool
        """
        return port in self._ports

    # --- Connection methods ---

    def iter_connections(self):
        """
        Iterate through all the known connections.
        :return: A connection generator.
        :rtype: Generator[ConnectionModel]
        """
        return iter(self._connections)

    def get_connections(self):
        return self._connections

    def add_connection(self, connection, emit=True):
        """
        Add a connection to the graph.
        :param ConnectionModel connection: The connection to add.
        :param bool emit: If True, the ``onConnectionAdded`` Qt Signal will be emitted.
        """
        if connection in self._connections:
            return

        self._connections.add(connection)

        # Update cache
        port_src = connection.get_source()
        port_dst = connection.get_destination()
        if not port_src in self._ports:
            self.add_port(port_src)
        if not port_dst in self._ports:
            self.add_port(port_dst)
        self._connections_by_port[port_src].add(connection)
        self._connections_by_port[port_dst].add(connection)
        self._ports_by_connection[connection].add(port_src)
        self._ports_by_connection[connection].add(port_dst)

        if emit:
            self.onConnectionAdded.emit(connection)

    def remove_connection(self, connection, emit=True):
        """Remove a connection from the graph.
        :param ConnectionModel connection: The connection to remove.
        :param emit: If True, the ``onConnectionRemoved`` Qt Signal will be emitted.
        """
        try:
            self._connections.remove(connection)
        except KeyError:
            log.debug("Connection is not in graph, %s", connection)
            return

        # Update cache
        for port in self._ports_by_connection[connection]:
            self._connections_by_port[port].remove(connection)
        self._ports_by_connection.pop(connection)

        if emit:
            self.onConnectionRemoved.emit(connection)

    def is_connection_visible(self, connection):
        """
        Query a connection visibility in the graph.
        :param connection: The connection to inspect.
        :return: True if the connection is visible in the graph. False otherwise.
        :rtype: bool
        """
        return connection in self._connections

    # --- clean under this ---

    def on_node_unexpectedly_deleted(self, node):
        """
        Called when the node is unexpectedly deleted.
        :param NodeModel node: A currently-visible NodeModel.
        """
        self.remove_node(node, emit=True)

    def on_attribute_unexpectedly_added(self, port):
        """
        Called when a new port is unexpectedly added.
        :param omtk.nodegraph.PortModel port: A not-yet-visible Attribute.
        """
        self.add_port(port)

    def on_attribute_unexpectedly_removed(self, port):
        """
        Callback called when a port is unexpectedly removed from the REGISTRY_DEFAULT associated with the graph.
        :param omtk.nodegraph.PortModel port: The port that was removed.
        """
        node = port.get_parent()
        node._unregister_port(port)
        self.remove_port(port)

    def on_connection_unexpectedly_added(self, connection):
        self.add_connection(connection)

    def on_connection_unexpectedly_removed(self, connection):
        self.remove_connection(connection)

    # --- Automatic node positioning ---

    def get_available_position(self, node):
        """
        Return a position where a provided node can be positioned without overlapping other nodes.
        :param NodeModel node: The node to reference in term of dimensions.
        :return: An available position in the graph.
        :rtype: QtCore.QRectF
        """
        # TODO: MAKE IT WORK :<
        try:
            self._counter += 1
        except AttributeError:
            self._counter = 0

        node_width = 100
        x = self._counter * node_width
        y = 0
        return QtCore.QPointF(x * 2, y * 2)

    def get_available_position_2(self, qrect_item):
        """
        Return a position where a provided node can be positioned without overlapping other nodes.
        2nd attempt.
        :param ??? node: The node to reference in term of dimensions.
        :return: An available position in the graph.
        :rtype: QtCore.QRectF
        """
        qrect_scene = self.sceneRect()
        item_width = qrect_item.width()
        item_height = qrect_item.height()

        def _does_intersect(guess):
            for node in self.iter_nodes():
                node_qrect = node.transform().mapRect(())
                if node_qrect.intersects(guess):
                    return True

            return False

        for x in libPython.frange(qrect_scene.left(), qrect_scene.right()*2, item_width):
            for y in libPython.frange(qrect_scene.top(), qrect_scene.bottom(), item_height):
                qrect_candidate = QtCore.QRectF(x, y, item_width, item_height)
                if not _does_intersect(qrect_candidate):
                    return QtCore.QPointF(x, y)
