import logging
from collections import defaultdict
from maya import OpenMaya
import pymel.core as pymel
import functools
from omtk import decorators
from omtk.core import entity_attribute, session
from omtk.core import module
from omtk.factories import factory_datatypes
from omtk.vendor.Qt import QtCore
from .models.node import node_base, node_rig, node_dag, node_dg, node_component, node_module
from .models.port import port_base

log = logging.getLogger('omtk.nodegraph')

# for type hinting
if False:
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphPortModel, NodeGraphConnectionModel


class NodeGraphRegistry(QtCore.QObject):  # QObject provide signals
    """
    Link node values to NodeGraph[Node/Port/Connection]Model.
    """
    # todo: connect the signals bellow? it seem like it should be the registry job to track changes in Maya and notify the models.

    # Signal emitted when a node is deleted from Maya.
    # In this case the registry will automatically unregister the node and notify the models.
    onNodeDeleted = QtCore.Signal(node_base.NodeGraphNodeModel)

    # Signal emitted when an attribute is added.
    # In this case the registry will automatically register the port and notify the models.
    onAttributeAdded = QtCore.Signal(port_base.NodeGraphPortModel)

    # Signal emitted when an attribute is removed from Maya.
    onAttributeRemoved = QtCore.Signal(port_base.NodeGraphPortModel)

    def __init__(self):
        super(NodeGraphRegistry, self).__init__()

        self._nodes = set()
        self._attributes = set()
        self._connections = set()

        self._nodes_by_metadata = {}

        # We could use memoized decorator instead, but it's clearer when we manage the memoization manually.
        self._cache_nodes = {}  # k is a node raw value
        self._cache_nodes_inv = {}
        self._cache_ports = {}  # k is a port raw value
        self._cache_ports_inv = {}
        self._cache_connections = {}  # k is a 2-tuple of port model

        # Used so we can invalidate ports when invalidating nodes
        self._cache_ports_by_node = defaultdict(set)
        self._cache_node_by_port = {}

        self._callback_id_by_node_model = defaultdict(set)
        self.add_callbacks()

    def __del__(self):
        self.remove_callbacks()

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

    def invalidate_node(self, node_model):
        # type: (NodeGraphNodeModel) -> None
        """Invalidate any cache referencing provided value."""
        # clean node cache
        try:
            node_value = self._cache_nodes_inv.pop(node_model)
            log.debug("Invalidating {0}".format(node_model))
            self._cache_nodes.pop(node_value)
            self._nodes.remove(node_model)  # todo: do we really need this cache? seem slower
        except LookupError:
            return

        # clear port cache
        for port_model in self._cache_ports_by_node.pop(node_model, []):
            try:
                log.debug("Invalidating {0}".format(port_model))
                attr = self._cache_ports_inv.pop(port_model)
                self._cache_node_by_port.pop(port_model)
                self._cache_ports.pop(attr)
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

        # remove callbacks
        self._remove_node_callback(node_model)

    # --- Access methods ---

    def get_node_from_value(self, key):
        # type: (object) -> NodeGraphNodeModel
        try:
            return self._cache_nodes[key]
        except Exception:  # LookupError
            val = self._get_node_from_value(key)
            self._cache_nodes[key] = val
            self._cache_nodes_inv[val] = key
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
            node = node_component.NodeGraphComponentModel(self, val)
            # Hack: Force registration of all component children.
            # This will ensure that node deletion signal get propagated.
            node.get_children()

            return node

        if data_type == factory_datatypes.AttributeType.Node:
            if isinstance(val, pymel.nodetypes.DagNode):
                node = node_dag.NodeGraphDagNodeModel(self, val)
            else:
                node = node_dg.NodeGraphDgNodeModel(self, val)
            self._add_node_callback(node)
            return node

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
            self._cache_ports_inv[val] = key
            node = val.get_parent()
            self._cache_ports_by_node[node].add(val)
            self._cache_node_by_port[val] = node
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

    # --- Maya callbacks ---
    def _add_node_callback(self, metadata):
        # type: (NodeGraphNodeModel) -> None

        mobject = metadata.get_metadata().__apimobject__()

        # Add attribute added callback
        callback_id = OpenMaya.MNodeMessage.addAttributeAddedOrRemovedCallback(
            mobject,
            self.callback_attribute_added
        )
        self._callback_id_by_node_model[metadata].add(callback_id)

        # Add attribute changed (connected)
        # callback_id = OpenMaya.MNodeMessage.addAttributeChangedCallback(
        #     mobject,
        #     self.callback_attribute_changed
        # )
        # self._callback_id_by_node_model[metadata].add(callback_id)

        # Add node deleted callback
        # callback_id = OpenMaya.MNodeMessage.addNodeAboutToDeleteCallback(
        #     mobject,
        #     functools.partial(self.callback_node_deleted, metadata)
        # )
        self._callback_id_by_node_model[metadata].add(callback_id)

    def add_callbacks(self):
        self.remove_callbacks()

        OpenMaya.MDGMessage.addNodeRemovedCallback(
            self.callback_some_node_deleted,
            "dependNode",
        )

    def callback_some_node_deleted(self, node, clientData):
        # type: (OpenMaya.MObject, object) -> None
        obj = pymel.PyNode(node)
        node = self.get_node_from_value(obj)
        self.callback_node_deleted(node)

    def _remove_node_callback(self, node):
        # type: (NodeGraphNodeModel) -> None
        callback_ids = self._callback_id_by_node_model.get(node)
        if callback_ids is None:
            log.warning("Cannot remove callback. No callback set for {0}.".format(node))
            return

        for callback_id in callback_ids:
            OpenMaya.MNodeMessage.removeCallback(callback_id)

        self._callback_id_by_node_model.pop(node)

    def remove_callbacks(self):
        for metadata in self._callback_id_by_node_model.keys():
            self._remove_node_callback(metadata)
        # for _, ids in self._callback_id_by_node_model.iteritems():
        #     for id_ in ids:
        #         OpenMaya.MNodeMessage.removeCallback(id_)
        # self._callback_id_by_node_model.clear()
        assert(len(self._callback_id_by_node_model) == 0)  # should be empty

    @staticmethod
    def _analayse_callback_message(msg):
        if msg & OpenMaya.MNodeMessage.kConnectionMade:
            yield 'kConnectionMade'
        if msg & OpenMaya.MNodeMessage.kConnectionBroken:
            yield 'kConnectionBroken'
        if msg & OpenMaya.MNodeMessage.kAttributeEval:
            yield 'kAttributeEval'
        if msg & OpenMaya.MNodeMessage.kAttributeSet:
            yield 'kAttributeSet'
        if msg & OpenMaya.MNodeMessage.kAttributeLocked:
            yield 'kAttributeLocked'
        if msg & OpenMaya.MNodeMessage.kAttributeUnlocked:
            yield 'kAttributeUnlocked'
        if msg & OpenMaya.MNodeMessage.kAttributeAdded:
            yield 'kAttributeAdded'
        if msg & OpenMaya.MNodeMessage.kAttributeRemoved:
            yield 'kAttributeRemoved'
        if msg & OpenMaya.MNodeMessage.kAttributeRenamed:
            yield 'kAttributeRenamed'
        if msg & OpenMaya.MNodeMessage.kAttributeKeyable:
            yield 'kAttributeKeyable'
        if msg & OpenMaya.MNodeMessage.kAttributeUnkeyable:
            yield 'kAttributeUnkeyable'
        if msg & OpenMaya.MNodeMessage.kIncomingDirection:
            yield 'kIncomingDirection'
        if msg & OpenMaya.MNodeMessage.kAttributeArrayAdded:
            yield 'kAttributeArrayAdded'
        if msg & OpenMaya.MNodeMessage.kAttributeArrayRemoved:
            yield 'kAttributeArrayRemoved'
        if msg & OpenMaya.MNodeMessage.kOtherPlugSet:
            yield 'kOtherPlugSet'

    def callback_attribute_added(self, callback_id, mplug, _):
        from omtk.qt_widgets.nodegraph.filters import filter_standard

        attr_dagpath = mplug.name()
        attr_name = attr_dagpath.split('.')[-1]

        # todo: make it cleaner
        if attr_name in filter_standard._attr_name_blacklist:
            log.info('Ignoring callback on {0}'.format(attr_dagpath))
            return

        attr_mobj = mplug.node()
        mfn = OpenMaya.MFnDependencyNode(attr_mobj)
        obj_name = mfn.name()
        log.info('Attribute {0} added on {1}'.format(attr_name, obj_name))

        attr = pymel.Attribute(attr_dagpath)

        port = self.get_port_model_from_value(attr)
        self.onAttributeAdded.emit(port)

    # @decorators.log_info
    def callback_attribute_changed(self, msg, plug, *args, **kwargs):
        """
        Called when an attribute related to the node change in Maya.
        :param msg:
        :param plug:
        :param args:
        :param kwargs:
        :return:
        """
        return  # todo: make it work
        from maya import OpenMaya
        # print(' + '.join(self._analayse_callback_message(msg)))

        if msg & OpenMaya.MNodeMessage.kAttributeArrayAdded:
            attr_dagpath = plug.name()
            # attr = pymel.Attribute(attr_dagpath)
            self.onAttributeAdded.emit(attr_dagpath)
            # print attr
            # self._ctrl.callback_attribute_array_added(attr_dagpath)

    @decorators.log_info
    def callback_node_deleted(self, node, *args, **kwargs):
        # type: (NodeGraphNodeModel, OpenMaya.MObject, OpenMaya.MDGModifier) -> None
        """
        Called when the node is deleted in Maya.
        :param pynode: The pynode that is being deleted
        :param args: Absorb the OpenMaya callback arguments
        :param kwargs: Absorb the OpenMaya callback keyword arguments
        """
        log.info("[Registry Callback] {0} was deleted".format(node))
        # node = self.get_node_from_value(pynode)



        # Hack: If the node is part of a compound, ensure that the compound delete
        # itself automatically if there's no more children.
        # This might not be the best way to do, see QUESTIONS.txt 1.1.
        if isinstance(node, node_dg.NodeGraphDgNodeModel):
            parent = node.get_parent()
            if parent:
                parent_children = set(parent.get_children())
                parent_children.remove(node)  # the node is not yet deleted
                print node, len(parent_children), parent_children
                if len(parent_children) == 0:
                    self.onNodeDeleted.emit(parent)
                    self.invalidate_node(parent)

        # node.onDeleted.emit(node)
        self.onNodeDeleted.emit(node)  # todo: do we need 2 signals?
        self.invalidate_node(node)


_g_registry = None
# @decorators.memoized
def get_registry():
    # type: () -> NodeGraphRegistry
    from .nodegraph_registry import NodeGraphRegistry
    global _g_registry
    if _g_registry is None:
        _g_registry = NodeGraphRegistry()
    return _g_registry
    # return NodeGraphRegistry()
