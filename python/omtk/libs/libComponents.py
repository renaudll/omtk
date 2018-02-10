import logging
import os
import itertools

import pymel.core as pymel
from omtk.core.component_definition import ComponentDefinition
from omtk.libs import libAttr
from omtk.libs import libPython
from omtk.libs import libRigging
from omtk.vendor import libSerialization

log = logging.getLogger('omtk')


def identify_network_io_ports(objs):
    """
    :param objs: Objects that are part of the network and that will define the bounds.
    :return: Two list of pymel.Attribute delimiting the inputs and outputs of the network.
    """
    all_objs = set(objs)

    # Search for input attributes
    def fn_search(attr, known_nodes, known_attributes, future=True):
        attr_node = attr.node()

        # If we encounter a multi attribute, we'll simply ignore it since it's elements attributes are next.
        # The main reason is that there can not be any connections directly on the multi attribute, calling
        # inputs/outputs on it will return the connections from all it's elements which is not precise.
        if attr.isMulti():
            return False

        plugs = attr.outputs(plugs=True) if future else attr.inputs(plugs=True)
        for plug in plugs:
            # Re-use information from previous scans
            # if plug in known_attributes:
            #     return known_attributes[plug]

            # Ignore self-referencing
            plug_node = plug.node()
            if plug_node == attr_node:
                continue

            if plug_node in all_objs:
                return True

            found = False
            for sub_attr in libAttr.iter_contributing_attributes(plug_node):
                found = fn_search(sub_attr, known_nodes, known_attributes, future=future)
                known_attributes[sub_attr] = found
                if found:
                    break
            known_nodes[plug_node] = found
            if found:
                return True

        return False

    result_out = set()
    result_inn = set()
    for obj in objs:
        known_nodes = {obj: False}
        known_attributes = {}
        for attr in libAttr.iter_contributing_attributes(obj):
            if fn_search(attr, known_nodes, known_attributes, future=True):
                result_inn.add(attr)
    for obj in objs:
        known_nodes = {obj: False}
        known_attributes = {}
        for attr in libAttr.iter_contributing_attributes(obj):
            if fn_search(attr, known_nodes, known_attributes, future=False):
                result_out.add(attr)

    return result_inn, result_out


def optimize_network_io_ports(attrs_inn, attrs_out):
    """
    Try to diminish the number of input and outputs ports by creating auxiliary nodes.
    :param attrs_inn: A list of pymel.Attribute representing the network input attributes.
    :param attrs_out: A list of pymel.Attribute representing the network output attributes.
    :return: Two list of pymel.Attribute representing the network optimized input and output attributes.
    """
    raise NotImplementedError


class MultipleComponentDefinitionError(Exception):
    """Raised when two component with the same uid and version are found."""


