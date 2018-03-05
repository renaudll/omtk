import abc
import logging

from omtk.vendor.Qt import QtCore
from omtk.qt_widgets.nodegraph.models.node import node_base as nodegraph_node_model_base

# from omtk.qt_widgets.nodegraph import nodegraph_connection_model
# from omtk.qt_widgets.nodegraph import nodegraph_port_model

log = logging.getLogger('omtk.nodegraph')

# for type hinting
if False:
    from omtk.qt_widgets.nodegraph.models.node.node_base import NodeGraphNodeModel
    from omtk.qt_widgets.nodegraph.nodegraph_connection_model import NodeGraphConnectionModel
    from omtk.qt_widgets.nodegraph import NodeGraphPortModel


class NodeGraphAbstractModel(QtCore.QObject):
    """
    Define a nodal network from various NodeGraph[Node/Port/Connection]Model instances.
    Subgraphs and filters can be implemented by feeding a NodeGraphRegistry through a NodeGraphProxyModel.
    NodeGraphRegistry are consumed
    """
    # __metaclass__ = abc.ABCMeta

    onNodeAdded = QtCore.Signal(nodegraph_node_model_base.NodeGraphNodeModel)
    onNodeRemoved = QtCore.Signal(nodegraph_node_model_base.NodeGraphNodeModel)
    onNodeMoved = QtCore.Signal(nodegraph_node_model_base.NodeGraphNodeModel, QtCore.QPointF)
    # onPortAdded = QtCore.Signal(nodegraph_port_model.NodeGraphPortModel)
    # onPortRemoved = QtCore.Signal(nodegraph_port_model.NodeGraphPortModel)
    # onConnectionAdded = QtCore.Signal(nodegraph_connection_model.NodeGraphConnectionModel)
    # onConnectionRemoved = QtCore.Signal(nodegraph_connection_model.NodeGraphConnectionModel)

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

    # --- Port methods ---

    def iter_ports(self):
        # type: () -> List[NodeGraphPortModel]
        """"""

    def get_ports(self):
        # type: () -> List[NodeGraphPortModel]
        return list(self.iter_ports())

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

    # --- Exploration methods ---

    @abc.abstractmethod
    def iter_ports(self, node):
        """"""

    # def expand_node_attributes(self, node_model):
    #     # type: (NodeGraphNodeModel) -> None
    #     """
    #     Show all available attributes for a PyFlowgraph Node.
    #     Add it in the pool if it didn't previously exist.
    #     :return:
    #     """
    #     for port.py in sorted(self.iter_ports(node_model)):
    #         self.get_port_widget(port.py)
