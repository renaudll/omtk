"""
Define a controller for one specific GraphView.
"""
import functools
import logging

import omtk.component.factory
import pymel.core as pymel
from omtk import decorators
from omtk import component
from omtk.core import manager, entity
from omtk.libs import libPyflowgraph, libPython
from omtk.factories import factory_rc_menu, factory_datatypes
from omtk.nodegraph.models.node import node_dg, node_root
from omtk.nodegraph.nodegraph_controller_cache import NodeGraphWidgetCache
from omtk.component import component_base
from omtk.vendor.Qt import QtCore, QtWidgets

log = logging.getLogger(__name__)


class NodeGraphController(QtCore.QObject):  # QtCore.QObject is necessary for signal handling
    """
    Link node values to NodeGraph[Node/Port/Connection]Model.
    DOES handle the Component representation by wrapper ``NodeGraphRegistry``.

    :param NodeGraphRegistry registry:
    :param GraphModel model:
    :param NodeGraphView view:
    """
    onLevelChanged = QtCore.Signal(object)
    actionRequested = QtCore.Signal(list)

    # Define the default root model to use
    _cls_root_model = node_root.NodeGraphNodeRootModel

    def __init__(self, registry, model=None, view=None):
        super(NodeGraphController, self).__init__()  # needed for signal handling

        self.cache = NodeGraphWidgetCache()

        self._registry = None
        self._model = None
        self._view = None
        self._filter = None

        # Hold a reference to the inn and out node when inside a compound.
        self._widget_bound_inn = None
        self._widget_bound_out = None

        # self.set_view(view)

        # Cache to prevent creating already defined nodes
        self._known_nodes = set()
        self._known_attrs = set()
        self._known_connections = set()

        # Keep track of which nodes, ports and connections are visible.
        self._visible_nodes = set()
        self._visible_ports = set()
        self._visible_connections = set()

        self._known_nodes_widgets = set()
        self._known_connections_widgets = set()

        # Cache to access model-widget relationship
        # self._cache_node_widget_by_model = {}
        # self._cache_node_model_by_widget = {}
        # self._cache_port_widget_by_model = {}
        # self._cache_port_model_by_widget = {}
        # self._cache_connection_widget_by_model = {}
        # self._cache_connection_model_by_widget = {}
        #
        # self._cache_node_by_port = {}
        # self._cache_ports_by_node = defaultdict(set)
        #
        # self._cache_nodes = {}

        self._old_scene_x = None
        self._old_scene_y = None

        # Keep track of which node and port have been expanded.
        # This allow easier update when switching between filters.
        self._buffer_old_nodes = set()  # nodes that the graph will try to display when the model is reset
        self._expanded_nodes = set()  # todo: duplicate?
        self._nodes_with_expanded_connections = set()

        if registry:
            self.set_registry(registry)
        if model:
            self.set_model(model)
        if view:
            self.set_view(view)

    @property
    def manager(self):
        return manager.get_session()

    @decorators.memoized_instancemethod
    def get_root_model(self):
        return None
        return self._cls_root_model(self._model) if self._cls_root_model else None

    def get_nodes(self):
        """

        :rtype: List[NodeModel]
        """
        # return self._known_nodes
        model = self.get_model()
        return model.get_nodes()

    def get_ports(self):
        """

        :return:
        :rtype: List[PortModel]
        """
        return self._known_attrs

    def get_model(self):
        """
        :return:
        :rtype: omtk.nodegraph.GraphModel
        """
        return self._model

    def set_model(self, model):
        """

        :param omtk.nodegraph.GraphModel model:
        """

        self._model = model
        if self._view:
            self.reset_view()

        # if self._model:
        #     model.onReset.disconnect(self.on_model_reset)
        #     model.onNodeAdded.disconnect(self.on_model_node_added)
        #     model.onNodeRemoved.disconnect(self.on_model_node_removed)
        #     model.onPortAdded.disconnect(self.on_model_port_added)
        #     model.onPortRemoved.disconnect(self.on_model_port_removed)
        #     model.onConnectionAdded.disconnect(self.on_model_connection_added)
        #     model.onConnectionRemoved.disconnect(self.on_model_connection_removed)

        # model.onAboutToBeReset.connect(self.on_model_about_to_be_reset)
        model.onReset.connect(self.on_model_reset)
        model.onNodeAdded.connect(self.on_model_node_added)
        model.onNodeRemoved.connect(self.on_model_node_removed)
        model.onNodeMoved.connect(self.on_model_node_moved)
        model.onPortAdded.connect(self.on_model_port_added)
        model.onPortRemoved.connect(self.on_model_port_removed)
        model.onConnectionAdded.connect(self.on_model_connection_added)
        model.onConnectionRemoved.connect(self.on_model_connection_removed)

        # note: We expect the last model to be a GraphComponentProxyFilterModel for now.
        # model.onLevelChanged.connect(self.onLevelChanged)

        # # Hack: Check if the model use a SubgraphProxyModel.
        # # If yes, we'll keep a reference to it
        # from omtk.nodegraph.models.graph import graph_component_proxy_model
        # while model:
        #     if isinstance(model, graph_component_proxy_model.GraphComponentProxyFilterModel):
        #         self._subgraph_proxy_model = model
        #         break

    def get_view(self):
        """
        Query the view associated with the controller (MVC)
        :return:
        :rtype: NodeGraphView
        """
        assert(bool(self._view))
        return self._view

    def set_view(self, view):
        """
        Bind a view to the controller (MVC)
        :param NodeGraphView view: The new view.
        """

        # Disconnect previous events
        if self._view:
            self._view.connectionAdded.disconnect(self.on_connection_added)
            self._view.connectionRemoved.disconnect(self.on_connected_removed)
            self._view.selectionChanged.disconnect(self.on_selection_changed)
            self._view.on_right_click.disconnect(self.on_right_click)
            self._view.nodeDragedIn.disconnect(self.on_node_draged_in)
            self._view.selectionMoved.disconnect(self.on_selected_nodes_moved)

        self._view = view

        # Restore visible nodes/ports/connections
        for node_model in self._visible_nodes:
            self.add_node_to_view(node_model)
        for port_model in self._visible_ports:
            self.add_port_model_to_view(port_model)
        for connection_model in self._visible_connections:
            self.add_connection_model_to_view(connection_model)

        # Connect events
        view.connectionAdded.connect(self.on_connection_added)
        view.connectionRemoved.connect(self.on_connected_removed)
        view.selectionChanged.connect(self.on_selection_changed)
        view.on_right_click.connect(self.on_right_click)
        view.nodeDragedIn.connect(self.on_node_draged_in)
        view.selectionMoved.connect(self.on_selected_nodes_moved)

        self.reset_view()

    def set_filter(self, filter_):
        """

        :param filter_: The new filter.
        :type filter: NodeGraphFilter or None
        """
        self._filter = filter_
        model = self.get_model()
        model.set_filter(filter_)

    def set_registry(self, registry):
        """
        Set the registry.
        :param NodeGraphRegistry registry:
        """
        self._registry = registry

    def get_registry(self):
        """
        Get the registry.
        :return: The registry where all the node, port and connections are stored.
        :rtype: NodeGraphRegistry
        """
        return self._registry

    # --- Events ---

    def _get_port_models_from_connection(self, connection):
        port_src_widget = connection.getSrcPort()
        port_dst_widget = connection.getDstPort()
        port_src_model = self.cache.get_port_from_widget(port_src_widget)
        port_dst_model = self.cache.get_port_from_widget(port_dst_widget)
        return port_src_model, port_dst_model

    def on_connection_added(self, connection):
        port_src_model, port_dst_model = self._get_port_models_from_connection(connection)
        port_dst_model.connect_from(port_src_model.get_metadata_output())

    def on_connected_removed(   self, connection):
        port_src_model, port_dst_model = self._get_port_models_from_connection(connection)
        port_src_value = port_src_model.get_metadata_input()
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

    # @decorators.log_info
    def on_component_created(self, component):
        """
        Ensure the component is added to the view on creation.
        This is not the place for any scene update routine.
        :param component:
        :return:
        """

        log.debug("Creating component {0} (id {1})".format(component, id(component)))
        registry = self.get_registry()
        node = registry.get_node(component)

        # todo: move this somewhere appropriate
        from omtk.core import module
        if isinstance(component, module.Module):
            rig = self.manager._root
            rig.add_module(component)

        self.add_node(node)
        # self.expand_node_ports(node)
        # self.expand_node_connections(node)

        if self._view and self.is_node_in_view(node):
            widget = self.get_node_widget(node)
            libPyflowgraph.arrange_upstream(widget)
            libPyflowgraph.arrange_downstream(widget)

    # --- Model events ---

    # @decorators.log_info
    def on_model_reset(self):
        for node in list(self.get_nodes()):  # hack: prevent change during iteration
            # self.remove_node(node, emit=False)
            self.remove_node_from_view(node)

        if self._view:
            self.reset_view()

    # @decorators.log_info
    def on_model_node_added(self, node):
        """
        Called when a node is added to the graph.
        :param NodeModel node: The node added.
        """
        if self._view:  # todo: move in add_node_to_view?
            self.add_node_to_view(node)

    # @decorators.log_info
    def on_model_node_removed(self, node):
        """
        Called when a node is removed from the graph.
        :param NodeModel node: The node removed.
        """
        if self._view and self.is_node_in_view(node):
            self.remove_node_from_view(node)

    # @decorators.log_info
    def on_model_node_moved(self, node, pos):
        """
        Called when a node position change in the graph.
        :param NodeModel node:
        :param QtCore.QPointF pos:
        """
        if self._view and self.is_node_in_view(node):
            widget = self.get_node_widget(node)
            widget.setPos(pos)

    # @decorators.log_info
    def on_model_port_added(self, port):
        """
        Called when a port is added to the graph.
        :param PortModel port: The port added.
        """
        if self._view:
            self.add_port_to_view(port)

    # @decorators.log_info
    def on_model_port_removed(self, port):
        """
        Called when a port is removed from the graph.
        :param PortModel port: The port removed
        """
        if self._view:
            self.remove_port_from_view(port)

    # @decorators.log_info
    def on_model_connection_added(self, connection):
        """
        Called when a connection is added to the graph.
        :param ConnectionModel connection: The connection added
        """
        if self._view:
            self.add_connection_to_view(connection)

    # @decorators.log_info
    def on_model_connection_removed(self, connection):
        """
        Called when a connection is removed from the graph.
        :param ConnectionModel connection:
        """
        if self._view:
            self.remove_connection_from_view(connection)

    def reset_view(self):
        self.clear()  # todo: rename to clear_view

        model = self.get_model()

        try:
            self._cache.clear()
        except AttributeError:
            pass
        # self._cache.clear()

        for node in model.iter_nodes():
            self.add_node_to_view(node)

        for port in sorted(model.iter_ports()):  # todo: use GraphProxyModel for sorting?
            self.get_port_widget(port)

        for connection in model.iter_connections():
            self.get_connection_widget(connection)

    # --- Model utilities ---

    def collapse_node_attributes(self, node_model):
        # There's no API method to remove a port in PyFlowgraph.
        # For now, we'll just re-created the node.
        # node_widget = self.get_widget_from_node(node_model)
        # self._view.removeNode(node_widget)
        # self.get_widget_from_node.cache[node_model]  # clear cache
        # node_widget = self.get_widget_from_node(node_model)
        # self._view.addNode(node_widget)
        raise NotImplementedError

    # todo: move to model?
    def iter_node_connections(self, node, inputs=True, outputs=True):
        """
        Iter through each connections associated to the provided node.
        :param NodeModel node:
        :param bool inputs:
        :param bool outputs:
        :return: A connection iterator.
        :rtype: Generator[ConnectionModel]
        """
        for port in self._model.iter_node_ports(node):
            if outputs:
                for connection in self._model.iter_port_output_connections(port):
                    yield connection
            if inputs:
                for connection in self._model.iter_port_input_connections(port):
                    yield connection

    def expand_node_connections(self, node, inputs=True, outputs=True):
        """
        Ensure that all node connections are visibile in the graph.
        :param NodeModel node: The node containing the connections.
        :param bool inputs: If True, all input connections will be visible (default: True).
        :param bool outputs: If True, all output connections will be visible (default: True).
        """
        self._model.expand_node_connections(node, inputs=inputs, outputs=outputs)

        # Update cache
        self._nodes_with_expanded_connections.add(node)

    # --- Widget factory ---

    @decorators.memoized
    def get_node_widget(self, node):
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param node: A NodeModel instance.
        :return: A PyFlowgraph Node instance.
        """
        node_widget = node.get_widget(self._view, self)
        node_widget._omtk_model = node  # monkey-patch

        # Restore previously set node position
        pos = libPyflowgraph.get_node_position(node)
        if pos:
            pos = QtCore.QPointF(*pos)
            pos = node_widget.mapToScene(pos)
            node_widget.setPos(pos)

        return node_widget

    @decorators.memoized
    def get_port_widget(self, port):
        """
        Get the QWidget associated with the port.
        :param PortModel port: The port to visualize.
        :return: A PyFlowgraph QWidget representing the port.
        :rtype: OmtkNodeGraphBasePortWidget
        """
        # log.debug('Creating widget for {0}'.format(port_base.py))

        # In Pyflowgraph, a Port need a Node.
        # Verify that we initialize the widget for the Node.
        # node_value = port.get_parent().get_metadata()
        # node_model = self.get_node_model_from_value(node_value)
        node_model = port.get_parent()

        # Hack: Hide Compound bound nodes when not inside the compound!
        # if isinstance(node_model, nodegraph_node_model_component.NodeGraphComponentBoundBaseModel):
        #     compound_model = self.get_node_model_from_value(node_model.get_parent())
        #     if self._current_level != compound_model:
        #         node_model = compound_model

        graph = self.get_model()
        is_input = graph.is_port_input(port)
        is_output = graph.is_port_output(port)
        node_widget = self.get_node_widget(node_model)
        port_widget = port.get_widget(self, self._view, node_widget, is_input=is_input, is_output=is_output)

        # Update cache
        # self._cache_port_model_by_widget[port_widget] = port
        # self._cache_port_widget_by_model[port] = port_widget

        return port_widget

    @decorators.memoized_instancemethod
    def get_connection_widget(self, connection_model):
        """
        The the PyFlowgraph QWidget associated with the provied connection.
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param ConnectionModel connection_model: The connection to visualize.
        :return: A PyFlowgraph QWidget.
        :rtype: OmtkNodeGraphBasePortWidget
        """
        # log.debug('Creating widget for {0}'.format(connection_model))

        # In Pyflowgraph, a Connection need two Port instances.
        # Ensure that we initialize the widget for the Ports.
        port_src_model = connection_model.get_source()
        port_dst_model = connection_model.get_destination()

        # Ensure ports are initialized
        widget_src_port = self.get_port_widget(port_src_model)
        widget_dst_port = self.get_port_widget(port_dst_model)

        model_src_node = port_src_model.get_parent()
        model_dst_node = port_dst_model.get_parent()

        if not self.is_node_in_view(model_src_node):
            widget_src_node = self.add_node_to_view(model_src_node)
        else:
            widget_src_node = self.get_node_widget(model_src_node)

        if not self.is_node_in_view(model_dst_node):
            widget_dst_node = self.add_node_to_view(model_dst_node)
        else:
            widget_dst_node = self.get_node_widget(model_dst_node)

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
            connection = self._view.connectPorts(
                widget_src_node,
                port_src_model.get_name(),
                widget_dst_node,
                port_dst_model.get_name()
            )

        except Exception, e:
            log.warning("Error connecting {0} to {1}, {2}".format(
                port_src_model.get_name(),
                port_dst_model.get_name(),
                e
            ))

        if connection:
            self._known_connections_widgets.add(connection)

        return connection

    # --- Widget/View methods ---

    def is_node_in_view(self, node):
        """
        Query a node visibility
        :param NodeModel node: The node to query.
        :return: True if the node is visible. False otherwise.
        :rtype: bool
        """
        return node in self._visible_nodes

    def is_port_in_view(self, port):
        """
        Query a port visibility.
        :param PortModel port: The port to query.
        :return: True if the port is visible. False otherwise.
        :rtype: bool
        """
        return port in self._visible_ports

    def is_connection_in_view(self, connection):
        """
        Query a connection visibility
        :param ConnectionModel connection: The connection to query.
        :return: True if the connection is visible. False otherwise.
        :rtype: bool
        """
        return connection in self._visible_connections

    def add_node_to_view(self, node):
        """
        Add a node to the view.
        :param omtk.nodegraph.NodeModel node: The node to add.
        """
        self._visible_nodes.add(node)

        if self.get_view():
            node_widget = self.get_node_widget(node)

            pos = node.get_position()
            if pos:
                node_widget.setPos(pos)

            # todo: check for name clash?
            self._view.addNode(node_widget)
            self._known_nodes_widgets.add(node_widget)

            # Hack: Enable the eventFilter on the node
            # We can only do this once it's added to the scene
            # todo: use signals for this?
            node.on_added_to_scene()
            node_widget.on_added_to_scene()

            return node_widget

    def remove_node_from_view(self, node):
        """
        Remove a node from the view.
        :param NodeModel node: The node to remove.
        """
        if not self.is_node_in_view(node):
            return

        self._visible_nodes.remove(node)
        model = self.get_model()

        if self.get_view():
            for port in model.get_node_ports(node):
                self.remove_port_from_view(port)

            node_widget = self.get_node_widget(node)
            node_widget.disconnectAllPorts(emitSignal=False)
            self._view.removeNode(node_widget)

            node.on_removed_from_scene()
            node_widget.on_removed_from_scene()

        self.cache.unregister_node(node)

    def add_port_to_view(self, port):
        """
        Add a port to the view.
        :param PortModel port: The port to add.
        """
        widget = self.get_port_widget(port)

        # Update the cache
        # self._cache_port_widget_by_model[port] = widget
        # self._cache_port_model_by_widget[widget] = port

        self._visible_ports.add(port)

        # todo: use an add_port_to_view method?
        self.cache.register_port(port, widget)

    def remove_port_from_view(self, port):
        """
        Remove a port from the view
        :param PortModel port: The port to remove
        """
        if not self.is_port_in_view(port):
            return

        self._visible_ports.remove(port)
        widget = self.cache.unregister_port(port)
        node_widget = self.cache.get_node_widget(port.get_parent())
        node_widget.removePort(widget)

    def add_connection_to_view(self, connection):
        """
        Add a connection to the graph view.
        :param connection: The connection to add.
        :type connection: ConnectionModel
        """
        # Simply creating the widget is enough
        widget = self.get_connection_widget(connection)

        # Update cache
        self._visible_connections.add(connection)
        self.cache.register_connection(connection, widget)

    def remove_connection_from_view(self, connection):
        """
        Remove a connection from the graph view
        :param connection: The connection to remove
        :type connection: ConnectionModel
        """
        if not self.is_connection_in_view(connection):
            return
        self._visible_connections.remove(connection)

        # Clear Model <-> Widget cache
        widget = self.cache.unregister_connection(connection)
        # widget = self._cache_connection_widget_by_model.pop(connection)
        # self._cache_connection_model_by_widget.pop(widget)

        if self.get_view():
            self._view.removeConnection(widget, emitSignal=False)

    # --- High-level methods ---

    def on_node_draged_in(self, value):
        registry = self.get_registry()
        node = registry.get_node(value)
        self.add_node(node)

    def on_selected_nodes_moved(self):
        for node in self.get_selected_node_models():
            node_widget = self.get_node_widget(node)
            pos = node_widget.scenePos()
            # pos = node_widget.mapToScene(pos)
            libPyflowgraph.save_node_position(node, (pos.x(), pos.y()))

    def add_nodes(self, *nodes, **kwargs):
        [self.add_node(node, **kwargs) for node in nodes]

    def add_node(self, node, expand_ports=True, expand_connections=True):
        """
        Create a widget in the graph for the provided model.
        :param NodeModel node: The node to display.
        :param bool expand_ports: If True, that all ports will be visible.
        :param bool expand_connections: If True, that all connections will be visible.
        """
        self._model.add_node(node)

        if expand_ports:
            self._model.expand_node_ports(node)
        if expand_connections:
            self.expand_node_connections(node)

    def remove_node(self, node_model):
        """
        Remove a node from the View.
        Note that by default, this will keep the QGraphicItem in memory.
        :param node_model: The node to remove.
        """
        try:
            self._known_nodes.remove(node_model)
        except KeyError, e:
            log.warning(e)  # todo: fix this
        model = self.get_model()
        model.remove_node(node_model, emit=True)
        # widget = self.get_widget_from_node(node_model)
        # widget.disconnectAllPorts(emitSignal=False)
        # self._view.removeNode(widget)

    def rename_node(self, model, new_name):
        """
        Called when the user rename a node via the UI.
        :param NodeModel model: The node to rename.
        :param str new_name: The name to use.
        """
        model.rename(new_name)
        widget = self.get_node_widget(model)
        # todo: implement node .update_label()?
        widget._widget_label.setText(new_name)

    def delete_node(self, model):
        """
        Remove a node from the scene.
        :param NodeModel model: The node to remove.
        """
        model.delete()  # this should fire some callbacks

    def get_selected_node_models(self):
        """
        Query the node selection.
        :return: A list of nodes.
        :rtype: List[NodeModel]
        """
        return [pfg_node._model for pfg_node in self._view.getSelectedNodes()]

    def get_selected_values(self):
        return [model.get_metadata() for model in self.get_selected_node_models()]

    def clear(self):
        for node in self._model.get_nodes():
            self._model.remove_node(node)

        # We won't call clear since we will keep a reference to the Widgets in case
        # we need to re-use them. Calling clear would make our cache point to invalid
        # data and cause a Qt crash.
        # self._view.clear()

        if self._view:
            for widget in list(self._view.iter_connections()):
                self._view.removeConnection(widget, emitSignal=False)
            for widget in list(self._view.iter_nodes()):
                self._view.removeNode(widget, emitSignal=False)

        # Clear Node Model/Widget cache
        #self._cache_node_widget_by_model.clear()
        #self._cache_node_model_by_widget.clear()

    # --- Level related methos ---

    def get_level(self):
        return self._model.get_level()

    def set_level(self, node_model):
        if self._model:
            self._model.set_level(node_model)

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
            menu_action.triggered.connect(self.group_selected_nodes)

        components = [val for val in values if isinstance(val, component.Component)]
        if components:
            inst = components[0]
            self._add_actions_for_component(menu, inst)

        values = [v for v in values if isinstance(v, entity.Entity)]  # limit ourself to _known_definitions

        # values = [v for v in values if factory_datatypes.get_datatype(v) == factory_datatypes.AttributeType.Component]
        # values = [node._meta_data for node in self.getSelectedNodes() if
        #           node._meta_type == factory_datatypes.AttributeType.Component]
        if not values:
            return

        menu = factory_rc_menu.get_menu(menu, values, self.on_execute_action)

    def _add_actions_for_component(self, menu, inst):
        """
        Add actions to provided menu specific to provided Component instance.
        :param QtWidgets.QMenu menu:
        :param Component inst:
        """
        from omtk.component import component_registry

        menu.addSection("Component")

        menu_action = menu.addAction("Properties")
        menu_action.triggered.connect(self.on_show_properties_panel)

        menu_action = menu.addAction('Publish...')
        menu_action.triggered.connect(self.on_rc_menu_publish_component)
        # menu_action = menu.addAction('Publish as Module')
        # menu_action.triggered.connect(self.on_rcmenu_publish_module)
        menu_action = menu.addAction('Ungroup')
        menu_action.triggered.connect(self.ungroup_selected_nodes)

        # If the component have a definition, we might want to update it.
        component_def = inst.get_definition()
        if not component_def:
            log.debug("Found no definition for component {0}. Skipping additional menus.")
        else:
            registry = component_registry.get_registry()
            component_versions = registry.get_component_versions(component_def)

            if len(component_versions) > 1:
                submenu = menu.addMenu("Update to...")
                for component_version in component_versions:
                    label = 'Update to {0}'.format(component_version.version)
                    if component_version == component_def:
                        label += ' (current)'
                    menu_action = submenu.addAction(label)
                    if component_version == component_def:
                        menu_action.setEnabled(False)
                    menu_action.triggered.connect(functools.partial(self.update_selected_nodes_to, component_version))

            menu_action = menu.addAction('Update')
            menu_action.triggered.connect(self.update_selected_nodes)

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

    def _get_nodes_outsider_ports(self, selected_nodes_model):
        inn_attrs = set()
        out_attrs = set()
        for node_model in selected_nodes_model:
            for port_dst in node_model.get_connected_input_ports():
                # Ignore message attributes
                attr = port_dst.get_metadata()
                attr_type = port_dst.get_metatype()
                if attr_type == factory_datatypes.AttributeType.AttributeMessage:
                    continue

                for connection_model in port_dst.get_input_connections():
                    src_port_model = connection_model.get_source()
                    src_node_model = src_port_model.get_parent()
                    if src_node_model in selected_nodes_model:
                        continue

                    metadata = port_dst.get_metadata()
                    if not metadata:
                        log.warning("Can't find metadata for {}".format(metadata))
                        continue
                    inn_attrs.add(metadata)

            for port_src in node_model.get_connected_output_ports():
                # Ignore message attributes
                attr = port_src.get_metadata()
                attr_type = port_src.get_metatype()
                if attr_type == factory_datatypes.AttributeType.AttributeMessage:
                    continue

                for connection_model in port_src.get_output_connections():
                    dst_port_model = connection_model.get_destination()
                    dst_node_model = dst_port_model.get_parent()
                    if dst_node_model in selected_nodes_model:
                        continue

                    metadata = port_src.get_metadata()
                    if not metadata:
                        log.warning("Can't find metadata for {}".format(metadata))
                        continue
                    out_attrs.add(port_src.get_metadata())

        return inn_attrs, out_attrs

    def _get_attr_map_from_nodes(self, nodes):
        """
        From a group of nodes, identify the visible connection that evade from the group and store their attributes in a map.
        This will be used to define which attribute will be part of a compound and what will be their names.
        :param nodes:
        :type nodes: List[NodeModel]
        :return:
        :rtype: Tuple[Dict[str, pymel.Attribute], Dict[str, pymel.Attribute]]
        """
        # todo: Move to GraphModel?
        model = self.get_model()
        map_inn = {}
        map_out = {}
        for node in nodes:
            # Fill inputs
            for connection in model.get_port_input_connections(node):
                port_src = connection.get_source()
                node_src = port_src.get_parent()

                # Ignore connections that stay in the same namespace
                if node_src in nodes:
                    continue

                # Get destination attribute, ignore any invalid type
                port_dst = connection.get_destination()
                metadata = port_dst.get_metadata()
                if not isinstance(metadata, pymel.Attribute):
                    log.warning("Ignoring connection %s, invalid destination metadata type. "
                                "Expected pymel.Attribute, got %s." % connection, metadata)
                    continue

                key = port_src.get_name()
                key = libPython.get_unique_key(key, map_inn)
                map_inn[key] = metadata

            # Fill outputs
            for connection in model.get_port_output_connections(node):
                port_dst = connection.get_destination()
                node_dst = port_dst.get_parent()

                # Ingore connections that say in the same namespace
                if node_dst in nodes:
                    continue

                # Get source attribute, ignore any invalid type
                port_src = connection.get_source()
                metadata = port_src.get_metadata()
                if not isinstance(metadata, pymel.Attribute):
                    log.warning("Ignoring port %s, invalid source metadata type. "
                                "Expected pymel.Attribute, got %s." % connection, metadata)
                    continue

                key = port_dst.get_name()
                key = libPython.get_unique_key(key, map_out)
                map_out[key] = metadata

        return map_inn, map_out


    # --- User actions, currently defined in the widget, should be moved in the controller ---

    def add_maya_selection_to_view(self):
        """
        Add the current Maya selection to the view.
        """
        registry = self.get_registry()
        for obj in pymel.selected():
            node = registry.get_node(obj)
            self.add_node(node)

    def remove_maya_selection_from_view(self):
        """
        Remove the current Maya selection from the view if applicable.
        """
        view = self.get_view()
        view.deleteSelectedNodes()  # todo: is this the desired way?

    def on_match_maya_editor_positions(self, multiplier=2.0):
        from omtk.libs import libMayaNodeEditor
        from omtk.libs import libPyflowgraph
        models = self.get_selected_node_models()
        for model in models:
            if not isinstance(model, node_dg.NodeGraphDgNodeModel):
                continue
            node = model.get_metadata()
            pos = libMayaNodeEditor.get_node_position(node)
            if not pos:
                log.warning("Can't read Maya NodeGraph position for {0}".format(node))
                continue

            pos = (pos[0] * multiplier, pos[1] * multiplier)

            widget = self.get_node_widget(model)
            widget.setPos(QtCore.QPointF(*pos))
            libPyflowgraph.save_node_position(node, pos)

    def delete_selected_nodes(self):
        for model in self.get_selected_node_models():
            self.delete_node(model)

    def duplicate_selected_nodes(self):
        registry = self.get_registry()
        pynodes = pymel.duplicate(pymel.selected())
        for pynode in pynodes:
            node = registry.get_node(pynode)
            self.add_node(node)

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

    def _get_active_node(self):
        view = self.get_view()
        return next(iter(view.getSelectedNodes()), None)

    def arrange_upstream(self):
        node = self._get_active_node()
        if not node:
            return
        libPyflowgraph.arrange_upstream(node)

    def arrange_downstream(self):
        node = self._get_active_node()
        if not node:
            return
        libPyflowgraph.arrange_downstream(node)

    def arrange_spring(self):
        view = self.get_view()
        pyflowgraph_nodes = view.getSelectedNodes()
        libPyflowgraph.spring_layout(pyflowgraph_nodes)
        self._view.frameAllNodes()

    def arrange_recenter(self):
        view = self.get_view()
        pyflowgraph_nodes = view.getSelectedNodes()
        libPyflowgraph.recenter_nodes(pyflowgraph_nodes)
        self._view.frameSelectedNodes()

    def frame_all(self):
        self._view.frameAllNodes()

    def frame_selected(self):
        self._view.frameSelectedNodes()

    def _update_node_to_latest_version(self, node):
        """
        ???
        :param NodeGraphComponentModel node:
        """
        from omtk.nodegraph.models.node import node_component
        from omtk import component_registry
        if not isinstance(node, node_component.NodeGraphComponentModel):
            raise Exception

        registry = component_registry.ComponentRegistry()  # todo: use singleton
        cmpnt = node.get_metadata()
        cmpnt_def = cmpnt.get_definition()
        if registry.is_latest_component_version(cmpnt_def):
            log.info("{} is already latest".format(cmpnt_def))
            return

        latest_def = registry.get_latest_component_version(cmpnt_def)
        if not latest_def:
            log.warning("Found no version available for {0} ({1})".format(cmpnt_def.name, cmpnt_def.uid))
            return

        self._update_node_to(cmpnt, latest_def)

    def _update_component_to(self, node, latest_def):
        """
        Update a provided NodeGraphComponentModel to a provided ComponentDefinition.
        This can be used to update/downgrade a Component to another version or to promote a Component to another type.
        :param NodeGraphComponentModel node:
        :param ComponentDefinition latest_def:
        """
        old_namespace = node.namespace
        data = node.hold_connections()
        node.delete()  # note: we'll let the callbacks kick in
        new_inst = latest_def.instanciate(name=old_namespace)  # todo: rename to namespace
        new_inst.fetch_connections(*data)
        new_node = self.get_registry().get_node(new_inst)
        self.add_node(new_node)

    def update_selected_nodes(self):
        for node_model in self.get_selected_node_models():
            self._update_node_to_latest_version(node_model)

    def update_selected_nodes_to(self, definition):
        """
        ???
        :param ComponentDefinition definition:
        """
        from omtk.nodegraph.models.node import node_component
        for node in self.get_selected_node_models():
            if isinstance(node, node_component.NodeGraphComponentModel):
                inst = node.get_metadata()
                self._update_component_to(inst, definition)

    # --- Right click menu events ---

    def group_selected_nodes(self):
        nodes = self.get_selected_node_models()

        # Resolve middle position, this is where the component will be positioned.
        # todo: it don't work... make it work... please? XD
        # middle_pos = QtCore.QPointF()
        # for selected_node in selected_nodes:
        #     model = self.get_node_model_from_value(selected_node)
        #     widget = self.get_widget_from_node(model)
        #     widget_pos = QtCore.QPointF(widget.transform().dx(), widget.transform().dy())
        #     middle_pos += widget_pos
        # middle_pos /= len(selected_nodes)
        self.group_nodes(nodes)

    def group_nodes(self, nodes):
        """
        Create a component from the selected nodes.
        Any selected nodes will be in the component.
        Any connection that exit the selection will be redirected to the component 'inn' or 'out' nodes.
        :param List[NodeModel] nodes:
        :rtype: NodeGraphComponentModel
        """
        registry = self.get_registry()

        # Remove grouped widgets
        for node in nodes:
            # node_model = self.get_node_model_from_value(node)
            self._model.remove_node(node)
            # self.remove_node_from_view(node)

        # todo: better detection of dagnodes
        dgnodes = [node.get_metadata() for node in nodes]


        map_inn, map_out = self._get_attr_map_from_nodes(nodes)
        inst = omtk.component.factory.from_attributes_map(map_inn, map_out, dagnodes=dgnodes)

        # inn_attrs, out_attrs = self._get_nodes_outsider_ports(nodes)
        # inst = component.from_attributes(inn_attrs, out_attrs, dagnodes=dgnodes)

        self.manager.export_network(inst)
        self.manager._register_new_component(inst)
        new_node = registry.get_node(inst)

        self.add_node(new_node)

        return new_node

    def on_rcmenu_add_attribute(self):
        # return mel.eval('AddAttribute')
        from omtk.qt_widgets import form_add_attribute
        form_add_attribute.show()

    def on_rcmenu_rename_attribute(self):
        new_name = QtWidgets.QInputDialog.getText(None, "Rename Attribute", "New Name:")
        print new_name
        raise NotImplementedError

    def on_rcmenu_delete_attribute(self):
        raise NotImplementedError

    def on_show_properties_panel(self):
        from omtk.qt_widgets import form_component_properties

        inst = next((val for val in self.get_selected_values() if isinstance(val, component.Component)), None)
        form_component_properties.show(inst)

    def on_rc_menu_publish_component(self):
        inst = self.get_selected_node_models()[0].get_metadata()  # todo: secure this
        from omtk.qt_widgets import form_publish_component
        form_publish_component.show(inst)

    def on_rcmenu_publish_module(self):
        from omtk.qt_widgets import form_create_component
        form_create_component.show()

    def ungroup_selected_nodes(self):
        # Get selection _known_definitions
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


