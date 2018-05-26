import logging
from collections import defaultdict
import functools
import pymel.core as pymel
from maya import OpenMaya
from omtk import decorators, constants
from omtk.libs import libAttr, libPyflowgraph, libMayaNodeEditor
from omtk.vendor.Qt import QtCore

from . import node_base
from omtk.qt_widgets.nodegraph import pyflowgraph_node_widget
from omtk.factories import factory_datatypes

log = logging.getLogger('omtk.nodegraph')



class NodeGraphDgNodeModel(node_base.NodeGraphNodeModel):
    """Define the data model for a Node representing a DagNode."""

    def __init__(self, registry, pynode):
        name = pynode.nodeName()
        self._pynode = pynode
        super(NodeGraphDgNodeModel, self).__init__(registry, name)

    def __hash__(self):
        return hash(self._pynode.nodeName())

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

    # @decorators.memoized_instancemethod
    def get_parent(self):
        # type: () -> NodeGraphNodeModel
        # todo: move out of node_dg?
        from omtk.core import session as session_
        session = session_.get_session()
        component = session.get_component_from_obj(self._pynode)
        if component:
            return self._registry.get_node_from_value(component)

    def get_metadata(self):
        return self._pynode

    def get_nodes(self):
        return [self.get_metadata()]

    # @decorators.memoized_instancemethod
    def get_ports_metadata(self):
        return list(libAttr.iter_contributing_attributes(self._pynode))
        # return list(libAttr.iter_contributing_attributes_openmaya2(self._pynode.__melobject__()))

    def scan_ports(self):
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

            if attr.isArray():
                # hack, If the attribute is a multi attribute, we'll want to expose the first available.
                attr.type()

                num_elements = attr.numElements()
                for i in xrange(num_elements):
                    attr_child = attr.elementByLogicalIndex(i)
                    inst = self._registry.get_port_model_from_value(attr_child)
                    yield inst

                # attr_available = attr[num_elements]
                # inst = self._registry.get_port_model_from_value(attr_available)
                # yield inst

    def _get_widget_cls(self):
        return pyflowgraph_node_widget.OmtkNodeGraphDagNodeWidget

    # --- Callbacks ---

    def get_position(node):
        # type: (PyFlowgraphNode) -> (float, float)
        meta_data = node.get_metadata()

        # If the node contain a saved position, use it.
        if meta_data.hasAttr(constants.PyFlowGraphMetadataKeys.Position):
            return meta_data.attr(constants.PyFlowGraphMetadataKeys.Position).get()

    def save_position(node, pos):
        meta_data = node.get_metadata()
        attr_name = constants.PyFlowGraphMetadataKeys.Position

        if not meta_data.hasAttr(attr_name):
            pymel.addAttr(meta_data, longName=attr_name, at='float2')
            pymel.addAttr(meta_data, longName=attr_name + 'X', at='float', parent=attr_name)
            pymel.addAttr(meta_data, longName=attr_name + 'Y', at='float', parent=attr_name)
            attr = meta_data.attr(attr_name)
        else:
            attr = meta_data.attr(attr_name)
        attr.set(pos)