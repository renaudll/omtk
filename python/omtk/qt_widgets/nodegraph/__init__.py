"""
The NodeGraphWidget use PyFlowgraph to display node, attribute and connections.
It use a NodeGraphModel generaly used as a singleton to store scene informations.
Multiple NodeGraphController bound to this model can interact with multiples NodeGraphView.

Usage example 1, handling MVC ourself
from omtk.qt_widgets import nodegraph_widget
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

win = QtWidgets.QMainWindow()
view = nodegraph_widget.NodeGraphView()
model = nodegraph_widget.NodeGraphModel()
ctrl = nodegraph_widget.NodeGraphController(model, view)
win.setCentralWidget(view)
win.show()

Usage example 1, using prefab Widget
from omtk.qt_widgets import nodegraph_widget
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

win = QtWidgets.QMainWindow()
widget = nodegraph_widget.NodeGraphWidget()
win.setCentralWidget(widget)
win.show()
"""

from . import nodegraph_registry
NodeGraphRegistry = nodegraph_registry.NodeGraphRegistry

from . import nodegraph_widget
NodeGraphWidget = nodegraph_widget.NodeGraphWidget

from . import nodegraph_view
NodeGraphView = nodegraph_view.NodeGraphView

from . import nodegraph_controller
NodeGraphController = nodegraph_controller.NodeGraphController

from . import nodegraph_filter
NodeGraphControllerFilter = nodegraph_filter.NodeGraphFilter


def reload_():
    from . import pyflowgraph_node_widget
    reload(pyflowgraph_node_widget)

    from . import pyflowgraph_port_widget
    reload(pyflowgraph_port_widget)

    from .. import widget_toolbar
    reload(widget_toolbar)

    from . import filters
    reload(filters)
    filters.reload_()

    from . import models
    reload(models)
    models.reload_()

    from . import nodegraph_registry
    reload(nodegraph_registry)

    from . import nodegraph_view
    reload(nodegraph_view)

    from . import nodegraph_filter
    reload(nodegraph_filter)

    from . import nodegraph_controller
    reload(nodegraph_controller)

    from . import nodegraph_widget
    reload(nodegraph_widget)

    from . import ui
    reload(ui)
    ui.reload_()

    global NodeGraphWidget
    NodeGraphWidget = nodegraph_widget.NodeGraphWidget

    global NodeGraphView
    NodeGraphView = nodegraph_view.NodeGraphView

    global NodeGraphController
    NodeGraphController = nodegraph_controller.NodeGraphController

    global NodeGraphModel
    NodeGraphModel = nodegraph_registry.NodeGraphRegistry

    global NodeGraphControllerFilter
    NodeGraphControllerFilter = nodegraph_filter.NodeGraphFilter
