"""
Factory providing compound instances.
"""
import logging

import pymel.core as pymel
from maya import cmds

from ._compound import Compound, CompoundValidationError
from ._constants import (
    INPUT_NODE_NAME,
    OUTPUT_NODE_NAME,
    COMPOUND_DEFAULT_NAMESPACE,
)
from ._utils import pairwise
from . import _utils_namespace

_LOG = logging.getLogger(__name__)


def create_empty(namespace=COMPOUND_DEFAULT_NAMESPACE):
    """
    Create a compound from nothing.

    :param str namespace: The desired namespace for the new compound.
    :return: A ``Compound`` instance.
    :rtype: Compound
    """
    namespace = _utils_namespace.get_unique_namespace(namespace)

    # Create namespace if necessary
    if not cmds.namespace(exists=namespace):
        cmds.namespace(add=namespace)

    # Create bounds if necessary
    bound_inn_dagpath = "%s:%s" % (namespace, INPUT_NODE_NAME)
    bound_out_dagpath = "%s:%s" % (namespace, OUTPUT_NODE_NAME)
    if not cmds.objExists(bound_inn_dagpath):
        cmds.createNode("network", name=bound_inn_dagpath)
    if not cmds.objExists(bound_out_dagpath):
        cmds.createNode("network", name=bound_out_dagpath)

    return Compound(namespace)


def create_from_nodes(objs, namespace=COMPOUND_DEFAULT_NAMESPACE, expose=False):
    """
    Create a compound from a set of nodes.
    This will move the nodes inside of a namespace.

    This will move these nodes into a unique namespace and return a compound instance.
    :param List[str] objs: A list of objects to include in the compound.
    :param str namespace: An optional namespace for the compound.
    :param bool expose: Should we expose attributes from connection
                        outside the nodes boundaries?
    :return: A compound object
    :rtype: Compound
    """
    # Conform objs to pynodes
    objs = [pymel.PyNode(obj) for obj in objs]

    common_namespace = _utils_namespace.get_common_namespace(objs)
    if common_namespace:
        namespace = "{0}:{1}".format(common_namespace, namespace)

    namespace = _utils_namespace.get_unique_namespace(namespace)
    cmds.namespace(add=namespace)

    # TODO: Ensure namespaces are always absolute,
    #  we don't want the current namespace to play any role here.
    # TODO: Error out if we are breaking a compound by splitting it in two?
    for obj in objs:
        new_name = _utils_namespace.join_namespace(
            namespace, _utils_namespace.relative_namespace(str(obj), common_namespace)
        )

        node_namespace = _utils_namespace.get_namespace(new_name)
        if node_namespace and not cmds.namespace(exists=node_namespace):
            cmds.namespace(add=node_namespace)

        obj.rename(new_name)

    inst = _create(namespace)

    if expose:
        inputs, outputs = _get_attributes_map_from_nodes(objs)
        _expose_attributes(inst, inputs, outputs)

    return Compound(namespace)


def from_namespace(namespace):
    """
    Create a compound instance from a namespace.

    :param namespace:
    :return:
    :raises ValueError: If the namespace does not contain a valid compound.
    """
    if cmds.objExists(namespace):
        raise ValueError("A node is already named %r" % namespace)

    if not cmds.namespace(exists=namespace):
        raise ValueError("Namespace %r does not exist." % namespace)

    inst = Compound(namespace)
    inst.validate()
    return inst


def from_scene():
    """
    Return all compound in the scene.

    :return: A compound generator
    :rtype: Generator[omtk_compound.Compound]
    """
    cmds.namespace(setNamespace=":")
    namespaces = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    for namespace in namespaces:
        try:
            yield Compound(namespace)
        except CompoundValidationError:
            pass


def from_attributes(
    attrs_inn, attrs_out, dagnodes=None, namespace=COMPOUND_DEFAULT_NAMESPACE
):
    """
    Create a compound from a set of provided input and output attributes.
    The network node will be automatically determined.

    :param attrs_inn:
    :type attrs_inn: list(str)
    :param List[pymel.Attribute] attrs_out:
    :type attrs_out: list(str)
    :param List[pymel.PyNode] dagnodes:
    :param str namespace:
    :return: A compound
    :rtype: Compound
    """
    # TODO: Remove pymel usage
    # Conform dagnodes to set
    dagnodes = set(pymel.PyNode(dagnode) for dagnode in dagnodes) if dagnodes else set()

    # Conform inputs and outputs to pymel
    attrs_inn = [pymel.Attribute(attr) for attr in attrs_inn]
    attrs_out = [pymel.Attribute(attr) for attr in attrs_out]

    additional_dagnodes = _get_nodes_from_attributes(attrs_inn, attrs_out)
    dagnodes.update(additional_dagnodes)

    inst = create_from_nodes(dagnodes, namespace=namespace, expose=False)
    _expose_attributes(inst, attrs_inn, attrs_out)

    return inst


