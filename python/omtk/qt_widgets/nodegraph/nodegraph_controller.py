"""
Define a controller for one specific GraphView.
"""
import copy
import logging

import pymel.core as pymel
from omtk import decorators
from omtk.core import component, session, entity
from omtk.libs import libPyflowgraph, libPython
from omtk.factories import  factory_rc_menu
from omtk.qt_widgets.nodegraph.models.node import node_dg, node_root
from omtk.qt_widgets.nodegraph import nodegraph_registry
from omtk.vendor.Qt import QtCore

# Used for type checking
if False:
    from typing import List, Generator
    from .nodegraph_view import NodeGraphView
    from omtk.qt_widgets.nodegraph.models import NodeGraphModel, NodeGraphNodeModel, NodeGraphPortModel, \
        NodeGraphConnectionModel
    from omtk.qt_widgets.nodegraph.nodegraph_registry import NodeGraphRegistry
    from omtk.qt_widgets.nodegraph.filters.filter_standard import NodeGraphFilter
    from omtk.qt_widgets.nodegraph.pyflowgraph_node_widget import OmtkNodeGraphNodeWidget
    from omtk.qt_widgets.nodegraph.pyflowgraph_port_widget import OmtkNodeGraphBasePortWidget
    from omtk.qt_widgets.nodegraph.models.node.node_component import NodeGraphComponentModel

log = logging.getLogger('omtk.nodegraph')


