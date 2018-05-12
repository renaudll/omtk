import logging
import pymel.core as pymel
from omtk.qt_widgets.nodegraph.models.port import port_base as port_model
from omtk.qt_widgets.nodegraph.models import connection as connection_model
from omtk.qt_widgets.nodegraph.models.node import node_dg

log = logging.getLogger('omtk.nodegraph')


class DagNodeParentPortModel(port_model.NodeGraphPortModel):
    # __metaclass__ = abc.ABCMeta

    def __init__(self, registry, parent):
        super(DagNodeParentPortModel, self).__init__(registry, parent, 'hierarchy')

    def is_interesting(self):
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
        result = []
        metadata = self.get_metadata()
        children = metadata.getChildren()
        for child in children:
            model_dst_node = self._registry.get_node_from_value(child)
            model_dst_port = DagNodeParentPortModel(self._registry, model_dst_node)
            model_connection = connection_model.NodeGraphConnectionModel(self._registry, self, model_dst_port)
            result.append(model_connection)
        return result

    def get_input_connections(self):
        result = []
        metadata = self.get_metadata()
        parent = metadata.getParent()
        if parent:
            model_src_node = self._registry.get_node_from_value(parent)
            model_src_port = DagNodeParentPortModel(self._registry, model_src_node)
            model_connection = connection_model.NodeGraphConnectionModel(self._registry, model_src_port, self)
            result.append(model_connection)
        return result

    def connect_to(self, val):
        # type: (pymel.PyNode) -> None
        metadata = self.get_metadata()
        val.setParent(metadata)

    def connect_from(self, val):
        # type: (pymel.PyNode) -> None
        # todo: cycle validation?
        metadata = self.get_metadata()
        metadata.setParent(val)

    def disconnect_from(self, val):
        # type: (pymel.PyNode) -> None
        metadata = self.get_metadata()
        metadata.setParent(world=True)

    # def disconnect_to(self, val):
    #     # type: (pymel.PyNode) -> None
    #     pass


class NodeGraphDagNodeModel(node_dg.NodeGraphDgNodeModel):
    """Define the data model for a Node representing a DagNode."""

    def scan_ports(self):
        # Expose parent attribute
        metadata = self.get_metadata()
        node_model = self._registry.get_node_from_value(metadata)
        inst = DagNodeParentPortModel(self._registry, node_model)
        # inst = nodegraph_port_model.NodeGraphEntityAttributePortModel(self, node_model, val)
        yield inst

        for yielded in super(NodeGraphDagNodeModel, self).scan_ports():
            yield yielded
