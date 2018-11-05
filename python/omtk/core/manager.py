import logging
from collections import defaultdict

from omtk import decorators
from omtk import constants
from omtk.core import preferences
from omtk.vendor import libSerialization
from omtk.vendor.Qt import QtCore
from omtk.vendor.libSerialization import cache as libSerializationCache

log = logging.getLogger(__name__)


class ComponentCache(object):
    """
    Speedup some component related queries by caching.
    """
    def __init__(self, parent):
        self._component_network_by_hub_inn = {}
        self._component_network_by_hub_out = {}
        self._component_by_namespace = {}
        self._cache_parent_by_node = {}
        self._cache_nodes_by_parent = defaultdict(set)
        self._session = parent

        self.init_cache()

    def init_cache(self):
        from omtk.libs import libComponents
        self._cache_parent_by_node = {}
        self._cache_nodes_by_parent = defaultdict(set)
        self._component_by_metadata = {}
        self._component_network_by_hub_inn = {}
        self._component_network_by_hub_out = {}
        self._component_by_namespace = {}

        for component in libComponents.iter_components():
            self.add_component_to_cache(component)

    def add_component_to_cache(self, component):

        # Hack: Add the component metadata node to the cache.
        # TODO: Remove this extra node, we want to keep thing as simple as possible.
        # Considering that a component always have an inn and out node, we should put the metadata here.
        # However for now we'll simply handle it.
        # self._component_network_by_metdata[component]
        for metadata in component.grp_inn.message.outputs():
            self._component_by_metadata[metadata] = component
            self._cache_parent_by_node[metadata] = component

        self._component_network_by_hub_inn[component.grp_inn] = component
        self._component_network_by_hub_out[component.grp_out] = component
        self._component_by_namespace[component.namespace] = component

        for child in component.get_children():
            self._cache_parent_by_node[child] = component
            self._cache_nodes_by_parent[component].add(child)

    # def get_component_from_namespace(self, namespace):
    #     # type: (str) -> Component
    #     return self._component_by_namespace.get(namespace, None)

    def get_component_from_obj(self, obj):
        try:
            return self._cache_parent_by_node[obj]
        except KeyError:
            val = self._get_node_parent(obj)
            self._cache_parent_by_node[obj] = val  # cache will update by itself
            self._cache_nodes_by_parent[val].add(obj)
            return val

    def get_component_from_input_hub(self, obj):
        """
        Return the component associated with an input hub.
        :param pymel.nodetypes.DependNode obj: An object that is used as input hub.
        :return: The associated Component or None if the provided object is not an input hub.
        :rtype Component or None
        """
        return self._component_network_by_hub_inn.get(obj, None)

    def get_component_from_output_hub(self, obj):
        """
        Return the component associated with an output hub.
        :param pymel.nodetypes.DependNode obj: An object that is used as output hub.
        :return: The associated Component or None if the provided object is not an output hub.
        :rtype: Component or None
        """
        return self._component_network_by_hub_out.get(obj, None)

    def get_component_from_metadata(self, obj):
        return self._component_by_metadata.get(obj)

    def _get_node_parent(self, obj):
        """
        Return the metadata of the component parent of the provided component, optimized for starting at the input network.
        :param obj: A pymel.nodetypes.Network representing the output of a component.
        :return: A pymel.nodetypes.Network that can be deserialized.
        """
        namespace = obj.namespace().strip(':')
        return self.get_component_from_namespace(namespace)

    def get_component_from_namespace(self, namespace):
        return self._component_by_namespace.get(namespace)


class AutoRigManager(QtCore.QObject):
    """
    Manager class that old the current user session."""
    # todo: move OmtkUI class logic to the manager and implement unit tests

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
        Fill the component registry with any serialized _known_definitions in the scene.
        """
        from omtk import component
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
        import pymel.core as pymel
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

    def get_component_from_obj(self, obj):
        """

        :param pymel.PyNode obj:
        :return:
        :rtype: Component
        """
        namespace = obj.namespace().strip(':')

        # A namespace might not be associated with a component but it's parent might.
        # For this reason we'll try each possibilities, ex:
        # - a:b:c
        # - a:b
        # - a
        tokens = namespace.split(':')
        for i in reversed(range(len(tokens))):
            namespace = ':'.join(tokens[:i+1])
            component = self._cache_components.get_component_from_namespace(namespace)
            if component:
                return component

    def get_component_from_input_hub(self, obj):
        """
        Return the component associated with an input hub.
        :param pymel.nodetypes.DependNode obj: An object that is used as input hub.
        :return: The associated Component or None if the provided object is not an input hub.
        :rtype Component or None
        """
        return self._cache_components.get_component_from_input_hub(obj)

    def get_component_from_output_hub(self, obj):
        """
        Return the component associated with an output hub.
        :param pymel.nodetypes.DependNode obj: An object that is used as output hub.
        :return: The associated Component or None if the provided object is not an output hub.
        :rtype: Component, None
        """
        return self._cache_components.get_component_from_output_hub(obj)

    def get_component_from_metadata(self, obj):
        return self._cache_components.get_component_from_metadata(obj)

    def get_component_from_namespace(self, namespace):
        return self._cache_components.get_component_from_namespace(namespace)

    def _register_new_component(self, component):
        self._cache_components.add_component_to_cache(component)


@decorators.memoized
def get_session():
    """

    :return:
    :rtype: AutoRigManager
    """
    return AutoRigManager()
