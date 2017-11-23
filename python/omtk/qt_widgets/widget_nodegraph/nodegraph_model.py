import logging

import pymel.core as pymel
from omtk import session
from omtk.core import classEntityAttribute
from omtk.core import classModule
from omtk.core.classComponent import Component
from omtk.factories import factory_datatypes
from omtk.libs import libComponents
from omtk.vendor import libSerialization

from . import nodegraph_connection_model
from . import nodegraph_node_model_component
from . import nodegraph_node_model_dagnode
from . import nodegraph_node_model_module
from . import nodegraph_node_model_rig
from . import nodegraph_port_model

log = logging.getLogger('omtk')

# for type hinting
if False:
    pass


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

        # We could use memoized decorator instead, but it's clearer when we manage the memoization manually.
        self._cache_nodes = {}  # k is a node raw value
        self._cache_ports = {}  # k is a port raw value
        self._cache_connections = {}  # k is a 2-tuple of port model

    @property
    def manager(self):
        return session.get_session()

    # --- Registration methods ---

    def _register_node(self, inst):
        self._nodes.add(inst)

    def _register_attribute(self, inst):
        self._attributes.add(inst)

    def _register_connections(self, inst):
        self._connections.add(inst)

    # --- Cache clearing method ---

    def invalidate_node(self, node):
        """Invalidate any cache referencing provided value."""
        # clean node cache
        try:
            node_model = self._cache_nodes.pop(node)
            log.debug("Invalidating {0}".format(node_model))
        except LookupError:
            return

        # clear port cache
        for attr in node_model.get_attributes_raw_values():
            try:
                port_model = self._cache_ports.pop(attr)
                log.debug("Invalidating {0}".format(port_model))
            except LookupError:
                continue

            # clean connection cache
            # note: We cannot used iteritems since we modify the dict
            for key, connection_model in self._cache_connections.items():
                model_src_port, model_dst_port = key
                if model_src_port == port_model or model_dst_port == port_model:
                    self._cache_connections.pop(key)
                    log.debug("Invalidating {0}".format(connection_model))

    # --- Access methods ---

    def get_node_from_value(self, key):
        try:
            return self._cache_nodes[key]
        except LookupError:
            val = self._get_node_from_value(key)
            self._cache_nodes[key] = val
            return val

    def _get_node_from_value(self, val):
        ## type: (object) -> NodeGraphModel
        """
        Factory function for creating NodeGraphModel instances.
        This handle all the caching and registration.
        """
        log.debug('Creating node model from {0}'.format(val))

        # Handle pointer to a component datatype
        data_type = factory_datatypes.get_datatype(val)
        if data_type == factory_datatypes.AttributeType.Component:
            return nodegraph_node_model_component.NodeGraphComponentModel(self, val)

        if data_type == factory_datatypes.AttributeType.Node:
            network = None
            if isinstance(val, pymel.nodetypes.Network):
                if libSerialization.is_network_from_class(val, Component.__name__):
                    network = val
                else:
                    network = libComponents.get_component_metanetwork_from_hub_network(val)

                    # todo: use internal data
                    component = self.manager.import_network(network)

                    from omtk import constants
                    if network:
                        if network.getAttr(constants.COMPONENT_HUB_INN_ATTR_NAME) == val:
                            return nodegraph_node_model_component.NodeGraphComponentInnBoundModel(self, val, component)
                        elif network.getAttr(constants.COMPONENT_HUB_OUT_ATTR_NAME) == val:
                            return nodegraph_node_model_component.NodeGraphComponentOutBoundModel(self, val, component)
                        else:
                            raise Exception("Unreconnised network")

            # if network:
            #     component = self._manager.import_network(network)
            #     return nodegraph_node_model_component.NodeGraphComponentModel(self, component)

            return nodegraph_node_model_dagnode.NodeGraphDagNodeModel(self, val)

        if data_type == factory_datatypes.AttributeType.Module:
            return nodegraph_node_model_module.NodeGraphModuleModel(self, val)

        if data_type == factory_datatypes.AttributeType.Rig:
            return nodegraph_node_model_rig.NodeGraphNodeRigModel(self, val)

        raise Exception("Unsupported value {0} of type {1}".format(
            val, data_type
        ))
        # self._register_node(inst)
        # return inst

    def get_port_model_from_value(self, key):
        try:
            return self._cache_ports[key]
        except LookupError:
            val = self._get_port_model_from_value(key)
            self._cache_ports[key] = val
            return val

    def _get_port_model_from_value(self, val):
        # log.debug('Creating port model from {0}'.format(val))

        # type: () -> List[NodeGraphPortModel]
        # todo: add support for pure EntityAttribute
        if isinstance(val, classEntityAttribute.EntityPymelAttribute):
            node_value = val._attr.node()
            # node_model = self.get_node_from_value(node_value)  # still needed?
            # Let EntityAttribute defined if they are inputs or outputs
            inst = nodegraph_port_model.NodeGraphEntityAttributePortModel(self, node_value, val)
        elif isinstance(val, classEntityAttribute.EntityAttribute):
            node_value = val.parent
            # node_model = self.get_node_from_value(val.parent)
            inst = nodegraph_port_model.NodeGraphEntityAttributePortModel(self, node_value, val)
        elif isinstance(val, pymel.Attribute):
            node_value = val.node()
            # node_model = self.get_node_from_value(val.node())  # still needed?
            inst = nodegraph_port_model.NodeGraphPymelPortModel(self, node_value, val)
        else:
            datatype = factory_datatypes.get_datatype(val)
            if datatype == factory_datatypes.AttributeType.Node:
                # node_model = self.get_node_from_value(val)  # still needed?
                inst = nodegraph_port_model.NodeGraphPymelPortModel(self, val, val.message)
            elif isinstance(val, classModule.Module):  # todo: use factory_datatypes?
                node_value = val.rig
                # node_model = self.get_node_from_value(val.rig)
                val = val.rig.get_attribute_by_name('modules')
                inst = nodegraph_port_model.NodeGraphEntityAttributePortModel(self, node_value, val)
            else:
                node_value = val.node()
                # node_model = self.get_node_from_value(val.node())  # still needed?
                inst = nodegraph_port_model.NodeGraphPymelPortModel(self, node_value, val)

        self._register_attribute(inst)
        return inst

    def get_connection_model_from_values(self, model_src, model_dst):
        key = (model_src, model_dst)
        try:
            return self._cache_connections[key]
        except LookupError:
            val = self._get_connection_model_from_values(model_src, model_dst)
            self._cache_ports[val] = val
            return val

    def _get_connection_model_from_values(self, model_src, model_dst):
        if not isinstance(model_src, nodegraph_port_model.NodeGraphPortModel):
            model_src = self.get_port_model_from_value(model_src)

        if not isinstance(model_dst, nodegraph_port_model.NodeGraphPortModel):
            model_dst = self.get_port_model_from_value(model_dst)

        inst = nodegraph_connection_model.NodeGraphConnectionModel(self, None, model_src, model_dst)
        self._register_connections(inst)
        return inst

    # def walk_inside_component(self, component):
    #     # type: (NodeGraphComponentModel) -> None

    def iter_nodes_from_parent(self, parent):
        for node in self._nodes:
            if node.get_parent() == parent:
                yield node
