"""
Define a controller for one specific GraphView.
"""
from omtk.libs import libPython

# Used for type checking
if False:
    from .graph_model_registry import GraphRegistry
    from .graph_model_node import GraphNodeModel
    from .graph_model_port import GraphPortModel
    from .graph_model_link import GraphLinkModel
    from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView
    from omtk.vendor.pyflowgraph.node import Node as PyFlowgraphNode
    from omtk.vendor.pyflowgraph.port import BasePort as PyFlowgraphBasePort
    from omtk.vendor.pyflowgraph.connection import Connection as PyFlowgraphConnection


class GraphController(object):
    def __init__(self, registry, graph):
        # type: (GraphRegistry, PyFlowgraphView) -> ()
        self._registry = registry
        self._graph = graph

        # Cache to prevent creating already defined nodes
        self._known_nodes = set()
        self._known_attrs = set()
        self._known_connections = set()

    @libPython.memoized_instancemethod
    def get_node_widget(self, model):
        # type: (GraphNodeModel) -> PyFlowgraphNode
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param node: A GraphNodeModel instance.
        :return: A PyFlowgraph Node instance.
        """
        return model.get_widget(self._graph)

    @libPython.memoized_instancemethod
    def get_port_widget(self, model):
        # type: (GraphPortModel) -> PyFlowgraphBasePort
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param port: A GraphPortModel instance.
        :return: A PyFlowgraph Port instance.
        """
        # In Pyflowgraph, a Port need a Node.
        # Verify that we initialize the widget for the Node.
        node_model = model.get_parent()
        node_widget = self.get_node_widget(node_model)

        return model.get_widget(self._graph, node_widget)

    @libPython.memoized_instancemethod
    def get_connection_widget(self, model):
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param model: A GraphLinkModel instance.
        :return: A PyFlowgraph Connection instance.
        """
        # In Pyflowgraph, a Connection need two Port instances.
        # Ensure that we initialize the widget for the Ports.
        port_src_model = model.get_source()
        port_dst_model = model.get_destination()

        widget_src_node = port_src_model.get_node().get_widget()
        widget_dst_node = port_dst_model.get_node().get_widget()
        return self._graph.connectPorts(
            widget_src_node,
            port_src_model.get_name(),
            widget_dst_node,
            port_dst_model.get_name()
        )

    def expand_node_attributes(self, node_model):
        # type: (GraphNodeModel) -> None
        """
        Show all available attributes for a PyFlowgraph Node.
        Add it in the pool if it didn't previously exist.
        :return:
        """
        node_widget = self.get_node_widget(node_model)

        # In PyFlowgraph, ports are accessible by name.
        for attr in node_model.get_attributes():
            port = node_widget.getPort(attr.get_name())
            if not port:
                self.get_port_widget(attr)

    def expand_attribute_connections(self, model_attr):
        # type: (GraphPortModel) -> None
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
