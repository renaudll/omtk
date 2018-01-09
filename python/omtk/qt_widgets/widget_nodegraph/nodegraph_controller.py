"""
Define a controller for one specific GraphView.
"""
import itertools
import logging

import pymel.core as pymel
from omtk import constants
from omtk.core import component, session
from omtk.core import entity
from omtk.factories import factory_datatypes, factory_rc_menu
from omtk.libs import libComponents
from omtk.libs import libPython
from omtk.vendor.Qt import QtCore

from . import nodegraph_node_model_base
from . import nodegraph_node_model_component
from . import nodegraph_node_model_dagnode
from . import nodegraph_node_model_root
from . import nodegraph_port_model

# Used for type checking
if False:
    from .nodegraph_port_model import NodeGraphPortModel
    from .nodegraph_view import NodeGraphView
    from .nodegraph_node_model_base import NodeGraphNodeModel
    from omtk.vendor.pyflowgraph.node import Node as PyFlowgraphNode
    from omtk.vendor.pyflowgraph.port import BasePort as PyFlowgraphBasePort

log = logging.getLogger('omtk.nodegraph')


def block_signal(fn):
    def _fn_decorated(self, *args, **kwargs):
        old_val = self._view.signalsBlocked()
        self._view.blockSignals(True)
        rv = fn(self, *args, **kwargs)
        self._view.blockSignals(old_val)
        return rv

    return _fn_decorated


