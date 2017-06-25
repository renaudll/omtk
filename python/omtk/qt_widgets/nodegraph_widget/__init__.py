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
from omtk.libs import libPyflowgraph
from omtk.libs import libPython
from omtk.qt_widgets.nodegraph_widget.ui import nodegraph_widget
from omtk.vendor.Qt import QtWidgets

from .nodegraph_model import NodeGraphModel
from .nodegraph_view import NodeGraphView
from .nodegraph_controller import NodeGraphController


@libPython.memoized
def _get_singleton_model():
    return NodeGraphModel()


def reload_():
    from omtk.qt_widgets.nodegraph_widget import nodegraph_port_model
    reload(nodegraph_port_model)

    from omtk.qt_widgets.nodegraph_widget import nodegraph_connection_model
    reload(nodegraph_connection_model)

    from omtk.qt_widgets.nodegraph_widget import nodegraph_node_model
    reload(nodegraph_node_model)

    from omtk.qt_widgets.nodegraph_widget import nodegraph_model
    reload(nodegraph_model)

    from omtk.qt_widgets.nodegraph_widget import nodegraph_view
    reload(nodegraph_view)

    from omtk.qt_widgets.nodegraph_widget import nodegraph_controller
    reload(nodegraph_controller)

    from . import ui
    reload(ui)
    ui.reload_()
reload_()  # debugging

class NodeGraphWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NodeGraphWidget, self).__init__(parent)
        self.ui = nodegraph_widget.Ui_Form()
        self.ui.setupUi(self)

        # Configure NodeGraphView
        self._nodegraph_view = self.ui.widget
        self._nodegraph_model = _get_singleton_model()
        self._nodegraph_ctrl = NodeGraphController(self._nodegraph_model, self._nodegraph_view)

        self._nodegraph_view.set_model(self._nodegraph_ctrl)

        # Connect events
        self.ui.pushButton.pressed.connect(self.on_add)
        self.ui.pushButton_2.pressed.connect(self.on_del)
        self.ui.pushButton_3.pressed.connect(self.on_expand)
        self.ui.pushButton_4.pressed.connect(self.on_colapse)
        self.ui.pushButton_5.pressed.connect(self.on_navigate_down)
        self.ui.pushButton_6.pressed.connect(self.on_navigate_up)

        self.ui.widget.endSelectionMoved.connect(self.on_selected_nodes_moved)

    def on_selected_nodes_moved(self):
        for node in self.ui.widget.getSelectedNodes():
            if node._meta_data:
                new_pos = node.pos()  # for x reason, .getGraphPos don't work here
                new_pos = (new_pos.x(), new_pos.y())
                libPyflowgraph.save_node_position(node, new_pos)

    def on_add(self):
        raise NotImplementedError

    def on_del(self):
        graph = self.ui.widget
        graph.deleteSelectedNodes()

    def on_expand(self):
        self._nodegraph_ctrl.expand_selected_nodes()

    def on_colapse(self):
        return self._nodegraph_ctrl.colapse_selected_nodes()

    def on_navigate_down(self):
        self._nodegraph_ctrl.navigate_down()

    def on_navigate_up(self):
        self._nodegraph_ctrl.navigate_up()

# from pyflowgraph.graph_view import GraphView as NodeGraphWidget
