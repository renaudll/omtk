import logging
import pymel.core as pymel
from . import nodegraph_connection_model
from . import nodegraph_port_model
from . import nodegraph_node_model_dgnode

log = logging.getLogger('omtk.nodegraph')


class DagNodeParentPortModel(nodegraph_port_model.NodeGraphPortModel):
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

    def get_output_connections(self, ctrl):
        result = []
        metadata = self.get_metadata()
        children = metadata.getChildren()
        for child in children:
            model_dst_node = ctrl.get_node_model_from_value(child)
            model_dst_port = DagNodeParentPortModel(self._registry, model_dst_node)
            model_connection = nodegraph_connection_model.NodeGraphConnectionModel(self._registry, self, model_dst_port)
            result.append(model_connection)
        return result

    def get_input_connections(self, ctrl):
        result = []
        metadata = self.get_metadata()
        parent = metadata.getParent()
        if parent:
            model_src_node = ctrl.get_node_model_from_value(parent)
            model_src_port = DagNodeParentPortModel(self._registry, model_src_node)
            model_connection = nodegraph_connection_model.NodeGraphConnectionModel(self._registry, model_src_port, self)
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


class NodeGraphDagNodeModel(nodegraph_node_model_dgnode.NodeGraphDgNodeModel):
    """Define the data model for a Node representing a DagNode."""

    def iter_attributes(self, ctrl):
        # Expose parent attribute
        metadata = self.get_metadata()
        parent = metadata.getParent()
        node_model = ctrl.get_node_model_from_value(metadata)
        inst = DagNodeParentPortModel(self, node_model)
        # inst = nodegraph_port_model.NodeGraphEntityAttributePortModel(self, node_model, val)
        yield inst

        for yielded in super(NodeGraphDagNodeModel, self).iter_attributes(ctrl):
            yield yielded
