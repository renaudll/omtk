from .graph_model_port import GraphPortModel
from .graph_model_node import GraphNodeModel


class GraphLinkModel(object):
    def __init__(self, registry, attr_src, attr_dst):
        self._registry = registry
        self._attr_src = attr_src
        self._attr_dst = attr_dst

    def __repr__(self):
        return '<GraphLinkModel {0}.{1} to {2}.{3}>'.format(
            self._attr_src.get_parent().get_name(),
            self._attr_src.get_name(),
            self._attr_dst.get_parent().get_name(),
            self._attr_dst.get_name()
        )

    def get_parent(self):
        # type: () -> GraphNodeModel
        """
        By default, a connection parent is either the same as it's input attribute or it's output attribute.
        This difference is important with Compound nodes.
        :return:
        """
        return self._attr_src.get_parent()

    def get_source(self):
        # type: () -> GraphPortModel
        return self._attr_src

    def get_destination(self):
        # type: () -> GraphPortModel
        return self._attr_dst

    def __hash__(self):
        return hash(self._attr_src) ^ hash(self._attr_dst)
