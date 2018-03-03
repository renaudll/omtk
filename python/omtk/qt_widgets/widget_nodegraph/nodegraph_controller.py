"""
Define a controller for one specific GraphView.
"""
import logging

from omtk import decorators
from maya import OpenMaya
import pymel.core as pymel
from omtk import constants
from omtk.core import component, session
from omtk.core import entity
from omtk.factories import factory_datatypes, factory_rc_menu
from omtk.libs import libComponents
from omtk.vendor.Qt import QtCore

from . import nodegraph_node_model_base
from . import nodegraph_node_model_component
from . import nodegraph_node_model_dgnode
from . import nodegraph_node_model_root

# Used for type checking
if False:
    from .nodegraph_port_model import NodeGraphPortModel
    from .nodegraph_connection_model import NodeGraphConnectionModel
    from .nodegraph_view import NodeGraphView
    from .nodegraph_node_model_base import NodeGraphNodeModel
    from .pyflowgraph_node_widget import OmtkNodeGraphNodeWidget
    from .pyflowgraph_port_widget import OmtkNodeGraphBasePortWidget
    from omtk.vendor.pyflowgraph.node import Node as PyFlowgraphNode

log = logging.getLogger('omtk.nodegraph')

# todo: implement proxy model outside of controller?
# todo: add model-in-view cache, calling set_view should display visible models


