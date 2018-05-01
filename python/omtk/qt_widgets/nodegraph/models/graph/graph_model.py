import functools
import logging
from collections import defaultdict

from omtk.qt_widgets.nodegraph.models.graph import graph_model_abstract
from omtk.vendor.Qt import QtCore

log = logging.getLogger('omtk.nodegraph')

# for type hinting
if False:
    from typing import List
    from omtk.qt_widgets.nodegraph.models.node.node_base import NodeGraphNodeModel
    from omtk.qt_widgets.nodegraph.nodegraph_connection_model import NodeGraphConnectionModel
    from omtk.qt_widgets.nodegraph.port_model import NodeGraphPortModel
    from omtk.qt_widgets.nodegraph.nodegraph_registry import NodeGraphRegistry


class NodeGraphModel(graph_model_abstract.NodeGraphAbstractModel):
    """
    Define a nodal network from various NodeGraph[Node/Port/Connection]Model instances.
    Subgraphs and filters can be implemented by feeding a NodeGraphRegistry through a NodeGraphProxyModel.
    NodeGraphRegistry are consumed
    """

    def __init__(self, registry=None):
        super(NodeGraphModel, self).__init__()  # initialize Qt signals

        self._registry = None
        self._nodes = set()
        self._ports = set()
        self._connections = set()
        self._pos_by_node = {}  # (k is a NodeGraphNodeModel, v is a QRectF).

        self._nodes_by_port = defaultdict(set)
        self._ports_by_nodes = defaultdict(set)

        self._ports_by_connection = defaultdict(set)
        self._connections_by_port = defaultdict(set)

        from omtk.qt_widgets.nodegraph import nodegraph_registry
        if registry is None:
            registry = nodegraph_registry.get_registry()
        self.set_registry(registry)

    def reset(self, expand=True):
        self.onAboutToBeReset.emit()

        for node in list(self.get_nodes()):  # hack: prevent change during iteration
            self.remove_node(node, emit_signal=False)

        # todo: remove this, they should get cleaned by themself
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

        self.onReset.emit()

    def set_registry(self, registry):
        # type: (NodeGraphRegistry) -> None
        if self._registry:
            self._registry.onNodeDeleted.disconnect(self.on_node_unexpectedly_deleted)
        #     self._registry.onAttributeAdded.disconnect(self.on_attribute_unexpectedly_added)
        #     # self._registry.onAttributeRemoved.disconnect(self.)
        registry.onNodeDeleted.connect(self.on_node_unexpectedly_deleted)
        # registry.onAttributeAdded.connect(self.on_attribute_unexpectedly_added)
        # # registry.onAttributeRemoved.connect()

        # Pass any signals emitted by the registry.
        registry.onNodeDeleted.connect(self.onNodeRemoved.emit)

        self._registry = registry

    # --- Node methods ---

    def iter_nodes(self):
        return iter(self._nodes)

    def get_nodes(self):
        # type: () -> List[NodeGraphNodeModel]
        return self._nodes

    def add_node(self, node, emit_signal=False):
        # type: (NodeGraphNodeModel, bool) -> None
        if node in self._nodes:
            return

        # node.onDeleted.connect(self.on_node_unexpectedly_deleted)
        # node.onAttributeAdded.connect(self.on_attribute_unexpectedly_added)

        pos = self.get_available_position(node)
        self._nodes.add(node)
        self._pos_by_node[node] = pos  # todo: handle automatic positioning
        if emit_signal:
            self.onNodeAdded.emit(node)

    def remove_node(self, node, emit_signal=False):
        # type: (NodeGraphNodeModel, bool) -> None

        if not self.is_node_visible(node):
            log.debug("Cannot remove Node {0}. Node is not in view.".format(node))
        else:

            self._nodes.remove(node)
            self._pos_by_node.pop(node)

            # node.onDeleted.disconnect(self.on_node_unexpectedly_deleted)
            # node.onAttributeAdded.disconnect(self.on_attribute_unexpectedly_added)

            # if node in self._expanded_nodes:
            #     self._expanded_nodes.remove(node)
            # if node in self._nodes_with_expanded_connections:
            #     self._nodes_with_expanded_connections.remove(node)

            # Remove node ports
            for port in list(self._ports_by_nodes[node]):  # hack: prevent change during iteration
                self.remove_port(port, emit_signal=False)  # we expect the user to know we're removing the port?
            self._ports_by_nodes.pop(node)

        if emit_signal:
            self.onNodeRemoved.emit(node)

    def is_node_visible(self, node):
        return node in self._nodes

    def get_node_position(self, node):
        # type: (NodeGraphNodeModel) -> None
        return self._pos_by_node[node]

    def set_node_position(self, node, pos, emit_signal=True):
        # type: (NodeGraphNodeModel, QtCore.QRectF, bool) -> None
        self._pos_by_node[node] = pos

        if emit_signal:
            self.onNodeMoved.emit(node, pos)

    # --- Port methods ---

    def iter_ports(self):
        for node in self.iter_nodes():
            for port in self.iter_node_ports(node):
                if not port in self._ports:
                    self._ports.add(port)
                yield port
        # return iter(self._ports)

    def get_ports(self):
        # # todo: optimize?
        # result = []
        # for node in self.get_nodes():
        #     for port in node.iter_ports():
        #         result.append(port)
        # return result
        # return self._ports
        return list(self.iter_ports())

    def iter_node_ports(self, node):
        for port in node.iter_ports():
            yield port

    def get_node_ports(self, node):
        return list(self.iter_node_ports(node))

    def add_port(self, port, emit_signal=True):
        # type: (NodeGraphPortModel, bool) -> None
        if port in self._ports:
            return

        self._ports.add(port)

        node = port.get_parent()
        if not node in self._nodes:
            self.add_node(node)

        self._ports_by_nodes[node].add(port)
        self._nodes_by_port[port].add(node)

        if emit_signal:
            self.onPortAdded.emit(port)

    def remove_port(self, port, emit_signal=True):
        # type: (NodeGraphPortModel, bool) -> None
        self._ports.remove(port)

        # Remove port connections
        for connection in list(self._connections_by_port[port]):  # hack: prevent change during iteration
            self.remove_connection(connection, emit_signal=emit_signal)
        self._connections_by_port.pop(port)

        # Update cache
        for node in self._nodes_by_port[port]:
            self._ports_by_nodes[node].remove(port)
        self._nodes_by_port.pop(port)

        if emit_signal:
            self.onPortRemoved.emit(port)

    def is_port_visible(self, port):
        return port in self._ports

    # --- Connection methods ---

    def iter_connections(self):
        return iter(self._connections)

    def get_connections(self):
        return self._connections

    def add_connection(self, connection, emit_signal=True):
        # type: (NodeGraphConnectionModel, bool) -> None
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

        if emit_signal:
            self.onConnectionAdded.emit(connection)

    def remove_connection(self, connection, emit_signal=True):
        # type: (NodeGraphConnectionModel, bool) -> None
        self._connections.remove(connection)

        # Update cache
        for port in self._ports_by_connection[connection]:
            self._connections_by_port[port].remove(connection)
        self._ports_by_connection.pop(connection)

        if emit_signal:
            self.onConnectionRemoved.emit(connection)

    def is_connection_visible(self, connection):
        return connection in self._connections

    # --- clean under this ---

    def on_node_unexpectedly_deleted(self, node):
        # type: (NodeGraphNodeModel) -> None
        """
        Called when the node is unexpectedly deleted.
        :param node: A currently-visible NodeGraphNodeModel.
        """
        self.remove_node(node, emit_signal=True)

    def on_attribute_unexpectedly_added(self, port):
        # type: (NodeGraphPortModel) -> None
        """
        Called when a new port is unexpectedly added.
        :param port: A not-yet-visible NodeGraphPortModel.
        """
        self.add_port(port)

    # --- Automatic node positioning ---

    def get_available_position(self, node):
        """Fake one until the real one work"""
        try:
            self._counter += 1
        except AttributeError:
            self._counter = 0

        node_width = 100
        x = self._counter * node_width
        y = x
        return QtCore.QPointF(x * 3, y * 2)

    def real_get_available_position(self, qrect_item):
        """
        Return a position where we can position a QRectF without overlapping existing widgets.
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
