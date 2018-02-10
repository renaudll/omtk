import logging
from collections import defaultdict
import itertools

from omtk import decorators
import pymel.core as pymel
from omtk import constants
from omtk.core import preferences
from omtk.libs import libPython
from omtk.libs import libComponents
from omtk.vendor import libSerialization
from omtk.vendor.Qt import QtCore
from omtk.vendor.libSerialization import cache as libSerializationCache

log = logging.getLogger('omtk')




class ComponentCache(object):
    """
    Speedup some component related queries by caching.
    """
    def __init__(self, parent):
        self._component_network_by_hub_inn = {}
        self._component_network_by_hub_out = {}
        self._cache_parent_by_node = {}
        self._cache_nodes_by_parent = defaultdict(set)
        self._session = parent

        self.init_cache()

    def init_cache(self):
        self._cache_parent_by_node = {}
        self._cache_nodes_by_parent = defaultdict(set)
        self._component_network_by_hub_inn, self._component_network_by_hub_out = libComponents.get_component_network_bounds()

    def get_node_parent(self, obj):
        try:
            return self._cache_parent_by_node[obj]
        except KeyError:
            val = self._get_node_parent(obj)
            self._cache_parent_by_node[obj] = val  # cache will update by itself
            self._cache_nodes_by_parent[val].add(obj)
            return val

    def _get_node_parent(self, obj):
        """
        Return the metadata of the component parent of the provided component, optimized for starting at the input network.
        :param obj: A pymel.nodetypes.Network representing the output of a component.
        :param cache: Initialized internally.
        :return: A pymel.nodetypes.Network that can be deserialized.
        """
        def _fn_goal_inn(n):
            return n in self._component_network_by_hub_inn and n is not obj

        def _fn_goal_out(n):
            return n in self._component_network_by_hub_out and n is not obj

        def _fn_explore_inn(n):
            if n in self._component_network_by_hub_out:
                n = libComponents.get_inn_network_from_out_network(n, strict=True)
            return pymel.listConnections(n, source=True, destination=False, skipConversionNodes=True)

        # When searching for the right-side bound, we expect to encounter an output.
        # If we encounter an component input network, this mean that this is a subcomponent and
        # we can switch directly to it's outputs.
        def _fn_explore_out(n):
            if n in self._component_network_by_hub_inn:
                n = libComponents.get_out_network_from_inn_network(n, strict=True)
            return pymel.listConnections(n, source=False, destination=True, skipConversionNodes=True)

        known_inn = set()
        known_out = set()

        try:
            hub_inn = next(reversed(libPython.id_dfs(obj, _fn_goal_inn, _fn_explore_inn, known=known_inn)), None)
        except StopIteration:
            hub_inn = None
        try:
            hub_out = next(reversed(libPython.id_dfs(obj, _fn_goal_out, _fn_explore_out, known=known_out)), None)
        except StopIteration:
            hub_out = None

        if hub_inn is None or hub_out is None:
            if hub_inn != hub_out:
                raise libComponents.BrokenComponentError("Found partial component bound for {0}. Input is {1}, output is {2}.".format(
                    obj, hub_inn, hub_out
                ))
            return None

        # Validate that we found two hub from the same component.
        # If that's not the case, it might be that something is wrong with the component setup
        # or that we are following connections that we didn't expected.
        meta_network_inn = libComponents.get_component_metanetwork_from_hub_network(hub_inn, strict=True)
        meta_network_out = libComponents.get_component_metanetwork_from_hub_network(hub_out, strict=True)
        if meta_network_inn != meta_network_out:
            raise libComponents.BrokenComponentError(
                "Found bounds are not part of the same metanetwork. " +
                "Input network {0} is part of {1}.".format(hub_inn, meta_network_inn) +
                "Output network {0} is part of {1}.".format(hub_out, meta_network_out)
            )

        net = libComponents.get_component_metanetwork_from_hub_network(hub_inn)
        if not net:
            raise libComponents.BrokenComponentError("Cannot resolve component from {0}".format(hub_inn))

        inst = self._session.import_network(net)

        # Ok, we got something, for speed purpose set the cache for all the nodes we explored.
        for node in itertools.chain(known_inn, known_out):
            if node not in self._cache_parent_by_node:
                self._cache_parent_by_node[node] = inst
                self._cache_nodes_by_parent[inst].add(node)

        return inst


