from omtk.qt_widgets.nodegraph.models.graph.graph_proxy_model import NodeGraphGraphProxyModel

if False:
    from typing import List, Generator
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphPortModel, NodeGraphConnectionModel


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

    def intercept_node(self, node):
        """Intercept a node to show something else instead."""
        if self._filter:
            if self._filter.can_show_node(node):
                for yielded in self._filter.intercept_node(node):
                    yield yielded
        else:
            yield node

    # todo: implement?
    def intercept_port(self, port):
        """Intercept a port to show something else instead."""
        if self._filter:
            if self._filter.can_show_port(port):
                for yielded in self._filter.intercept_port(port):
                    yield yielded
        else:
            yield port

    # todo: implement?
    # todo: rename with something more understandable
    def intercept_connection(self, connection):
        """Intercept a connection to show something else instead."""
        if self._filter:
            if self._filter.can_show_connection(connection):
                for yielded in self._filter.intercept_connection(connection):
                    yield yielded
        else:
            yield connection
