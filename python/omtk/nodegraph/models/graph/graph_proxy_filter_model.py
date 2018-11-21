import logging

from omtk.nodegraph.models.graph.graph_proxy_model import NodeGraphGraphProxyModel

log = logging.getLogger(__name__)


# TODO: Get rig of can_show_[node/port/connection] in favor of intercept_[node/port/connection]?


class GraphFilterProxyModel(NodeGraphGraphProxyModel):
    """
    ProxyModel that filter a NodeGraphNode.
    Consume ``NodeGraphFilter`` instance via set_filter().
    :param omtk.nodegraph.NodeGraphFilter filter: An optional default filter.
    :param omtk.nodegrpah.GraphModel: The graph to filter.
    """

    def __init__(self, registry, filter=None, model=None):
        super(GraphFilterProxyModel, self).__init__(registry, model=model)

        self._filters = []
        if filter:
            self.add_filter(filter)

    def set_filter(self, filter_):
        """
        Set the active filter.
        :param omtk.nodegraph.NodeGraphFilter filter_: The new filter.
        """
        log.warning("Deprecated. Please use add_filter or set_filters.")
        if filter_:
            self.set_filters([filter_])
        else:
            self.clear_filters()


    def clear_filters(self):
        self._filters = []
        self.reset()

    def set_filters(self, filters):
        model = self.get_model()

        for filter_ in filters:
            filter_.set_model(model)

        self._filters = filters
        self.reset()

    def add_filter(self, filter_):
        model = self.get_model()

        filter_.set_model(model)
        self._filters.append(filter_)
        self.reset()

    def remove_filter(self, filter_):
        self._filters.remove(filter_)
        self.reset()

    def intercept_node(self, node):
        """Intercept a node to show something else instead."""
        filters = self._filters

        # No filters
        if not filters:
            yield node
            return

        for filter_ in filters:
            if not filter_.can_show_node(node):
                continue

            for yielded in filter_.intercept_node(node):
                yield yielded

    def intercept_port(self, port):
        """Intercept a port to show something else instead."""
        filters = self._filters

        if not filters:
            yield port
            return

        for filter_ in filters:
            if not filter_.can_show_port(port):
                continue

            for yielded in filter_.intercept_port(port):
                yield yielded

    # todo: implement?
    # todo: rename with something more understandable
    def intercept_connection(self, connection):
        """Intercept a connection to show something else instead."""
        filters = self._filters

        if not filters:
            yield connection
            return

        for filter_ in filters:
            if not filter_.can_show_connection(connection):
                continue

            for yielded in filter_.intercept_connection(connection):
                yield yielded
    #
    # def expand_node_connections(self, node, inputs=True, outputs=True):
    #     """Redirect any connection expansion to the soure model."""
    #     for connection in super(GraphFilterProxyModel, self).expand_node_connections(node, inputs=inputs, outputs=outputs):
    #         for yielded in self.intercept_connection(connection):
    #             yield yielded
    #     # self._model.expand_node_connections(node, inputs=inputs, outputs=outputs)
    #
    # def expand_port_input_connections(self, port):
    #     """Redirect any connection expansion to the soure model."""
    #     for connection in super(GraphFilterProxyModel, self).expand_port_input_connections(port):
    #         for yielded in self.intercept_connection(connection):
    #             yield yielded
    #     # self._model.expand_port_input_connections(port)
    #
    # def expand_port_output_connections(self, port):
    #     """Redirect any connection expansion to the soure model."""
    #     for connection in super(GraphFilterProxyModel, self).expand_port_output_connections(port):
    #         for yielded in self.intercept_connection(connection):
    #             yield yielded
    #     # self._model.expand_port_output_connections(port)
    #
