import abc
import logging

from omtk.vendor.Qt import QtCore
from omtk.qt_widgets.nodegraph.models.node import node_base as node_model
from omtk.qt_widgets.nodegraph.models import port as port_model
from omtk.qt_widgets.nodegraph.models import connection as connection_model

log = logging.getLogger('omtk.nodegraph')

# for type hinting
if False:
    from omtk.qt_widgets.nodegraph.models.node.node_base import NodeGraphNodeModel
    from omtk.qt_widgets.nodegraph.nodegraph_connection_model import NodeGraphConnectionModel
    from omtk.qt_widgets.nodegraph import NodeGraphPortModel


class QtCoreAbcMeta(type(QtCore.QObject), abc.ABCMeta):
    """
    Helper class so abc.ABCMeta and QtCore.QObject play nicely together.
    src: https://stackoverflow.com/questions/46837947/how-to-create-an-abstract-base-class-in-python-which-derived-from-qobject
    """
    pass


class NodeGraphAbstractModel(QtCore.QObject):

    """
    Define a nodal network from various NodeGraph[Node/Port/Connection]Model instances.
    Subgraphs and filters can be implemented by feeding a NodeGraphRegistry through a NodeGraphProxyModel.
    NodeGraphRegistry are consumed
    """
    __metaclass__ = QtCoreAbcMeta

    onNodeAdded = QtCore.Signal(node_model.NodeGraphNodeModel)
    onNodeRemoved = QtCore.Signal(node_model.NodeGraphNodeModel)
    onNodeMoved = QtCore.Signal(node_model.NodeGraphNodeModel, QtCore.QPointF)
    onPortAdded = QtCore.Signal(port_model.NodeGraphPortModel)
    onPortRemoved = QtCore.Signal(port_model.NodeGraphPortModel)
    onConnectionAdded = QtCore.Signal(connection_model.NodeGraphConnectionModel)
    onConnectionRemoved = QtCore.Signal(connection_model.NodeGraphConnectionModel)

    # def __init__(self):
    #     super(NodeGraphAbstractModel, self).__init__()  # initialize Qt signals

    @abc.abstractmethod
    def reset(self):
        # type: () -> None
        """"""

    # --- Node methods ---

    @abc.abstractmethod
    def iter_nodes(self):
        # type: () -> List[NodeGraphNodeModel]
        """"""

    def get_nodes(self):
        # type: () -> List[NodeGraphNodeModel]
        """"""
        return list(self.iter_nodes())

    @abc.abstractmethod
    def add_node(self, node, emit_signal=False):
        # type: (NodeGraphNodeModel, bool) -> None
        """"""

    @abc.abstractmethod
    def remove_node(self, node, emit_signal=False):
        # type: (NodeGraphNodeModel, bool) -> None
        """"""

    @abc.abstractmethod
    def get_node_position(self, node):
        # type: (NodeGraphNodeModel) -> None
        """"""

    @abc.abstractmethod
    def set_node_position(self, node, pos, emit_signal=True):
        # type: (NodeGraphNodeModel, QtCore.QRectF, bool) -> None
        """"""

    @abc.abstractmethod
    # --- Port methods ---

    def iter_ports(self):
        # type: () -> Generator[NodeGraphPortModel]
        """"""
        return
        yield

    def get_ports(self):
        # type: () -> List[NodeGraphPortModel]
        return list(self.iter_ports())

    def iter_node_ports(self, node):
        # type: (NodeGraphNodeModel) -> Generator[NodeGraphPortModel]
        """"""
        return
        yield

    def get_node_ports(self, node):
        # type: (NodeGraphNodeModel) -> List[NodeGraphPortModel]
        return list(self.iter_node_ports(node))

    @abc.abstractmethod
    def add_port(self, port, emit_signal=False):
        # type: (NodeGraphPortModel, bool) -> None
        """"""

    @abc.abstractmethod
    def remove_port(self, port, emit_signal=False):
        # type: (NodeGraphPortModel, bool) -> None
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

    # def expand_node(self, node_model):
    #     # type: (NodeGraphNodeModel) -> None
    #     """
    #     Show all available attributes for a PyFlowgraph Node.
    #     Add it in the pool if it didn't previously exist.
    #     :return:
    #     """
    #     for port.py in sorted(self.iter_ports(node_model)):
    #         self.get_port_widget(port.py)

    # --- clean this

    # @abc.abstractmethod
    # def expand_node(self, node):
    #     # type: (NodeGraphNodeModel) -> None
    #     """"""
    #
    # @abc.abstractmethod
    # def expand_port(self, port):
    #     """"""
    #
    # # todo: replace with self.get_node_ports?
    # @abc.abstractmethod
    # def expand_node_ports(self, node_model, expand_downstream=True, expand_upstream=True):
    #     """"""
    #
    # @abc.abstractmethod
    # def expand_port_input_connections(self, port_model):
    #     """"""
    #
    # @abc.abstractmethod
    # def expand_port_output_connections(self, port_model):
    #     """"""

    # --- Utility methods
    # --- These method use the abstract methods

    def expand_node(self, node):
        # type: (NodeGraphNodeModel) -> None
        """
        Show all available attributes for a PyFlowgraph Node.
        Add it in the pool if it didn't previously exist.
        :return:
        """
        for port in sorted(self.iter_node_ports(node)):
            self.add_port(port)
            # self.get_port_widget(port_model)

        # Update cache
        self._expanded_nodes.add(node)

    def expand_port(self, port, inputs=True, outputs=True):
        # type: (NodeGraphPortModel, bool, bool) -> None
        if inputs:
            self.expand_port_input_connections(port)
        if outputs:
            self.expand_port_output_connections(port)

    def expand_port_input_connections(self, port):
        for connection in self.get_port_input_connections(port):
            self.add_connection(connection, emit_signal=True)
            # self.get_connection_widget(connection_model)

    def expand_port_output_connections(self, port):
        for connection in self.get_port_output_connections(port):
            self.add_connection(connection, emit_signal=True)
            # self.get_connection_widget(connection_model)

    def expand_node_ports(self, node, inputs=True, outputs=True):
        # type: (NodeGraphNodeModel, bool, bool) -> None
        for port in self.get_node_ports(node):
            if port not in self._ports:
                self.add_port(port, emit_signal=False)
            if outputs:
                self.expand_port_output_connections(port)
            if inputs:
                self.expand_port_input_connections(port)

        # Update cache
        self._expanded_nodes_ports.add(node)

    def iter_port_connections(self, port):
        # type: (NodeGraphPortModel) -> Generator[NodeGraphConnectionModel]
        for connection in self._iter_port_input_connections(port):
            yield connection
        for connection in self._iter_port_output_connections(port):
            yield connection

        # for connection in port.get_input_connections(self):
        #     yield connection

    def _iter_port_input_connections(self, model):
        # type: (NodeGraphPortModel) -> list[NodeGraphConnectionModel]
        """
        Control what input connection models are exposed for the provided port model.
        :param model: The destination port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as destination.
        """
        for connection in model.get_input_connections():
            yield connection

    def get_port_input_connections(self, model):
        return list(self._iter_port_input_connections(model))  # cannot memoize a generator

    def _iter_port_output_connections(self, model):
        # type: (NodeGraphPortModel) -> List[NodeGraphPortModel]
        """
        Control what output connection models are exposed for the provided port model.
        :param model: The source port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as source.
        """
        for connection in model.get_output_connections():
            yield connection

    def get_port_output_connections(self, model):
        return list(self._iter_port_output_connections(model))  # cannot memoize a generator

