"""
The ``NodeGraphWidget`` use ``PyFlowgraph`` to display node, attribute and connections.
It use a ``GraphModel`` generaly used as a singleton to store scene informations.
Multiple NodeGraphController bound to this model can interact with multiples NodeGraphView.

Usage example 1, handling MVC ourself


    >>> from omtk import nodegraph
    >>> from omtk.vendor.Qt import QtCore, QtGui, QtWidgets
    >>> win = QtWidgets.QMainWindow()
    >>> view = nodegraph.NodeGraphView()
    >>> model = nodegraph.GraphModel()
    >>> ctrl = nodegraph.NodeGraphController(model, view)
    >>> win.setCentralWidget(view)
    >>> win.show()

Usage example 1, using prefab Widget

    >>> from omtk import nodegraph
    >>> from omtk.vendor.Qt import QtCore, QtGui, QtWidgets
    >>> win = QtWidgets.QMainWindow()
    >>> widget = nodegraph.NodeGraphWidget()
    >>> win.setCentralWidget(widget)
    >>> win.show()
"""

from omtk.nodegraph.registry import base

NodeGraphRegistry = base.NodeGraphRegistry

# from omtk.nodegraph import nodegraph_widget
# NodeGraphWidget = nodegraph_widget.NodeGraphWidget

# from omtk.nodegraph import nodegraph_view
# NodeGraphView = nodegraph_view.NodeGraphView

from omtk.nodegraph import nodegraph_controller

NodeGraphController = nodegraph_controller.NodeGraphController

# from omtk_nodegraph import nodegraph_filter

# NodeGraphFilter = nodegraph_filter.NodeGraphFilter

from omtk.nodegraph.models import GraphModel, NodeModel, PortModel, ConnectionModel
from omtk.nodegraph.models.graph.graph_model_abstract import IGraphModel
from omtk.nodegraph.models.graph.graph_proxy_model import NodeGraphGraphProxyModel
from omtk.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel
