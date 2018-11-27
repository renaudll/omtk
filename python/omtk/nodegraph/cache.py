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

    def __contains__(self, item):
        return item in self._map

    def __len__(self):
        return len(self._map)

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
        Unregister a resource
        :param object key: A registered value or a registered key.
        :raise LookupError: When the resource is not registered.
        """
        log.debug("Registering %s", key)

        val = self._map_inv.pop(key, None)
        if val:
            self._map.pop(val, None)

        val = self._map.pop(key, None)
        if val:
            self._map_inv.pop(val, None)

    # --- Access methods ---

    def get(self, key):
        return self._map[key]

    def get_key(self, val):
        return self._map_inv[val]

    def keys(self):
        return self._map.keys()


class CachedDefaultDict(Cache):
    def __init__(self, type_):
        super(CachedDefaultDict, self).__init__()
        self._map = defaultdict(type_)

    def register(self, key, val):
        self._map[key].add(val)
        self._map_inv[val] = key

    def unregister(self, key):
        vals = self._map.pop(key, None)
        if vals:
            for val in vals:
                self._map_inv.pop(val, None)

    def unregister_val(self, key, val):
        container = self._map.get(key)
        if not container:
            return

        container.discard(val)
        # If there's no more entry, remove the set
        if not container:
            self._map.pop(key)


class NodeCache(Cache):
    pass


class PortCache(Cache):
    pass


class ConnectionCache(Cache):
    pass
