"""
Factory providing component instances.
"""
from maya import cmds
import pymel.core as pymel
from omtk import constants
from omtk.component.component_base import Component, _get_parent_namespace, _get_nodes_from_attributes
from omtk.libs import libNamespaces, libPython, libAttr
from omtk.vendor import libSerialization


def create_empty(namespace='component'):
    """
    Create an empty component.
    :param str namespace: The desired namespace for the new component.
    :return: A ``Component`` instance.
    :rtype: Component
    """
    namespace = libNamespaces.get_unique_namespace(namespace, enforce_suffix=True)
    cmds.namespace(add=namespace)
    inst = Component(namespace)
    return inst


def from_nodes(objs, connections=True, namespace='component'):
    """
    Create a component from a set of nodes.
    This will move these nodes into a unique namespace and return a Component instance.
    :param List[pymel.nodetypes.DependNode] objs: A list of pymel.nodetypes.DependNode.
    :param str namespace: The desired namespace. If not unique, a suffix will be added.
    :return: A ``Component`` instance.
    :rtype: Component
    """
    parent_namespace = _get_parent_namespace(objs)
    if parent_namespace:
        namespace = '{0}:{1}'.format(parent_namespace, namespace)
    namespace = libNamespaces.get_unique_namespace(namespace, enforce_suffix=True)
    cmds.namespace(add=namespace)

    for obj in objs:
        old_name = obj.stripNamespace().nodeName()
        new_name = '{0}:{1}'.format(namespace, old_name)
        obj.rename(new_name)

    inst = Component(namespace)

    # We need an hub in and hub_out
    # However we don't known about which attributes to expose so we'll just create the objects.
    # todo: do we want to automatically populate the hubs?
    hub_inn_dagpath = '{0}:{1}'.format(namespace, constants.COMPONENT_HUB_INN_NAME)
    hub_out_dagpath = '{0}:{1}'.format(namespace, constants.COMPONENT_HUB_OUT_NAME)
    hub_inn = pymel.PyNode(hub_inn_dagpath) if cmds.objExists(hub_inn_dagpath) else pymel.createNode('network', name=hub_inn_dagpath)
    hub_out = pymel.PyNode(hub_out_dagpath) if cmds.objExists(hub_out_dagpath) else pymel.createNode('network', name=hub_out_dagpath)
    inst.grp_inn = hub_inn
    inst.grp_out = hub_out

    return inst


def from_attributes(attrs_inn, attrs_out, dagnodes=None, namespace='component'):
    """
    Create a component from existing providedattributes.

    :param List[pymel.Attribute] attrs_inn:
    :param List[pymel.Attribute] attrs_out:
    :param List[pymel.PyNode] dagnodes:
    :param str namespace:
    :return: A Component
    :rtype: Component
    """
    attrs_inn_map = {}
    attrs_out_map = {}

    for attr in attrs_inn:
        if attr in attrs_inn_map:
            continue
        attr_name = libPython.get_unique_key(attr.longName(), attrs_inn_map)
        attrs_inn_map[attr_name] = attr

    for attr in attrs_out:
        if attr in attrs_out_map:
            continue
        attr_name = libPython.get_unique_key(attr.longName(), attrs_out_map)
        attrs_out_map[attr_name] = attr

    inst = from_attributes_map(attrs_inn_map, attrs_out_map, dagnodes=dagnodes, namespace=namespace)
    return inst


def from_attributes_map(attrs_inn, attrs_out, dagnodes=None, namespace='component'):
    """
    Create a Component from existing nodes.
    :param Dict[str, pymel.Attribute] attrs_inn: A dict(k, v) of public input attributes where k is attr name and v is the reference attribute.
    :param Dict[str, pymel.Attribute] attrs_out: A dict(k, v) of publish output attributes where k is attr name v is the reference attribute.
    :param List[pymel.PyNode] dagnodes: A list of nodes to include in the component.
    :param str namespace: A str for the created component namespace.
    :return: Component instance.
    :rtype: Component
    """
    # Determine the parent namespace
    if dagnodes is None:
        dagnodes = set()
    else:
        dagnodes = set(dagnodes)  # enforce set for now...
    additional_dagnodes = _get_nodes_from_attributes(attrs_inn.values(), attrs_out.values())
    dagnodes.update(additional_dagnodes)

    from omtk.libs import libNamespaces

    # Determine the parent namespace
    parent_namespace = None
    if parent_namespace is None:
        for node in dagnodes:
            node_namespace = libNamespaces.get_namespace(node)
            if node_namespace:
                parent_namespace = node_namespace
                new_namespace = ':{}:{}'.format(parent_namespace, namespace)
                print namespace, parent_namespace, new_namespace
                namespace = new_namespace


    # todo: do we want to force readable or writable attributes? can this fail?
    # Find an available namespace
    # This allow us to make sure that we'll have access to unique name.
    # Note theses namespaces will be removed in any exported file.
    namespace = libNamespaces.get_unique_namespace(namespace, enforce_suffix=True)
    cmds.namespace(add=namespace)

    inst = Component(namespace)

    hub_inn = pymel.createNode('network', name='{0}:{1}'.format(namespace, constants.COMPONENT_HUB_INN_NAME))
    hub_out = pymel.createNode('network', name='{0}:{1}'.format(namespace, constants.COMPONENT_HUB_OUT_NAME))

    def _escape_attr_name(attr_name):
        return attr_name.replace('[', '').replace(']', '')  # todo: find a better way

    # Create the hub_inn attribute.
    for attr_name, attr_ref in attrs_inn.iteritems():
        data = libAttr.AttributeData.from_pymel_attribute(attr_ref, store_inputs=True, store_outputs=True)
        if not data.is_writable:
            raise IOError("Expected a writable attribute as an input reference.")

        attr_name = _escape_attr_name(attr_name)

        data.rename(attr_name)
        hub_attr = data.copy_to_node(hub_inn)
        pymel.connectAttr(hub_attr, attr_ref, force=True)
        data.connect_stored_inputs(hub_inn)

    # Create the hub_out attribute.
    for attr_name, attr_ref in attrs_out.iteritems():
        data = libAttr.AttributeData.from_pymel_attribute(attr_ref, store_inputs=True, store_outputs=True)
        if not data.is_readable:
            raise IOError("Expected a readable attribute as an output reference.")

        attr_name = _escape_attr_name(attr_name)

        data.rename(attr_name)
        hub_attr = data.copy_to_node(hub_out)
        pymel.connectAttr(attr_ref, hub_attr)
        data.connect_stored_outputs(hub_out)

    # Resolve the objects between the hubs
    dagnodes = set(dagnodes) if dagnodes else set()
    dagnodes |= set(hub_inn.listHistory(future=True)) & set(hub_out.listHistory(future=False))

    dagnodes.discard(hub_inn)  # already correctly named
    dagnodes.discard(hub_out)  # already correctly named

    inst.grp_inn = hub_inn
    inst.grp_out = hub_out

    def _get_name(n):
        try:  # pynodes
            return n.nodeName()
        except:  # component
            return n.namespace

    if dagnodes:
        for dagnode in dagnodes:
            from omtk.libs import libNamespaces
            dagnode.rename('{0}:{1}'.format(namespace, _get_name(dagnode).split(':')[-1]))

    libSerialization.export_network(inst)

    return inst