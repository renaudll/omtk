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
        self.ui.actionMatchMayaEditorPositions.triggered.connect(self.on_match_maya_editor_positions)
        self.ui.actionLayoutRecenter.triggered.connect(self.on_arrange_recenter)

        self.ui.widget_toolbar.onNodeCreated.connect(self.on_add)

        # At least create one tab
        self.create_tab()

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
        self.get_controller().group_selected_nodes()

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

    def set_controller(self, ctrl):
        self._ctrl = ctrl

    def create_tab(self):
        from . import nodegraph_tab_widget
        widget = nodegraph_tab_widget.NodeGraphTabWidget(self)

        # tab_view.setCurrentWidget(self._view)
        self.ui.tabWidget.addTab(widget, 'Tab 1')
        self.ui.tabWidget.addTab(QtWidgets.QWidget(), '+')

        from omtk.qt_widgets.nodegraph import nodegraph_controller
        ctrl = nodegraph_controller.NodeGraphController()
        widget.set_ctrl(ctrl)

        self.set_controller(widget.get_controller())

        # Debugging
        i = self.ui.tabWidget.currentIndex()
        log.info('Current tab index is {}'.format(i))

    def on_selected_nodes_moved(self):
        for node in self._current_view.getSelectedNodes():
            if node._meta_data:
                new_pos = node.pos()  # for x reason, .getGraphPos don't work here
                new_pos = (new_pos.x(), new_pos.y())
                libPyflowgraph.save_node_position(node, new_pos)

    # Connect shortcut buttons to the active controller.

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
        self.get_controller().navigate_down()

    def on_navigate_up(self):
        self.get_controller().navigate_up()

    def on_arrange_upstream(self):
        self.get_controller().arrange_upstream()

    def on_arrange_downstream(self):
        self.get_controller().arrange_downstream()

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

