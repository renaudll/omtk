import logging

import omtk.nodegraph.models.port
from omtk.nodegraph.models.port import port_base as port_model
from omtk.nodegraph.models import connection as connection_model
from omtk.nodegraph.models._deprecated import node_dg

log = logging.getLogger(__name__)


class DagNodeParentPortModel(omtk.nodegraph.models.port.PortModel):
    # __metaclass__ = abc.ABCMeta

    def __init__(self, registry, parent):
        super(DagNodeParentPortModel, self).__init__(registry, parent, 'hierarchy')

    def is_interesting(self):
        # A dag node is always interesting.
        return True

    def is_readable(self):
        return True

    def is_writable(self):
        return True

    def get_metadata(self):
        return self._node.get_metadata()

    def get_metatype(self):
        from omtk.factories import factory_datatypes
        return factory_datatypes.AttributeType.AttributeCompound

    def get_output_connections(self):
        registry = self._registry
        result = set()
        children = registry.get_children(self._node)
        for child in children:
            model_dst_port = DagNodeParentPortModel(self._registry, child)
            model_connection = connection_model.ConnectionModel(self._registry, self, model_dst_port)
            result.add(model_connection)
        return result

    def get_input_connections(self):
        registry = self._registry
        result = set()
        parent = registry.get_parent(self._node)
        if parent:
            model_src_port = DagNodeParentPortModel(registry, parent)
            model_connection = connection_model.ConnectionModel(registry, model_src_port, self)
            result.add(model_connection)
        return result

    def connect_to(self, val):
        """
        :param pymel.PyNode val:
        """
        metadata = self.get_metadata()
        val.setParent(metadata)

    def connect_from(self, val):
        """
        :param pymel.PyNode val:
        """
        # todo: cycle validation?
        metadata = self.get_metadata()
        metadata.setParent(val)

    def disconnect_from(self, val):
        """
        :param pymel.PyNode val:
        """
        metadata = self.get_metadata()
        metadata.setParent(world=True)

    # def disconnect_to(self, val):
    #     # type: (pymel.PyNode) -> None
    #     pass


class NodeGraphDagNodeModel(node_dg.NodeGraphDgNodeModel):
    """Define the data model for a Node representing a DagNode."""

    def __hash__(self):
        return hash(self._pynode.fullPath())

    def get_parent(self):
        return self._registry.get_parent(self)

    def scan_ports(self):
        # Expose parent attribute
        metadata = self.get_metadata()
        node_model = self._registry.get_node(metadata)
        inst = DagNodeParentPortModel(self._registry, node_model)
        # component_inst_v1 = nodegraph_port_model.NodeGraphEntityAttributePortModel(self, model_node, val)
        yield inst

        for yielded in super(NodeGraphDagNodeModel, self).scan_ports():
            yield yielded
