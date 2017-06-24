"""
Define a controller for one specific GraphView.
"""
from omtk.libs import libPython

# Used for type checking
if False:
    from .nodegraph_model import NodeGraphModel
    from .nodegraph_node_model import NodeGraphNodeModel
    from .nodegraph_port_model import NodeGraphPortModel
    from .nodegraph_view import NodeGraphView
    from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView
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

    def get_nodes(self):
        # type: () -> (List[NodeGraphNodeModel])
        return self._known_nodes

    def get_ports(self):
        # type: () -> (List[NodeGraphPortModel])
        return self._known_attrs

    @libPython.memoized_instancemethod
    def get_node_widget(self, model):
        # type: (NodeGraphNodeModel) -> PyFlowgraphNode
        """
        Main entry-point for Widget creation.
        Handle caching and registration for widgets.
        :param node: A NodeGraphNodeModel instance.
        :return: A PyFlowgraph Node instance.
        """
        return model.get_widget(self._view)

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

        return model.get_widget(self._view, node_widget)

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

        widget_src_node = port_src_model.get_node().get_widget()
        widget_dst_node = port_dst_model.get_node().get_widget()
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
        for attr in node_model.get_attributes():
            port = node_widget.getPort(attr.get_name())
            if not port:
                self.get_port_widget(attr)

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

    def add_node(self, pynode):
        node_model = self._model.get_node_from_value(pynode)
        self._known_nodes.add(node_model)
        node_widget = node_model.create_node_widget(self._view)
        self._view.addNode(node_widget)

    def redraw(self):
        """
        Draw the current graph on the view.
        :return:
        """

        # Draw nodes
        nodes = {node for node in self.get_nodes() if node.get_parent() == self._current_level}
        for node in nodes:
            widget = node.create_node_widget()
            self._view.addNode(widget)
