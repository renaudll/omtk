# for type hinting only
if False:
    from omtk.qt_widgets.nodegraph.models.port.port_base import NodeGraphPortModel


class NodeGraphConnectionModel(object):
    def __init__(self, registry, attr_src, attr_dst):
        self._registry = registry
        self._attr_src = attr_src
        self._attr_dst = attr_dst

    def __repr__(self):
        return '<NodeGraphConnectionModel {0}.{1} to {2}.{3}>'.format(
            self._attr_src.get_parent(),
            self._attr_src.get_name(),
            self._attr_dst.get_parent(),
            self._attr_dst.get_name()
        )

    def __hash__(self):
        return hash(self._attr_src) ^ hash(self._attr_dst)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other

    def get_source(self):
        # type: () -> NodeGraphPortModel
        return self._attr_src

    def get_destination(self):
        # type: () -> NodeGraphPortModel
        return self._attr_dst
