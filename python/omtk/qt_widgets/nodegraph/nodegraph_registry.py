import logging

import pymel.core as pymel
from omtk import decorators
from omtk.core import entity_attribute, session
from omtk.core import module
from omtk.factories import factory_datatypes

from .models.node import node_rig, node_dag, node_dg, node_component, node_module
from .models.port import port_base

log = logging.getLogger('omtk.nodegraph')

# for type hinting
if False:
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphPortModel, NodeGraphConnectionModel


class NodeGraphRegistry(object):
    """
    Link node values to NodeGraph[Node/Port/Connection]Model.
    Does not handle the Component representation.
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
        for attr in node_model.get_ports_metadata():
            try:
                port_model = self._cache_ports.pop(attr)
                log.debug("Invalidating {0}".format(port_model))
            except LookupError:
                continue

            # clean connection cache
            # note: We cannot used iteritems since we modify the dict
            for key, connection_model in self._cache_connections.items():
                # model_src_port, model_dst_port = key
                model_src_port = connection_model.get_source()
                model_dst_port = connection_model.get_destination()
                if model_src_port == port_model or model_dst_port == port_model:
                    self._cache_connections.pop(key)
                    log.debug("Invalidating {0}".format(connection_model))

    # --- Access methods ---

    def get_node_from_value(self, key):
        # type: (object) -> NodeGraphNodeModel
        try:
            return self._cache_nodes[key]
        except LookupError:
            val = self._get_node_from_value(key)
            self._cache_nodes[key] = val
            return val

    def _get_node_from_value(self, val):
        # type: (object) -> NodeGraphNodeModel
        """
        Factory function for creating NodeGraphRegistry instances.
        This handle all the caching and registration.
        """
        log.debug('Creating node model from {0}'.format(val))

        # Handle pointer to a component datatype
        data_type = factory_datatypes.get_datatype(val)
        if data_type == factory_datatypes.AttributeType.Component:
            return node_component.NodeGraphComponentModel(self, val)

        if data_type == factory_datatypes.AttributeType.Node:
            # network = val
            # if isinstance(val, pymel.nodetypes.Network):
            #     if libSerialization.is_network_from_class(val, Component.__name__):
            #         network = val
            #     else:
            #         network = libComponents.get_component_metanetwork_from_hub_network(val)
            #
            #         # todo: use internal data
            #         component = self.manager.import_network(network)
            #
            #         from omtk import constants
            #         if network:
            #             if network.getAttr(constants.COMPONENT_HUB_INN_ATTR_NAME) == val:
            #                 return component.NodeGraphComponentInnBoundModel(self, val, component)
            #             elif network.getAttr(constants.COMPONENT_HUB_OUT_ATTR_NAME) == val:
            #                 return component.NodeGraphComponentOutBoundModel(self, val, component)
            #             else:
            #                 raise Exception("Unreconnised network")

            # if network:
            #     component = self._manager.import_network(network)
            #     return nodegraph_node_model_component.NodeGraphComponentModel(self, component)

            if isinstance(val, pymel.nodetypes.DagNode):
                return node_dag.NodeGraphDagNodeModel(self, val)
            else:
                return node_dg.NodeGraphDgNodeModel(self, val)

        if data_type == factory_datatypes.AttributeType.Module:
            return node_module.NodeGraphModuleModel(self, val)

        if data_type == factory_datatypes.AttributeType.Rig:
            return node_rig.NodeGraphNodeRigModel(self, val)

        raise Exception("Unsupported value {0} of type {1}".format(
            val, data_type
        ))
        # self._register_node(inst)
        # return inst

    def get_port_model_from_value(self, key):
        # type: (object) -> NodeGraphPortModel
        try:
            return self._cache_ports[key]
        except LookupError:
            val = self._get_port_model_from_value(key)
            self._cache_ports[key] = val
            return val

    def _get_port_model_from_value(self, val):
        # type: (object) -> NodeGraphPortModel
        # log.debug('Creating port model from {0}'.format(val))
        # todo: add support for pure EntityAttribute
        if isinstance(val, entity_attribute.EntityPymelAttribute):
            node_value = val.parent
            node_model = self.get_node_from_value(node_value)
            inst = port_base.NodeGraphEntityAttributePortModel(self, node_model, val)
        elif isinstance(val, entity_attribute.EntityAttribute):
            node_value = val.parent
            node_model = self.get_node_from_value(node_value)
            # node_model = self.get_node_from_value(val.parent)
            inst = port_base.NodeGraphEntityAttributePortModel(self, node_model, val)
        elif isinstance(val, pymel.Attribute):
            node_value = val.node()
            node_model = self.get_node_from_value(node_value)
            inst = port_base.NodeGraphPymelPortModel(self, node_model, val)
        else:
            datatype = factory_datatypes.get_datatype(val)
            if datatype == factory_datatypes.AttributeType.Node:
                node_model = self.get_node_from_value(val)
                inst = port_base.NodeGraphPymelPortModel(self, node_model, val.message)
            elif isinstance(val, module.Module):  # todo: use factory_datatypes?
                node_value = val.rig
                node_model = self.get_node_from_value(val.rig)
                val = val.rig.get_attribute_by_name('modules')
                inst = port_base.NodeGraphEntityAttributePortModel(self, node_model, val)
            else:
                node_value = val.node()
                node_model = self.get_node_from_value(val.node())
                inst = port_base.NodeGraphPymelPortModel(self, node_model, val)

        self._register_attribute(inst)
        return inst

    def get_connection_model_from_values(self, model_src, model_dst):
        # type: (NodeGraphPortModel, NodeGraphPortModel) -> NodeGraphConnectionModel
        key = (model_src, model_dst)
        try:
            return self._cache_connections[key]
        except LookupError:
            val = self._get_connection_model_from_values(model_src, model_dst)
            self._cache_connections[key] = val
            return val

    def _get_connection_model_from_values(self, model_src, model_dst):
        # type: (NodeGraphPortModel, NodeGraphPortModel) -> NodeGraphConnectionModel
        # assert(isinstance(model_src, port_base.NodeGraphPortModel))
        # assert(isinstance(model_dst, port_base.NodeGraphPortModel))
        from omtk.qt_widgets.nodegraph.models import connection

        if not isinstance(model_src, port_base.NodeGraphPortModel):
            model_src = self.get_port_model_from_value(model_src)

        if not isinstance(model_dst, port_base.NodeGraphPortModel):
            model_dst = self.get_port_model_from_value(model_dst)

        inst = connection.NodeGraphConnectionModel(self, model_src, model_dst)
        self._register_connections(inst)
        return inst

    def iter_nodes_from_parent(self, parent):
        for node in self._nodes:
            if node.get_parent() == parent:
                yield node

    def get_node_parent(self, node):
        return self.manager._cache_components.get_component_from_obj(node)


@decorators.memoized
def _get_singleton_model():
    from .nodegraph_registry import NodeGraphRegistry

    return NodeGraphRegistry()
