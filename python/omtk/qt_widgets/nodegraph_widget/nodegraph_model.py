import logging

import pymel.core as pymel
from omtk import factory_datatypes
from omtk.core.classComponent import Component
from omtk.libs import libPython
from omtk.vendor import libSerialization

from .nodegraph_node_model import NodeGraphDagNodeModel, NodeGraphComponentModel

log = logging.getLogger('omtk')


class NodeGraphModel(object):
    """
    This class act a sort of global cache for the multiple models that compose the GraphView.
    This allow multiple view can re-use the same data.
    """

    def __init__(self):
        self._nodes = set()
        self._attributes = set()
        self._connections = set()

        self._nodes_by_metadata = {}

    # --- Registration methods ---

    def _register_node(self, inst):
        self._nodes.add(inst)

    def _register_attribute(self, inst):
        self._attributes.add(inst)

    def _register_connections(self, inst):
        self._connections.add(inst)

    # --- Access methods ---

    @libPython.memoized_instancemethod
    def get_node_from_value(self, val):
        # type: (object) -> GraphNodeModel
        """
        Public entry point to access a Node from a provided value.
        This handle all the caching and registration.
        """
        log.debug('Exploring new value {0}'.format(val))
        data_type = factory_datatypes.get_component_attribute_type(val)
        if data_type == factory_datatypes.AttributeType.Component:
            inst = NodeGraphComponentModel(self, val)
        elif data_type == factory_datatypes.AttributeType.Node:
            # If we encounter a Node, it could still be a Component input/output network.
            if isinstance(val, pymel.nodetypes.Network) and libSerialization.is_network_from_class(
                    val, Component.__name__):
                component = libSerialization.import_network(val)
                inst = NodeGraphComponentModel(self, component)
            else:
                inst = NodeGraphDagNodeModel(self, val)
        else:
            raise Exception("Unsupported value {0} of type {1}".format(
                val, data_type
            ))
        log.info('Resolved {0}'.format(inst))
        self._register_node(inst)
        return inst

    # def walk_inside_component(self, component):
    #     # type: (NodeGraphComponentModel) -> None


    def iter_nodes_from_parent(self, parent):
        for node in self._nodes:
            if node.get_parent() == parent:
                yield node
