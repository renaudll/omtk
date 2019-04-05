import logging
from collections import defaultdict
from contextlib import contextmanager

import pymel.core as pymel

from omtk.nodegraph.adaptors.node.pymel_ import NodeGraphNodePymelAdaptor
from omtk.nodegraph.models.node import NodeModel
from omtk.nodegraph.registry.base import NodeGraphRegistry

log = logging.getLogger(__name__)


class MayaRegistry(NodeGraphRegistry):
    """
    Registry linked to Maya.
    """

    def __init__(self, *args, **kwargs):
        self._mutex = True  # If False, Maya events are ignored.

        self._callback_attribute_added_or_removed = None
        self._callback_attribute_changed = None
        self._callback_id_node_removed = None
        self._callback_id_by_node = defaultdict(set)

        super(MayaRegistry, self).__init__(*args, **kwargs)

        self.cache_nodes_by_value.onUnregistered.connect(self.remove_node_callbacks)

        self.add_callbacks()

    def __del__(self):
        self.remove_callbacks()

    @contextmanager
    def lock(self):
        self._mutex = False
        yield
        self._mutex = True

    def _conform_node_key(self, key):
        """
        Allow multiple values to be map to the same key.
        For example in Maya, a node can be represented by:
        - It's fully qualified DagPath
        - A pymel.Node object
        - A OpenMaya.MObject
        - An OpenMaya2.MObject
        We want all of theses potential values to be mapped to the same key.
        """
        # OpenMaya
        # if isinstance(value, OpenMaya.MObject):
        #     return value

        # pymel
        if isinstance(key, pymel.PyNode):
            return key

        # cmds
        if isinstance(key, basestring):
            return pymel.PyNode(key)

        raise Exception("Unsupported value {} ({})".format(key, type(key)))

    def _get_node(self, val):
        """
        Return a node representation of the provided value.
        :param object val:
        :return:
        :rtype: NodeModel
        """
        assert (isinstance(val, pymel.PyNode))
        impl = NodeGraphNodePymelAdaptor(val)
        return NodeModel(self, impl)

    def _get_port(self, val):
        """
        Create a port from a value.
        :param val: An object representable as a port (str, pymel.Attribute, etc)
        :return: A port
        :rtype: omtk.nodegraph.PortModel
        """
        from omtk.nodegraph import factory
        inst = factory.get_port_from_value(self, val)
        return inst

    def _get_parent_impl(self, val):
        """
        Get a node parent.

        :param pymel.PyNode val: The node to query
        :return: The node parent. None if node have not parent.
        :rtype: pymel.PyNode or None
        """
        return val.getParent()

    def _get_children_impl(self, val):
        """
        Get a node children.

        :param pymel.PyNode val: The node to query
        :return: A list of child.
        :rtype: List[pymel.PyNode]
        """
        return val.getChildren()

    def _set_parent_impl(self, node, parent):
        """
        :param pymel.PyNode child: The node to parent
        :param pymel.PyNode parent: The parent
        """
        return node.setParent(parent)

    def _scan_nodes(self):
        import pymel.core as pymel
        for node in pymel.ls():
            self.get_node(node)

    def _scan_node_ports(self, node):
        """
        :param pymel.PyNode node: The node to scan.
        """
        from omtk.libs import libAttr
        attrs = libAttr.iter_contributing_attributes(node)

        for attr in attrs:
            inst = self.get_port(attr)
            # component_inst_v1 = nodegraph_port_model.NodeGraphPymelPortModel(self._session, self, attr)
            # self._session._register_port(component_inst_v1)
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

                # Hack: Some multi attribute like transform.worldInverseMatrix will be empty at first,
                # but might be lazy initialized when we look at them. For consistency, we'll force them
                # to be initialized so we only deal with one state.
                attr.type()

                num_elements = attr.numElements()
                for i in xrange(num_elements):
                    attr_child = attr.elementByLogicalIndex(i)
                    inst = self.get_port(attr_child)
                    yield inst

                # Note: Accessing an attribute that don't exist will trigger it's creation.
                # We need to use safer methods?
                from maya import mel
                next_available_index = mel.eval('getNextFreeMultiIndex "{0}" 0'.format(attr.__melobject__()))
                attr_available = attr[next_available_index]
                inst = self.get_port(attr_available)
                yield inst

    def get_translator(self):
        """
        Return the logic to use when interpreting values from the session.
        The translator
        :return:
        """

    def add_callbacks(self):
        """
        Add callbacks to maya so what we are notify of general events.
        """
        pass
        # self._callback_id_node_removed = OpenMaya.MDGMessage.addNodeRemovedCallback(
        #     self._callback_node_removed, "dependNode")

    def _register_node(self, node, val):
        super(MayaRegistry, self)._register_node(node, val)
        self.add_node_callbacks(node, val)

    def add_node_callbacks(self, node, val):
        """
        Called when a node is atted to the REGISTRY_DEFAULT bound to the DCC application or mock. ???

        :param NodeModel node: The node being add to the REGISTRY_DEFAULT.
        :param pymel.PyNode val: Conformed internal value.
        """
        from maya import OpenMaya
        mobject = val.__apimobject__()

        # Add attribute added callback
        callback_id = OpenMaya.MNodeMessage.addAttributeAddedOrRemovedCallback(mobject, self._on_port_added_or_removed)
        self._callback_id_by_node[node].add(callback_id)

        # Add attribute changed (connected)
        callback_id = OpenMaya.MNodeMessage.addAttributeChangedCallback(mobject, self._on_attribute_changed)
        self._callback_id_by_node[node].add(callback_id)

        # Add node deleted callback
        callback_id = OpenMaya.MNodeMessage.addNodeAboutToDeleteCallback(
            mobject,
            self._callback_node_removed,
        )
        self._callback_id_by_node[node].add(callback_id)

    def remove_node_callbacks(self, node):
        """
        Remove only callbacks associated with nodes.
        :param NodeModel node: The node to remove the callbacks from.
        """
        from maya import OpenMaya

        callback_ids = self._callback_id_by_node.get(node)
        if callback_ids is None:
            log.debug("Cannot remove callback. No callback set for {0}.".format(node))
            return

        for callback_id in callback_ids:
            OpenMaya.MNodeMessage.removeCallback(callback_id)

        self._callback_id_by_node.pop(node)

    def remove_callbacks(self):
        """
        Remove all registered callbacks (including node callbacks.
        """
        from maya import OpenMaya
        if self._callback_id_node_removed is not None:
            OpenMaya.MNodeMessage.removeCallback(self._callback_id_node_removed)

        for node in self._callback_id_by_node.keys():
            self.remove_node_callbacks(node)

        self._callback_id_by_node.clear()

        assert (len(self._callback_id_by_node) == 0)  # should be empty

    def _on_port_added_or_removed(self, callback_id, mplug, _):
        from maya import OpenMaya
        from omtk.libs import libOpenMaya
        from omtk.constants import BLACKLISTED_PORT_NAMES

        dagpath = mplug.name()
        attr_name = dagpath.split('.')[-1]

        # TODO: make it cleaner
        if attr_name in BLACKLISTED_PORT_NAMES:
            log.info('Ignoring callback on {0}'.format(dagpath))
            return

        txt = libOpenMaya.pformat_MNodeMessage_callback(callback_id)  # TODO: evaluate lazily
        log.debug('[_on_port_added_or_removed] %s %s ', mplug.name(), txt)

        # todo: add support for multi attribute added/removed
        if callback_id == OpenMaya.MNodeMessage.kAttributeAdded:
            log.debug("Attribute %s added", dagpath)
            self._callback_port_added(dagpath)

        elif callback_id == OpenMaya.MNodeMessage.kAttributeRemoved:
            log.debug('Attribute %s removed', attr_name)
            self._callback_port_removed(dagpath)

        elif callback_id == OpenMaya.MNodeMessage.kAttributeArrayAdded:
            log.debug('To Implement: kAttributeArrayAdded %s', dagpath)
        elif callback_id == OpenMaya.MNodeMessage.kAttributeArrayRemoved:
            log.warning('To Implement: kAttributeArrayRemoved %s', dagpath)
        elif callback_id == OpenMaya.MNodeMessage.kAttributeRenamed:
            log.warning('To Implement: kAttributeRenamed %s', dagpath)
        elif callback_id == OpenMaya.MNodeMessage.kConnectionMade:
            log.warning('To Implement: kConnectionMade %s', dagpath)
        elif callback_id == OpenMaya.MNodeMessage.kConnectionBroken:
            log.warning('To Implement: kConnectionBroken %s', dagpath)

    def _callback_port_added(self, dagpath):
        import pymel.core as pymel

        # log.debug('Attribute {0} added to {1}'.format(attr_name, obj_name))
        attr = pymel.Attribute(dagpath)
        port = self.get_port(attr)
        self.onPortAdded.emit(attr, port)

    def _callback_port_removed(self, dagpath):
        import pymel.core as pymel
        attr = pymel.Attribute(dagpath)
        port = self.get_port(attr)
        self._unregister_port(port)
        self.onPortRemoved.emit(port)

    def _callback_node_removed(self, node, clientData, *args):
        """
        OpenMaya.MNodeFunction compatible callback.
        This is called everytime a node is removed in Maya.
        :param OpenMaya.MObject node: The node being added.
        :param object clientData: ???
        :return:
        """
        import pymel.core as pymel

        obj = pymel.PyNode(node)
        node = self.get_node(obj)
        self._unregister_node(node)
        self.onNodeDeleted.emit(node)

    # @decorators.log_info
    def _on_attribute_changed(self, callback_id, plug, other_plug, clientData):
        """
        Called when an attribute related to the node change in Maya.
        :param callback_id: maya.OpenMaya.MCallbackId
        :param plug:
        :return:
        """
        from maya import OpenMaya
        from omtk.libs import libOpenMaya

        with self.lock():

            plug_name = plug.name()

            # Ignore evaluation events
            if callback_id & OpenMaya.MNodeMessage.kAttributeEval:
                return

            # Ignore blacklisted attribute
            attr_name = plug_name.split('.')[-1]
            from omtk import constants
            if attr_name in constants.BLACKLISTED_PORT_NAMES:
                return

            log.debug('[addAttributeChangedCallback] {0} {1}'.format(
                plug.name(),
                libOpenMaya.pformat_MNodeMessage_callback(callback_id))
            )

            other_plug_name = other_plug.name()

            if callback_id & OpenMaya.MNodeMessage.kAttributeArrayAdded:
                self._on_attribute_array_added(other_plug_name)
                return

            if callback_id & OpenMaya.MNodeMessage.kConnectionMade:
                if callback_id & OpenMaya.MNodeMessage.kIncomingDirection:  # listen to the destination
                    self._on_connection_made(other_plug_name, plug_name)
                return

            if callback_id & OpenMaya.MNodeMessage.kConnectionBroken:
                self._on_connection_broken(callback_id, other_plug_name, plug_name)
                return

    def _on_connection_broken(self, callback_id, otherPlug_name, plug_name):
        """

        :param callback_id:
        :param otherPlug_name:
        :param plug_name:
        :param component_registry:
        :return:
        """
        import pymel.core as pymel
        from maya import OpenMaya

        if callback_id & OpenMaya.MNodeMessage.kIncomingDirection:  # listen to the destination
            log.info('[addAttributeChangedCallback] kConnectionBroken %s to %s', otherPlug_name, plug_name)
            attr_src = pymel.Attribute(otherPlug_name)
            attr_dst = pymel.Attribute(plug_name)
            port_src = self.get_port(attr_src)
            port_dst = self.get_port(attr_dst)
            connection = self.get_connection(port_src, port_dst)
            self._unregister_connection(connection)
            self.onConnectionRemoved.emit(connection)

    def _on_connection_made(self, otherPlug_name, plug_name):
        """

        :param otherPlug_name:
        :param plug_name:
        :param component_registry:
        :return:
        """
        import pymel.core as pymel

        log.info('[addAttributeChangedCallback] kConnectionMade: %s to %s', otherPlug_name, plug_name)
        attr_src = pymel.Attribute(otherPlug_name)
        attr_dst = pymel.Attribute(plug_name)
        port_src = self.get_port(attr_src)
        port_dst = self.get_port(attr_dst)
        connection = self.get_connection(port_src, port_dst)
        self.onConnectionAdded.emit(connection)

    def _on_attribute_array_added(self, plug_name):
        """

        :param plug_name:
        :param component_registry:
        :return:
        """
        import pymel.core as pymel

        log.debug('[addAttributeChangedCallback] kAttributeArrayAdded %s', plug_name)
        attr = pymel.Attribute(plug_name)
        port = self.get_port(attr)
        self.onPortAdded.emit(port)
        # self._ctrl.callback_attribute_array_added(attr_dagpath)
