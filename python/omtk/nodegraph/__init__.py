"""
The ``NodeGraphWidget`` use ``PyFlowgraph`` to display node, attribute and connections.
It use a ``GraphModel`` generaly used as a singleton to store scene informations.
Multiple NodeGraphController bound to this model can interact with multiples NodeGraphView.

Usage example 1, handling MVC yourself


    >>> from omtk.nodegraph import NodeGraphView, GraphModel, NodeGraphController
    >>> from omtk.vendor.Qt import QtCore, QtGui, QtWidgets
    >>> win = QtWidgets.QMainWindow()
    >>> view = NodeGraphView()
    >>> model = GraphModel()
    >>> ctrl = NodeGraphController(model, view)
    >>> win.setCentralWidget(view)
    >>> win.show()

Usage example 1, using prefab Widget

    >>> from omtk.nodegraph import NodeGraphWidget
    >>> from omtk.vendor.Qt import QtCore, QtGui, QtWidgets
    >>> win = QtWidgets.QMainWindow()
    >>> widget = NodeGraphWidget()
    >>> win.setCentralWidget(widget)
    >>> win.show()
"""

from omtk.nodegraph.registry import NodeGraphRegistry
from omtk.nodegraph.filter_ import NodeGraphFilter
from omtk.nodegraph.models import GraphModel, NodeModel, PortModel, ConnectionModel
from omtk.nodegraph.models.graph.graph_model_abstract import IGraphModel
from omtk.nodegraph.models.graph.graph_proxy_model import NodeGraphGraphProxyModel
from omtk.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel
from omtk.nodegraph.bindings.base import ISession
from omtk.nodegraph.signal import Signal