class NodeGraphController(QtCore.QObject):  # note: QtCore.QObject is necessary for signal handling
    onLevelChanged = QtCore.Signal(object)
    actionRequested = QtCore.Signal(list)

    # Define the default root model to use
    _cls_root_model = nodegraph_node_model_root.NodeGraphNodeRootModel

    def __init__(self, model):
        super(NodeGraphController, self).__init__()  # needed for signal handling
        # type: (NodeGraphModel, NodeGraphView) -> ()
        self._model = model
        self._view = None
        self._filter = None
        self._current_level_model = None
        self._current_level_data = None

        # Hold a reference to the inn and out node when inside a compound.
        self._widget_bound_inn = None
        self._widget_bound_out = None

        # self.set_view(view)

        # Cache to prevent creating already defined nodes
        self._known_nodes = set()
        self._known_attrs = set()
        self._known_connections = set()

        self._known_nodes_widgets = set()
        self._known_connections_widgets = set()

        # Cache to access model-widget relationship
        self._cache_port_widget_by_model = {}
        self._cache_port_model_by_widget = {}

        self._cache_nodes = {}

        self._old_scene_x = None
        self._old_scene_y = None

    @property
    def manager(self):
        return session.get_session()

    @libPython.memoized_instancemethod
    def get_root_model(self):
        return self._cls_root_model(self._model) if self._cls_root_model else None

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

        # view.scene().sceneRectChanged.connect(self.on_scene_rect_changed)

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

    def set_filter(self, filter):
        # type: (NodeGraphControllerFilter) -> None
        self._filter = filter

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
        scene_x = rect.x()
        scene_y = rect.y()
        if scene_x == self._old_scene_x and scene_y == self._old_scene_y:
            return
        self._old_scene_x = scene_x
        self._old_scene_y = scene_y

        # todo: this get called to many times, we might want to block signals
        log.debug('scene_rect_changed: {0}'.format(rect))
        # Resize inn bound
        if self._widget_bound_inn:
            self._widget_bound_inn.setMinimumWidth(60)
            self._widget_bound_inn.setMinimumHeight(rect.height())
            self._widget_bound_inn.setGraphPos(QtCore.QPointF(rect.topLeft()))

    # --- Cache clearing method ---

    # todo: deprecate in favor of invalidate_node_model?
    def invalidate_node_value(self, key):
        """Invalidate any cache referencing provided value."""
        self._model.invalidate_node(key)
        try:
            self._cache_nodes.pop(key)
        except LookupError:
            pass

        # For components, ensure that we also invalidate all their bounds.
        # if isinstance(key, classComponent.Component):
        #     self.invalidate_node(key.grp_inn)
        #     self.invalidate_node(key.grp_out)

    def invalidate_node_model(self, model):
        # type: (NodeGraphNodeModel) -> None
        """
        Since the goal of a NodeGraphNodeModel is to take control of what the NodeGraph display even if it is
        not related to the REAL networks in the Maya file, it can happen that we want to remove any cached value
        related to that model when the context change.

        For example, when going inside a Component, the NodeGraph will suddenly start to display the component
        grp_inn and grp_out. When going outside a Component, theses node won't be shown.
        :param model: A NodeGraphNodeModel instance to invalidate.
        """
        value = model.get_metadata()

        # Note that we never invalidate the stored model related to the component.
        # This is because we will always return this model when asked directly about it.
        # Also the NodeGraphRootModel store reference it's children so we want to prevent
        # as much as we can a new NodeGraphComponentModel instance from being created.
        if isinstance(value, component.Component):
            self.invalidate_node_value(value.grp_inn)
            self.invalidate_node_value(value.grp_out)
        else:
            self.invalidate_node_value(value)

    # --- Model factory ---

    def get_node_model_from_value(self, key):
        try:
            return self._cache_nodes[key]
        except LookupError:
            log.debug("Cannot find model for {0}. Creating a new one.".format(key))
            val = self._get_node_model_from_value(key)

            # If we got a component model, ensure that we also cache it's bounds.
            if isinstance(val, nodegraph_node_model_component.NodeGraphComponentModel):
                component = val.get_metadata()
                self._cache_nodes[component] = val
                self._cache_nodes[component.grp_inn] = val
                self._cache_nodes[component.grp_out] = val
            else:
                self._cache_nodes[key] = val

            return val

    def _get_node_model_from_value(self, val):
        """
        Return the visible model associated with a single value.
        Handle the special Component context.
        """
        # todo: cleanup
        log.debug('Requesting model from {0}'.format(val))

        # Handle Compount bound networks
        if isinstance(val, pymel.nodetypes.Network):
            net = libComponents.get_component_metanetwork_from_hub_network(val, strict=False)
            if net:
                component = self.manager.import_network(net)
                if self._current_level_data == component:
                    if net.getAttr(constants.COMPONENT_HUB_INN_ATTR_NAME) == val:
                        return nodegraph_node_model_component.NodeGraphComponentInnBoundModel(self._model, val,
                                                                                              component)
                    if net.getAttr(constants.COMPONENT_HUB_OUT_ATTR_NAME) == val:
                        return nodegraph_node_model_component.NodeGraphComponentOutBoundModel(self._model, val,
                                                                                              component)
                else:
                    return self._model.get_node_from_value(component)
            return nodegraph_node_model_dagnode.NodeGraphDagNodeModel(self._model, val)

        # model = self._model.get_node_from_value(val)
        # if isinstance(model, nodegraph_node_model_component.NodeGraphComponentBoundBaseModel):
        #     component = model.get_component()
        #     if component != self._current_level:
        #         return self._model.get_node_from_value(component)

        return self._model.get_node_from_value(val)

    # @libPython.memoized_instancemethod
    def get_port_model_from_value(self, val):
        return self._model.get_port_model_from_value(val)

    # @libPython.memoized_instancemethod
    def get_connection_model_from_value(self, val):
        return self._model.get_connection_model_from_values

    def expand_node_attributes(self, node_model):
        # type: (NodeGraphNodeModel) -> None
        """
        Show all available attributes for a PyFlowgraph Node.
        Add it in the pool if it didn't previously exist.
        :return:
        """
        log.debug('Creating widget for {0}'.format(node_model))

        # In PyFlowgraph, ports are accessible by name.
        if self._view:
            node_widget = self.get_node_widget(node_model)

            # todo: find a unified way of always having the ports sorted...
            for port_model in sorted(node_model.get_attributes(), key=lambda x: x.get_name()):
                if not port_model.is_interesting():
                    continue
                port = node_widget.getPort(port_model.get_name())
                if not port:
                    port_widget = self.get_port_widget(port_model)

    def expand_node_connections(self, node_model, expand_downstream=True, expand_upstream=True):
        # type: (NodeGraphNodeModel) -> None
        for port_model in node_model.get_attributes():

            def _can_show_connection(connection_model):
                # Get the node associated with the connection
                # Even if a connection is between two nodes, only one can have ownership.
                node_inst = connection_model.get_parent()
                # Get the model for that node
                node_model = self.get_node_model_from_value(node_inst)
                # Use the model to get the parent of the node.
                # This is either the None or a component.
                node_parent_inst = node_model.get_parent()
                # Note that we don't check self._current_level_model since it have a value (the root model).
                if node_parent_inst is None:
                    return self._current_level_data is None
                # node_parent_model = self.get_node_model_from_value(node_parent_inst) if node_parent_inst else None
                return node_parent_inst == self._current_level_data

            if expand_upstream and port_model.is_source():
                # for connection_model in port_model.get_output_connections():
                for connection_model in self.get_port_output_connections(port_model):
                    if not _can_show_connection(connection_model):
                        continue
                    port_model_dst = connection_model.get_destination()
                    node_dst = port_model_dst.get_parent()  # todo: remove ambiguity in .get_parent() return type
                    node_model_dst = self.get_node_model_from_value(node_dst)

                    # Apply filter
                    if self._filter:
                        if not self._filter.can_show_node(node_model_dst):
                            continue
                        if not self._filter.can_show_connection(connection_model):
                            continue

                    # if node_model_dst.get_parent() != self._current_level:
                    #     continue
                    self.get_connection_widget(connection_model)

            if expand_downstream and port_model.is_destination():
                for connection_model in self.get_port_input_connections(port_model):
                    if not _can_show_connection(connection_model):
                        continue
                    port_model_src = connection_model.get_source()
                    node_src = port_model_src.get_parent()  # todo: remove ambiguity in .get_parent() return type
                    node_model_src = self.get_node_model_from_value(node_src)

                    # Apply filter
                    if self._filter:
                        if not self._filter.can_show_node(node_model_src):
                            continue
                        if not self._filter.can_show_connection(connection_model):
                            continue

                    self.get_connection_widget(connection_model)

    def collapse_node_attributes(self, node_model):
        # There's no API method to remove a port in PyFlowgraph.
        # For now, we'll just re-created the node.
        # node_widget = self.get_node_widget(node_model)
        # self._view.removeNode(node_widget)
        # self.get_node_widget.cache[node_model]  # clear cache
        # node_widget = self.get_node_widget(node_model)
        # self._view.addNode(node_widget)
        raise NotImplementedError

    # @libPython.memoized_instancemethod
    # def get_node_parent(self, node_model):
    #     parent_model = node_model.get_parent()
    #
    #     #
    #     if isinstance(node_model, nodegraph_node_model_dagnode.NodeGraphDagNodeModel):
    #         parent_grp_inn, _ = libComponents.get_component_parent_network(self._pynode)
    #         if not parent_grp_inn:
    #             return None
    #         net = libComponents.get_component_metanetwork_from_hub_network(parent_grp_inn)
    #         if not net:
    #             return None
    #         inst = self._registry._manager.import_network(net)
    #         # inst = libSerialization.import_network(net)  # todo: use some kind of singleton/registry?
    #         if not inst:
    #             return None
    #         parent_model = self._registry.get_node_from_value(inst)
    #
    #     return parent_model

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
        # log.debug('Creating widget for {0}'.format(port_model))

        # In Pyflowgraph, a Port need a Node.
        # Verify that we initialize the widget for the Node.
        node_value = port_model.get_parent()
        node_model = self.get_node_model_from_value(node_value)

        # Hack: Hide Compound bound nodes when not inside the compound!
        # if isinstance(node_model, nodegraph_node_model_component.NodeGraphComponentBoundBaseModel):
        #     compound_model = self.get_node_model_from_value(node_model.get_parent())
        #     if self._current_level != compound_model:
        #         node_model = compound_model

        node_widget = self.get_node_widget(node_model)
        port_widget = port_model.get_widget(self, self._view, node_widget)

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
        # log.debug('Creating widget for {0}'.format(connection_model))

        # In Pyflowgraph, a Connection need two Port instances.
        # Ensure that we initialize the widget for the Ports.
        port_src_model = connection_model.get_source()
        port_dst_model = connection_model.get_destination()

        # Ensure ports are initialized
        # self.get_port_widget(port_src_model)
        widget_src_port = self.get_port_widget(port_src_model)
        widget_dst_port = self.get_port_widget(port_dst_model)

        widget_src_node = self.get_node_widget(self.get_node_model_from_value(port_src_model.get_parent()))
        widget_dst_node = self.get_node_widget(self.get_node_model_from_value(port_dst_model.get_parent()))

        # Hack:
        widget_dst_node_in_circle = widget_dst_port.inCircle()
        if not widget_dst_node_in_circle:
            raise Exception("Expected an inCircle widget for destination when connecting {0}.{1} to {2}.{3}".format(
                widget_src_node.getName(), widget_src_port.getName(),
                widget_dst_node.getName(), widget_dst_port.getName(),
            ))
        widget_dst_node_in_circle.setSupportsOnlySingleConnections(False)

        connection = None
        try:
            # log.debug("Connecting {0} to {1}".format(
            #     '{0}.{1}'.format(widget_src_node.getName(), port_src_model.get_name()),
            #     '{0}.{1}'.format(widget_dst_node.getName(), port_dst_model.get_name())
            # ))
            connection = self._view.connectPorts(
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

        if connection:
            self._known_connections_widgets.add(connection)

        return connection

    def add_node(self, node_model):
        if not isinstance(node_model, nodegraph_node_model_base.NodeGraphNodeModel):
            node_model = self.get_node_model_from_value(node_model)
        self._known_nodes.add(node_model)

        # Ensure the root model is remembering it's session
        if isinstance(self._current_level_model, self._cls_root_model):
            self._current_level_model.add_child(node_model)

        node_widget = None
        if self._view:
            node_widget = self.get_node_widget(node_model)
            # self._known_nodes_widgets(node_widget)
        self.expand_node_attributes(node_model)
        self.expand_node_connections(node_model)

        return node_model, node_widget

    def redraw(self):
        """
        Draw the current graph on the view.
        :return:
        """

        # Draw nodes
        nodes = {node for node in self.get_nodes() if node.get_parent() == self._current_level_data}
        for node in nodes:
            widget = node.get_widget()
            self._view.addNode(widget)

    def get_selected_node_models(self):
        # type: () -> List[NodeGraphNodeModel]
        # Retrieve monkey-patched model in PyFlowgraph widgets.
        return [pfg_node._omtk_model for pfg_node in self._view.getSelectedNodes()]

    def get_selected_values(self):
        return [model.get_metadata() for model in self.get_selected_node_models()]

    def expand_selected_nodes(self):
        for node_model in self.get_selected_node_models():
            self.expand_node_connections(node_model)

    def colapse_selected_nodes(self):
        for node_model in self.get_selected_node_models():
            self.collapse_node_attributes(node_model)

    def clear(self):
        # for connection_widget in self._known_connections_widgets:
        #     self._view.removeConnection(connection_widget)
        # for node_widget in self._known_nodes_widgets:
        #     self._view.removeNode(node_widget)
        self._view.reset()
        self._known_nodes_widgets.clear()

        try:
            self._cache.pop('get_node_widget', None)
        except KeyError:
            pass
        try:
            self._cache.pop('get_port_widget', None)
        except KeyError:
            pass
        try:
            self._cache.pop('get_connection_widget', None)
        except KeyError:
            pass

    def set_level(self, node_model):
        # If None was provided, we will switch to the top level.
        if node_model is None:
            root_model = self.get_root_model()
            if root_model:
                node_model = root_model

        self.invalidate_node_model(node_model)
        if self._current_level_data:
            self.invalidate_node_model(self._current_level_model)

        self._current_level_model = node_model
        self._current_level_data = node_model.get_metadata()

        self.clear()
        self._widget_bound_inn = None
        self._widget_bound_out = None

        # If we don't have anything to redraw, simply exit.
        if not node_model:
            return

        widgets = set()
        children = node_model.get_children()
        for child_model in children:
            child_model._node = node_model  # hack: parent is not correctly set at the moment
            widget = self.get_node_widget(child_model)
            widgets.add(widget)
            self.expand_node_attributes(child_model)
            self.expand_node_connections(child_model)

        component = node_model.get_metadata()
        metatype = factory_datatypes.get_datatype(component)

        if metatype == factory_datatypes.AttributeType.Component:
            # Create inn node
            grp_inn = component.grp_inn
            node_model = self.get_node_model_from_value(grp_inn)
            node_widget = self.get_node_widget(node_model)
            self.expand_node_attributes(node_model)
            self.expand_node_connections(node_model)
            self._widget_bound_inn = node_widget
            # widgets.remove(node_widget)

            # Create out node
            grp_out = component.grp_out
            node_model = self.get_node_model_from_value(grp_out)
            node_widget = self.get_node_widget(node_model)
            self.expand_node_attributes(node_model)
            self.expand_node_connections(node_model)
            self._widget_bound_out = node_widget

            self._widget_bound_inn.setGraphPos(QtCore.QPointF(-5000.0, 0))
            self._widget_bound_out.setGraphPos(QtCore.QPointF(5000.0, 0))

    def can_navigate_to(self, node_model):
        if node_model is None:
            return True

        # We need at least one children to be able to jump into something.
        # todo: is that always true? what happen to empty compound?
        if not node_model.get_children():
            log.debug("Cannot enter into {0} because there's no children!".format(node_model))
            return False

        # We don't want to enter the same model twice.
        if self._current_level_data == node_model:
            return False

        # Currently since we can have 3 node model for a single compound (one model when seen from outside and two
        # model when seen from the inside, the inn and the out), we need a better way to distinguish them.
        # For now we'll use a monkey-patched data from libSerialization, however we need a better approach.
        meta_data = node_model.get_metadata()
        if hasattr(self._current_level_data, '_network') and hasattr(meta_data, '_network'):
            current_network = self._current_level_data._network
            new_network = meta_data._network
            if current_network == new_network:
                return False

        return True

    def navigate_down(self):
        node_model = next(iter(self.get_selected_node_models()), None)
        # if not node_model:
        #     return None

        if self.can_navigate_to(node_model):
            self.set_level(node_model)
            self.onLevelChanged.emit(node_model)
        else:
            log.debug("Cannot naviguate to {0}".format(node_model))

    def navigate_up(self):
        if self._current_level_data is None:
            return

        node_model = self._current_level_model.get_parent()
        if self.can_navigate_to(node_model):
            self.set_level(node_model)
            self.onLevelChanged.emit(node_model)
        else:
            log.debug("Cannot naviguate to {0}".format(node_model))

    def on_right_click(self, menu):
        values = self.get_selected_values()

        if values:
            menu_action = menu.addAction('Group')
            menu_action.triggered.connect(self.group_selection)

        if any(True for val in values if isinstance(val, component.Component)):
            menu_action = menu.addAction('Ungroup')
            menu_action.triggered.connect(self.ungroup_selection)

        values = [v for v in values if isinstance(v, entity.Entity)]  # limit ourself to components

        # values = [v for v in values if factory_datatypes.get_datatype(v) == factory_datatypes.AttributeType.Component]
        # values = [node._meta_data for node in self.getSelectedNodes() if
        #           node._meta_type == factory_datatypes.AttributeType.Component]
        if not values:
            return

        menu = factory_rc_menu.get_menu(menu, values, self.on_execute_action)

    def on_execute_action(self, actions):
        self.manager.execute_actions(actions)

    def _get_selected_nodes_outsider_ports(self):
        selected_nodes_model = self.get_selected_node_models()
        inn_attrs = set()
        out_attrs = set()
        for node_model in selected_nodes_model:
            for port_dst in node_model.get_connected_input_attributes():
                # Ignore message attributes
                attr = port_dst.get_metadata()
                attr_type = attr.type()
                if attr_type == 'message':
                    continue

                for connection_model in port_dst.get_input_connections():
                    src_port_model = connection_model.get_source()
                    src_node_model = self.get_node_model_from_value(src_port_model.get_parent())
                    if src_node_model in selected_nodes_model:
                        continue

                    inn_attrs.add(port_dst.get_metadata())

            for port_src in node_model.get_connected_output_attributes():
                # Ignore message attributes
                attr = port_src.get_metadata()
                attr_type = attr.type()
                if attr_type == 'message':
                    continue

                for connection_model in port_src.get_output_connections():
                    dst_port_model = connection_model.get_destination()
                    dst_node_model = self.get_node_model_from_value(dst_port_model.get_parent())
                    if dst_node_model in selected_nodes_model:
                        continue

                    out_attrs.add(port_src.get_metadata())

        return inn_attrs, out_attrs

    @libPython.memoized_instancemethod
    def get_port_input_connections(self, model):
        # type: (NodeGraphPortModel) -> list[NodeGraphPortModel]
        """
        Control what input connection models are exposed for the provided port model.
        :param model: The destination port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as destination.
        """
        # Ignore message attributes
        attr = model.get_metadata()
        attr_type = attr.type()
        if attr_type == 'message':
            return

        for connection in model.get_input_connections():
            # Redirect unitConversion nodes
            attr_dst = connection.get_source().get_metadata()
            node_dst = attr_dst.node()
            if isinstance(node_dst, pymel.nodetypes.UnitConversion) and attr_dst.longName() == 'output':
                model_src = self.get_port_model_from_value(node_dst.input)
                for new_connection in self.get_port_input_connections(model_src):
                    yield self._model.get_connection_model_from_values(new_connection.get_source(), model)
                return

            yield connection

    @libPython.memoized_instancemethod
    def get_port_output_connections(self, model):
        # type: (NodeGraphPortModel) -> List[NodeGraphPortModel]
        """
        Control what output connection models are exposed for the provided port model.
        :param model: The source port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as source.
        """
        # Ignore message attributes
        attr = model.get_metadata()
        attr_type = attr.type()
        if attr_type == 'message':
            return

        for connection in model.get_output_connections():

            # Redirect unitConversion input attribute
            attr_dst = connection.get_destination().get_metadata()
            node_dst = attr_dst.node()
            if isinstance(node_dst, pymel.nodetypes.UnitConversion) and attr_dst.longName() == 'input':
                model_dst = self.get_port_model_from_value(node_dst.output)
                for new_connection in self.get_port_output_connections(model_dst):
                    yield self._model.get_connection_model_from_values(model, new_connection.get_destination())
                return

            yield connection

    def group_selection(self):
        # selected_nodes = self.get_selected_node_models()
        inn_attrs, out_attrs = self._get_selected_nodes_outsider_ports()

        inn_attrs = dict((attr.longName(), attr) for attr in inn_attrs)
        out_attrs = dict((attr.longName(), attr) for attr in out_attrs)
        inst = component.Component.create(inn_attrs, out_attrs)  # todo: how do we handle dag nodes?

        selected_nodes = set()
        for attr in itertools.chain(inn_attrs.itervalues(), out_attrs.itervalues()):
            selected_nodes.add(attr.node())

        # Resolve middle position, this is where the component will be positioned.
        # todo: it don't work... make it work... please? XD
        # middle_pos = QtCore.QPointF()
        # for selected_node in selected_nodes:
        #     model = self.get_node_model_from_value(selected_node)
        #     widget = self.get_node_widget(model)
        #     widget_pos = QtCore.QPointF(widget.transform().dx(), widget.transform().dy())
        #     middle_pos += widget_pos
        # middle_pos /= len(selected_nodes)

        self.manager.export_network(inst)

        # Remove grouped widgets
        for node in selected_nodes:
            node_model = self.get_node_model_from_value(node)
            node_widget = self.get_node_widget(node_model)
            node_widget.disconnectAllPorts()
            self._view.removeNode(node_widget, emitSignal=False)

        # Invalided grouped models
        for node in selected_nodes:
            self.invalidate_node_value(node)

        inst_model, inst_widget = self.add_node(inst)
        # inst_widget.setGraphPos(middle_pos)

        return inst

    def ungroup_selection(self):
        # Get selection components
        components = [val for val in self.get_selected_values() if isinstance(val, component.Component)]
        if not components:
            return

        new_nodes = set()
        for component in components:
            component_model = self.get_node_model_from_value(component)
            component_widget = self.get_node_widget(component_model)

            new_nodes.update(component.get_children())

            component.explode()

            component_widget.disconnectAllPorts()
            self._view.removeNode(component_widget, emitSignal=False)

        for node in new_nodes:
            self.invalidate_node_value(node)

        for node in new_nodes:
            self.add_node(node)

        # for component in components:
        #     component_model = self.get_node_model_from_value(component)
        #     for connection_model in component_model.get_input_connections():
        #         if connection_model in self._known_connections_widgets:
        #             widget = self.get_connection_widget(connection_model)  # todo: prevent creation
        #             self._view.removeConnection(widget, emitSignal=False)
        #             self._known_connections_widgets.remove(connection_model)
        #     for connection_model in component_model.get_output_connections():
        #         if connection_model in self._known_connections_widgets:
        #             widget = self.get_connection_widget(connection_model)  # todo: prevent creation
        #             self._view.removeConnection(widget, emitSignal=False)
        #             self._known_connections_widgets.remove(connection_model)
        #
        #     children = component.get_children()
        #     new_nodes.extend(children)
        #     component.explode()
        #
        #     Hack: children model parent have changed, we need to invalidate the cache
        #     for child in children:
        #         self.invalidate_node(child)
            #
            # component_model = self.get_node_model_from_value(component)
            # widget = self.get_node_widget(component_model)
            # self._view.removeNode(widget, emitSignal=False)
        #
        # self._cache.clear()
        # for node in new_nodes:
        #     self.add_node(node)
