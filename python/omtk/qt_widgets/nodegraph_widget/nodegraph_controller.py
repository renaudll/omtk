"""
Define a controller for one specific GraphView.
"""
import logging

import omtk.qt_widgets.nodegraph_widget.nodegraph_node_model_component
import pymel.core as pymel
from omtk.core import classComponent
from omtk.libs import libComponents
from omtk.libs import libPyflowgraph
from omtk.libs import libPython
from omtk.vendor import libSerialization
from omtk.vendor.Qt import QtCore

from . import nodegraph_node_model_base

# Used for type checking
if False:
    from .nodegraph_port_model import NodeGraphPortModel
    from .nodegraph_view import NodeGraphView
    from .nodegraph_node_model_base import NodeGraphNodeModel
    from omtk.vendor.pyflowgraph.node import Node as PyFlowgraphNode
    from omtk.vendor.pyflowgraph.port import BasePort as PyFlowgraphBasePort

log = logging.getLogger('omtk')


class NodeGraphController(QtCore.QObject):  # needed for signal handling
    onLevelChanged = QtCore.Signal(object)

    def __init__(self, model):
        super(NodeGraphController, self).__init__()  # needed for signal handling
        # type: (NodeGraphModel, NodeGraphView) -> ()
        self._model = model
        self._view = None
        self._current_level = None

        # Hold a reference to the inn and out node when inside a compound.
        self._widget_bound_inn = None
        self._widget_bound_out = None

        # self.set_view(view)

        # Cache to prevent creating already defined nodes
        self._known_nodes = set()
        self._known_attrs = set()
        self._known_connections = set()

        self._known_nodes_widgets = set()

        # Cache to access model-widget relationship
        self._cache_port_widget_by_model = {}
        self._cache_port_model_by_widget = {}

    def get_nodes(self):
        # type: () -> (List[NodeGraphNodeModel])
        return self._known_nodes

    def get_ports(self):
        # type: () -> (List[NodeGraphPortModel])
        return self._known_attrs

    def set_view(self, view):
        # type: (NodeGraphView) -> None

        # Disconnect previous events
        if self._view:
            self._view.connectionAdded.disconnect(self.on_connection_added)

        self._view = view

        # Connect events
        view.connectionAdded.connect(self.on_connection_added)

        view.scene().sceneRectChanged.connect(self.on_scene_rect_changed)

        # NodeGraphView events:
        # nodeAdded = QtCore.Signal(Node)
        # nodeRemoved = QtCore.Signal(Node)
        # nodeNameChanged = QtCore.Signal(str, str)
        # beginDeleteSelection = QtCore.Signal()
        # endDeleteSelection = QtCore.Signal()
        # beginConnectionManipulation = QtCore.Signal()
        # endConnectionManipulation = QtCore.Signal()
        # connectionAdded = QtCore.Signal(Connection)
        # connectionRemoved = QtCore.Signal(Connection)
        # beginNodeSelection = QtCore.Signal()
        # endNodeSelection = QtCore.Signal()
        # selectionChanged = QtCore.Signal(list, list)
        # # During the movement of the nodes, this signal is emitted with the incremental delta.
        # selectionMoved = QtCore.Signal(set, QtCore.QPointF)
        # # After moving the nodes interactively, this signal is emitted with the final delta.
        # endSelectionMoved = QtCore.Signal(set, QtCore.QPointF)

    # --- Events ---

    def _get_port_models_from_connection(self, connection):
        port_src_widget = connection.getSrcPort()
        port_dst_widget = connection.getDstPort()
        port_src_model = self._cache_port_model_by_widget[port_src_widget]
        port_dst_model = self._cache_port_model_by_widget[port_dst_widget]
        return port_src_model, port_dst_model

    def on_connection_added(self, connection):
        port_src_model, port_dst_model = self._get_port_models_from_connection(connection)
        port_dst_model.connect_from(port_src_model.get_metadata())

    def on_connected_removed(self, connection):
        port_src_model, port_dst_model = self._get_port_models_from_connection(connection)
        port_dst_model.disconnect_from(port_src_model.get_metadata())
        # todo: find related port models

    def on_scene_rect_changed(self, rect):
        # Resize inn bound
        if self._widget_bound_inn:
            self._widget_bound_inn.setMinimumWidth(60)
            self._widget_bound_inn.setMinimumHeight(rect.height())
            self._widget_bound_inn.setGraphPos(QtCore.QPointF(rect.topLeft()))

    # --- Model factory ---

    @libPython.memoized_instancemethod
    def get_node_model_from_value(self, val):
        log.debug('Requesting model from {0}'.format(val))
        # If we encounter a compount and are not inside it, we'll want to return a different model than
        # act like the two hub networks merged together.
        # todo: handle libSerialization lazy feature?
        if isinstance(val, classComponent.Component):
            return omtk.qt_widgets.nodegraph_widget.nodegraph_node_model_component.NodeGraphComponentModel(self._model, val)

        elif isinstance(val, pymel.nodetypes.Network):
            if libSerialization.is_network_from_class(val, classComponent.Component.__name__):
                network = val
            else:
                network = libComponents.get_component_metanetwork_from_hub_network(val)

            if network:
                component = libSerialization.import_network(network)
                return omtk.qt_widgets.nodegraph_widget.nodegraph_node_model_component.NodeGraphComponentModel(self._model, component)

            return nodegraph_node_model_base.NodeGraphDagNodeModel(self._model, val)

        return self._model.get_node_from_value(val)

    # @libPython.memoized_instancemethod
    def get_port_model_from_value(self, val):
        return self._model.get_port_model_from_value(val)

    # @libPython.memoized_instancemethod
    def get_connection_model_from_value(self, val):
        return self._model.get_connection_model_from_values

    # --- Widget factory ---

    @libPython.memoized_instancemethod
    def get_node_widget(self, model):
        # type: (NodeGraphNodeModel) -> PyFlowgraphNode
        # todo: how to we prevent from calling .get_widget() from the model directly? do we remove it?
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param node: A NodeGraphNodeModel instance.
        :return: A PyFlowgraph Node instance.
        """
        node_widget = model.get_widget(self._view)
        node_widget._omtk_model = model  # monkey-patch
        self._view.addNode(node_widget)

        self._known_nodes_widgets.add(node_widget)

        return node_widget

    @libPython.memoized_instancemethod
    def get_port_widget(self, port_model):
        # type: (NodeGraphPortModel) -> PyFlowgraphBasePort
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param port: A NodeGraphPortModel instance.
        :return: A PyFlowgraph Port instance.
        """
        log.info('Creating widget for {0}'.format(port_model))

        # In Pyflowgraph, a Port need a Node.
        # Verify that we initialize the widget for the Node.
        node_model = port_model.get_parent()
        node_widget = self.get_node_widget(node_model)
        port_widget = port_model.get_widget(self, self._view, node_widget)
        node_widget.addPort(port_widget)

        # Update cache
        self._cache_port_model_by_widget[port_widget] = port_model
        self._cache_port_widget_by_model[port_model] = port_widget

        return port_widget

    @libPython.memoized_instancemethod
    def get_connection_widget(self, connection_model):
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param connection_model: A NodeGraphConnectionModel instance.
        :return: A PyFlowgraph Connection instance.
        """
        log.info('Creating widget for {0}'.format(connection_model))

        # In Pyflowgraph, a Connection need two Port instances.
        # Ensure that we initialize the widget for the Ports.
        port_src_model = connection_model.get_source()
        port_dst_model = connection_model.get_destination()

        # Ensure ports are initialized
        self.get_port_widget(port_src_model)
        self.get_port_widget(port_dst_model)

        widget_src_node = self.get_node_widget(port_src_model.get_parent())
        widget_dst_node = self.get_node_widget(port_dst_model.get_parent())

        try:
            return self._view.connectPorts(
                widget_src_node,
                port_src_model.get_name(),
                widget_dst_node,
                port_dst_model.get_name()
            )
        except Exception, e:
            log.warning("Error connecting {0} to {1}".format(
                '{0}.{1}'.format(widget_src_node.getName(), port_src_model.get_name()),
                '{0}.{1}'.format(widget_dst_node.getName(), port_dst_model.get_name())
            ))

    def expand_node_attributes(self, node_model):
        # type: (NodeGraphNodeModel) -> None
        """
        Show all available attributes for a PyFlowgraph Node.
        Add it in the pool if it didn't previously exist.
        :return:
        """
        log.info('Creating widget for {0}'.format(node_model))

        # In PyFlowgraph, ports are accessible by name.
        if self._view:
            node_widget = self.get_node_widget(node_model)

            for port_model in sorted(node_model.get_attributes()):
                if not port_model.is_interesting():
                    continue
                port = node_widget.getPort(port_model.get_name())
                if not port:
                    port_widget = self.get_port_widget(port_model)

    def expand_node_connections(self, node_model, expand_downstream=True, expand_upstream=True):
        # type: (NodeGraphNodeModel) -> None
        for port_model in node_model.get_attributes():

            if expand_upstream and port_model.is_source():
                for connection_model in port_model.get_output_connections():
                    port_model_dst = connection_model.get_destination()
                    node_model_dst = port_model_dst.get_parent()
                    if node_model_dst.get_parent() != self._current_level:
                        continue
                    self.get_connection_widget(connection_model)

            if expand_downstream and port_model.is_destination():
                for connection_model in port_model.get_input_connections():
                    port_model_src = connection_model.get_source()
                    node_model_src = port_model_src.get_parent()
                    if node_model_src.get_parent() != self._current_level:
                        continue
                    self.get_connection_widget(connection_model)

            # if port_model.is_connected():
            #     for connection_model in port_model.get_connections():
            #         self.get_connection_widget(connection_model)

    def collapse_node_attributes(self, node_model):
        # There's no API method to remove a port in PyFlowgraph.
        # For now, we'll just re-created the node.
        # node_widget = self.get_node_widget(node_model)
        # self._view.removeNode(node_widget)
        # self.get_node_widget.cache[node_model]  # clear cache
        # node_widget = self.get_node_widget(node_model)
        # self._view.addNode(node_widget)
        raise NotImplementedError

    # def expand_attribute_connections(self, model_attr):
    #     # type: (NodeGraphPortModel) -> None
    #     """
    #     Show all connections for a specific PyFlowgraph Port.
    #     Add the destination Port and Node in the View if it didn't previously exist.
    #     :param model_attr:
    #     :return:
    #     """
    #     # todo: is this really the place for is_writable, should this be in .get_input_connections()?
    #     if model_attr.is_writable():
    #         for connection_model in model_attr.get_input_connections():
    #             self.get_connection_widget(connection_model)
    #     if model_attr.is_readable():
    #         for connection_model in model_attr.get_output_connections():
    #             self.get_connection_widget(connection_model)

    def add_node(self, node_model):
        if not isinstance(node_model, nodegraph_node_model_base.NodeGraphNodeModel):
            node_model = self.get_node_model_from_value(node_model)
        self._known_nodes.add(node_model)

        if self._view:
            node_widget = self.get_node_widget(node_model)
            # self._known_nodes_widgets(node_widget)
        self.expand_node_attributes(node_model)

        return node_model

    def redraw(self):
        """
        Draw the current graph on the view.
        :return:
        """

        # Draw nodes
        nodes = {node for node in self.get_nodes() if node.get_parent() == self._current_level}
        for node in nodes:
            widget = node.get_widget()
            self._view.addNode(widget)

    def get_selected_nodes(self):
        # type: () -> List[NodeGraphNodeModel]
        # Retrieve monkey-patched model in PyFlowgraph widgets.
        return [pfg_node._omtk_model for pfg_node in self._view.getSelectedNodes()]

    def expand_selected_nodes(self):
        for node_model in self.get_selected_nodes():
            self.expand_node_connections(node_model)

    def colapse_selected_nodes(self):
        for node_model in self.get_selected_nodes():
            self.collapse_node_attributes(node_model)

    def clear(self):
        for node_widget in self._known_nodes_widgets:
            self._view.removeNode(node_widget)
        self._known_nodes_widgets.clear()

    def set_level(self, node_model):
        # todo: handle top level
        self._current_level = node_model
        self.clear()
        for child_model in node_model.get_children():
            child_model._node = node_model  # hack: parent is not correctly set at the moment
            self.get_node_widget(child_model)
            self.expand_node_attributes(child_model)
            self.expand_node_connections(child_model)

        component = node_model.get_metadata()
        grp_inn = component.grp_inn
        grp_out = component.grp_out
        node_model = self.get_node_model_from_value(grp_inn)
        node_widget = self.get_node_widget(node_model)

        self._widget_bound_inn = node_widget


        # tmp
        node_model = self.get_node_model_from_value(grp_out)
        node_widget = self.get_node_widget(node_model)

        self._widget_bound_out = node_widget

        libPyflowgraph.arrange_downstream(node_widget)

        self.onLevelChanged.emit(node_model)

    def navigate_down(self):
        node_model = next(iter(self.get_selected_nodes()), None)
        if not node_model:
            return None

        # We need at least one children to be able to jump into something.
        # todo: is that always true? what happen to empty compound?
        if not node_model.get_children():
            log.debug("Cannot enter into {0} because there's no children!".format(node_model))
            return

        # We only can go down Compounds
        # if not isinstance(node_model, nodegraph_node_model.NodeGraphComponentModel):
        #     return

        # Hack: We also want to prevent entering the same compound twice.
        # Currently since we can have 3 node model for a single compound (one model when seen from outside and two
        # model when seen from the inside, the inn and the out), we need a better way to distinguish them.
        # For now we'll use a monkey-patched data from libSerialization, however we need a better approach.
        if self._current_level and node_model and node_model.get_metadata()._network == self._current_level.get_metadata()._network:
            return

        self.set_level(node_model)

    def navigate_up(self):
        if self._current_level is None:
            return
        self.set_level(self._current_level.get_parent())
