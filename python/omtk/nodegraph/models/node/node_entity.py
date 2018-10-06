import logging

from omtk import decorators
from . import node_base

log = logging.getLogger(__name__)


class NodeGraphEntityModel(node_base.NodeModel):
    """
    Define the data model for a Node representing a Component.
    A Component is a special OMTK datatypes that consist of an input network, an output network and one or multiple
    maya nodes sandwitched in between.
    """

    def __init__(self, registry, entity):
        self._entity = entity
        name = entity.get_name()
        super(NodeGraphEntityModel, self).__init__(registry, name)

    def __hash__(self):
        return hash(self._entity)

    def get_metadata(self):
        # type: () -> Component
        return self._entity

    def get_ports_metadata(self):
        # Used to invalidate cache
        return list(self._entity.iter_attributes())

    def scan_ports(self):
        # type: () -> List[PortModel]
        for attr_def in self.get_ports_metadata():
            yield self._registry.get_port(attr_def)

    def _get_widget_label(self):
        result = self._name
        version_major, version_minor, version_patch = self._entity.get_version()
        if version_major is not None and version_minor is not None and version_patch is not None:  # todo: more eleguant
            result += 'v{0}.{1}.{2}'.format(version_major, version_minor, version_patch)

        return result