import abc
import logging

from omtk.vendor.Qt import QtCore
from omtk.qt_widgets.nodegraph.models.node import node_base as node_model
from omtk.qt_widgets.nodegraph.models.port import port_base as port_model
from omtk.qt_widgets.nodegraph.models import connection as connection_model

log = logging.getLogger('omtk.nodegraph')

# for type hinting
if False:
    from typing import List, Generator
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphPortModel, NodeGraphConnectionModel


class QtCoreAbcMeta(type(QtCore.QObject), abc.ABCMeta):
    """
    Helper class so abc.ABCMeta and QtCore.QObject play nicely together.
    src: https://stackoverflow.com/questions/46837947/how-to-create-an-abstract-base-class-in-python-which-derived-from-qobject
    """
    # todo: abc.ABCMeta don't seem to work
    pass


class NodeGraphAbstractModel(QtCore.QObject):

    """
    Define a nodal network from various NodeGraph[Node/Port/Connection]Model instances.
    Subgraphs and filters can be implemented by feeding a NodeGraphRegistry through a NodeGraphProxyModel.
    NodeGraphRegistry are consumed
    """
    __metaclass__ = QtCoreAbcMeta

    # Signal emitted when a node is added in the model.
    onNodeAdded = QtCore.Signal(node_model.NodeGraphNodeModel)

    # Signal emitted when a node is removed from the model.
    onNodeRemoved = QtCore.Signal(node_model.NodeGraphNodeModel)

    # Signal emitted when a node position change.
    onNodeMoved = QtCore.Signal(node_model.NodeGraphNodeModel, QtCore.QPointF)

    # Signal emitted when a node port is added in the model.
    onPortAdded = QtCore.Signal(port_model.NodeGraphPortModel)

    # Signal emitted when a node port is removed from the model.
    onPortRemoved = QtCore.Signal(port_model.NodeGraphPortModel)

    # Signal emitted when a port connection is added in the model.
    onConnectionAdded = QtCore.Signal(connection_model.NodeGraphConnectionModel)

    # Signal emitted when a port connection is removed from the model.
    onConnectionRemoved = QtCore.Signal(connection_model.NodeGraphConnectionModel)

    # Signal emitted before the model internal state has been invalidated.
    onAboutToBeReset = QtCore.Signal()

    # Signal emitted after the model internal state has been invalidated.
    onReset = QtCore.Signal()

    @abc.abstractmethod
    def reset(self):
        # type: () -> None
        """"""
        self.onAboutToBeReset.emit()
        self.onReset.emit()

    # --- Node methods ---

    @abc.abstractmethod
    def iter_nodes(self):
        # type: () -> List[NodeGraphNodeModel]
        """
        Yield all the nodes visible in the graph.
        :return: A generator that yield NodeGraphNodeModel instances.
        """

    def get_nodes(self):
        # type: () -> List[NodeGraphNodeModel]
        """
        Return all node visible in the graph.
        :return: A list of NodeGraphNodeModel instances.
        """
        return list(self.iter_nodes())

    @abc.abstractmethod
    def add_node(self, node, emit_signal=False):
        # type: (NodeGraphNodeModel, bool) -> None
        """
        Add a node to the graph.
        :param node: A NodeGraphNodeModel instance.
        :param emit_signal: If True, the onNodeAdded QSignal will emit.
        """

    @abc.abstractmethod
    def remove_node(self, node, emit_signal=False):
        # type: (NodeGraphNodeModel, bool) -> None
        """"""

    @abc.abstractmethod
    def is_node_visible(self, node):
        # type: (NodeGraphNodeModel) -> bool
        """"""

    @abc.abstractmethod
    def get_node_position(self, node):
        # type: (NodeGraphNodeModel) -> None
        """"""

    @abc.abstractmethod
    def set_node_position(self, node, pos, emit_signal=True):
        # type: (NodeGraphNodeModel, QtCore.QRectF, bool) -> None
        """"""

    # --- Port methods ---

    @abc.abstractmethod
    def iter_ports(self):
        # type: () -> Generator[NodeGraphPortModel]
        """"""
        return
        yield

    def get_ports(self):
        # type: () -> List[NodeGraphPortModel]
        """
        Return all node visible in the graph.
        :return: A list of NodeGraphNodeModel instances.
        """
        return list(self.iter_ports())

    @abc.abstractmethod
    def add_port(self, port, emit_signal=False):
        # type: (NodeGraphPortModel, bool) -> None
        """"""

    @abc.abstractmethod
    def remove_port(self, port, emit_signal=False):
        # type: (NodeGraphPortModel, bool) -> None
        """"""

    @abc.abstractmethod
    def is_port_visible(self, port):
        # type: (NodeGraphPortModel) -> bool
        """"""

    # --- Connection methods ---

    @abc.abstractmethod
    def iter_connections(self):
        # type: () -> List[NodeGraphConnectionModel]
        """"""

    @abc.abstractmethod
    def get_connections(self):
        # type: () -> List[NodeGraphConnectionModel]
        """"""
        return list(self.iter_connections())

    @abc.abstractmethod
    def add_connection(self, connection, emit_signal=False):
        # type: (NodeGraphConnectionModel, bool) -> None
        """"""

    @abc.abstractmethod
    def remove_connection(self, connection, emit_signal=False):
        # type: (NodeGraphConnectionModel, bool) -> None
        """"""

    @abc.abstractmethod
    def is_connection_visible(self, connection):
        # type: (NodeGraphConnectionModel) -> bool
        """"""

    # --- Exploration methods that add nothing to the graph ---

    def iter_node_ports(self, node):
        # type: (NodeGraphNodeModel) -> Generator[NodeGraphPortModel]
        """
        Yield all ports inside a node model. This don't add the port into the graph.
        :param node: A NodeGraphNodeModel instance.
        :return: A generator that yield NodeGraphPortModel.
        """
        return
        yield

    def get_node_ports(self, node):
        # type: (NodeGraphNodeModel) -> List[NodeGraphPortModel]
        return list(self.iter_node_ports(node))

    def iter_port_connections(self, port):
        # type: (NodeGraphPortModel) -> Generator[NodeGraphConnectionModel]
        for connection in self.iter_port_input_connections(port):
            yield connection
        for connection in self.iter_port_output_connections(port):
            yield connection

    def get_port_connections(self, port):
        return list(self.iter_port_connections(port))

    def iter_port_input_connections(self, port):
        # type: (NodeGraphPortModel) -> list[NodeGraphConnectionModel]
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
        # type: (NodeGraphPortModel) -> List[NodeGraphPortModel]
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
        # type: (NodeGraphNodeModel, bool, bool) -> Generator[NodeGraphConnectionModel]
        for port in self.iter_node_ports(node):
            if outputs:
                for connection in self.iter_port_output_connections(port):
                    yield connection
            if inputs:
                for connection in self.iter_port_input_connections(port):
                    yield connection

    # --- Utility methods ---

    def expand_node_ports(self, node):
        # type: (NodeGraphNodeModel) -> None
        """
        Show all available attributes for a PyFlowgraph Node.
        Add it in the pool if it didn't previously exist.
        :return:
        """
        for port in sorted(self.iter_node_ports(node)):
            self.add_port(port, emit_signal=True)

    def expand_node_connections(self, node, inputs=True, outputs=True):
        for port in self.iter_node_ports(node):
            if inputs:
                for connection in self.iter_port_input_connections(port):
                    self.add_connection(connection)
            if outputs:
                for connection in self.iter_port_output_connections(port):
                    self.add_connection(connection)

    def expand_port_input_connections(self, port):
        # type: (NodeGraphPortModel) -> None
        for connection in self.iter_port_input_connections(port):
            self.add_connection(connection)

    def expand_port_output_connections(self, port):
        # type: (NodeGraphPortModel) -> None
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
