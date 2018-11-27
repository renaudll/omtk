from omtk.nodegraph.models.port import PortModel


class NodeGraphEntityAttributePortModel(PortModel):
    """Define an attribute bound to an EntityPort instance."""

    def __init__(self, registry, node, attr_def):
        name = attr_def.name
        super(NodeGraphEntityAttributePortModel, self).__init__(registry, node, name)
        self._impl = omtk.nodegraph.models.port.port_adaptor_entity.EntityAttributeNodeGraphPortImpl(
            attr_def)