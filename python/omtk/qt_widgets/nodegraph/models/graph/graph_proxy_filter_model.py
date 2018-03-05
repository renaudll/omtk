from omtk import decorators
from omtk.qt_widgets.nodegraph.models.graph.graph_proxy_model import NodeGraphGraphProxyModel
from pymel import core as pymel

if False:
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

    def reset(self):
        return self.get_model().reset()

    def set_filter(self, filter, expand=True):
        self._filter = filter

        nodes = self.get_nodes()[:]

        self.reset()

        # Restore the visible nodes
        for node in nodes:
            self.add_node(node, emit_signal=False)

            if expand:
                for port in self.iter_ports():
                    self.add_port(port, emit_signal=False)

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

    def collapse_node_attributes(self, node_model):
        # There's no API method to remove a port in PyFlowgraph.
        # For now, we'll just re-created the node.
        # node_widget = self.get_node_widget(node_model)
        # self._view.removeNode(node_widget)
        # self.get_node_widget.cache[node_model]  # clear cache
        # node_widget = self.get_node_widget(node_model)
        # self._view.addNode(node_widget)
        raise NotImplementedError

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

        for connection in model.get_output_connections():

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

    def get_node_ports(self, node):
        # type: (NodeGraphNodeModel) -> List[NodeGraphPortModel]
        return self.get_model().get_node_ports(node)