def from_file(path, namespace=COMPOUND_DEFAULT_NAMESPACE):
    """
    Create a compound in the scene from a CompoundDefinition.

    :param str path: Path to a maya ascii file (.ma) to load.
    :param str namespace: The namespace to use for the compound.
    :return: A compound instance.
    :rtype: omtk_compound.core.Compound
    """
    namespace = _utils_namespace.get_unique_namespace(namespace)
    _LOG.info("Creating compound with namespace: %s", namespace)
    cmds.file(path, i=True, namespace=namespace)
    return from_namespace(namespace)


def _create(namespace):
    """
    Create a new compound from a provided namespace.

    :param namespace: The compound namespace
    :return: A compound instance
    :rtype: Compound
    """
    hub_inn_dagpath = "{0}:{1}".format(namespace, INPUT_NODE_NAME)
    if not cmds.objExists(hub_inn_dagpath):
        cmds.createNode("network", name=hub_inn_dagpath)

    hub_out_dagpath = "{0}:{1}".format(namespace, OUTPUT_NODE_NAME)
    if not cmds.objExists(hub_out_dagpath):
        cmds.createNode("network", name=hub_out_dagpath)

    return Compound(namespace)


def _expose_attributes(inst, inputs, outputs):
    """
    Expose a compound attributes.

    :param Compound inst: A compound object
    :param list[str] inputs: Input attributes to expose
    :param list[str] outputs: Output attributes to expose
    """
    # TODO: Should the expose redirect attribute by itself???

    # Conform inputs and outputs to str
    inputs = sorted((str(input_) for input_ in inputs))
    outputs = sorted((str(output) for output in outputs))

    # We can have multiple connections starting from the same attributes
    # outside the network to multiple attributes inside the network.
    # If we encounter the same attribute twice,
    # we'll want to re-use the already existing destination.
    known_network_inputs = set()

    for dst_attr in inputs:
        src_attrs = _hold_input_attributes(dst_attr)

        # Any source attribute we already encountered
        # will re-use the previously exposed destination attribute.
        for src_attr in src_attrs:
            if src_attr in known_network_inputs:
                continue

            exposed_dst_attr = inst.expose_input_attr(dst_attr)
            known_network_inputs.add(src_attr)
            cmds.connectAttr(src_attr, exposed_dst_attr)

    for src_attr in outputs:
        dst_attributes = _hold_output_attributes(src_attr)

        exposed_src_attr = inst.expose_output_attr(src_attr)
        for dst_attr in dst_attributes:
            cmds.connectAttr(exposed_src_attr, dst_attr)


def _get_nodes_from_attributes(inputs, outputs):
    """
    Determine the common history between attributes
    that would be used to create a compound.

    :param list[str] inputs: A list of input attributes.
    :param list[str] outputs: A list of output attributes.
    """
    # Conform to pymel
    inputs = [pymel.Attribute(attr) for attr in inputs]
    outputs = [pymel.Attribute(attr) for attr in outputs]

    hist_inn = set()
    hist_out = set()
    for attr_inn in inputs:
        hist_inn.update(attr_inn.listHistory(future=True))
    for attr_out in outputs:
        hist_out.update(attr_out.listHistory(future=False))
    return hist_inn & hist_out


def _get_attributes_map_from_nodes(nodes):
    """
    Determine the attribute to expose from a set of node.

    :param list[str] nodes: A list of nodes
    :return: The inputs attributes and output attributes
    :rtype: tuple[list[str], list[str]]
    """
    # TODO: Ignore attributes that point back to the network.

    # For now we don't want to deal with name mismatch so we'll again use pymel.
    nodes_pm = {pymel.PyNode(node) for node in nodes}

    # Create an attribute map of the attributes we need to expose.
    inputs = set()
    outputs = set()

    input_connections = (
        cmds.listConnections(
            nodes, source=True, destination=False, connections=True, plugs=True
        )
        or []
    )
    output_connections = (
        cmds.listConnections(
            nodes, source=False, destination=True, connections=True, plugs=True
        )
        or []
    )

    for dst, src in pairwise(input_connections):
        # Ignore message connection
        attr = pymel.Attribute(src)
        if attr.type() == "message":
            continue
        if attr.node() in nodes_pm:
            continue
        inputs.add(dst)

    for src, dst in pairwise(output_connections):
        attr = pymel.Attribute(dst)
        if attr.type() == "message":
            continue
        if attr.node() in nodes_pm:
            continue
        outputs.add(src)

    return inputs, outputs


def _hold_input_attributes(attr):
    """
    Find all connections to a provided attribute, remove them,
    and return the source attributes.

    :param str attr: A destination attribute
    :return: A list of source attribute
    :rtype: list[str]
    """
    inputs = cmds.listConnections(attr, destination=False, plugs=True) or []
    for input_ in inputs:
        cmds.disconnectAttr(input_, attr)
    return inputs


def _hold_output_attributes(attr):
    """
    Find all connections from a provided attribute, remote them,
    and return the destination attributes.

    :param str attr: A source attribute
    :return: A list of destination attribute
    :rtype: list[str]
    """
    outputs = cmds.listConnections(attr, source=False, plugs=True) or []
    for output in outputs:
        cmds.disconnectAttr(attr, output)
    return outputs
