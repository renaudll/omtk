import itertools
import os

import pymel.core as pymel
from maya import cmds
from omtk.core.classComponentDefinition import ComponentDefinition
from omtk.libs import libAttr

_HUB_INN_NAME = 'hub_inn'
_HUB_OUT_NAME = 'hub_out'


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


def _escape_attr_name(attr_name):
    return attr_name.replace('[', '_').replace(']', '_')


def _get_unique_attr_name(obj, attr_name):
    if not obj.hasAttr(attr_name):
        return attr_name
    for i in itertools.count():
        new_attr_name = attr_name + str(i)
        if not obj.hasAttr(new_attr_name):
            return new_attr_name


def _get_all_namespaces():
    cmds.namespace(setNamespace="::")
    return cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)


def _get_unique_namespace(namespace):
    all_namespaces = _get_all_namespaces()
    if namespace not in all_namespaces:
        return namespace
    for i in itertools.count():
        new_namespace = namespace + str(i)
        if new_namespace not in all_namespaces:
            return new_namespace


def import_component_from_file(path, namespace='untitled'):
    namespace = _get_unique_namespace(namespace)
    cmds.file(path, i=True, namespace=namespace)
    hub_inn = pymel.PyNode('|{0}:{1}'.format(namespace, _HUB_INN_NAME))
    hub_out = pymel.PyNode('|{0}:{1}'.format(namespace, _HUB_OUT_NAME))
    return hub_inn, hub_out


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
        if os.path.exists(dirname):
            for filename in os.listdir(dirname):
                basename, ext = os.path.splitext(filename)
                if ext != '.ma':
                    continue
                path = os.path.join(dirname, filename)

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
    component_network_by_bound = {}
    networks = libSerialization.get_networks_from_class('Component')
    for network in networks:
        grp_inn = next(iter(network.attr('grp_inn').inputs()), None)
        if grp_inn:
            component_network_by_bound[grp_inn] = network
        grp_out = next(iter(network.attr('grp_out').inputs()), None)
        if grp_out:
            component_network_by_bound[grp_out] = network
    return component_network_by_bound


def get_component_parent_network(obj, source=True, destination=True, cache=None):
    """
    Return the metadata of the component parent of the provided component, optimized for starting at the input network.
    :param obj: A pymel.nodetypes.Network representing the output of a component.
    :param cache: Initialized internally.
    :return: A pymel.nodetypes.Network that can be deserialized.
        """
    if not cache:
        cache = get_component_network_bounds()

    def _fn_goal(n):
        return n in cache

    def _fn_get_paths(n):
        return pymel.listConnections(n, source=source, destination=destination, skipConversionNodes=True)

    return libPython.id_dfs(obj, _fn_goal, _fn_get_paths)


def get_component_parent_network_from_output(obj, cache=None):
    """
    Return the metadata of the component parent of the provided component, optimized for starting at the output network.
    :param obj: A pymel.nodetypes.Network representing the output of a component.
    :param cache: Initialized internally.
    :return: A pymel.nodetypes.Network that can be deserialized.
    """
    return get_component_parent_network(obj, source=False, destination=True)


def get_component_parent_network_from_input(obj, cache=None):
    return get_component_parent_network(obj, source=True, destination=False)
