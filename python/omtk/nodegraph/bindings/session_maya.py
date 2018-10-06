from collections import defaultdict

from pymel import core as pymel
from maya import OpenMaya

import omtk.constants
from omtk.libs import libOpenMaya
from omtk.nodegraph.nodegraph_registry import log
from omtk.nodegraph.bindings.base import ISession


# TODO: Add mutex when loading a new scene?
# TODO: Remove dependence on registry? We have signals for this.

class MayaSession(ISession):
    """
    Interface between the registry and a Maya session.
    :param NodeGraphRegistry registry: A registry to bind to the session.
    """
    def __init__(self, registry=None):
        super(MayaSession, self).__init__(registry)

        self._mutex = True  # If False, Maya events are ignored.

        self._callback_attribute_added_or_removed = None
        self._callback_attribute_changed = None
        self._callback_id_node_removed = None
        self._callback_id_by_node = defaultdict(set)

    def add_node_callbacks(self, node):
        """
        Called when a node is atted to the registry bound to the DCC application or mock. ???
        :param NodeModel node: The node being add to the registry.
        """
        mobject = node.get_metadata().__apimobject__()

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

    def add_callbacks(self):
        """
        Add callbacks to maya so what we are notify of general events.
        """
        pass
        # self._callback_id_node_removed = OpenMaya.MDGMessage.addNodeRemovedCallback(
        #     self._callback_node_removed, "dependNode")

    def remove_node_callbacks(self, node):
        """
        :param NodeModel node:
        :return:
        """
        callback_ids = self._callback_id_by_node.get(node)
        if callback_ids is None:
            log.debug("Cannot remove callback. No callback set for {0}.".format(node))
            return

        for callback_id in callback_ids:
            OpenMaya.MNodeMessage.removeCallback(callback_id)

        self._callback_id_by_node.pop(node)

    def remove_callbacks(self):
        if self._callback_id_node_removed is not None:
            OpenMaya.MNodeMessage.removeCallback(self._callback_id_node_removed)

        for node in self._callback_id_by_node.keys():
            self.remove_node_callbacks(node)

        self._callback_id_by_node.clear()

        assert (len(self._callback_id_by_node) == 0)  # should be empty

    def _on_port_added_or_removed(self, callback_id, mplug, _):
        registry = self.registry

        dagpath = mplug.name()
        attr_name = dagpath.split('.')[-1]

        # TODO: make it cleaner
        if attr_name in omtk.constants._attr_name_blacklist:
            log.info('Ignoring callback on {0}'.format(dagpath))
            return

        txt = libOpenMaya.pformat_MNodeMessage_callback(callback_id)  # TODO: evaluate lazily
        log.debug('[_on_port_added_or_removed] %s %s ', mplug.name(), txt)

        # todo: add support for multi attribute added/removed
        if callback_id == OpenMaya.MNodeMessage.kAttributeAdded:
            log.debug("Attribute %s added", dagpath)
            self._callback_port_added(dagpath, registry)

        elif callback_id == OpenMaya.MNodeMessage.kAttributeRemoved:
            log.debug('Attribute %s removed', attr_name)
            self._callback_port_removed(dagpath, registry)

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

    def _callback_port_added(self, dagpath, registry):
        # log.debug('Attribute {0} added to {1}'.format(attr_name, obj_name))
        attr = pymel.Attribute(dagpath)
        port = registry.get_port(attr)
        # registry.onPortAdded.emit(port)
        self.portAdded.emit(attr, port)

    def _callback_port_removed(self, dagpath, registry):
        attr = pymel.Attribute(dagpath)
        port = registry.get_port(attr)
        self.portRemoved.emit(port)

    def _callback_node_removed(self, node, clientData, *args):
        """
        OpenMaya.MNodeFunction compatible callback.
        This is called everytime a node is removed in Maya.
        :param OpenMaya.MObject node: The node being added.
        :param object clientData: ???
        :return:
        """
        registry = self.registry
        obj = pymel.PyNode(node)
        node = registry.get_node(obj)
        self.nodeRemoved.emit(node)

    # @decorators.log_info
    def _on_attribute_changed(self, callback_id, plug, otherPlug, clientData):
        """
        Called when an attribute related to the node change in Maya.
        :param callback_id:
        :param plug:
        :return:
        """
        registry = self.registry

        # When we receive an event from Maya, we update our internal data in consequence.
        # We are not suppose to modify the scene while inside a callback.
        # However a lot of things in Maya can modify the scene even if we are just looking at some data.
        # (ex: accidentally initializing an empty array plug by looking at it's type using Pymel)
        # If this happen, we'll raise a warning but refuse to go further to prevent any potential loop.
        # if not self._mutex:
        #     # log.warning("Ignoring nested callbacks {0}: {1}".format(plug_name, libOpenMaya.pformat_MNodeMessage_callback(callback_id)))
        #     return

        self._mutex = False

        plug_name = plug.name()

        # Ignore evaluation events
        if callback_id & OpenMaya.MNodeMessage.kAttributeEval:
            return

        # Ignore blacklisted attribute
        attr_name = plug_name.split('.')[-1]
        from omtk import constants
        if attr_name in constants._attr_name_blacklist:
            return

        log.debug('[addAttributeChangedCallback] {0} {1}'.format(plug.name(), libOpenMaya.pformat_MNodeMessage_callback(callback_id)))

        if callback_id & OpenMaya.MNodeMessage.kAttributeArrayAdded:
            log.debug('[addAttributeChangedCallback] kAttributeArrayAdded %s', plug_name)
            attr = pymel.Attribute(plug_name)
            port = registry.get_port(attr)
            registry.onPortAdded.emit(port)
            # self._ctrl.callback_attribute_array_added(attr_dagpath)

        elif callback_id & OpenMaya.MNodeMessage.kConnectionMade:
            otherPlug_name = otherPlug.name()
            if callback_id & OpenMaya.MNodeMessage.kIncomingDirection:  # listen to the destination
                log.info('[addAttributeChangedCallback] kConnectionMade: %s to %s', otherPlug_name, plug_name)
                attr_src = pymel.Attribute(otherPlug_name)
                attr_dst = pymel.Attribute(plug_name)
                port_src = registry.get_port(attr_src)
                port_dst = registry.get_port(attr_dst)
                connection = registry.get_connection(port_src, port_dst)
                self.connectionAdded.emit(connection)

        elif callback_id & OpenMaya.MNodeMessage.kConnectionBroken:
            otherPlug_name = otherPlug.name()
            if callback_id & OpenMaya.MNodeMessage.kIncomingDirection:  # listen to the destination
                log.info('[addAttributeChangedCallback] kConnectionBroken %s to %s', otherPlug_name, plug_name)
                attr_src = pymel.Attribute(otherPlug_name)
                attr_dst = pymel.Attribute(plug_name)
                port_src = registry.get_port(attr_src)
                port_dst = registry.get_port(attr_dst)
                connection = registry.get_connection(port_src, port_dst)
                self.connectionRemoved.emit(connection)

        self._mutex = True

