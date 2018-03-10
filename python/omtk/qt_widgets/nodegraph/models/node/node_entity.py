import logging

from omtk import decorators
from . import node_base

log = logging.getLogger('omtk')


class NodeGraphEntityModel(node_base.NodeGraphNodeModel):
    """
    Define the data model for a Node representing a Component.
    A Component is a special OMTK datatypes that consist of an input network, an output network and one or multiple
    maya nodes sandwitched in between.
    """

    def __init__(self, registry, entity):
        name = entity.get_name()
        super(NodeGraphEntityModel, self).__init__(registry, name)
        self._entity = entity

    def get_metadata(self):
        # type: () -> Component
        return self._entity

    def get_ports_metadata(self):
        # Used to invalidate cache
        return list(self._entity.iter_attributes())

    @decorators.memoized_instancemethod
    def get_ports(self):
        # type: () -> List[NodeGraphPortModel]
        result = set()

        for attr_def in self.get_ports_metadata():
            # todo: use a factory?
            log.debug('{0}'.format(attr_def))
            inst = self._registry.get_port_model_from_value(attr_def)

            # inst._node = self  # hack currently compound attribute won't point to the compound object...


            # inst = NodeGraphEntityPymelAttributePortModel(self._registry, self, attr_def)
            # self._registry._register_attribute(inst)
            result.add(inst)

        return result

    def _get_widget_label(self):
        result = self._name
        version_major, version_minor, version_patch = self._entity.get_version()
        if version_major is not None and version_minor is not None and version_patch is not None:  # todo: more eleguant
            result += 'v{0}.{1}.{2}'.format(version_major, version_minor, version_patch)

        return result