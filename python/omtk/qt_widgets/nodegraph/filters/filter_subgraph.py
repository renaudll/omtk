import pymel.core as pymel

from omtk import decorators
from omtk.core import session
from omtk.qt_widgets.nodegraph import nodegraph_filter
from omtk.qt_widgets.nodegraph.models.node import node_component

if False:
    from typing import Generator
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel


class NodeGraphSubgraphFilter(nodegraph_filter.NodeGraphFilter):
    def __init__(self, level=None):
        super(NodeGraphSubgraphFilter, self).__init__()
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

    def get_level(self):
        # type: () -> NodeGraphNodeModel
        return self._level

    def set_level(self, level):
        # type: (NodeGraphNodeModel) -> None
        # assert(isinstance(level, node_component.NodeGraphComponentModel))

        if level is None:  # root level
            self._cur_level_bound_inn = None
            self._cur_level_bound_out = None
        else:
            self._bound_inn_dirty = False
            self._bound_out_dirty = False


            registry = level._registry

            # Pre-allocate bounds on Component levels
            if isinstance(level, node_component.NodeGraphComponentModel):
                c = level.get_metadata()

                if c.grp_inn:
                    g = node_component.NodeGraphComponentInnBoundModel(registry, c.grp_inn, c)
                    self._cur_level_bound_inn = g

                if c.grp_out:
                    g = node_component.NodeGraphComponentOutBoundModel(registry, c.grp_out, c)
                    self._cur_level_bound_out = g

                self._cur_level_children = [registry.get_node_from_value(child) for child in c.get_children()]
                self._children_dirty = False
                self._need_refresh = True

        self._level = level

    # --- Implementation

    # def can_show_node(self, node):
    #     # type: (NodeGraphNodeModel) -> bool
    #     """
    #     Determine if a node can be shown.
    #     If we are into a subgraph, we don't want to show a node which parent is not the same as the current level.
    #     """
    #     parent = node.get_parent()
    #     return parent == self._level

    def can_show_port(self, port):
        node = port.get_parent()
        if isinstance(node, node_component.NodeGraphComponentBoundBaseModel):
            if not port.is_user_defined():
                return False
        super(NodeGraphSubgraphFilter, self).can_show_port(port)

    def can_show_connection(self, connection):
        # Get the node associated with the connection
        # Even if a connection is between two nodes, only one can have ownership.
        node_model = connection.get_parent()

        if not self.can_show_node(node_model):
            return False

        return super(NodeGraphSubgraphFilter, self).can_show_connection(node_model)

    def intercept_node(self, node):
        # type: (NodeGraphNodeModel) -> Generator[NodeGraphNodeModel]
        s = session.get_session()
        registry = node._registry

        pynode = node.get_metadata()
        c = s.get_component_from_obj(pynode) if isinstance(pynode, pymel.PyNode) else None

        # If we just entered a level, yield the bound
        if self._level and self._need_refresh:
            self._need_refresh = False
            if self._cur_level_bound_inn:
                yield self._cur_level_bound_inn

            if self._cur_level_bound_out:
                yield self._cur_level_bound_out

            for child in self._cur_level_children:
                yield child

        if c:
            # If we are inside the component, should it's input and output hub.
            # Otherwise show only the component.
            if self._level and c == self._level.get_metadata():
               pass
            else:
                yield registry.get_node_from_value(c)
            return
        else:
            # If the object parent is NOT a compound and we are NOT at root level, the object is hidden.
            # We decided to hide the object here instead of in can_show_node in case the user
            if self._level:
                print("Hiding {}".format(node))
                return

        for yielded in super(NodeGraphSubgraphFilter, self).intercept_node(node):
            yield yielded
        return

