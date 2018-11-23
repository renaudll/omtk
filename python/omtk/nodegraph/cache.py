from collections import defaultdict

import logging
from omtk.nodegraph.signal import Signal

log = logging.getLogger(__name__)


class Cache(object):
    onRegistered = Signal(object)
    onUnregistered = Signal(object)

    def __init__(self):
        super(Cache, self).__init__()

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


class CachedDefaultDict(Cache):
    def __init__(self, type_):
        super(CachedDefaultDict, self).__init__()
        self._map = defaultdict(type_)


class NodeCache(Cache):
    def unregister(self, node_model):
        super(NodeCache, self).unregister(node_model)



class PortCache(Cache):
    pass


class ConnectionCache(Cache):
    pass
