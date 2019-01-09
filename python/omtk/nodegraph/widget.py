import logging
import functools

from omtk.core import manager
from omtk.nodegraph.ui import nodegraph_widget
from omtk.nodegraph.models.graph import graph_proxy_filter_model, graph_component_proxy_model
from omtk.nodegraph.filters import filter_standard
from omtk.nodegraph.registry import base
from omtk.vendor.Qt import QtWidgets, QtCore, QtGui

log = logging.getLogger('omtk.nodegraph')


class NodeGraphWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):

        # HACK: This QMainWindow will have no parent
        # Otherwise we won't see the QMainWindow if embedded in another QMainWindow
        # Here's a reproduction example, tested in Maya-2017:
        #
        #     win = QtWidgets.QMainWindow()
        #     win_embeded = QtWidgets.QMainWindow()  # this don't work if win is provided as a parent
        #     btn = QtWidgets.QPushButton(win_embeded)
        #     win_embeded.setCentralWidget(btn)
        #     win.setCentralWidget(win_embeded)
        #     win.show()
        super(NodeGraphWidget, self).__init__()

        self.ui = nodegraph_widget.Ui_MainWindow()
        self.ui.setupUi(self)

        # The REGISTRY_DEFAULT keep track of what is in Maya and listen to events.
        # It need to be shared with each controllers (tabs) of the ui.
        # It also need to be destroyed correctly.
        # For this reason we'll initialize it in the NodeGraphWidget itself.
        # Any tips for a better design is appreciated.
        self._registry = base.NodeGraphRegistry()

        # Keep track of the multiple views provided by the QTabWidget
        self._ctrl = None
        self._view = None
        self._ctrls = []
        self._views = []

        self._subgraph_proxy_model = None

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
        self.ui.actionMatchMayaEditorPositions.triggered.connect(self.on_arrange_maya)
        self.ui.actionLayoutSpring.triggered.connect(self.on_arrange_spring)
        self.ui.actionMatchMayaEditorPositions.triggered.connect(self.on_match_maya_editor_positions)
        self.ui.actionLayoutRecenter.triggered.connect(self.on_arrange_recenter)

        self.ui.widget_toolbar.onNodeCreated.connect(self.on_add)
        self.ui.tabWidget.currentChanged.connect(self.on_tab_change)

        # At least create one tab
        self.ui.tabWidget.blockSignals(True)
        self.create_tab()
        self.create_tab_new()
        self.ui.tabWidget.blockSignals(False)

        # Hack: Select the first tab
        self.ui.tabWidget.setCurrentIndex(0)
        self.set_view(self._views[0])
        self.set_controller(self._ctrls[0])

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

        self.destroyed.connect(functools.partial(NodeGraphWidget.on_destroyed, self._registry))

    # Note: The method is static, otherwise it make Maya crash.
    # see: https://stackoverflow.com/questions/16842955/widgets-destroyed-signal-is-not-fired-pyqt
    @staticmethod
    def on_destroyed(registry):
        print("NodeGraphWidget was destroyed")
        session = registry.session
        if session:
            session.remove_callbacks()

    def keyPressEvent(self, event):
        """
        This method is declared to prevent Maya from catching key events
        """
        pass

    # --- Shortcuts ---

    def _create_shortcut(self, key, fn_):
        qt_key_sequence = QtGui.QKeySequence(key)
        qt_shortcut = QtWidgets.QShortcut(qt_key_sequence, self)
        qt_shortcut.activated.connect(fn_)

    def on_shortcut_frame(self):
        """
        Called when the user press ``f``. Frame selected nodes if there's a selection, otherwise frame everything.
        """
        view = self.get_view()
        if view.getSelectedNodes():
            view.frameSelectedNodes()
        else:
            view.frameAllNodes()

    def on_shortcut_tab(self):
        ctrl = self.get_controller()
        from omtk.outliner import widget_component_list
        dialog = widget_component_list.WidgetComponentList(self._view)
        dialog.signalComponentCreated.connect(ctrl.on_component_created)  # todo: move method?
        # dialog.setMinimumHeight(self.height())
        dialog.show()
        dialog.ui.lineEdit_search.setFocus(QtCore.Qt.PopupFocusReason)

    def on_shortcut_delete(self):
        self.get_controller().delete_selected_nodes()

    def on_shortcut_group(self):
        self.get_controller().group_selected_nodes()

    def on_shortcut_duplicate(self):
        self.get_controller().duplicate_selected_nodes()

    def on_select_all(self):
        self.get_controller().select_all_nodes()

    def on_parent_selected(self):
        self.get_controller().on_parent_selected()

    @property
    def manager(self):
        return manager.get_session()

    def get_controller(self):
        # type: () -> NodeGraphController
        return self._ctrl

    def get_view(self):
        return self._view

    def set_controller(self, ctrl):
        self._ctrl = ctrl

    def add_controller(self, ctrl):
        self.set_controller(ctrl)
        self._ctrls.append(ctrl)

    def set_view(self, view):
        self._view = view

    def add_view(self, view):
        self.set_view(view)
        self._views.append(view)

    def create_tab(self):
        from omtk.nodegraph import view
        from omtk.nodegraph import controller
        from omtk.nodegraph.models.graph import graph_model

        tabWidget = self.ui.tabWidget
        registry = self._registry
        source_model = graph_model.GraphModel(registry)
        filter = filter_standard.NodeGraphStandardFilter()
        model = graph_proxy_filter_model.GraphFilterProxyModel()
        model.set_source_model(source_model)
        model.set_filter(filter)
        self._subgraph_proxy_model = graph_component_proxy_model.GraphComponentProxyFilterModel()
        self._subgraph_proxy_model.set_source_model(model)
        view = view.NodeGraphView(self)
        ctrl = controller.NodeGraphController(
            registry=registry,
            model=self._subgraph_proxy_model,
            view=view
        )
        self.add_view(view)
        self.add_controller(ctrl)

        # from omtk.nodegraph import nodegraph_tab_widget
        # widget = nodegraph_tab_widget.NodeGraphTabWidget(tabWidget)

        # Proper layout setup for tab
        widget = QtWidgets.QWidget()
        widget._widget = view
        layout = QtWidgets.QVBoxLayout(widget)

        from omtk.qt_widgets import widget_breadcrumb
        breadcrumb = widget_breadcrumb.WidgetBreadcrumb(self)

        self._subgraph_proxy_model.onLevelChanged.connect(breadcrumb.set_path)

        def _debug(level):
            self._subgraph_proxy_model.set_level(level)
            # print args, kwargs

        breadcrumb.onPathChanged.connect(_debug)

        layout.addWidget(breadcrumb)
        layout.addWidget(view)

        num_tabs = len(self._views)

        tabWidget.addTab(widget, 'Tab {0}'.format(num_tabs))

        # Add a close button, is this how we want to do it?
        # view._tb = QtWidgets.QPushButton()
        # view._tb.setText("x")
        # tabWidget.tabBar().setTabButton(0, QtWidgets.QTabBar.RightSide, view._tb)

    def create_tab_new(self):
        widget = QtWidgets.QWidget()
        tabWidget = self.ui.tabWidget
        tabWidget.blockSignals(True)
        tabWidget.addTab(widget, '+')
        tabWidget.blockSignals(False)

    # Connect shortcut buttons to the active controller.

    def on_tab_change(self, index):
        if index == -1:
            return
        if index == len(self._views):  # '+' tab
            self.ui.tabWidget.blockSignals(True)
            self.ui.tabWidget.removeTab(index)
            self.ui.tabWidget.blockSignals(False)
            self.create_tab()
            self.create_tab_new()

        else:
            index = index
            view = self._views[index]
            ctrl = self._ctrls[index]
            self.set_controller(ctrl)
            self.set_view(view)

    def on_add(self):
        self.get_controller().add_maya_selection_to_view()

    def on_del(self):
        self.get_controller().remove_maya_selection_from_view()

    def on_clear(self):
        self.get_controller().clear()

    def on_expand(self):
        self.get_controller().expand_selected_nodes()

    def on_expand_more(self):
        self.on_expand()
        self.on_expand()

    def on_expand_more_more(self):
        self.on_expand()
        self.on_expand()
        self.on_expand()

    def on_colapse(self):
        self.get_controller().colapse_selected_nodes()

    def on_navigate_down(self):
        model = self._subgraph_proxy_model

        for node in self.get_controller().get_selected_node_models():
            if not model.can_set_level_to(node):
                continue

            model.set_level(node)
            return

    def on_navigate_up(self):
        # if self._current_level_data is None:
        #     return
        model = self._subgraph_proxy_model
        level = model.get_level()

        parent = level.get_parent()
        model.set_level(parent)

    def on_arrange_upstream(self):
        self.get_controller().arrange_upstream()

    def on_arrange_downstream(self):
        self.get_controller().arrange_downstream()

    def on_arrange_maya(self):
        self.get_controller().on_match_maya_editor_positions()

    def on_arrange_spring(self):
        self.get_controller().arrange_spring()

    def on_match_maya_editor_positions(self):
        self.get_controller().on_match_maya_editor_positions()

    def on_group(self):
        self.get_controller().group_selected_nodes()

    def on_ungroup(self):
        self.get_controller().ungroup_selected_nodes()

    def on_arrange_recenter(self):
        self.get_controller().arrange_recenter()

    def on_frame_all(self):
        self.get_controller().frame_all()

    def on_frame_selected(self):
        self.get_controller().frame_selected()

