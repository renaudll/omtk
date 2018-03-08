from omtk import decorators
from omtk.qt_widgets.nodegraph.models.graph.graph_proxy_model import NodeGraphGraphProxyModel
from pymel import core as pymel

if False:
    from typing import List
    from omtk.qt_widgets.nodegraph.port_model import NodeGraphPortModel
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel


class GraphFilterProxyModel(NodeGraphGraphProxyModel):
    """
    ProxyModel that filter a NodeGraphNode.
    Consume ``NodeGraphFilter`` instance via set_filter().
    """
    def __init__(self, filter=None, model=None):
        super(GraphFilterProxyModel, self).__init__(model=model)

        self._filter = None
        if filter:
            self.set_filter(filter)

    def set_filter(self, filter_, expand=True):
        model = self.get_model()

        self._filter = filter_
        if filter_:
            filter_.set_model(model)

        self.reset()

    def can_show_node(self, node):
        # type: (NodeGraphNodeModel) -> bool
        if self._filter:
            if not self._filter.can_show_node(node):
                return False

        return super(GraphFilterProxyModel, self).can_show_node(node)

    def can_show_port(self, port):
        # type: (NodeGraphPortModel) -> bool
        if self._filter:
            if not self._filter.can_show_port(port):
                return False

        return super(GraphFilterProxyModel, self).can_show_port(port)

    def can_show_connection(self, connection):
        if self._filter:
            if not self._filter.can_show_connection(connection):
                return False

        return super(GraphFilterProxyModel, self).can_show_connection(connection)

    def iter_nodes(self):
        for node in super(GraphFilterProxyModel, self).iter_nodes():
            for yielded in self.intercept_node(node):
                yield yielded

    def intercept_node(self, node):
        """Intercept a node to show something else instead."""
        if self._filter:
            for yielded in self._filter.intercept_node(node):
                yield yielded
        else:
            yield node

    # todo: implement?
    def intercept_port(self, port):
        """Intercept a port to show something else instead."""
        if self._filter:
            for yielded in self._filter.intercept_port(port):
                yield yielded
        else:
            yield port

    # todo: implement?
    # todo: rename with something more understandable
    def intercept_connection(self, connection):
        """Intercept a connection to show something else instead."""
        if self._filter:
            for yielded in self._filter.intercept_connection(connection):
                yield yielded
        else:
            yield connection

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

            yield self.intercept_connection(connection_model)

    def _iter_node_output_connections(self, node_model):
        for port_model in node_model.get_connected_output_ports(self):
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

                yield self.intercept_connection(connection_model)

    def _iter_node_input_connections(self, node_model):
        for port_model in node_model.get_connected_input_ports():
            if not self.can_show_port(port_model):
                continue

            for connection_model in self.iter_port_input_connections(port_model):
                node_model_src = connection_model.get_source().get_parent()

                # Ignore blacklisted nodes
                if self._filter:
                    if not self._filter.can_show_node(node_model_src):
                        continue

                # Ignore blacklisted connections
                if not self._filter.can_show_connection(connection_model):
                    continue

                yield self.intercept_connection(connection_model)

    def collapse_node_attributes(self, node_model):
        # There's no API method to remove a port in PyFlowgraph.
        # For now, we'll just re-created the node.
        # node_widget = self.get_node_widget(node_model)
        # self._view.removeNode(node_widget)
        # self.get_node_widget.cache[node_model]  # clear cache
        # node_widget = self.get_node_widget(node_model)
        # self._view.addNode(node_widget)
        raise NotImplementedError

    def iter_port_connections(self, port):
        # type: (NodeGraphPortModel) -> Generator[NodeGraphConnectionModel]
        for connection in self.iter_port_input_connections(port):
            yield self.intercept_connection(connection)
        for connection in self.iter_port_output_connections(port):
            yield self.intercept_connection(connection)

    def get_port_connections(self, port):
        return list(self.iter_port_connections(port))

    def iter_port_input_connections(self, model):
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

        for connection in model.get_input_connections():
            for yielded in self.intercept_connection(connection):
                yield yielded

    @decorators.memoized_instancemethod
    def get_port_input_connections(self, model):
        return list(self.iter_port_input_connections(model))  # cannot memoize a generator

    def iter_port_output_connections(self, port):
        # type: (NodeGraphPortModel) -> List[NodeGraphPortModel]
        """
        Control what output connection models are exposed for the provided port model.
        :param port: The source port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as source.
        """
        # Ignore message attributes
        attr = port.get_metadata()
        attr_type = attr.type()
        if attr_type == 'message':
            return

        for connection in port.get_output_connections():
            for yielded in self.intercept_connection(connection):
                yield connection

    @decorators.memoized_instancemethod
    def get_port_output_connections(self, model):
        return list(self.iter_port_output_connections(model))  # cannot memoize a generator

    def expand_port(self, port, inputs=True, outputs=True):
        # type: (NodeGraphPortModel, bool, bool) -> None
        self._model.expand_port(port, inputs=inputs, outputs=outputs)

    def expand_port_input_connections(self, port):
        self._model.expand_port_input_connections(port)

    def expand_port_output_connections(self, port):
        self._model.expand_port_output_connections(port)

    def expand_node_ports(self, node, inputs=True, outputs=True):
        # type: (NodeGraphNodeModel, bool, bool) -> None
        self._model.expand_node_ports(node, inputs=True, outputs=True)
