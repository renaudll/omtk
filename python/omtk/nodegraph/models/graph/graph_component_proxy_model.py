import logging
from collections import defaultdict

import pymel.core as pymel
from omtk.core import manager
from omtk.nodegraph.models.node import node_component
from omtk.vendor.enum34 import Enum
from omtk.vendor.Qt import QtCore

from . import graph_proxy_model

log = logging.getLogger(__name__)

if False:
    from typing import List, Generator
    from omtk.nodegraph.models import NodeModel


class GraphComponentProxyFilterModel(graph_proxy_model.NodeGraphGraphProxyModel):
    """
    Wrap the interface of a ``GraphModel`` instance to modify what the user (and controller) see (and interact via signals).
    """
    onLevelChanged = QtCore.Signal(object)

    def __init__(self, model=None, level=None):
        super(GraphComponentProxyFilterModel, self).__init__(model=model)

        self._level = None
        if level:
            self.set_level(level)

        self._cur_level_bound_inn = None
        self._cur_level_bound_out = None
        self._cur_level_children = None
        self._bound_inn_dirty = False
        self._bound_out_dirty = False
        self._children_dirty = False
        self._need_refresh = False

        # Used to keep reference of invisible children
        self._child_by_component = defaultdict(set)
        self._component_by_child = {}

        self._nodes_by_level = defaultdict(set)
        # self.onNodeRemoved.connect(self.on_node_removed)

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
        # type: () -> NodeModel
        return self._level

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
        # type: (NodeModel | None) -> None
        # assert(isinstance(level, node_component.NodeGraphComponentModel))

        self.onAboutToBeReset.emit()  # hack
        self.hold_nodes()

        self._level = level
        self.reset()  # is this the right call? do we need to define a clear?

        if level is None:  # root level
            self._cur_level_bound_inn = None
            self._cur_level_bound_out = None
            self._cur_level_children = []
        else:
            self._bound_inn_dirty = False
            self._bound_out_dirty = False

            registry = level._registry

            # Pre-allocate bounds on Component levels
            if isinstance(level, node_component.NodeGraphComponentModel):
                c = level.get_metadata()

                c_model = registry.get_node(c)

                new_nodes = []

                if c.grp_inn:
                    g = node_component.NodeGraphComponentInnBoundModel(registry, c.grp_inn, c_model)
                    self._cur_level_bound_inn = g
                    new_nodes.append(g)

                if c.grp_out:
                    g = node_component.NodeGraphComponentOutBoundModel(registry, c.grp_out, c_model)
                    self._cur_level_bound_out = g
                    new_nodes.append(g)

                self._cur_level_children = [registry.get_node(child) for child in c.get_children()]

                new_nodes.extend(self._cur_level_children)

                for node in new_nodes:
                    self.add_node(node)

                for node in new_nodes:
                    self.expand_node_ports(node)

                for node in new_nodes:
                    self.expand_node_connections(node)

                # for child in self._cur_level_children:
                #     self.add_node_callbacks(child)
                #     self.expand_node_ports(child)
                #     self.expand_node_connections(child)

                self._children_dirty = False
                self._need_refresh = True

        # self.reset()  # we need to refresh everything
        self.fetch_nodes()
        self.onLevelChanged.emit(level)

    def add_node(self, node, emit=True):
        # If we add a component, we want to keep trace of it's children.
        # This will allow us to properly react to Maya delete callbacks and remove the component
        # if it ever become empty.
        if isinstance(node, node_component.NodeGraphComponentModel):
            children = node.get_children()
            self._child_by_component[node] = children
            for child in children:
                self._component_by_child[child] = node

        super(GraphComponentProxyFilterModel, self).add_node(node, emit=emit)

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

    def can_show_node(self, node):
        # type: (NodeModel) -> bool
        return node.get_parent() == self._level

    def can_show_port(self, port):
        node = port.get_parent()
        if isinstance(node, node_component.NodeGraphComponentBoundBaseModel):
            if not port.is_user_defined():
                return False
        return super(GraphComponentProxyFilterModel, self).can_show_port(port)

    def is_port_input(self, port):
        node = port.get_parent()

        # If the node is an input bound, we don't want to show the inputs.
        if node == self._cur_level_bound_inn:
            return False

        return super(GraphComponentProxyFilterModel, self).is_port_input(port)

    def is_port_output(self, port):
        node = port.get_parent()

        # If the node is an output bound, we don't want to show the outputs.
        if node == self._cur_level_bound_out:
            return False

        return super(GraphComponentProxyFilterModel, self).is_port_output(port)

    def can_show_connection(self, connection):
        return True

    # still used?
    def intercept_node(self, node):
        # type: (NodeModel) -> Generator[NodeModel]
        from omtk.nodegraph.models.node import node_component

        # Handle compound bound.
        # If we receive a bound node, only yield it if it's part of the current level.
        if isinstance(node, node_component.NodeGraphComponentBoundBaseModel):
            component_model = node.get_parent()
            if self._level == component_model:
                yield node
            return

        # Handle compound.
        # We only show compound nodes if the compound is not the current level.
        # NOT TRUE, we want to display the compound if is a children of another level!
        # todo: move to node?
        def is_child_of(node_, parent):
            while node_:
                node_ = node_.get_parent()
                if node_ == parent:
                    return True
            return False

        if isinstance(node, node_component.NodeGraphComponentModel):
            # If we are not in a subgraph, accept only nodes that have no parent.
            if self._level is None:
                if node.get_parent() is None:
                    yield node
            # If we are in a subgraph, accept any component that is child of the current subgraph.
            else:
                if is_child_of(node, self._level):
                    yield node
                else:
                    print("Hiding {0} since it is not a child of {1}".format(node, self._level))
            return

        # Is the node inside the current level?
        parent = node.get_parent()
        if parent == self._level:
            yield node
        # Is the node inside a compound that is inside the current level?
        elif isinstance(parent, node_component.NodeGraphComponentModel):
            if parent.get_parent() == self._level:
                yield parent

    def intercept_port(self, port):
        registry = port._registry
        s = manager.get_session()
        node = port.get_parent()
        pynode = node.get_metadata()
        component_data = s.get_component_from_obj(pynode) if isinstance(pynode, pymel.PyNode) else None

        if component_data:
            component = registry.get_node(component_data)
            if component != self._level:
                pass

        yield port

    def intercept_connection(self, connection):
        from omtk import component

        def _get_port_by_name(node, name):
            for port in node.iter_ports():
                if port.get_name() == name:
                    return port

        for connection in self.get_model().intercept_connection(connection):
            # If we encounter a connection to an hub node and we are NOT in the compound, we want to replace it with
            # a conenction to the compound itself.
            registry = connection._registry
            s = manager.get_session()

            need_swap = False
            port_src = connection.get_source()
            port_dst = connection.get_destination()
            node_src = port_src.get_parent()
            node_dst = port_dst.get_parent()

            node_src_data = node_src.get_metadata()
            node_dst_data = node_dst.get_metadata()

            if isinstance(node_src_data, component.Component):
                # If the source is the current compound, remap the connection to the hub inn.
                if self._level and self._level.get_metadata() == node_src_data:
                    # Ignore internal connection
                    if node_dst.get_parent() != self._level:
                        return
                    attr = node_src_data.grp_inn.attr(port_src.get_name())
                    port_src = registry.get_port(attr)
                    need_swap = True

            elif isinstance(node_src_data, pymel.PyNode):
                # If the source port from an input hub?
                # If so, what component is the input hub associated with?
                # If it's the current component, do nothing, let's show the hub.
                # If it's a component UNDER the current component, show the component.
                # Otherwise show nothing.

                # If the source is a component metadata, we don't want to display it.
                c = s.get_component_from_metadata(node_src_data)
                if c:
                    return

                c = s.get_component_from_input_hub(node_src_data) or \
                    s.get_component_from_output_hub(node_src_data)
                if c:
                    c_model = registry.get_node(c)
                    # If the source if from the current component input hub, do nothing.
                    if self._level == c_model:
                        pass
                    # If the source if from a component child of the current component, show the component instead of the hub.
                    elif c_model.get_parent() == self._level:
                        port_src = _get_port_by_name(c_model, port_src.get_name())
                        need_swap = True
                    # This should not happen, the intercept_node should have done the job already.
                    # Just in case we'll shot a warning.
                    else:
                        log.warning("{0} source is not visible in the current context. Hiding connection.".format(connection))
                        return

            if isinstance(node_dst_data, component.Component):
                # If the destination is the current compound, remap the connection to the hub out.
                if self._level and self._level.get_metadata() == node_dst_data:
                    # Ignore external connection
                    if node_src.get_parent() != self._level:
                        return
                    attr = node_dst_data.grp_out.attr(port_dst.get_name())
                    port_dst = registry.get_port(attr)
                    need_swap = True

            # If the connection from an input hub?
            elif isinstance(node_dst_data, pymel.PyNode):
                # If the destination port from an output hub?
                # If so, what component is the output hub associated with?
                # If it's the current component, do nothing, let's show the hub.
                # If it's a component UNDER the current component, show the component.
                # Otherwise show nothing.

                # If the destination is from a component metadata, we don't want to display it.
                c = s.get_component_from_metadata(node_dst_data)
                if c:
                    return

                c = s.get_component_from_input_hub(node_dst_data) or \
                    s.get_component_from_output_hub(node_dst_data)
                if c:
                    c_model = registry.get_node(c)
                    # If the source if from the current component input hub, do nothing.
                    if self._level == c_model:
                        pass
                    # If the source if from a component child of the current component, show the component instead of the hub.
                    elif c_model.get_parent() == self._level:
                        port_dst = _get_port_by_name(c_model, port_dst.get_name())
                        need_swap = True
                    # This should not happen, the intercept_node should have done the job already.
                    # Just in case we'll shot a warning.
                    else:
                        log.warning("{0} destination is not visible in the current context. Hiding connection.".format(connection))
                        return

            if need_swap:
                # Hack: Ignore invalid ports for now...
                # todo: fix this
                if port_src is None or port_dst is None:
                    log.warning("Received invalid data when intercepting connection. Ignoring. {0} {1}".format(port_src, port_dst))
                    yield connection
                else:
                    yield registry.get_connection(port_src, port_dst)
            else:
                yield connection

    def iter_node_ports(self, node):
        for port in super(GraphComponentProxyFilterModel, self).iter_node_ports(node):
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
