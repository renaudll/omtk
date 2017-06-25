"""
Define a controller for one specific GraphView.
"""
from omtk.libs import libPython
from omtk.libs import libPyflowgraph
from .nodegraph_node_model import NodeGraphNodeModel

# Used for type checking
if False:
    from .nodegraph_model import NodeGraphModel
    from .nodegraph_port_model import NodeGraphPortModel
    from .nodegraph_view import NodeGraphView
    from omtk.vendor.pyflowgraph.node import Node as PyFlowgraphNode
    from omtk.vendor.pyflowgraph.port import BasePort as PyFlowgraphBasePort


class NodeGraphController(object):
    def __init__(self, model, view):
        # type: (NodeGraphModel, NodeGraphView) -> ()
        self._model = model
        self._view = view
        self._current_level = None

        # Cache to prevent creating already defined nodes
        self._known_nodes = set()
        self._known_attrs = set()
        self._known_connections = set()

        self._known_nodes_widgets = set()

    def get_nodes(self):
        # type: () -> (List[NodeGraphNodeModel])
        return self._known_nodes

    def get_ports(self):
        # type: () -> (List[NodeGraphPortModel])
        return self._known_attrs

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
        return node_widget

    @libPython.memoized_instancemethod
    def get_port_widget(self, model):
        # type: (NodeGraphPortModel) -> PyFlowgraphBasePort
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param port: A NodeGraphPortModel instance.
        :return: A PyFlowgraph Port instance.
        """
        # In Pyflowgraph, a Port need a Node.
        # Verify that we initialize the widget for the Node.
        node_model = model.get_parent()
        node_widget = self.get_node_widget(node_model)
        port_widget = model.get_widget(self._view, node_widget)
        node_widget.addPort(port_widget)
        # self._known_attrs.add(port_widget)
        return port_widget

    @libPython.memoized_instancemethod
    def get_connection_widget(self, model):
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param model: A NodeGraphConnectionModel instance.
        :return: A PyFlowgraph Connection instance.
        """
        # In Pyflowgraph, a Connection need two Port instances.
        # Ensure that we initialize the widget for the Ports.
        port_src_model = model.get_source()
        port_dst_model = model.get_destination()

        # Ensure ports are initialized
        self.get_port_widget(port_src_model)
        self.get_port_widget(port_dst_model)

        widget_src_node = self.get_node_widget(port_src_model.get_parent())
        widget_dst_node = self.get_node_widget(port_dst_model.get_parent())

        return self._view.connectPorts(
            widget_src_node,
            port_src_model.get_name(),
            widget_dst_node,
            port_dst_model.get_name()
        )

    def expand_node_attributes(self, node_model):
        # type: (NodeGraphNodeModel) -> None
        """
        Show all available attributes for a PyFlowgraph Node.
        Add it in the pool if it didn't previously exist.
        :return:
        """
        node_widget = self.get_node_widget(node_model)

        # In PyFlowgraph, ports are accessible by name.
        for port_model in sorted(node_model.get_attributes()):
            if not port_model.is_interesting():
                continue
            port = node_widget.getPort(port_model.get_name())
            if not port:
                port_widget = self.get_port_widget(port_model)

    def expand_node_connections(self, node_model):
        # type: (NodeGraphNodeModel) -> None
        for port_model in node_model.get_attributes():
            if port_model.is_connected():
                for connection_model in port_model.get_connections():
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

    def expand_attribute_connections(self, model_attr):
        # type: (NodeGraphPortModel) -> None
        """
        Show all connections for a specific PyFlowgraph Port.
        Add the destination Port and Node in the View if it didn't previously exist.
        :param model_attr:
        :return:
        """
        # todo: is this really the place for is_writable, should this be in .get_input_connections()?
        if model_attr.is_writable():
            for connection_model in model_attr.get_input_connections():
                self.get_connection_widget(connection_model)
        if model_attr.is_readable():
            for connection_model in model_attr.get_output_connections():
                self.get_connection_widget(connection_model)

    def add_node(self, node_model):
        if not isinstance(node_model, NodeGraphNodeModel):
            node_model = self._model.get_node_from_value(node_model)
        self._known_nodes.add(node_model)
        node_widget = self.get_node_widget(node_model)
        self._known_nodes_widgets.add(node_widget)
        # node_widget = node_model.get_widget(self._view)
        # node_widget._omtk_model = node_model  # monkey-patch
        # self._view.addNode(node_widget)

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
        # Retreive monkey-patched model in PyFlowgraph widgets.
        return [pfg_node._omtk_model for pfg_node in self._view.getSelectedNodes()]

    def expand_selected_nodes(self):
        for node_model in self.get_selected_nodes():
            self.expand_node_attributes(node_model)

    def colapse_selected_nodes(self):
        for node_model in self.get_selected_nodes():
            self.collapse_node_attributes(node_model)

    def clear(self):
        for node_widget in self._known_nodes_widgets:
            self._view.removeNode(node_widget)
        self._known_nodes_widgets.clear()

    def navigate_down(self):
        node_model = next(iter(self.get_selected_nodes()), None)
        if not node_model:
            return None

        self.clear()
        for child_model in node_model.get_children():
            self.get_node_widget(child_model)
            self.expand_node_attributes(child_model)
            self.expand_node_connections(child_model)
            from omtk.libs import libPyflowgraph

        grp_inn = node_model.get_metadata().grp_out
        node_model = self._model.get_node_from_value(grp_inn)
        node_widget = self.get_node_widget(node_model)
        libPyflowgraph.arrange_upstream(node_widget)

    def navigate_up(self):
        raise NotImplementedError