class NodeGraphController(QtCore.QObject):  # QtCore.QObject is necessary for signal handling
    """
    Link node values to NodeGraph[Node/Port/Connection]Model.
    DOES handle the Component representation by wrapper ``NodeGraphRegistry``.
    """
    onLevelChanged = QtCore.Signal(object)
    actionRequested = QtCore.Signal(list)

    # Define the default root model to use
    _cls_root_model = node_root.NodeGraphNodeRootModel

    def __init__(self, model=None, view=None):
        super(NodeGraphController, self).__init__()  # needed for signal handling
        # type: (NodeGraphModel, NodeGraphView) -> ()
        self._model = None
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
        self._visible_nodes = set()
        self._visible_ports = set()
        self._visible_connections = set()

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

        # Keep track of which node and port have been expanded.
        # This allow easier update when switching between filters.
        self._buffer_old_nodes = set()  # nodes that the graph will try to display when the model is reset
        self._expanded_nodes = set()  # todo: duplicate?
        self._nodes_with_expanded_connections = set()

        if model:
            self.set_model(model)
        if view:
            self.set_view(view)

    @property
    def manager(self):
        return session.get_session()

    @decorators.memoized_instancemethod
    def get_root_model(self):
        return None
        return self._cls_root_model(self._model) if self._cls_root_model else None

    def get_nodes(self):
        # type: () -> (List[NodeGraphNodeModel])
        return self._known_nodes

    def get_ports(self):
        # type: () -> (List[NodeGraphPortModel])
        return self._known_attrs

    def get_model(self):
        # type: () -> NodeGraphModel
        return self._model

    def set_model(self, model):
        # type: (NodeGraphModel) -> None

        self._model = model
        if self._view:
            self.reset_view()

        model.onAboutToBeReset.connect(self.on_model_about_to_be_reset)
        model.onReset.connect(self.on_model_reset)
        model.onNodeAdded.connect(self.on_model_node_added)
        model.onNodeRemoved.connect(self.on_model_node_removed)
        model.onPortAdded.connect(self.on_model_port_added)
        # model.onPortAdded.connect(self.on_model_reset)
        model.onPortRemoved.connect(self.on_model_port_removed)
        model.onConnectionAdded.connect(self.on_model_connection_added)
        model.onConnectionRemoved.connect(self.on_model_connection_removed)

        # note: We expect the last model to be a GraphComponentProxyFilterModel for now.
        model.onLevelChanged.connect(self.onLevelChanged)

    def get_view(self):
        # type: () -> NodeGraphView
        assert(bool(self._view))
        return self._view

    def set_view(self, view):
        # type: (NodeGraphView) -> None

        # Disconnect previous events
        if self._view:
            self._view.connectionAdded.disconnect(self.on_connection_added)
            self._view.connectionRemoved.disconnect(self.on_connected_removed)
            self._view.selectionChanged.disconnect(self.on_selection_changed)
            self._view.on_right_click.disconnect(self.on_right_click)
            self._view.nodeDragedIn.disconnect(self.on_node_draged_in)

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

        self.reset_view()

    def set_filter(self, filter_):
        # type: (NodeGraphFilter | None) -> None
        self._filter = filter_
        model = self.get_model()
        model.set_filter(filter_)

    def get_registry(self):
        # type: () -> NodeGraphRegistry
        return nodegraph_registry._get_singleton_model()

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

    def on_connected_removed(   self, connection):
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

    # @decorators.log_info
    def on_component_created(self, component):
        """
        Ensure the component is added to the view on creation.
        This is not the place for any scene update routine.
        :param component:
        :return:
        """
        from omtk.qt_widgets.nodegraph import nodegraph_registry

        log.debug("Creating component {0} (id {1})".format(component, id(component)))
        registry = nodegraph_registry._get_singleton_model()
        node = registry.get_node_from_value(component)

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

    def on_model_about_to_be_reset(self):
        self._buffer_old_nodes.update(copy.copy(self._model.get_nodes()))

    # @decorators.log_info
    def on_model_reset(self, expand=True):
        for node in list(self.get_nodes()):  # hack: prevent change during iteration
            # self.remove_node(node, emit_signal=False)
            self.remove_node_from_view(node)

        # If the new filter don't like previous nodes, don't add them.
        # todo: is there a more stable way of retreiving this?
        nodes_to_add = [node for node in self._buffer_old_nodes if not self._filter or self._filter.can_show_node(node)]

        # Fetch nodes
        for node in nodes_to_add:
            self._model.add_node(node, emit_signal=False)

        # Fetch nodes status
        if expand:
            for node in nodes_to_add:
                if node in self._expanded_nodes:
                    self._model.expand_node(node)

                if node in self._nodes_with_expanded_connections:
                    self.expand_node_connections(node)

        if self._view:
            self.reset_view()

    # @decorators.log_info
    def on_model_node_added(self, node):
        # type: (NodeGraphNodeModel) -> None
        if self._view:  # todo: move in add_node_to_view?
            self.add_node_to_view(node)

    # @decorators.log_info
    def on_model_node_removed(self, node):
        # type: (NodeGraphNodeModel) -> None
        if self._view and self.is_node_in_view(node):
            self.remove_node_from_view(node)

    # @decorators.log_info
    def on_model_node_moved(self, node, pos):
        # type: (NodeGraphNodeModel, QtCore.QPointF) -> None
        widget = self.get_node_widget(node)
        widget.setPos(pos)

    # @decorators.log_info
    def on_model_port_added(self, port):
        # type: (NodeGraphPortModel) -> None
        # print port
        if self._view:
            self.get_port_widget(port)

    # @decorators.log_info
    def on_model_port_removed(self, port):
        # type: (NodeGraphPortModel) -> None
        raise NotImplementedError

    # @decorators.log_info
    def on_model_connection_added(self, connection):
        # type: (NodeGraphConnectionModel) -> None
        if self._view:
            self.get_connection_widget(connection)

    # @decorators.log_info
    def on_model_connection_removed(self, connection):
        # type: (NodeGraphConnectionModel) -> None
        raise NotImplementedError

    def reset_view(self):
        self.clear()  # todo: rename to clear_view

        model = self.get_model()

        # Hack: clear cache for now
        # todo: ensure correct cleanup
        self._cache_port_model_by_widget.clear()
        self._cache_port_widget_by_model.clear()
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
        # node_widget = self.get_node_widget(node_model)
        # self._view.removeNode(node_widget)
        # self.get_node_widget.cache[node_model]  # clear cache
        # node_widget = self.get_node_widget(node_model)
        # self._view.addNode(node_widget)
        raise NotImplementedError

    # todo: move to model?
    def iter_node_connections(self, node, inputs=True, outputs=True):
        # type: (NodeGraphNodeModel, bool, bool) -> Generator[NodeGraphConnectionModel]
        for port in self._model.iter_node_ports(node):
            if outputs:
                for connection in self._model.iter_port_output_connections(port):
                    yield connection
            if inputs:
                for connection in self._model.iter_port_input_connections(port):
                    yield connection

    def expand_node_connections(self, node, inputs=True, outputs=True):
        # type: (NodeGraphNodeModel, bool, bool) -> None
        self._model.expand_node_connections(node, inputs=inputs, outputs=outputs)

        # Update cache
        self._nodes_with_expanded_connections.add(node)

    # --- Widget factory ---

    def get_node_widget(self, node):
        # assert(isinstance(node, nodegraph_node_model_base.NodeGraphNodeModel))
        try:
            return self._cache_node_widget_by_model[node]
        except LookupError:
            log.debug("Cannot find widget for {0}. Creating a new one.".format(node))
            widget = self._get_node_widget(node)
            self._cache_node_widget_by_model[node] = widget
            self._cache_node_model_by_widget[widget] = node
            return widget

    def _get_node_widget(self, node):
        # type: (NodeGraphNodeModel) -> OmtkNodeGraphNodeWidget
        # todo: how to we prevent from calling .get_widget() from the node directly? do we remove it?
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param node: A NodeGraphNodeModel instance.
        :return: A PyFlowgraph Node instance.
        """
        node_widget = node.get_widget(self._view, self)
        node_widget._omtk_model = node  # monkey-patch

        return node_widget

    @decorators.memoized_instancemethod
    def get_port_widget(self, port):
        # type: (NodeGraphPortModel) -> OmtkNodeGraphBasePortWidget
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param port: A NodeGraphPortModel instance.
        :return: A PyFlowgraph Port instance.
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

        node_widget = self.get_node_widget(node_model)
        port_widget = port.get_widget(self, self._view, node_widget)

        # Update cache
        self._cache_port_model_by_widget[port_widget] = port
        self._cache_port_widget_by_model[port] = port_widget

        return port_widget

    @decorators.memoized_instancemethod
    def get_connection_widget(self, connection_model):
        # type: (NodeGraphConnectionModel) -> OmtkNodeGraphBasePortWidget
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
        # type: (NodeGraphNodeModel) -> bool
        return node in self._visible_nodes

    def is_port_in_view(self, port):
        return port in self._visible_ports

    def is_connection_in_view(self, connection):
        return connection in self._visible_connections

    def add_node_to_view(self, node):
        # type: (NodeGraphNodeModel) -> None
        self._visible_nodes.add(node)

        if self.get_view():
            node_widget = self.get_node_widget(node)
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
        if not self.is_node_in_view(node):
            return
        self._visible_nodes.remove(node)

        if self.get_view():
            node_widget = self.get_node_widget(node)
            node_widget.disconnectAllPorts(emitSignal=False)
            self._view.removeNode(node_widget)

            node.on_removed_from_scene()
            node_widget.on_removed_from_scene()

        # Clear cache
        widget = self._cache_node_widget_by_model.pop(node)
        self._cache_node_model_by_widget.pop(widget)

    def remove_port_from_view(self, port):
        if not self.is_port_in_view(port):
            return

        # widget = self._cache_port_widget_by_model.pop(port)
        # self._cache_port_model_by_widget.pop(widget)

        self._visible_ports.remove(port)

    def remove_connection_from_view(self, connection):
        if not self.is_connection_in_view(connection):
            return
        self._visible_connections.remove(connection)

        if self.get_view():
            self._view.removeConnection(connection, emitSignal=False)

    # --- High-level methods ---

    def on_node_draged_in(self, value):
        registry = self.get_registry()
        node = registry.get_node_from_value(value)
        self.add_node(node)

    def add_nodes(self, *nodes, **kwargs):
        [self.add_node(node, **kwargs) for node in nodes]

    def add_node(self, node, expand_ports=True, expand_connections=True):
        # type: (NodeGraphNodeModel) -> None
        """
        Create a Widget in the NodeGraph for the provided NodeModel.
        :param node: An NodeGraphNodeModel to display.
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
        model.delete()  # this should fire some callbacks

    def get_selected_node_models(self):
        # type: () -> List[NodeGraphNodeModel]
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
        self._cache_node_widget_by_model.clear()
        self._cache_node_model_by_widget.clear()

    # --- Level related methos ---

    def set_level(self, node_model):
        if self._model:
            self._model.set_level(node_model)

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
        # if self._current_level_data is None:
        #     return

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
            menu_action.triggered.connect(self.group_selected_nodes)

        if any(True for val in values if isinstance(val, component.Component)):
            menu_action = menu.addAction('Publish as Component')
            menu_action.triggered.connect(self.on_rc_menu_publish_component)

            menu_action = menu.addAction('Publish as Module')
            menu_action.triggered.connect(self.on_rcmenu_publish_module)

            menu_action = menu.addAction('Ungroup')
            menu_action.triggered.connect(self.ungroup_selected_nodes)

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

    def _get_nodes_outsider_ports(self, selected_nodes_model):
        inn_attrs = set()
        out_attrs = set()
        for node_model in selected_nodes_model:
            for port_dst in node_model.get_connected_input_ports():
                # Ignore message attributes
                attr = port_dst.get_metadata()
                attr_type = attr.type()
                if attr_type == 'message':
                    continue

                for connection_model in port_dst.get_input_connections():
                    src_port_model = connection_model.get_source()
                    src_node_model = src_port_model.get_parent()
                    if src_node_model in selected_nodes_model:
                        continue

                    inn_attrs.add(port_dst.get_metadata())

            for port_src in node_model.get_connected_output_ports():
                # Ignore message attributes
                attr = port_src.get_metadata()
                attr_type = attr.type()
                if attr_type == 'message':
                    continue

                for connection_model in port_src.get_output_connections():
                    dst_port_model = connection_model.get_destination()
                    dst_node_model = dst_port_model.get_parent()
                    if dst_node_model in selected_nodes_model:
                        continue

                    out_attrs.add(port_src.get_metadata())

        return inn_attrs, out_attrs

    # --- User actions, currently defined in the widget, should be moved in the controller ---

    def add_maya_selection_to_view(self):
        """
        Add the current Maya selection to the view.
        """
        registry = self.get_registry()
        for obj in pymel.selected():
            node = registry.get_node_from_value(obj)
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

    # --- Right click menu events ---

    def group_selected_nodes(self):
        nodes = self.get_selected_node_models()

        # Resolve middle position, this is where the component will be positioned.
        # todo: it don't work... make it work... please? XD
        # middle_pos = QtCore.QPointF()
        # for selected_node in selected_nodes:
        #     model = self.get_node_model_from_value(selected_node)
        #     widget = self.get_node_widget(model)
        #     widget_pos = QtCore.QPointF(widget.transform().dx(), widget.transform().dy())
        #     middle_pos += widget_pos
        # middle_pos /= len(selected_nodes)
        self.group_nodes(nodes)

    def group_nodes(self, nodes):
        # type: (List[NodeGraphNodeModel]) -> NodeGraphComponentModel
        """
        Create a component from the selected nodes.
        Any selected nodes will be in the component.
        Any connection that exit the selection will be redirected to the component 'inn' or 'out' nodes.
        """
        # Remove grouped widgets
        for node in nodes:
            # node_model = self.get_node_model_from_value(node)
            self._model.remove_node(node)
            # self.remove_node_from_view(node)

        registry = node._registry

        # todo: better detection of dagnodes
        dgnodes = [node.get_metadata() for node in nodes]

        inn_attrs, out_attrs = self._get_nodes_outsider_ports(nodes)
        inn_attrs = dict((attr.longName(), attr) for attr in inn_attrs)
        out_attrs = dict((attr.longName(), attr) for attr in out_attrs)
        inst = component.from_attributes(
            inn_attrs, 
            out_attrs,
            dagnodes=dgnodes,
        )

        self.manager.export_network(inst)
        self.manager._register_new_component(inst)
        new_node = registry.get_node_from_value(inst)

        self.add_node(new_node)

        return new_node

    def on_rcmenu_add_attribute(self):
        # return mel.eval('AddAttribute')
        from omtk.qt_widgets import form_add_attribute
        form_add_attribute.show()

    def on_rcmenu_rename_attribute(self):
        raise NotImplementedError

    def on_rcmenu_delete_attribute(self):
        raise NotImplementedError

    def on_rc_menu_publish_component(self):
        inst = self.get_selected_node_models()[0].get_metadata()  # todo: secure this
        from omtk.qt_widgets import form_publish_component
        form_publish_component.show(inst)

    def on_rcmenu_publish_module(self):
        from omtk.qt_widgets import form_create_component
        form_create_component.show()

    def ungroup_selected_nodes(self):
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


