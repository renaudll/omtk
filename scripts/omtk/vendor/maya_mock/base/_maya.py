"""Module for all of Maya entry point functions."""
import logging

from maya import cmds

_LOG = logging.getLogger(__name__)


def get_node_type_namespace(node_type):
    """
    Return the namespace of a node as a list of string.

    >>> get_node_type_namespace('transform')
    [u'containerBase', u'entity', u'dagNode', u'transform']

    :param str node_type: A node type string.
    :return: The name of the parent type of the provided node type.
    :rtype: list(str)
    """
    try:
        return cmds.nodeType(node_type, isTypeName=True, inherited=True) or []
    except RuntimeError as error:  # TODO: Document why this can happen
        _LOG.warning(error)
        return []


def get_node_attributes_info(node_type):
    """
    Retrieve information about about a registered attribute as a dict.

    :param str node_type: The type of the node being inspect
    :return: An object dict
    :rtype: dict
    """
    result = {}

    try:
        attributes = cmds.attributeInfo(allAttributes=True, type=node_type)
    except RuntimeError as error:  # TODO: Document why this can happen
        _LOG.warning(error)
        return result

    return {attribute: get_attribute_info(node_type, attribute) for attribute in attributes}


def get_attribute_info(node_type, attribute):
    """
    Retrieve information about a node attribute definition.

    :param str node_type: Node type name
    :param str attribute: Attribute name
    :return: A dict of attribute related data
    :rtype: dict
    """
    # TODO: All these calls to cmds are slowing down generation! (26 seconds for scan)
    attr_type = cmds.attributeQuery(attribute, type=node_type, attributeType=True)

    # Some attributes will return 'typed' as the type.
    # I don't know of any way of knowing in advance the type.
    # However for what we need, guessing might be enough.
    if attr_type == "typed":
        if "matrix" in attribute.lower():  # HACK
            attr_type = "matrix"

    attr_name_short = cmds.attributeQuery(attribute, type=node_type, shortName=True)
    attr_name_nice = cmds.attributeQuery(attribute, type=node_type, niceName=True)
    attr_parents = cmds.attributeQuery(attribute, type=node_type, listParent=True)
    attr_parent = attr_parents[0] if attr_parents else None
    attr_readable = cmds.attributeQuery(attribute, type=node_type, readable=True)
    attr_writable = cmds.attributeQuery(attribute, type=node_type, writable=True)

    return {
        "port_type": attr_type,
        "short_name": attr_name_short,
        "nice_name": attr_name_nice,
        "parent": attr_parent,
        "readable": attr_readable,
        "writable": attr_writable,
    }


def get_node_classification(node_type):
    """
    Return the classification string associated with a registered node in maya.

    >>> get_node_classification('transform')
    u'drawdb/geometry/transform'

    :param str node_type: The type of the node to inspect.
    :return: The node classification string
    :rtype: str
    """
    classifications = cmds.getClassification(node_type)
    # Get the node identification tags
    if len(classifications) != 1:
        # This should not happen, we don't know why getClassification return a list.
        raise Exception("Unexpected classification return value for %r" % node_type)
    classification = classifications[0]

    return classification
