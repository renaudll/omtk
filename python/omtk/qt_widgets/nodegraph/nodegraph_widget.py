import logging

import pymel.core as pymel
from omtk.core import session
from omtk.libs import libPyflowgraph
from omtk.qt_widgets.nodegraph.nodegraph_registry import _get_singleton_model
from omtk.qt_widgets.nodegraph.ui import nodegraph_widget
from omtk.qt_widgets.nodegraph.models import NodeGraphModel
from omtk.qt_widgets.nodegraph.models.graph import graph_proxy_filter_model, graph_component_proxy_model
from omtk.qt_widgets.nodegraph.filters import filter_standard
from omtk.vendor.Qt import QtWidgets, QtCore, QtGui

from . import nodegraph_view

log = logging.getLogger('omtk.nodegraph')

if False:  # for type hinting
    from .nodegraph_controller import NodeGraphController


class NodeGraphWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        from .nodegraph_controller import NodeGraphController

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
        self._registry = _get_singleton_model()

        self._source_model = NodeGraphModel()

        # Create filter
        self._filter = filter_standard.NodeGraphStandardFilter()

        # Add a proxy-model to apply user display preferences
        self._model = graph_proxy_filter_model.GraphFilterProxyModel()
        self._model.set_source_model(self._source_model)
        self._model.set_filter(self._filter)

        # Add a proxy-model to allow encapsulation
        self._proxy_model_subgraph = graph_component_proxy_model.GraphComponentProxyFilterModel()
        self._proxy_model_subgraph.set_source_model(self._model)

        # Create ctrl
        self._ctrl = NodeGraphController(model=self._proxy_model_subgraph)
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
        # self._proxy_model_subgraph_filter.set_level(None)

        # Pre-fill the node editor
        self.on_add()
        self.on_arrange_spring()

        self._create_shortcut(QtCore.Qt.Key_Tab, self.on_shortcut_tab)
        self._create_shortcut(QtCore.Qt.Key_F, self.on_shortcut_frame)
        self._create_shortcut(QtCore.Qt.Key_Delete, self.on_shortcut_delete)
        self._create_shortcut(QtCore.Qt.Key_Backspace, self.on_shortcut_delete)
        self._create_shortcut(QtCore.Qt.ControlModifier + QtCore.Qt.Key_G, self.on_shortcut_group)
        self._create_shortcut(QtCore.Qt.ControlModifier + QtCore.Qt.Key_D, self.on_shortcut_duplicate)
        self._create_shortcut(QtCore.Qt.ControlModifier + QtCore.Qt.Key_A, self.on_select_all)
        self._create_shortcut(QtCore.Qt.Key_P, self.on_parent_selected)
        self._create_shortcut(QtCore.Qt.Key_Plus, self.on_add)
        self._create_shortcut(QtCore.Qt.Key_Minus, self.on_del)

        # todo: move elsewhere?
        self._create_shortcut(QtCore.Qt.Key_T, self.ui.widget_toolbar.create_favorite_callback('transform'))

    def _create_shortcut(self, key, fn_):
        qt_key_sequence = QtGui.QKeySequence(key)
        qt_shortcut = QtWidgets.QShortcut(qt_key_sequence, self)
        qt_shortcut.activated.connect(fn_)

    def on_shortcut_frame(self):
        """
        Called when the user press ``f``. Frame selected nodes if there's a selection, otherwise frame everything.
        """
        view = self._current_view
        if view.getSelectedNodes():
            view.frameSelectedNodes()
        else:
            view.frameAllNodes()

    def on_shortcut_tab(self):
        from omtk.qt_widgets.outliner import widget_component_list
        dialog = widget_component_list.WidgetComponentList(self._current_view)
        dialog.signalComponentCreated.connect(self._current_view.on_component_created)  # todo: move method?
        # dialog.setMinimumHeight(self.height())
        dialog.show()
        dialog.ui.lineEdit_search.setFocus(QtCore.Qt.PopupFocusReason)

    def on_shortcut_delete(self):
        self.get_controller().delete_selected_nodes()

    def on_shortcut_group(self):
        self.get_controller().on_rcmenu_group_selection()

    def on_shortcut_duplicate(self):
        self.get_controller().duplicate_selected_nodes()

    def on_select_all(self):
        self.get_controller().select_all_nodes()

    def on_parent_selected(self):
        self.get_controller().on_parent_selected()

    @property
    def manager(self):
        return session.get_session()

    def get_controller(self):
        # type: () -> NodeGraphController
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
            node = self._registry.get_node_from_value(obj)
            self._ctrl.add_node(node)

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
        """Called when the current level is changed using the nodegraph_tests."""
        self.ui.widget_breadcrumb.set_path(model)

    def keyPressEvent(self, event):
        # Prevent Maya from catching key events
        pass