class NodeGraphController(QtCore.QObject):  # note: QtCore.QObject is necessary for signal handling
    """
    Link node values to NodeGraph[Node/Port/Connection]Model.
    DOES handle the Component representation by wrapper ``NodeGraphModel``.
    """
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

        # Keep track of which nodes, ports and connections are visible.
        self._visible_node_models = set()
        self._visible_port_models = set()
        self._visible_connection_models = set()

        self._known_nodes_widgets = set()
        self._known_connections_widgets = set()

        # Cache to access model-widget relationship
        self._cache_node_widget_by_model = {}
        self._cache_node_model_by_widget = {}
        self._cache_port_widget_by_model = {}
        self._cache_port_model_by_widget = {}

        self._cache_nodes = {}

        self._old_scene_x = None
        self._old_scene_y = None

    @property
    def manager(self):
        return session.get_session()

    @decorators.memoized_instancemethod
    def get_root_model(self):
        return self._cls_root_model(self._model) if self._cls_root_model else None

    def get_nodes(self):
        # type: () -> (List[NodeGraphNodeModel])
        return self._known_nodes

    def get_ports(self):
        # type: () -> (List[NodeGraphPortModel])
        return self._known_attrs

    def get_view(self):
        # type: () -> NodeGraphView
        return self._view

    def set_view(self, view):
        # type: (NodeGraphView) -> None

        # Disconnect previous events
        if self._view:
            self._view.connectionAdded.disconnect(self.on_connection_added)
            self._view.connectionRemoved.disconnect(self.on_connected_removed)

        self._view = view

        # Restore visible nodes/ports/connections
        for node_model in self._visible_node_models:
            self.add_node_model_to_view(node_model)
        for port_model in self._visible_port_models:
            self.add_port_model_to_view(port_model)
        for connection_model in self._visible_connection_models:
            self.add_connection_model_to_view(connection_model)

        # Connect events
        view.connectionAdded.connect(self.on_connection_added)
        view.connectionRemoved.connect(self.on_connected_removed)

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
        port_src_value = port_src_model.get_metadata()
        port_dst_model.disconnect_from(port_src_value)
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

    # --- Registration methods ---

    def _register_node_model(self, model):
        self._known_nodes.add(model)

    # --- Cache clearing method ---

    def invalidate_node_value(self, key):
        """Invalidate any cache referencing provided value."""
        # todo: deprecate in favor of invalidate_node_model?
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

    def invalidate_value(self, value):
        # type: (NodeGraphPortModel) -> None
        model = self.get_port_model_from_value(value)
        widget = self._cache_node_widget_by_model.pop(model)
        self._cache_port_model_by_widget.pop(model)
        self._cache_port_widget_by_model.pop(widget)

    def invalidate_port_model(self, model):
        # type: (NodeGraphPortModel) -> None

        # Invalidate any connection related to the attribute
        for connection_model in self.iter_port_connections(model):
            self.invalidate_connection_model(connection_model)

        # Invalidate widget related with the model
        # Note: PyFlowGraph does not allow us remove a port, we need to remove the whole node...

        # self.invalidate_node_model(node_model)
        widget = self._cache_port_widget_by_model.pop(model, None)
        if widget:
            self._cache_port_model_by_widget.pop(widget)

            node_model = model.get_parent()
            node_widget = self.get_node_widget(node_model)
            node_widget.removePort(widget)

    def invalidate_port_value(self, value):
        # type: (object) -> None
        model = self.get_port_model_from_value(value)
        self.invalidate_port_model(model)

    def invalidate_connection_value(self, value):
        # type: (object) -> None
        model = self.get_port_model_from_value(value)
        self.invalidate_connection_model(model)

    def invalidate_connection_model(self, model):
        # type: (NodeGraphConnectionModel) -> None
        # Invalidate widget related with the model
        pass  # do we have something with the model? there's no cache

        widget = self.get_connection_widget(model)
        view = self.get_view()
        view.removeConnection(widget, emitSignal=False)

    def unregister_node_widget(self, widget):
        """
        Remove a PyFlowGraphNode from the cache.
        :return:
        """
        model = self._cache_node_model_by_widget[widget]
        self._cache_node_model_by_widget.pop(widget)
        self._cache_node_widget_by_model.pop(model)
        # self._known_nodes_widgets.remove(widget)

    def unregister_node_model(self, model):
        # type: (NodeGraphNodeModel) -> None
        """
        Remove a NodeGraphNodeModel from the cache.
        For obvious reasons, this will also unregister it's associated Widget if any.
        :param model:
        :return:
        """
        # Remove associated widget if necessary
        if self.is_node_model_in_view(model):
            self.remove_node_model_from_view(model)


        widget = self._cache_node_widget_by_model.get(model, None)
        if widget:
            self.unregister_node_widget(widget)
        # self._known_nodes.remove(model)

        self.invalidate_node_model(model)

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
            return nodegraph_node_model_dgnode.NodeGraphDgNodeModel(self._model, val)

        # model = self._model.get_node_from_value(val)
        # if isinstance(model, nodegraph_node_model_component.NodeGraphComponentBoundBaseModel):
        #     component = model.get_component()
        #     if component != self._current_level:
        #         return self._model.get_node_from_value(component)

        return self._model.get_node_from_value(val)

    def get_port_model_from_value(self, val):
        return self._model.get_port_model_from_value(val)

    def get_connection_model_from_value(self, val):
        return self._model.get_connection_model_from_values

    def get_node_model_from_widget(self, widget):
        # type: (PyFlowgraphNode) -> NodeGraphNodeModel
        """
        Return the data model associated with a Node widget.
        :param widget: A PyflowgraphNode widget instance.
        :return: A NodeGraphNodeModel instance.
        """
        # Retrieve monkey-patched model in PyFlowgraph widgets.
        return widget._omtk_model

    # --- Filter Interface ---

    def can_show_port(self, port_model):
        # type: (NodeGraphPortModel) -> bool
        if not self._filter:
            return True

        if not self._filter.can_show_port(port_model):
            return False

        node_model = port_model.get_parent()
        if not self._filter.can_show_node(node_model):
            return False

        return True

    def can_show_connection(self, connection_model):
        # Get the node associated with the connection
        # Even if a connection is between two nodes, only one can have ownership.
        node_model = connection_model.get_parent()

        # Use the model to get the parent of the node.
        # This is either the None or a component.
        node_parent_inst = node_model.get_parent()

        # Note that we don't check self._current_level_model since it have a value (the root model).
        if node_parent_inst is None:
            return self._current_level_data is None

        # node_parent_model = self.get_node_model_from_value(node_parent_inst) if node_parent_inst else None
        return node_parent_inst == self._current_level_data

    def _iter_node_port_models(self, node_model):
        for port_model in node_model.get_attributes(self):
            if self.can_show_port(port_model):
                yield port_model

    def expand_node_attributes(self, node_model):
        # type: (NodeGraphNodeModel) -> None
        """
        Show all available attributes for a PyFlowgraph Node.
        Add it in the pool if it didn't previously exist.
        :return:
        """
        for port_model in sorted(self._iter_node_port_models(node_model)):
            self.get_port_widget(port_model)

    def expand_port_input_connections(self, port_model):
        for connection_model in self.get_port_input_connections(port_model):
            self.get_connection_widget(connection_model)

    def expand_port_output_connections(self, port_model):
        for connection_model in self.get_port_output_connections(port_model):
            self.get_connection_widget(connection_model)

    def iter_port_output_connections(self, port_model):
        for connection_model in self.get_port_output_connections(port_model):
            if not self.can_show_connection(connection_model):
                continue
            port_model_dst = connection_model.get_destination()
            node_model_dst = port_model_dst.get_parent()

            # Apply filter
            if self._filter:
                if not self._filter.can_show_node(node_model_dst):
                    continue
                if not self._filter.can_show_connection(connection_model):
                    continue

            yield connection_model

    def _iter_node_output_connections(self, node_model):
        for port_model in node_model.get_connected_output_attributes(self):
            if not self.can_show_port(port_model):
                continue

            for connection_model in self.iter_port_output_connections(port_model):
                node_model_dst = connection_model.get_destination().get_parent()

                # Ignore blacklisted nodes
                if self._filter:
                    if not self._filter.can_show_node(node_model_dst):
                        continue

                # todo: ignore blacklisted ports?

                # Ignore blacklisted connections
                if not self._filter.can_show_connection(connection_model):
                    continue

                yield connection_model

    def _iter_node_input_connections(self, node_model):
        for port_model in node_model.get_connected_input_attributes():
            if not self.can_show_port(port_model):
                continue

            for connection_model in self._iter_port_input_connections(port_model):
                node_model_src = connection_model.get_source().get_parent()

                # Ignore blacklisted nodes
                if self._filter:
                    if not self._filter.can_show_node(node_model_src):
                        continue

                # Ignore blacklisted connections
                if not self._filter.can_show_connection(connection_model):
                    continue

                yield connection_model

    def expand_node_connections(self, node_model, expand_downstream=True, expand_upstream=True):
        # type: (NodeGraphNodeModel) -> None
        if expand_upstream:
            for port_model in node_model.get_connected_output_attributes(self):
                self.expand_port_output_connections(port_model)
        if expand_downstream:
            for port_model in node_model.get_connected_input_attributes(self):
                self.expand_port_input_connections(port_model)

    def collapse_node_attributes(self, node_model):
        # There's no API method to remove a port in PyFlowgraph.
        # For now, we'll just re-created the node.
        # node_widget = self.get_node_widget(node_model)
        # self._view.removeNode(node_widget)
        # self.get_node_widget.cache[node_model]  # clear cache
        # node_widget = self.get_node_widget(node_model)
        # self._view.addNode(node_widget)
        raise NotImplementedError

    # --- Widget factory ---

    def get_node_widget(self, model):
        # assert(isinstance(model, nodegraph_node_model_base.NodeGraphNodeModel))
        try:
            return self._cache_node_widget_by_model[model]
        except LookupError:
            log.debug("Cannot find widget for {0}. Creating a new one.".format(model))
            widget = self._get_node_widget(model)
            self._cache_node_widget_by_model[model] = widget
            self._cache_node_model_by_widget[widget] = model
            return widget

    def _get_node_widget(self, model):
        # type: (NodeGraphNodeModel) -> OmtkNodeGraphNodeWidget
        # todo: how to we prevent from calling .get_widget() from the model directly? do we remove it?
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param node: A NodeGraphNodeModel instance.
        :return: A PyFlowgraph Node instance.
        """
        node_widget = model.get_widget(self._view, self)
        node_widget._omtk_model = model  # monkey-patch

        return node_widget

    @decorators.memoized_instancemethod
    def get_port_widget(self, port_model):
        # type: (NodeGraphPortModel) -> OmtkNodeGraphBasePortWidget
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param port: A NodeGraphPortModel instance.
        :return: A PyFlowgraph Port instance.
        """
        # log.debug('Creating widget for {0}'.format(port_model))

        # In Pyflowgraph, a Port need a Node.
        # Verify that we initialize the widget for the Node.
        node_value = port_model.get_parent().get_metadata()
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

    @decorators.memoized_instancemethod
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
        widget_src_port = self.get_port_widget(port_src_model)
        widget_dst_port = self.get_port_widget(port_dst_model)

        model_src_node = self.get_node_model_from_value(port_src_model.get_parent().get_metadata())
        model_dst_node = self.get_node_model_from_value(port_dst_model.get_parent().get_metadata())

        if not self.is_node_model_in_view(model_src_node):
            widget_src_node = self.add_node_model_to_view(model_src_node)

        if not self.is_node_model_in_view(model_dst_node):
            widget_dst_node = self.add_node_model_to_view(model_dst_node)
        # widget_src_node = self.get_node_widget(model_src_node)
        # if not self._is_node_widget_in_view(widget_src_node):
        #     self._add_node_widget_to_view(widget_src_node)
        # widget_dst_node = self.get_node_widget(model_dst_node)
        # if not self._is_node_widget_in_view(widget_dst_node):
        #     self._add_node_widget_to_view(widget_dst_node)

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
            print '|||', connection_model
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

    # --- Widget/View methods ---

    def is_node_model_in_view(self, node_model):
        return node_model in self._visible_node_models

    # todo: deprecate
    def _is_node_widget_in_view(self, node_widget):
        """Check if a QGraphicsItem instance is in the View."""
        return node_widget in self._known_nodes_widgets

    def add_node_model_to_view(self, node_model):
        # type: (NodeGraphNodeModel) -> None
        self._visible_node_models.add(node_model)

        if self.get_view():
            node_widget = self.get_node_widget(node_model)
            # todo: check for name clash?
            self._view.addNode(node_widget)
            self._known_nodes_widgets.add(node_widget)

            # Hack: Enable the eventFilter on the node
            # We can only do this once it's added to the scene
            # todo: use signals for this?
            node_widget.on_added_to_scene()

            return node_widget

    def remove_node_model_from_view(self, node_model):
        if not self.is_node_model_in_view(node_model):
            return
        self._visible_node_models.remove(node_model)

        if self.get_view():
            node_widget = self.get_node_widget(node_model)
            node_widget.disconnectAllPorts(emitSignal=False)
            self._view.removeNode(node_widget)
            node_widget.on_removed_from_scene()

    # --- High-level methods ---

    def add_node(self, node_model):
        # type: (NodeGraphNodeModel) -> OmtkNodeGraphNodeWidget
        """
        Create a Widget in the NodeGraph for the provided NodeModel.
        :param node_model: An NodeGraphNodeModel to display.
        """
        if not isinstance(node_model, nodegraph_node_model_base.NodeGraphNodeModel):
            node_model = self.get_node_model_from_value(node_model)
        self._register_node_model(node_model)

        # Ensure the root model is remembering it's session
        if isinstance(self._current_level_model, self._cls_root_model):
            self._current_level_model.add_child(node_model)

        node_widget = self.add_node_model_to_view(node_model)
        if node_widget:

            qrect = node_widget.rect()
            pos = self.get_view().get_available_position(qrect)

            # node_widget.setGraphPos(pos)
            node_widget.setPos(pos)

            self.expand_node_attributes(node_model)
            self.expand_node_connections(node_model)

            return node_widget

    def remove_node(self, node_model, clear_cache=False):
        """
        Remove a node from the View.
        Note that by default, this will keep the QGraphicItem in memory.
        :param node_model:
        :param clear_cache:
        """
        try:
            self._known_nodes.remove(node_model)
        except KeyError, e:
            log.warning(e)  # todo: fix this
        widget = self.get_node_widget(node_model)
        widget.disconnectAllPorts(emitSignal=False)
        self._view.removeNode(widget)

        if clear_cache:
            self.unregister_node_model(node_model)

    def rename_node(self, model, new_name):
        # type: (NodeGraphNodeModel, str) -> None
        """
        Called when the user rename a node via the UI.
        """
        model.rename(new_name)
        widget = self.get_node_widget(model)
        # todo: implement node .update_label()?
        widget._widget_label.setText(new_name)
        print model, new_name

    def delete_node(self, model):
        # type: (NodeGraphNodeModel) -> None
        model.delete()  # this should fire some callbacks0
        self.unregister_node_model(model)

    def get_selected_node_models(self):
        # type: () -> List[NodeGraphNodeModel]
        return [self.get_node_model_from_widget(pfg_node) for pfg_node in self._view.getSelectedNodes()]

    def get_selected_values(self):
        return [model.get_metadata() for model in self.get_selected_node_models()]

    def clear(self):
        # We won't call clear since we will keep a reference to the Widgets in case
        # we need to re-use them. Calling clear would make our cache point to invalid
        # data and cause a Qt crash.
        # self._view.clear()
        for connection in list(self._view.iter_connections()):
            self._view.removeConnection(connection, emitSignal=False)
        for node_widget in list(self._view.iter_nodes()):
            self._view.removeNode(node_widget, emitSignal=False)

        # Clear Node Model/Widget cache
        self._cache_node_widget_by_model.clear()
        self._cache_node_model_by_widget.clear()

        try:
            self._cache.pop('get_port_widget', None)
        except KeyError:
            pass
        try:
            self._cache.pop('get_connection_widget', None)
        except KeyError:
            pass

    # --- Level related methos ---

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
            self.add_node_model_to_view(child_model)
            # widgets.add(widget)
            self.expand_node_attributes(child_model)
            self.expand_node_connections(child_model)

        component = node_model.get_metadata()
        metatype = factory_datatypes.get_datatype(component)

        if metatype == factory_datatypes.AttributeType.Component:
            # Create inn node
            grp_inn = component.grp_inn
            node_model = self.get_node_model_from_value(grp_inn)
            node_widget = self.add_node_model_to_view(node_model)
            self.expand_node_attributes(node_model)
            self.expand_node_connections(node_model)
            self._widget_bound_inn = node_widget

            # Create out node
            grp_out = component.grp_out
            node_model = self.get_node_model_from_value(grp_out)
            node_widget = self.add_node(node_model)
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

    # --- Events ---

    def on_right_click(self, menu):
        values = self.get_selected_values()

        if values:
            menu_action = menu.addAction('Add Attribute')
            menu_action.triggered.connect(self.on_rcmenu_add_attribute)

            menu_action = menu.addAction('Rename Attribute')
            menu_action.triggered.connect(self.on_rcmenu_rename_attribute)

            menu_action = menu.addAction('Rename Attribute')
            menu_action.triggered.connect(self.on_rcmenu_delete_attribute)

            menu_action = menu.addAction('Group')
            menu_action.triggered.connect(self.on_rcmenu_group_selection)

            menu_action = menu.addAction('Publish as Component')
            menu_action.triggered.connect(self.on_rc_menu_publish_component)

            menu_action = menu.addAction('Publish as Module')
            menu_action.triggered.connect(self.on_rcmenu_publish_module)

        if any(True for val in values if isinstance(val, component.Component)):
            menu_action = menu.addAction('Ungroup')
            menu_action.triggered.connect(self.on_rcmenu_ungroup_selection)

        values = [v for v in values if isinstance(v, entity.Entity)]  # limit ourself to components

        # values = [v for v in values if factory_datatypes.get_datatype(v) == factory_datatypes.AttributeType.Component]
        # values = [node._meta_data for node in self.getSelectedNodes() if
        #           node._meta_type == factory_datatypes.AttributeType.Component]
        if not values:
            return

        menu = factory_rc_menu.get_menu(menu, values, self.on_execute_action)

    def on_execute_action(self, actions):
        self.manager.execute_actions(actions)

    def on_selection_changed(self):
        models = self.get_selected_node_models()

        new_selection = set()
        for model in models:
            nodes = model.get_nodes()
            if nodes:
                new_selection.update(nodes)

        if new_selection:
            pymel.select(new_selection)
        else:
            pymel.select(clear=True)

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

                for connection_model in port_dst.get_input_connections(self):
                    src_port_model = connection_model.get_source()
                    src_node_model = src_port_model.get_parent()
                    if src_node_model in selected_nodes_model:
                        continue

                    inn_attrs.add(port_dst.get_metadata())

            for port_src in node_model.get_connected_output_attributes(self):
                # Ignore message attributes
                attr = port_src.get_metadata()
                attr_type = attr.type()
                if attr_type == 'message':
                    continue

                for connection_model in port_src.get_output_connections(self):
                    dst_port_model = connection_model.get_destination()
                    dst_node_model = dst_port_model.get_parent()
                    if dst_node_model in selected_nodes_model:
                        continue

                    out_attrs.add(port_src.get_metadata())

        return inn_attrs, out_attrs

    def _get_decomposematrix_inputmatrix_output_connections(self, attr):
        """
        To call when encountering a decomposeMatrix.inputMatrix attribute.
        This is used to skip previsible decomposeMatrix in the NodeGraph.
        This will yield the inputMatrix attribute if the decomposeMatrix have non-previsible connections.
        Otherwise it will yield all destination port of the decomposeMatrix.
        A previsible connection it either:
        - outputTranslate to translate
        - outputRotate to rotate
        - outputScale to scale
        :param attr: A pymel.Attribute instance representing a decomposeMatrix.inputMatrix attribute.
        """
        def _is_previsible(connection_):
            attr_src_ = connection_.get_source().get_metadata()
            attr_dst_ = connection_.get_destination().get_metadata()
            attr_src_name = attr_src_.longName()
            attr_dst_name = attr_dst_.longName()
            if attr_src_name == 'outputTranslate':  # and attr_dst_name == 'translate':
                return True
            if attr_src_name == 'outputRotate':  # and attr_dst_name == 'rotate':
                return True
            if attr_src_name == 'outputScale':  # and attr_dst_name == 'scale':
                return True
            return False

        # attr_inputmatrix_model = self.get_port_mode
        node = attr.node()
        node_model = self.get_node_model_from_value(node)

        # We will hold the connections in case we encounter an anormal connection.
        results = []
        for attr_dst in node_model.get_connected_output_attributes(self):
            for connection in self.get_port_output_connections(attr_dst):
                # for connection2 in self.get_port_output_connections(dst_node_model):
                if _is_previsible(connection):
                    new_connection = connection.get_destination()
                    results.append(new_connection)
                else:
                    log.warning("Will no ignore {0} because of an unprevisible connection {1}.".format(node, connection))
                    yield attr
                    return

        for result in results:
            yield result

    def iter_port_connections(self, model):
        # type: (NodeGraphPortModel) -> Generator[NodeGraphConnectionModel]
        for connection in self._iter_port_input_connections(model):
            yield connection
        for connection in self._iter_port_output_connections(model):
            yield connection

    def _iter_port_input_connections(self, model):
        # type: (NodeGraphPortModel) -> list[NodeGraphConnectionModel]
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

        for connection in model.get_input_connections(self):

            # Redirect unitConversion nodes
            attr_src = connection.get_source().get_metadata()
            node_src = attr_src.node()
            if isinstance(node_src, pymel.nodetypes.UnitConversion) and attr_src.longName() == 'output':
                model_src = self.get_port_model_from_value(node_src.input)
                for new_connection in self.get_port_input_connections(model_src):
                    yield self._model.get_connection_model_from_values(new_connection.get_source(), model)
                return

            # Redirect decomposeMatrix nodes
            # todo: test
            if isinstance(node_src, pymel.nodetypes.DecomposeMatrix) and attr_src.longName() in ('outputTranslate', 'outputRotate', 'outputScale'):
                inputmatrix_model = self.get_port_model_from_value(node_src.attr('inputMatrix'))
                for sub_connection in self.get_port_input_connections(inputmatrix_model):
                    new_connection = self._model.get_connection_model_from_values(sub_connection.get_source(), model)
                    yield new_connection
                return

            yield connection

    @decorators.memoized_instancemethod
    def get_port_input_connections(self, model):
        return list(self._iter_port_input_connections(model))  # cannot memoize a generator

    def _iter_port_output_connections(self, model):
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

        for connection in model.get_output_connections(self):

            # Redirect unitConversion input attribute
            attr_dst = connection.get_destination().get_metadata()
            node_dst = attr_dst.node()
            if isinstance(node_dst, pymel.nodetypes.UnitConversion) and attr_dst.longName() == 'input':
                model_dst = self.get_port_model_from_value(node_dst.output)
                for new_connection in self.get_port_output_connections(model_dst):
                    yield self._model.get_connection_model_from_values(model, new_connection.get_destination())
                return

            # Redirect decomposeMatrix
            if isinstance(node_dst, pymel.nodetypes.DecomposeMatrix) and attr_dst.longName() == 'inputMatrix':
                for real_attr_dst in self._get_decomposematrix_inputmatrix_output_connections(attr_dst):
                    new_connection = self._model.get_connection_model_from_values(model, real_attr_dst)
                    yield new_connection
                return

            yield connection

    @decorators.memoized_instancemethod
    def get_port_output_connections(self, model):
        return list(self._iter_port_output_connections(model))  # cannot memoize a generator

    # --- User actions, currently defined in the widget, should be moved in the controller ---

    def on_match_maya_editor_positions(self, multiplier=2.0):
        from omtk.libs import libMayaNodeEditor
        from omtk.libs import libPyflowgraph
        models = self.get_selected_node_models()
        for model in models:
            if not isinstance(model, nodegraph_node_model_dgnode.NodeGraphDgNodeModel):
                continue
            node = model.get_metadata()
            pos = libMayaNodeEditor.get_node_position(node)
            if not pos:
                log.warning("Can't read Maya NodeGraph position for {0}".format(node))
                continue

            pos = (pos[0] * multiplier, pos[1] * multiplier)

            widget = self.get_node_widget(model)
            widget.setPos(QtCore.QPointF(*pos))
            libPyflowgraph.save_node_position(widget, pos)

    def delete_selected_nodes(self):
        for model in self.get_selected_node_models():
            self.delete_node(model)

    def duplicate_selected_nodes(self):
        new_nodes = pymel.duplicate(pymel.selected())
        for new_node in new_nodes:
            self.add_node(new_node)

    def select_all_nodes(self):
        view = self.get_view()
        view.clearSelection()
        for node in view.iter_nodes():
            view.selectNode(node, emitSignal=True)

    def on_parent_selected(self):
        pymel.parent()
        # todo: this should trigger internal callbacks

    def expand_selected_nodes(self):
        for node_model in self.get_selected_node_models():
            self.expand_node_connections(node_model)

    def colapse_selected_nodes(self):
        for node_model in self.get_selected_node_models():
            self.collapse_node_attributes(node_model)

    # --- Right click menu events ---

    def on_rcmenu_group_selection(self):
        # selected_nodes = self.get_selected_node_models()
        inn_attrs, out_attrs = self._get_selected_nodes_outsider_ports()

        selected_models = self.get_selected_node_models()
        # selected_nodes = set()
        # for attr in itertools.chain(inn_attrs.itervalues(), out_attrs.itervalues()):
        #     selected_nodes.add(attr.node())

        # Resolve middle position, this is where the component will be positioned.
        # todo: it don't work... make it work... please? XD
        # middle_pos = QtCore.QPointF()
        # for selected_node in selected_nodes:
        #     model = self.get_node_model_from_value(selected_node)
        #     widget = self.get_node_widget(model)
        #     widget_pos = QtCore.QPointF(widget.transform().dx(), widget.transform().dy())
        #     middle_pos += widget_pos
        # middle_pos /= len(selected_nodes)

        # Remove grouped widgets
        for model in selected_models:
            # node_model = self.get_node_model_from_value(node)
            self.remove_node(model, clear_cache=True)

        inn_attrs = dict((attr.longName(), attr) for attr in inn_attrs)
        out_attrs = dict((attr.longName(), attr) for attr in out_attrs)
        inst = component.Component.create(inn_attrs, out_attrs)  # todo: how do we handle dag nodes?

        self.manager.export_network(inst)

        self.add_node(inst)

        return inst

    def on_rcmenu_add_attribute(self):
        # return mel.eval('AddAttribute')
        from omtk.qt_widgets import form_add_attribute
        form_add_attribute.show()

    def on_rcmenu_rename_attribute(self):
        raise NotImplementedError

    def on_rcmenu_delete_attribute(self):
        raise NotImplementedError

    def on_rc_menu_publish_component(self):
        component = self.get_selected_node_models()[0].get_metadata()  # todo: secure this
        from omtk.qt_widgets import form_publish_component
        form_publish_component.show(component)

    def on_rcmenu_publish_module(self):
        from omtk.qt_widgets import form_create_component
        form_create_component.show()

    def on_rcmenu_ungroup_selection(self):
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

            component_widget.disconnectAllPorts(emitSignal=False)
            self._view.removeNode(component_widget, emitSignal=False)

        for node in new_nodes:
            self.invalidate_node_value(node)

        for node in new_nodes:
            self.add_node(node)

    # --- Callbacks ---

    def callback_attribute_added(self, value):
        # return
        # self.invalidate_port_value(value)
        port_model = self.get_port_model_from_value(value)
        node_model = port_model.get_parent()
        port_widget = self.get_port_widget(port_model)
        # self.invalidate_node_model(node_model)
        # self.invalidate_port_model(port_model)
        self.expand_port_input_connections(port_model)  # todo: check first?
        self.expand_port_output_connections(port_model)

    def callback_attribute_array_added(self, value):
        # Something Maya will send notification for an attribute at index 99 (ex: multMatrix.matrixIn).
        # We are not sure how to react at the moment so we'll simply ignore it.
        if value.index() > value.array().numElements():
            log.warning('Received a strange out of bound attribute. Ignoring. {0}'.format(value))
            return

        port_model = self.get_port_model_from_value(value)
        self.invalidate_port_model(port_model)
        # node_model = port_model.get_parent()
        # self.expand_node_attributes(node_model)

        self.get_port_widget(port_model)

    def callback_node_deleted(self, model, *args, **kwargs):
        """
        Called when a known node is deleted in Maya.
        Notify the view of the change.
        :param model: The model that is being deleted
        :param args: Absorb the OpenMaya callback arguments
        :param kwargs: Absorb the OpenMaya callback keyword arguments
        """
        # todo: unregister node
        log.debug("Removing {0} from nodegraph".format(model))
        if model:
            self.remove_node(model, clear_cache=True)

