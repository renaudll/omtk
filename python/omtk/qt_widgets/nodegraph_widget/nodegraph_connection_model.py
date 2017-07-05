from .nodegraph_port_model import NodeGraphPortModel

# for type hinting only
if False:
    from .nodegraph_node_model_base import NodeGraphNodeModel


class NodeGraphConnectionModel(object):
    def __init__(self, registry, name, attr_src, attr_dst):
        self._registry = registry
        self._attr_src = attr_src
        self._attr_dst = attr_dst

    def __repr__(self):
        return '<NodeGraphConnectionModel {0}.{1} to {2}.{3}>'.format(
            self._attr_src.get_parent().get_name(),
            self._attr_src.get_name(),
            self._attr_dst.get_parent().get_name(),
            self._attr_dst.get_name()
        )

    def get_parent(self):
        # type: () -> NodeGraphNodeModel
        """
        By default, a connection parent is either the same as it's input attribute or it's output attribute.
        This difference is important with Compound nodes.
        :return:
        """
        return self._attr_src.get_parent()

    def get_source(self):
        # type: () -> NodeGraphPortModel
        return self._attr_src

    def get_destination(self):
        # type: () -> NodeGraphPortModel
        return self._attr_dst

    def __hash__(self):
        return hash(self._attr_src) ^ hash(self._attr_dst)