class AutoRigManager(QtCore.QObject):
    """
    Manager class that old the current user session."""
    # todo: move AutoRig class logic to the manager and implement unit tests

    # Used when a new Rig instance is added to the scene.
    onRigCreated = QtCore.Signal(object)

    onComponentCreated = QtCore.Signal(object)

    # Trigger a complete redraw
    onSceneChanged = QtCore.Signal()

    def __init__(self):
        super(AutoRigManager, self).__init__()
        self._root = None
        self._roots = []

        self._components = []

        self.preferences = preferences.get_preferences()

        # Initialize libSerialization cache.
        # This will allow to re-use data.
        # Note that we will reset the cache at each import.
        self._cache_serialization = None
        self.clear_cache_serialization()

        self._cache_components = ComponentCache(self)

        # Note: This should be done in a lazy way and linked to the current scene.
        self.import_components()

        self.import_networks()

    def _add_rig(self, rig):
        self._roots.append(rig)
        if self._root is None:
            self._root = next(iter(self._roots), None)
        libSerialization.export_network(rig, cache=self._cache_serialization)

    def clear_cache_serialization(self):
        self._cache_serialization = libSerializationCache.Cache()

    def clear_cache_components(self):
        return self._cache_components.init_cache()

    def import_components(self):
        """
        Fill the component registry with any serialized components in the scene.
        """
        from omtk.core import component
        cls_name = component.Component.__name__
        networks = libSerialization.get_networks_from_class(cls_name)
        results = [libSerialization.import_network(network, module='omtk', cache=self._cache_serialization) for network
                   in networks]
        results = filter(None, results)
        self._components = results
        return results

    def import_network(self, network, **kwargs):
        return libSerialization.import_network(network, cache=self._cache_serialization, **kwargs)

    def export_network(self, data, **kwargs):
        return libSerialization.export_network(data, cache=self._cache_serialization, **kwargs)

    def import_networks(self):
        """
        Re-import everything from the scene.
        Warning, this is a SLOW operation.
        :return:
        """
        from omtk.vendor.libSerialization import cache
        from omtk import api
        self._cache_serialization = cache.Cache()
        self._roots = api.find(cache=self._cache_serialization)
        self._root = next(iter(self._roots), None)

    def export_networks(self):
        """
        Re-export everything in the scene.
        Warning, this is a SLOW operation.
        :return:
        """
        for root in self._roots:
            try:
                network = root._network
                if network and network.exists():
                    pymel.delete(network)
            except AttributeError:
                pass

        self.clear_cache_serialization()
        for root in self._roots:
            self.export_network(root)

    def get_rigs(self):
        return self._roots

    def create_rig(self, rig_type=None):
        # todo: ensure api use this
        from omtk import api

        if rig_type is None:
            # todo: get default rig definition
            raise NotImplementedError
        # rig_type = self.get_selected_rig_definition()

        # Initialize the scene
        rig_ = api.create(cls=rig_type)
        rig_.build()
        self._add_rig(rig_)
        libSerialization.export_network(rig_)

        self.onRigCreated.emit(rig_)

        return rig_

    def create_component(self, component_def):
        """
        Main entry point for initialization of a new Component.
        Ensure that the session cache is updated accordingly.
        :param component_def: A ComponentDefinition.
        :return:
        """
        # todo: ensure api use this
        inst = component_def.instanciate()

        # todo: update part of the cache, not the whole cache
        self.clear_cache_components()

        return inst


    def execute_actions(self, actions):
        need_export_network = False
        # entities = self.get_selected_components()
        # action_map = self._get_actions(entities)
        for action in actions:
            action.execute()
            if constants.ComponentActionFlags.trigger_network_export in action.iter_flags():
                need_export_network = True

        if need_export_network:
            self.export_networks()

            self.onSceneChanged.emit()
            # todo: update node editor?


@decorators.memoized
def get_session():
    # type: () -> AutoRigManager
    return AutoRigManager()