def get_component_dir():
    """Return the directory to save component to."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'components'))


def walk_available_component_definitions(search_scripted=True):
    # todo: clearly define where are the components in omtk
    path_component_dir = get_component_dir()
    if not os.path.exists(path_component_dir):
        raise Exception()
    paths = [path_component_dir]

    known = set()

    for dirname in paths:
        log.debug('Searching component in {0}'.format(dirname))
        if os.path.exists(dirname):
            for filename in os.listdir(dirname):
                basename, ext = os.path.splitext(filename)
                if ext != '.ma':
                    continue
                path = os.path.join(dirname, filename)

                log.debug('Creating ComponentDefinition from {0}'.format(path))
                component_def = ComponentDefinition.from_file(path)
                if not component_def:
                    continue

                key = hash((component_def.uid, component_def.version))
                if key in known:
                    raise MultipleComponentDefinitionError(
                        "Found more than two component with the same uid and version: {0}".format(
                            component_def
                        )
                    )
                known.add(key)

                log.debug('Registering {0} from {1}'.format(component_def, path))
                yield component_def

    from omtk.core import plugin_manager
    pm = plugin_manager.plugin_manager

    if search_scripted:
        log.info("Searching ComponentScripted")
        for plugin in pm.get_loaded_plugins_by_type(plugin_manager.ComponentScriptedType.type_name):
            component_def = plugin.cls.get_definition()
            log.debug('Registering {0} from {1}'.format(component_def, plugin))
            yield component_def

    log.info("Searching modules")
    for plugin in pm.get_loaded_plugins_by_type(plugin_manager.ModulePluginType.type_name):
        try:
            component_def = plugin.cls.get_definition()
        except AttributeError, e:
            log.warning("Error obtaining plugin class definition for {0}: {1}".format(plugin, e))
            continue
        log.debug('Registering {0} from {1}'.format(component_def, plugin))
        yield component_def

from omtk import decorators


class BrokenComponentError(Exception):
    """Raised when something fail because a node is inside and outside of a component at the same time."""




def get_component_network_bounds():
    """
    Return the metadata of the component parent of the provided component, starting from any object.
    :param obj: A pymel.nodetypes.Network representing the output of a component.
    :param cache: Initialized internally.
    :return: A pymel.nodetypes.Network that can be deserialized.
    """
    component_network_by_hub_inn = {}
    component_network_by_hub_out = {}
    networks = libSerialization.get_networks_from_class('Component')
    for network in networks:
        grp_inn = next(iter(network.attr('grp_inn').inputs()), None)
        if grp_inn:
            component_network_by_hub_inn[grp_inn] = network
        grp_out = next(iter(network.attr('grp_out').inputs()), None)
        if grp_out:
            component_network_by_hub_out[grp_out] = network
    return component_network_by_hub_inn, component_network_by_hub_out


def get_component_metanetwork_from_hub_network(network, strict=True):
    def _filter(net):
        return libSerialization.is_network_from_class(net, 'Component')
    result = next(iter(libSerialization.get_connected_networks(network, key=_filter, recursive=False)), None)
    if not result and strict:
        raise Exception("Can't resolve meta-network from {0}".format(network))
    return result


def get_inn_network_from_metadata_network(network, strict=True):
    try:
        result = next(iter(network.grp_inn.inputs()), None)
    except AttributeError:
        result = None
    if not result and strict:
        raise Exception("Can't resolve input network from meta-network {0}".format(network))
    return result


def get_inn_network_from_out_network(network, strict=True):
    metanetwork = get_component_metanetwork_from_hub_network(network, strict=strict)
    result = get_inn_network_from_metadata_network(metanetwork, strict=strict)
    return result


def get_out_network_from_metanetwork(network, strict=True):
    try:
        result = next(iter(network.grp_out.inputs()), None)
    except AttributeError:
        result = None
    if not result and strict:
        raise Exception("Can't resolve input network from meta-network {0}".format(network))
    return result


def get_out_network_from_inn_network(network, strict=True):
    metanetwork = get_component_metanetwork_from_hub_network(network, strict=True)
    result = get_out_network_from_metanetwork(metanetwork, strict=strict)
    return result


class ComponentMetanetworkRole:
    NoRole = 0
    Inn = 1
    Out = 2


# todo: cache this?
def get_metanetwork_role(obj):
    # if not isinstance(obj, pymel.nodetypes.Network):
    #     return ComponentMetanetworkRole.NoRole
    network = get_component_metanetwork_from_hub_network(obj, strict=False)
    if not network:
        return ComponentMetanetworkRole.NoRole
    net_inn = get_inn_network_from_metadata_network(network, strict=False)
    if net_inn == obj:
        return ComponentMetanetworkRole.Inn
    net_out = get_out_network_from_metanetwork(network, strict=False)
    if net_out == obj:
        return ComponentMetanetworkRole.Out
    return ComponentMetanetworkRole.NoRole


def get_component_parent_network(obj, source=True, destination=True, cache=None, strict=False):
    """
    Return the metadata of the component parent of the provided component, optimized for starting at the input network.
    :param obj: A pymel.nodetypes.Network representing the output of a component.
    :param cache: Initialized internally.
    :return: A pymel.nodetypes.Network that can be deserialized.
    """
    component_network_by_hub_inn, component_network_by_hub_out = get_component_network_bounds()

    def _fn_goal_inn(n):
        return n in component_network_by_hub_inn and n is not obj

    def _fn_goal_out(n):
        return n in component_network_by_hub_out and n is not obj

    def _fn_explore_inn(n):
        if n in component_network_by_hub_out:
            n = get_inn_network_from_out_network(n, strict=True)
        return pymel.listConnections(n, source=True, destination=False, skipConversionNodes=True)

    # When searching for the right-side bound, we expect to encounter an output.
    # If we encounter an component input network, this mean that this is a subcomponent and
    # we can switch directly to it's outputs.
    def _fn_explore_out(n):
        if n in component_network_by_hub_inn:
            n = get_out_network_from_inn_network(n, strict=True)
        return pymel.listConnections(n, source=False, destination=True, skipConversionNodes=True)

    # Keep track of the nodes we encounter while exploring.
    # We'll add them to the cache since they are also between the same hub networks.
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
            msg = "Found partial component bound for {0}. Input is {1}, output is {2}.".format(
                obj, hub_inn, hub_out
            )
            if strict:
                raise Exception(msg)
            else:
                log.warning(msg)
        return hub_inn, hub_out

    # Validate that we found two hub from the same component.
    # If that's not the case, it might be that something is wrong with the component setup
    # or that we are following connections that we didn't expected.
    meta_network_inn = get_component_metanetwork_from_hub_network(hub_inn, strict=True)
    meta_network_out = get_component_metanetwork_from_hub_network(hub_out, strict=True)
    if meta_network_inn != meta_network_out:
        raise Exception(
            "Found bounds are not part of the same metanetwork. " +
            "Input network {0} is part of {1}.".format(hub_inn, meta_network_inn) +
            "Output network {0} is part of {1}.".format(hub_out, meta_network_out)
        )
    return hub_inn, hub_out


def create_component_from_bounds(objs):
    """Initialize an unregistred Compound from objects defining the bounds."""
    input_attrs, output_attrs = identify_network_io_ports(objs)

    from omtk.core.component import Component
    inst = Component.from_attributes(input_attrs, output_attrs)

    return inst


def create_component(component_cls, name=None, **kwargs):
    inst = component_cls()
    inst.build()
    grp_inn = inst.grp_inn
    grp_out = inst.grp_out
    for sAttrName, pAttrValue in kwargs.iteritems():
        if grp_inn.hasAttr(sAttrName):
            libRigging.connect_or_set_attr(grp_inn.attr(sAttrName), pAttrValue)
        elif grp_out.hasAttr(sAttrName):
            libRigging.connect_or_set_attr(grp_out.attr(sAttrName), pAttrValue)
        else:
            raise Exception(
                '[CreateUtilityNode] UtilityNode {0} doesn\'t have an {1} attribute.'.format(inst, sAttrName))
    return inst


def get_component_class_by_name(name, strict=False):
    # type: (str) -> ComponentDefinition
    for cls in walk_available_component_definitions():
        if cls.name == name:
            return cls
    if strict:
        raise Exception("Cannot find component with name: {0}".format(name))


def get_component_class_by_uid(uid, strict=False):
    # type: (int) -> ComponentDefinition
    for cls in walk_available_component_definitions():
        if cls.uid == uid:
            return cls
    if strict:
        raise Exception("Cannot find component with uid: {0}".format(uid))


def _connect_component_attributes(inst, map_inn=None, map_out=None):
    if map_inn:
        for attr_name, attr_val in map_inn.iteritems():
            if not inst.has_input_attr(attr_name):
                raise Exception("Component {0} don't have an {1} input attribute.".format(
                    inst, attr_name)
                )
            attr = inst.get_input_attr(attr_name)
            libRigging.connect_or_set_attr(attr, attr_val)

    # todo: we are not supposed to set an output
    # however we can connect it, make the distinction clear by
    # raising an exception if needed
    if map_out:
        for attr_name, attr_val in map_out.iteritems():
            if not inst.has_output_attr(attr_name):
                raise Exception("Component {0} don't have an {1} output attribute.".format(
                    inst, attr_name)
                )
            attr = inst.get_output_attr(attr_name)
            libRigging.connect_or_set_attr(attr, attr_val)


def create_component_by_name(name, map_inn=None, map_out=None):
    """
    Flexible method to create and configure a component in one call.
    :param name: The name of the component to create.
    :param map_inn: A dict{k:v} where k is the attribute and v is the attribute value.
    :param map_out: A dict{k:v} where k is the attribute and v is the attribute value.
    :return: A Component instance.
    """
    cls = get_component_class_by_name(name, strict=True)
    inst = cls.instanciate(map_inn=map_inn, map_out=map_out)  # todo: clean constructor signature
    return inst


def create_component_by_uid(uid, map_inn=None, map_out=None):
    """
    Flexible method to create and configure a component in one call.
    :param name: The name of the component to create.
    :param map_inn: A dict{k:v} where k is the attribute and v is the attribute value.
    :param map_out: A dict{k:v} where k is the attribute and v is the attribute value.
    :return: A Component instance.
    """
    cls = get_component_class_by_uid(uid, strict=True)
    inst = cls.instanciate(map_inn=map_inn, map_out=map_out)  # todo: clean constructor signature
    return inst
