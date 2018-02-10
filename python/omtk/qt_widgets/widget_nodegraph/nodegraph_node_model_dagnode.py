from omtk import decorators
from omtk.libs import libPython, libAttr, libPyflowgraph
from omtk import constants
from . import nodegraph_node_model_base
from . import nodegraph_port_model
from omtk.vendor.Qt import QtCore
from omtk.libs import libComponents
import logging


log = logging.getLogger('omtk.nodegraph')


class NodeGraphDagNodeModel(nodegraph_node_model_base.NodeGraphNodeModel):
    """Define the data model for a Node representing a DagNode."""

    # Hide the attributes we are ourself creating
    _attr_name_blacklist = (
        constants.PyFlowGraphMetadataKeys.Position,
        constants.PyFlowGraphMetadataKeys.Position + 'X',
        constants.PyFlowGraphMetadataKeys.Position + 'Y',
        constants.PyFlowGraphMetadataKeys.Position + 'Z',
    )

    def __init__(self, registry, pynode):
        name = pynode.nodeName()
        self._pynode = pynode
        super(NodeGraphDagNodeModel, self).__init__(registry, name)

    def __hash__(self):
        return hash(self._pynode)

    @decorators.memoized_instancemethod
    def get_parent(self):
        # type: () -> NodeGraphNodeModel
        return self._registry.get_node_parent(self._pynode)

    def get_metadata(self):
        return self._pynode

    def _can_show_attr(self, attr):
        return not attr.longName() in self._attr_name_blacklist

    @decorators.memoized_instancemethod
    def get_attributes_raw_values(self):
        return list(libAttr.iter_contributing_attributes(self._pynode))
        # return list(libAttr.iter_contributing_attributes_openmaya2(self._pynode.__melobject__()))

    def iter_attributes(self):
        for attr in self.get_attributes_raw_values():
            if not self._can_show_attr(attr):
                log.debug("Hiding attribute {0}".format(attr))
                continue

            inst = nodegraph_port_model.NodeGraphPymelPortModel(self._registry, self, attr)
            self._registry._register_attribute(inst)
            yield inst

    @decorators.memoized_instancemethod
    def get_attributes(self):
        # type: () -> List[NodeGraphPortModel]
        result = set()
        for attr in self.iter_attributes():
            result.add(attr)
        return result

    def get_widget(self, graph):
        node = super(NodeGraphDagNodeModel, self).get_widget(graph)

        # Set position
        pos = libPyflowgraph.get_node_position(node)
        if pos:
            pos = QtCore.QPointF(*pos)
            node.setGraphPos(pos)

        return node


