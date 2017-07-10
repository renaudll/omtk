from omtk.libs import libPython, libAttr, libPyflowgraph
from . import nodegraph_node_model_base
from . import nodegraph_port_model
from omtk.vendor.Qt import QtCore


class NodeGraphDagNodeModel(nodegraph_node_model_base.NodeGraphNodeModel):
    """Define the data model for a Node representing a DagNode."""

    def __init__(self, registry, pynode):
        name = pynode.nodeName()
        super(NodeGraphDagNodeModel, self).__init__(registry, name)
        self._pynode = pynode

    def get_metadata(self):
        return self._pynode

    @libPython.memoized_instancemethod
    def get_attributes(self):
        # type: () -> List[NodeGraphPortModel]
        result = set()
        for attr in libAttr.iter_contributing_attributes(self._pynode):
            inst = nodegraph_port_model.NodeGraphPymelPortModel(self._registry, self, attr)
            self._registry._register_attribute(inst)
            result.add(inst)
        return result

    def get_widget(self, graph):
        node = super(NodeGraphDagNodeModel, self).get_widget(graph)

        # Set position
        pos = libPyflowgraph.get_node_position(node)
        if pos:
            pos = QtCore.QPointF(*pos)
            node.setGraphPos(pos)

        return node


