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
import logging

from omtk import manager
from omtk.core import classComponent
from omtk.libs import libPyflowgraph
from omtk.libs import libPython
from omtk.qt_widgets.nodegraph_widget.ui import nodegraph_widget
from omtk.vendor.Qt import QtWidgets

from . import nodegraph_view

log = logging.getLogger('omtk')


@libPython.memoized
def _get_singleton_model():
    from .nodegraph_model import NodeGraphModel

    return NodeGraphModel()


class NodeGraphWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        from .nodegraph_controller import NodeGraphController

        super(NodeGraphWidget, self).__init__(parent)
        self.ui = nodegraph_widget.Ui_Form()
        self.ui.setupUi(self)

        # Configure NodeGraphView
        # self._manager = None
        self._model = _get_singleton_model()
        self._ctrl = NodeGraphController(self._model)
        self._ctrl.onLevelChanged.connect(self.on_breadcrumb_changed)

        # Keep track of the multiple views provided by the QTabWidget
        self._current_view = None
        self._views = []

        # Connect events
        self.ui.pushButton_add.pressed.connect(self.on_add)
        self.ui.pushButton_del.pressed.connect(self.on_del)
        self.ui.pushButton_expand.pressed.connect(self.on_expand)
        self.ui.pushButton_collapse.pressed.connect(self.on_colapse)
        self.ui.pushButton_down.pressed.connect(self.on_navigate_down)
        self.ui.pushButton_up.pressed.connect(self.on_navigate_up)
        self.ui.pushButton_arrange_upstream.pressed.connect(self.on_arrange_upstream)
        self.ui.pushButton_arrange_downstream.pressed.connect(self.on_arrange_downstream)
        self.ui.pushButton_arrange_spring.pressed.connect(self.on_arrange_spring)
        self.ui.pushButton_group.pressed.connect(self.on_group)
        self.ui.pushButton_ungroup.pressed.connect(self.on_ungroup)

        # Connect events (breadcrumb)
        self.ui.widget_breadcrumb.path_changed.connect(self.on_breadcrumb_changed)

        # At least create one tab
        self.create_tab()

        # Load root level
        self._ctrl.set_level(None)

    @property
    def manager(self):
        return manager.get_manager()

    def get_controller(self):
        return self._ctrl

    def create_tab(self):
        view = nodegraph_view.NodeGraphView(self)
        view.set_model(self._ctrl)
        view.endSelectionMoved.connect(self.on_selected_nodes_moved)  # ???

        # view.setMouseTracking(True)
        # Proper layout setup for tab
        widget = QtWidgets.QWidget()
        # widget.setMouseTracking(True)
        layout = QtWidgets.QVBoxLayout(widget)
        layout.addWidget(view)

        # tab_view.setCurrentWidget(self._view)
        self.ui.tabWidget.addTab(widget, 'Tab 1')

        self._ctrl.set_view(view)

        # Update internals
        self._current_view = view
        self._views.append(view)

        # Debugging
        i = self.ui.tabWidget.currentIndex()
        log.info('Current tab index is {}'.format(i))

    def on_selected_nodes_moved(self):
        for node in self._current_view.getSelectedNodes():
            if node._meta_data:
                new_pos = node.pos()  # for x reason, .getGraphPos don't work here
                new_pos = (new_pos.x(), new_pos.y())
                libPyflowgraph.save_node_position(node, new_pos)

    def on_add(self):
        raise NotImplementedError

    def on_del(self):
        graph = self.ui.widget_view
        graph.deleteSelectedNodes()

    def on_expand(self):
        self._ctrl.expand_selected_nodes()

    def on_colapse(self):
        return self._ctrl.colapse_selected_nodes()

    def on_navigate_down(self):
        self._ctrl.navigate_down()

    def on_navigate_up(self):
        self._ctrl.navigate_up()

    def _get_active_node(self):
        return next(iter(self._current_view.getSelectedNodes()), None)

    def on_arrange_upstream(self):
        node = self._get_active_node()
        if not node:
            return
        libPyflowgraph.arrange_upstream(node)

    def on_arrange_downstream(self):
        node = self._get_active_node()
        if not node:
            return
        libPyflowgraph.arrange_downstream(node)

    def on_arrange_spring(self):
        pyflowgraph_nodes = self._current_view.getSelectedNodes()
        libPyflowgraph.spring_layout(pyflowgraph_nodes)
        self._current_view.frameAllNodes()

    def _get_selected_nodes_outsider_ports(self):
        selected_nodes_model = self._ctrl.get_selected_nodes()
        inn_attrs = set()
        out_attrs = set()
        for node_model in selected_nodes_model:
            for port_dst in node_model.get_connected_input_attributes():
                for connection_model in port_dst.get_input_connections():
                    src_port_model = connection_model.get_source()
                    src_node_model = src_port_model.get_parent()
                    if src_node_model not in selected_nodes_model:
                        inn_attrs.add(port_dst.get_metadata())
            for port_src in node_model.get_connected_output_attributes():
                for connection_model in port_src.get_output_connections():
                    dst_port_model = connection_model.get_destination()
                    dst_node_model = dst_port_model.get_parent()
                    if dst_node_model not in selected_nodes_model:
                        out_attrs.add(port_src.get_metadata())
        return inn_attrs, out_attrs

    def on_group(self):
        inn_attrs, out_attrs = self._get_selected_nodes_outsider_ports()
        inst = classComponent.Component.from_attributes(inn_attrs, out_attrs)
        self.manager.export_network(inst)

        # hack: do not redraw everything, remove only necessary items
        self._ctrl.clear()
        self._ctrl.add_node(inst)

        return inst

    def on_ungroup(self):
        raise NotImplementedError

    def on_breadcrumb_changed(self, model):
        """Called when the current level is changed using the breadcrumb widget."""
        self._ctrl.set_level(model)
        self.ui.widget_breadcrumb.set_path(model)

# from pyflowgraph.graph_view import GraphView as NodeGraphWidget
