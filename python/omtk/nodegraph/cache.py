from collections import defaultdict

import logging

from omtk.core import manager
from omtk.vendor.Qt import QtCore

log = logging.getLogger(__name__)


class Cache(QtCore.QObject):
    onRegistered = QtCore.Signal(object)
    onUnregistered = QtCore.Signal(object)

    def __init__(self, registry):  # note: registry might be temp
        super(Cache, self).__init__()  # QObject.__init__
        self._registry = registry

        # Note that we use two dictionary instead of a two-way dictionary.
        # This is because key and val can share the same hash.
        # This is undesirable but possible (ex: A NodeGraphComponentModel hash is the Component hash).
        self._map = {}
        self._map_inv = {}

    def register(self, key, val):
        """
        Register a ressource
        :param object key:
        :param object val:
        :return:
        """
        self._map[key] = val  # All the node to the
        self._map_inv[val] = key

    def unregister(self, key):
        """
        Unregister a ressource
        :param omtk.nodegraph.NodeModel key: An instance or the key to an instance.
        :raise LookupError: When the resource is not registered.
        """
        log.debug("Registering %s", key)
        val = self._map.pop(key, None)
        self._map_inv.pop(val, None)

    # --- Access methods ---

    def get(self, key):
        return self._map[key]

    def get_key(self, val):
        return self._map_inv[val]


class CacheDefaultDict(Cache):
    def __init__(self, registry, type_):
        super(CacheDefaultDict, self).__init__(registry)
        self._map = defaultdict(type_)


class NodeCache(Cache):
    def unregister(self, node_model):
        # session = manager.get_session()
        session = self._registry.session

        super(NodeCache, self).unregister(node_model)

        # remove callbacks
        if session:
            session.remove_node_callbacks(node_model)


class PortCache(Cache):
    pass


class ConnectionCache(Cache):
    pass
