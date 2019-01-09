import logging
from collections import defaultdict

from omtk.nodegraph.adaptors.node.component import NodeGraphComponentNodeAdaptor
from omtk.nodegraph.cache import NodeCache
from omtk.nodegraph.models._deprecated import node_component
from omtk.nodegraph.models.node import NodeModel
from omtk.nodegraph.signal import Signal
from omtk.vendor.enum34 import Enum

from . import graph_proxy_model

log = logging.getLogger(__name__)


class SubgraphProxyModel(graph_proxy_model.NodeGraphGraphProxyModel):
    """
    Wrap the interface of a ``GraphModel`` instance to modify what the user (and controller) see (and interact via signals).

    :param GraphModel model: The graph that we wish to filter.
    :param NodeModel level: The initial level.
    """
    onLevelChanged = Signal(object)

    def __init__(self, registry, model=None, level=None):
        super(SubgraphProxyModel, self).__init__(registry, model=model)

        self._level = None
        if level:
            self.set_level(level)

        self._bound_inn_before = None
        self._bound_inn_after = None
        self._bound_out_before = None
        self._bound_out_after = None

        self.node_by_component = NodeCache()

        # Used to keep reference of invisible children
        self._child_by_component = defaultdict(set)
        self._component_by_child = {}

        self._nodes_by_level = defaultdict(set)

        self._component_by_level = {}
        # self.onNodeRemoved.connect(self.on_node_removed)

    def iter_nodes(self):
        # Hack: Prevent the same node from being yielded twice.
        # TODO: Put somewhere else?
        known = set()
        for yielded in super(SubgraphProxyModel, self).iter_nodes():
            if yielded in known:
                continue
            known.add(yielded)

            if yielded == self._bound_inn_before:
                yield self._bound_inn_after
                continue

            if yielded == self._bound_out_before:
                yield self._bound_out_after
                continue

            yield yielded

    def hold_nodes(self):
        level = self.get_level()
        nodes = self.get_model().get_nodes()
        self._nodes_by_level[level] = nodes

    def fetch_nodes(self, expand=True):
        level = self.get_level()
        nodes = self._nodes_by_level.get(level)

        if not nodes:
            return

        # If the new filter don't like previous nodes, don't add them.
        # todo: is there a more stable way of retreiving this?
        # nodes = [node for node in nodes if not self._filter or self._filter.can_show_node(node)]

        # Fetch nodes
        for node in nodes:
            self.add_node(node, emit=True)

        # Fetch nodes status
        if expand:
            for node in nodes:
                self.expand_node_ports(node)

                self.expand_node_connections(node)

                # todo: remember visible ports and connections?

    def get_level(self):
        """
        Retrieve the current visibile level.
        Example of values are:
        - "component1"
        - "component1:component2"

        :return: The current level as a str
        :rtype: str
        """
        return self._level or ""

    def can_set_level_to(self, node):
        if node is None:
            return True

        # We need at least one children to be able to jump into something.
        # todo: is that always true? what happen to empty compound?
        if not node.get_children():
            log.debug("Cannot enter into {0} because there's no children!".format(node))
            return False

        # We don't want to enter the same model twice.
        if self._level == node:
            return False

        # # Currently since we can have 3 node model for a single compound (one model when seen from outside and two
        # # model when seen from the inside, the inn and the out), we need a better way to distinguish them.
        # # For now we'll use a monkey-patched data from libSerialization, however we need a better approach.
        # meta_data = node.get_metadata()
        # if hasattr(self._current_level_data, '_network') and hasattr(meta_data, '_network'):
        #     current_network = self._current_level_data._network
        #     new_network = meta_data._network
        #     if current_network == new_network:
        #         return False

        return True

    def set_level(self, level):
        """
        :param str level: The new level in the form of a namespace (ex: "component1")
        """
        assert (isinstance(level, str))

        self._level = level

        if not level:
            return

        registry = self.registry
        session = registry.session

        # Pre-allocate bounds on Component levels
        node_inn_dagpath = "{}:inn".format(level)
        node_inn = session.get_node_by_name(node_inn_dagpath)
        node_inn_model = registry.get_node(node_inn)
        node_inn_bound = node_component.NodeGraphComponentInnBoundModel(registry, node_inn_model)

        self._bound_inn_before = node_inn_model
        self._bound_inn_after = node_inn_bound

        node_out_dagpath = "{}:out".format(level)
        node_out = session.get_node_by_name(node_out_dagpath)
        node_out_model = registry.get_node(node_out)
        node_out_bound = node_component.NodeGraphComponentOutBoundModel(registry, node_out_model)

        self._bound_out_before = node_out_model
        self._bound_out_after = node_out_bound

    def add_node(self, node, emit=True):
        # If we add a component, we want to keep trace of it's children.
        # This will allow us to properly react to Maya delete callbacks and remove the component
        # if it ever become empty.
        if isinstance(node, node_component.NodeGraphComponentModel):
            children = node.get_children()
            self._child_by_component[node] = children
            for child in children:
                self._component_by_child[child] = node

        super(SubgraphProxyModel, self).add_node(node, emit=emit)

    # todo: move upper?
    def expand_node_ports(self, node):
        # type: (NodeModel) -> None
        """
        Show all available attributes for a PyFlowgraph Node.
        Add it in the pool if it didn't previously exist.
        :return:
        """
        for node in self.intercept_node(node):
            for port_model in sorted(self.iter_node_ports(node)):
                self.add_port(port_model, emit=True)

    # todo: move upper?
    def expand_node_connections(self, node, inputs=True, outputs=True):
        # type: (NodeModel, bool, bool) -> None
        for node in self.intercept_node(node):
            for connection in self.iter_node_connections(node, inputs=inputs, outputs=outputs):
                self._model.add_connection(connection)

    def is_port_input(self, port):
        node = port.get_parent()

        # If the node is an input bound, we don't want to show the inputs.
        if node == self._cur_level_bound_inn:
            return False

        return super(SubgraphProxyModel, self).is_port_input(port)

    def is_port_output(self, port):
        node = port.get_parent()

        # If the node is an output bound, we don't want to show the outputs.
        if node == self._cur_level_bound_out:
            return False

        return super(SubgraphProxyModel, self).is_port_output(port)

    def can_show_connection(self, connection):
        return True

    def _is_valid_level(self, level):
        """
        :param REGISTRY_DEFAULT:
        :param level:
        :return:
        """
        fn_exist = self.registry.session.node_exist
        node_in_dagpath = "{}:inn".format(level)
        node_out_dagpath = "{}:out".format(level)
        return fn_exist(node_in_dagpath) and fn_exist(node_out_dagpath)

    def _get_nearest_level(self, parent, child):
        """
        Given a parent and child level, move down from the parent to the child
        and return the first valid level encountered.
        :param str parent: The parent level.
        :param str child: The child level.
        """
        from omtk.libs import libNamespaces
        assert (libNamespaces.is_child_of(child, parent))

        guess = child
        guesses = []
        while guess and guess != parent:
            guesses.append(guess)
            guess = libNamespaces.get_parent(guess)
        guesses = reversed(guesses)

        for guess in guesses:
            if self._is_valid_level(guess):
                return guess

    def _get_node_level(self, node):
        """
        Resolve level associated to a graph node.

        :param node: The level
        :type node: NodeModel or None
        :return:
        :rtype: GraphModel or None
        """
        from omtk.libs import libNamespaces
        if node is None:
            return None

        dagpath = node.get_name()
        namespace = libNamespaces.get_parent(dagpath)

        def _routine(n):
            """

            :param str n: A namespace
            :return:
            """
            if not n:
                return None
            if self._is_valid_level(n):
                return n
            else:
                parent = libNamespaces.get_parent(n)
                return _routine(parent)

        return _routine(namespace)

    def _get_component_by_level(self, level):
        try:
            return self._component_by_level[level]
        except LookupError:

            from omtk.component import Component
            cls = Component
            inst = cls(level)
            self._component_by_level[level] = inst
            return inst

    def _registry_component(self, component, level):
        self._component_by_level[level] = component

    # still used?
    def intercept_node(self, node):
        """
        Allow the filter to alter the output of the graph.

        The thinking is simple:
        - A node inside the same level is displayed.
        - A node inside a compound in the same level will display the compound.
        - A node inside a compound outside of the same level will not be displayed.

        :param NodeModel node: The intercepted node
        :return: A node generator
        :rtype: Generator[NodeModel]
        """
        from omtk.libs import libNamespaces
        registry = node._registry
        level = self.get_level()

        # If the node is in the current level, display it.
        node_level = self._get_node_level(node)
        if node_level == level:
            yield node
            return

        # If the node outside of the current level, ignore it.
        if not libNamespaces.is_child_of(node_level, level):
            return

        # If the node is inside the current level, display it as a compound.
        # Note that there can be hold in compound since encapsulation is suggested.
        # For example let's say we are at the root level with the following graph:
        # - "component1:component2:inn"
        # - "component1:component2:out"
        # This will display "component1:component2" and not "component1".
        actual_level = self._get_nearest_level(level, node_level)
        component = self._get_component_by_level(actual_level)
        inst = self.get_node_from_component(component)
        yield inst
        return

    def get_node_from_component(self, component):
        # Memoize
        try:
            node = self.node_by_component.get(component)

        # Fetch and register if necessary
        except LookupError:
            node = self._get_node_from_component(component)
            self.node_by_component.register(component, node)
        return node

    def _get_node_from_component(self, component):
        impl = NodeGraphComponentNodeAdaptor(component)
        node = NodeModel(self.registry, impl)
        return node

    def intercept_port(self, port):
        from omtk.libs import libNamespaces

        # Ignore any port that is not on the current level
        node = port.get_parent()
        node_level = self._get_node_level(node)
        level = self.get_level()
        if not libNamespaces.is_child_of(node_level, level):
            return

        yield port

    def iter_node_ports(self, node):
        for port in super(SubgraphProxyModel, self).iter_node_ports(node):
            for yielded in self.intercept_port(port):
                yield yielded

    def _iter_node_output_connections(self, node_model):
        for port in node_model.get_connected_output_ports(self):
            if not self.can_show_port(port):
                continue

            for connection_model in self.iter_port_output_connections(port):
                node_model_dst = connection_model.get_destination().get_parent()
                for yielded in self.intercept_connection(connection_model, port):
                    yield yielded

    def _iter_node_input_connections(self, node_model):
        for port_model in node_model.get_connected_input_ports():
            if not self.can_show_port(port_model):
                continue

            for connection_model in self.iter_port_input_connections(port_model):
                node_model_src = connection_model.get_source().get_parent()

                for yielded in self.intercept_connection(connection_model, port_model):
                    yield yielded

    def iter_port_input_connections(self, port):
        """
        Control what output connection models are exposed for the provided port model.
        :param omtk.nodegraph.PortModel port: The source port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as source.
        :rtype: List[omtk.nodegraph.PortModel]
        """
        for connection in port.get_input_connections():
            if self.can_show_connection(connection):
                for yielded in self.intercept_connection(connection):
                    yield yielded

    def iter_port_output_connections(self, port):
        """
        Control what output connection models are exposed for the provided port model.
        :param omtk.nodegraph.PortModel port: The source port model to use while resolving the connection models.
        :return: A list of connection models using the provided port model as source.
        :rtype: List[omtk.nodegraph.PortModel]
        """
        for connection in port.get_output_connections():
            if self.can_show_connection(connection):
                for yielded in self.intercept_connection(connection):
                    yield yielded

    def get_connection_parent(self, connection):
        """
        By default, a connection parent is either the same as it's input attribute or it's output attribute.
        This difference is important with Compound nodes.
        :param omtk.nodegraph.ConnectionModel: The connection to inspect
        :return: omtk.nodegraph.PortModel
        """
        port_src = connection.get_source()
        port_dst = connection.get_destination()
        node_src = port_src.get_parent()
        node_dst = port_dst.get_parent()

        # If the connection if from a component, this is an external connection.
        if isinstance(node_src, node_component.NodeGraphComponentModel):
            return node_src.get_parent()
        if isinstance(node_dst, node_component.NodeGraphComponentModel):
            return node_dst.get_parent()

        pynode_src = node_src.get_metadata()
        pynode_dst = node_dst.get_metadata()

        class ConnectionKind(Enum):
            normal = 1
            normal_to_compound_inn = 2  # src (node is outside the compound)
            normal_to_compound_out = 3  # dst (node is inside the compound)
            compound_inn_to_normal = 4  # src (node is inside the compound)
            compound_out_to_normal = 5  # dst (node is outside the compound)
            compound_inn_to_compound_inn = 6  # dst (destination is inside source)
            compound_inn_to_compound_out = 7  # any (source and destination are inside the same compound)
            compound_out_to_compound_inn = 8  # any (source and destination are inside the same compound)
            compound_out_to_compound_out = 9  # src (source is inside destination)

        def get_connection_kind():
            """
            The possibilities are:
            - Connection from a component out to a component on the same level.
            - Connection from a component inn to a component inn inside this same component.
            - Connection from a component out to a parent component out.
            """
            from omtk.libs import libComponents
            src_role = libComponents.get_metanetwork_role(pynode_src)
            dst_role = libComponents.get_metanetwork_role(pynode_dst)

            src_is_compound_bound = src_role != libComponents.ComponentMetanetworkRole.NoRole
            dst_is_compound_bound = dst_role != libComponents.ComponentMetanetworkRole.NoRole
            if src_is_compound_bound and dst_is_compound_bound:
                src_is_inn = src_role == libComponents.ComponentMetanetworkRole.Inn
                dst_is_inn = dst_role == libComponents.ComponentMetanetworkRole.Out
                # Connection from a component inn to another component inn.
                # In that case the destination component is a child of the source component.
                if src_is_inn and dst_is_inn:
                    return ConnectionKind.compound_inn_to_compound_inn
                # Connection from a component inn to a component out.
                # In that case the connection is from the same component (or there's something really wrong in the scene).
                # In that case both src and dst are in the same space.
                elif src_is_inn and not dst_is_inn:
                    return ConnectionKind.compound_inn_to_compound_out
                # Connection from a component out to a component inn
                # In that case the source component is a child of the destination component.
                elif not src_is_inn and dst_is_inn:
                    return ConnectionKind.compound_out_to_compound_inn
                # Connection from a component out to a component out
                # In that case the source component is a child of the destination component.
                else:
                    return ConnectionKind.compound_out_to_compound_out

            elif src_is_compound_bound:  # exiting a compounds
                src_is_inn = src_role == libComponents.ComponentMetanetworkRole.Inn
                if src_is_inn:
                    return ConnectionKind.compound_inn_to_normal
                else:
                    return ConnectionKind.compound_out_to_normal
            elif dst_is_compound_bound:  # entering a compound
                dst_is_inn = dst_role == libComponents.ComponentMetanetworkRole.Inn
                if dst_is_inn:
                    return ConnectionKind.normal_to_compound_inn
                else:
                    return ConnectionKind.normal_to_compound_out

        def get_connection_node_model():
            """
            Define if we should use the source or destination node model to fetch the parent.
            normal_to_compound_inn = 2  # src (node is outside the compound)
            normal_to_compound_out = 3  # dst (node is inside the compound)
            compound_inn_to_normal = 4  # src (node is inside the compound)
            compound_out_to_normal = 5  # dst (node is outside the compound)
            compound_inn_to_compound_inn = 6  # dst (destination is inside source)
            compound_inn_to_compound_out = 7  # any (source and destination are inside the same compound)
            compound_out_to_compound_inn = 8  # any (source and destination are inside the same compound)
            compound_out_to_compound_out = 9  # src (source is inside destination)
            """
            connection_kind = get_connection_kind()
            if connection_kind in (
                    ConnectionKind.compound_inn_to_normal,
                    ConnectionKind.compound_inn_to_compound_inn,
                    ConnectionKind.compound_out_to_compound_out,
                    ConnectionKind.compound_out_to_normal,
            ):
                return node_dst
            else:
                return node_src

        node_model = get_connection_node_model()
        return node_model

    # --- Events ---

    # def on_node_removed(self, node):
    #     """
    #     Ensure that if the user remove anything under a Component we remove the component from the model.
    #     """
    #     print 'proxymodel', str(node)
    #     for node in self.intercept_node(node):
    #         if isinstance(node, node_component.NodeGraphComponentModel):
    #             print len(node.get_children())
    #             print node.get_children()
