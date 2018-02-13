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

from omtk import decorators
import pymel.core as pymel
from omtk.core import session
from omtk.libs import libPyflowgraph
from omtk.libs import libPython
from omtk.qt_widgets.widget_nodegraph.ui import nodegraph_widget
from omtk.vendor.Qt import QtWidgets

from . import nodegraph_view

log = logging.getLogger('omtk.nodegraph')


@decorators.memoized
def _get_singleton_model():
    from .nodegraph_model import NodeGraphModel

    return NodeGraphModel()


class NodeGraphWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        from .nodegraph_controller import NodeGraphController
        from omtk.qt_widgets.widget_nodegraph.nodegraph_filter import NodeGraphControllerFilter

        # Hack: We are NOT providing any parent
        # Otherwise we won't see the QMainWindow if embeded in another QMainWindow
        # Here's a reproduction example, tested in Maya-2017:
        # win = QtWidgets.QMainWindow()
        # win_embeded = QtWidgets.QMainWindow()  # this don't work if win is provided as a parent
        # btn = QtWidgets.QPushButton(win_embeded)
        # win_embeded.setCentralWidget(btn)
        # win.setCentralWidget(win_embeded)
        # win.show()
        super(NodeGraphWidget, self).__init__()

        self.ui = nodegraph_widget.Ui_MainWindow()
        self.ui.setupUi(self)

        # Configure NodeGraphView
        # self._manager = None
        self._model = _get_singleton_model()
        self._ctrl = NodeGraphController(self._model)
        self._filter = NodeGraphControllerFilter(self._ctrl)  # todo: set filter in constructor?
        self._ctrl.set_filter(self._filter)
        self._ctrl.onLevelChanged.connect(self.on_level_changed)

        # Keep track of the multiple views provided by the QTabWidget
        self._current_view = None
        self._views = []

        # Connect events
        self.ui.actionAdd.triggered.connect(self.on_add)
        self.ui.actionRemove.triggered.connect(self.on_del)
        self.ui.actionClear.triggered.connect(self.on_clear)
        self.ui.actionExpand.triggered.connect(self.on_expand)
        self.ui.actionExpandMore.triggered.connect(self.on_expand_more)
        self.ui.actionExpandMoreMore.triggered.connect(self.on_expand_more_more)
        self.ui.actionCollapse.triggered.connect(self.on_colapse)
        self.ui.actionGoDown.triggered.connect(self.on_navigate_down)
        self.ui.actionGoUp.triggered.connect(self.on_navigate_up)
        self.ui.actionGroup.triggered.connect(self.on_group)
        self.ui.actionUngroup.triggered.connect(self.on_ungroup)
        self.ui.actionFrameAll.triggered.connect(self.on_frame_all)
        self.ui.actionFrameSelected.triggered.connect(self.on_frame_selected)

        self.ui.actionLayoutUpstream.triggered.connect(self.on_arrange_upstream)
        self.ui.actionLayoutDownstream.triggered.connect(self.on_arrange_downstream)
        self.ui.actionLayoutSpring.triggered.connect(self.on_arrange_spring)
        self.ui.actionMatchMayaEditorPositions.triggered.connect(self._ctrl.on_match_maya_editor_positions)
        self.ui.actionLayoutRecenter.triggered.connect(self.on_arrange_recenter)

        # self.ui.pushButton_arrange_upstream.pressed.connect(self.on_arrange_upstream)
        # self.ui.pushButton_arrange_downstream.pressed.connect(self.on_arrange_downstream)
        # self.ui.pushButton_arrange_spring.pressed.connect(self.on_arrange_spring)

        self.ui.widget_toolbar.onNodeCreated.connect(self.on_add)

        # Connect events (breadcrumb)
        # self.ui.widget_breadcrumb.path_changed.connect(self.on_breadcrumb_changed)

        # At least create one tab
        self.create_tab()

        # Load root level
        self._ctrl.set_level(None)

        # Pre-fill the node editor
        self.on_add()
        self.on_arrange_spring()

    @property
    def manager(self):
        return session.get_session()

    def get_controller(self):
        return self._ctrl

    def get_view(self):
        return self._ctrl._view

    def create_tab(self):
        from .. import widget_breadcrumb
        breakcrumb = widget_breadcrumb.WidgetBreadcrumb()
        breakcrumb.path_changed.connect(self.on_breadcrumb_changed)

        controller = self.get_controller()

        view = nodegraph_view.NodeGraphView(self)
        view.set_model(self._ctrl)
        view.endSelectionMoved.connect(self.on_selected_nodes_moved)  # ???
        view.nodeDoubleClicked.connect(controller.on_node_double_click)

        # view.setMouseTracking(True)
        # Proper layout setup for tab
        widget = QtWidgets.QWidget()
        # widget.setMouseTracking(True)
        layout = QtWidgets.QVBoxLayout(widget)
        layout.addWidget(breakcrumb)
        layout.addWidget(view)

        # tab_view.setCurrentWidget(self._view)
        self.ui.tabWidget.addTab(widget, 'Tab 1')
        self.ui.tabWidget.addTab(QtWidgets.QWidget(), '+')

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
        for obj in pymel.selected():
            self._ctrl.add_node(obj)

    def on_del(self):
        graph = self.ui.widget_view
        graph.deleteSelectedNodes()

    def on_clear(self):
        self._ctrl.clear()

    def on_expand(self):
        self._ctrl.expand_selected_nodes()

    def on_expand_more(self):
        self.on_expand()
        self.on_expand()

    def on_expand_more_more(self):
        self.on_expand()
        self.on_expand()
        self.on_expand()

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

    def on_group(self):
        self._ctrl.on_rcmenu_group_selection()

    def on_ungroup(self):
        self._ctrl.on_rcmenu_ungroup_selection()

    def on_arrange_recenter(self):
        pyflowgraph_nodes = self._current_view.getSelectedNodes()
        libPyflowgraph.recenter_nodes(pyflowgraph_nodes)
        self._current_view.frameSelectedNodes()

    def on_frame_all(self):
        self._current_view.frameAllNodes()

    def on_frame_selected(self):
        self._current_view.frameSelectedNodes()

    def on_breadcrumb_changed(self, model):
        """Called when the current level is changed using the breadcrumb widget."""
        self._ctrl.set_level(model)
        self.ui.widget_breadcrumb.set_path(model)

    def on_level_changed(self, model):
        """Called when the current level is changed using the nodegraph."""
        self.ui.widget_breadcrumb.set_path(model)

# from pyflowgraph.graph_view import GraphView as NodeGraphWidget
