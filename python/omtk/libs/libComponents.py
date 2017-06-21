import os
import logging

import pymel.core as pymel
from omtk.core.classComponentDefinition import ComponentDefinition
from omtk.libs import libAttr

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
            for sub_attr in libAttr.iter_interesting_attributes(plug_node):
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
        for attr in libAttr.iter_interesting_attributes(obj):
            if fn_search(attr, known_nodes, known_attributes, future=True):
                result_inn.add(attr)
    for obj in objs:
        known_nodes = {obj: False}
        known_attributes = {}
        for attr in libAttr.iter_interesting_attributes(obj):
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


# def create_component(objs):
#     attrs_inn, attrs_out = identify_network_io_ports(objs)
#     if not attrs_inn:
#         raise Exception("Found no inputs")
#     if not attrs_out:
#         raise Exception("Found no outputs")
#
#     hub_inn, hub_out = isolate_network_io_ports(attrs_inn, attrs_out, isolate=True)
#
#     module = Module2()
#     module.grp_inn = hub_inn
#     module.grp_out = hub_out
#
#     network = libSerialization.export_network(module)
#     pymel.select(network)
#
#     return module


class MultipleComponentDefinitionError(Exception):
    """Raised when two component with the same uid and version are found."""


def walk_available_component_definitions():
    # todo: clearly define where are the components in omtk
    path_component_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'components')
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

                log.debug('Creating component from {0}'.format(path))
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

                yield component_def


from omtk.vendor import libSerialization
from omtk.libs import libPython


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
    result = next(iter(libSerialization.get_connected_networks(network)), None)
    if not result and strict:
        raise Exception("Can't resolve meta-network from {0}".format(network))
    return result


def get_inn_network_from_out_network(network, strict=True):
    metanetwork = get_component_metanetwork_from_hub_network(network, strict=strict)
    result = next(iter(metanetwork.grp_inn.inputs()), None)
    if not result and strict:
        raise Exception("Can't resolve input network from meta-network {0}".format(network))
    return result


def get_out_network_from_inn_network(network, strict=True):
    metanetwork = get_component_metanetwork_from_hub_network(network, strict=True)
    result = next(iter(metanetwork.grp_out.inputs()), None)
    if not result and strict:
        raise Exception("Can't resolve input network from meta-network {0}".format(network))
    return result


def get_component_parent_network(obj, source=True, destination=True, cache=None):
    """
    Return the metadata of the component parent of the provided component, optimized for starting at the input network.
    :param obj: A pymel.nodetypes.Network representing the output of a component.
    :param cache: Initialized internally.
    :return: A pymel.nodetypes.Network that can be deserialized.
    """
    component_network_by_hub_inn, component_network_by_hub_out = get_component_network_bounds()

    def _fn_goal_inn(n):
        return n in component_network_by_hub_inn

    def _fn_goal_out(n):
        return n in component_network_by_hub_out

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

    try:
        hub_inn = next(reversed(libPython.id_dfs(obj, _fn_goal_inn, _fn_explore_inn)), None)
    except StopIteration:
        hub_inn = None
    try:
        hub_out = next(reversed(libPython.id_dfs(obj, _fn_goal_out, _fn_explore_out)), None)
    except StopIteration:
        hub_out = None

    if hub_inn is None or hub_inn is None:
        if hub_inn != hub_out:
            raise Exception("Found partial component bound. Input is {0}, output is {1}.".format(
                hub_inn, hub_out
            ))
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
