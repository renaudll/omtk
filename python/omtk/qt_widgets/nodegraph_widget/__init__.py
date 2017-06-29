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

from . import nodegraph_widget


def reload_():
    from . import nodegraph_port_model
    reload(nodegraph_port_model)

    from . import nodegraph_connection_model
    reload(nodegraph_connection_model)

    from . import nodegraph_node_model
    reload(nodegraph_node_model)

    from . import nodegraph_model
    reload(nodegraph_model)

    from . import nodegraph_view
    reload(nodegraph_view)

    from . import nodegraph_controller
    reload(nodegraph_controller)

    from . import nodegraph_widget
    reload(nodegraph_widget)

    from . import ui
    reload(ui)
    ui.reload_()

# NodeGraphWidget = nodegraph_widget.NodeGraphWidget
