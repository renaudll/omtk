import logging

import pymel.core as pymel
from omtk.core import session
from omtk.libs import libPyflowgraph
from omtk.qt_widgets.nodegraph.nodegraph_registry import _get_singleton_model
from omtk.qt_widgets.nodegraph.ui import nodegraph_tab_widget
from omtk.qt_widgets.nodegraph.models.graph import graph_model
from omtk.qt_widgets.nodegraph.models.graph import graph_proxy_filter_model, graph_component_proxy_model
from omtk.qt_widgets.nodegraph.filters import filter_standard
from omtk.vendor.Qt import QtWidgets, QtCore, QtGui


log = logging.getLogger('omtk.nodegraph')

if False:  # for type hinting
    from .nodegraph_controller import NodeGraphController


class NodeGraphTabWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        from .nodegraph_controller import NodeGraphController

        super(NodeGraphTabWidget, self).__init__(parent)

        self.ui = nodegraph_tab_widget.Ui_Form()
        self.ui.setupUi(self)

        # Configure NodeGraphView
        self._registry = _get_singleton_model()

        self._source_model = graph_model.NodeGraphModel()

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

        view = self.ui.widget_nodegraph
        self._view = view
        self._ctrl.set_view(view)

        # Pre-fill the node editor
        self.on_add()
        self.on_arrange_spring()

    @property
    def manager(self):
        return session.get_session()

    def get_controller(self):
        # type: () -> NodeGraphController
        return self._ctrl

    def set_controller(self, ctrl):
        # type: (NodeGraphController) -> ()
        self._ctrl = ctrl

    def get_view(self):
        return self._ctrl._view

    def on_selected_nodes_moved(self):
        for node in self._current_view.getSelectedNodes():
            if node._meta_data:
                new_pos = node.pos()  # for x reason, .getGraphPos don't work here
                new_pos = (new_pos.x(), new_pos.y())
                libPyflowgraph.save_node_position(node, new_pos)

    # todo: move all of this in the controller?

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
        self._ctrl.arrange_spring()

    def on_group(self):
        self._ctrl.group_selected_nodes()

    def on_ungroup(self):
        self._ctrl.ungroup_selected_nodes()

    def on_arrange_recenter(self):
        pyflowgraph_nodes = self._current_view.getSelectedNodes()
        libPyflowgraph.recenter_nodes(pyflowgraph_nodes)
        self._current_view.frameSelectedNodes()

    def on_frame_all(self):
        self._current_view.frameAllNodes()

    def on_frame_selected(self):
        self._current_view.frameSelectedNodes()

    def on_level_changed(self, model):
        """Called when the current level is changed using the nodegraph_tests."""
        self.ui.widget_breadcrumb.set_path(model)

    def keyPressEvent(self, event):
        # Prevent Maya from catching key events
        pass
