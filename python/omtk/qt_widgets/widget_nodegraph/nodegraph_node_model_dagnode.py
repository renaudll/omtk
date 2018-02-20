import logging
import pymel.core as pymel
from omtk import decorators
from omtk.libs import libAttr, libPyflowgraph
from omtk.vendor.Qt import QtCore

from . import nodegraph_node_model_base
from . import nodegraph_port_model
from . import pyflowgraph_node_widget

log = logging.getLogger('omtk.nodegraph')


class NodeGraphDagNodeModel(nodegraph_node_model_base.NodeGraphNodeModel):
    """Define the data model for a Node representing a DagNode."""

    def __init__(self, registry, pynode):
        name = pynode.nodeName()
        self._pynode = pynode
        super(NodeGraphDagNodeModel, self).__init__(registry, name)

    def __hash__(self):
        return hash(self._pynode)

    def rename(self, new_name):
        self._pynode.rename(new_name)
        # Fetch the nodeName in case of name clash Maya
        # will give the node another name
        self._name = self._pynode.nodeName()

    def delete(self):
        if not self._pynode.exists():
            log.warning("Can't delete already deleted node! {0}".format(self._pynode))
            return
        pymel.delete(self._pynode)

    @decorators.memoized_instancemethod
    def get_parent(self):
        # type: () -> NodeGraphNodeModel
        return self._registry.get_node_parent(self._pynode)

    def get_metadata(self):
        return self._pynode

    # @decorators.memoized_instancemethod
    def get_attributes_raw_values(self):
        return list(libAttr.iter_contributing_attributes(self._pynode))
        # return list(libAttr.iter_contributing_attributes_openmaya2(self._pynode.__melobject__()))

    def iter_attributes(self):
        for attr in self.get_attributes_raw_values():
            inst = self._registry.get_port_model_from_value(attr)
            # inst = nodegraph_port_model.NodeGraphPymelPortModel(self._registry, self, attr)
            # self._registry._register_attribute(inst)
            yield inst

            if attr.isMulti():
                for attr_child in attr:
                    inst = self._registry.get_port_model_from_value(attr_child)
                    # inst = nodegraph_port_model.NodeGraphPymelPortModel(self._registry, self, attr_child)
                    # self._registry._register_attribute(inst)
                    yield inst

    # @decorators.memoized_instancemethod
    def get_attributes(self):
        # type: () -> List[NodeGraphPortModel]
        result = set()
        for attr in self.iter_attributes():
            result.add(attr)
        return result

    def _get_widget_cls(self):
        return pyflowgraph_node_widget.OmtkNodeGraphDagNodeWidget

    def get_widget(self, graph, ctrl):
        node = super(NodeGraphDagNodeModel, self).get_widget(graph, ctrl)

        # Set position
        pos = libPyflowgraph.get_node_position(node)
        if pos:
            pos = QtCore.QPointF(*pos)
            node.setGraphPos(pos)

        return node


