import logging
import pymel.core as pymel
from omtk import decorators
from omtk.libs import libAttr, libPyflowgraph
from omtk.vendor.Qt import QtCore

from omtk.qt_widgets.nodegraph.models.node import node_base
from omtk.qt_widgets.nodegraph import pyflowgraph_node_widget

log = logging.getLogger('omtk.nodegraph')


class NodeGraphDgNodeModel(node_base.NodeGraphNodeModel):
    """Define the data model for a Node representing a DagNode."""

    def __init__(self, registry, pynode):
        name = pynode.nodeName()
        self._pynode = pynode
        super(NodeGraphDgNodeModel, self).__init__(registry, name)

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
        return self._registry.get_component_from_obj(self._pynode)

    def get_metadata(self):
        return self._pynode

    def get_nodes(self):
        return [self.get_metadata()]

    # @decorators.memoized_instancemethod
    def get_ports_metadata(self):
        return list(libAttr.iter_contributing_attributes(self._pynode))
        # return list(libAttr.iter_contributing_attributes_openmaya2(self._pynode.__melobject__()))

    def iter_ports(self):
        for attr in self.get_ports_metadata():
            inst = self._registry.get_port_model_from_value(attr)
            # inst = nodegraph_port_model.NodeGraphPymelPortModel(self._registry, self, attr)
            # self._registry._register_attribute(inst)
            yield inst

            # Note: Multi-attribute are disabled for now, we might want to handle 'free' item
            # if a special way before re-activating this.
            # Otherwise we might have strange side effects.
            # n = pymel.createNode('transform')
            # n.worldMatrix.numElements()  # -> 0
            # n.worldMatrix.type()
            # n.worldMatrix.numElements() # -> 1, wtf
            # n.worldMatrix[1]  # if we try to use the free index directly
            # n.worldMatrix.numElements() # -> 2, wtf

            # If the attribute is a multi attribute, we'll want to expose the first available.
            # if attr.isMulti():
            #     next_available_index = attr.numElements() if attr.numElements() else 0
            #     attr_available = attr[next_available_index]
            #     inst = self._registry.get_port_model_from_value(attr_available)
            #     yield inst

            # if attr.isMulti():
            #     num_elements = attr.numElements()
            #     for i in xrange(num_elements):
            #         attr_child = attr.elementByLogicalIndex(i)
            #     # for attr_child in attr:
            #         inst = self._registry.get_port_model_from_value(attr_child)
            #         # inst = nodegraph_port_model.NodeGraphPymelPortModel(self._registry, self, attr_child)
            #         # self._registry._register_attribute(inst)
            #         yield inst

    def _get_widget_cls(self):
        return pyflowgraph_node_widget.OmtkNodeGraphDagNodeWidget

    def get_widget(self, graph, ctrl):
        node = super(NodeGraphDgNodeModel, self).get_widget(graph, ctrl)

        # Set position
        pos = libPyflowgraph.get_node_position(node)
        if pos:
            pos = QtCore.QPointF(*pos)
            node.setGraphPos(pos)

        return node
