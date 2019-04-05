from omtk import constants
from omtk.libs import libMayaNodeEditor
import pymel.core as pymel

_GRAPH_POS_ATTR_NAME = constants.PyFlowGraphMetadataKeys.Position


def _get_position_from_metadata_attributes(node):
    if node.hasAttr(constants.PyFlowGraphMetadataKeys.Position):
        return node.attr(constants.PyFlowGraphMetadataKeys.Position).get()
    return None


def _get_position_from_maya_nodegraph(node):
    return libMayaNodeEditor.get_node_position(node)


def get_node_position(node):
    """
    Get the stored position for a provided node.

    :param pymel.PyNode node: The node to query.
    :return: A x and y coordinate. None if no position could be determined.
    :rtype: tuple(float, float) or None
    """
    result = _get_position_from_metadata_attributes(node)
    if result:
        return result

    result = _get_position_from_maya_nodegraph(node)
    if result:
        return result

    return None


def save_node_position(node, pos):
    """
    Save a provided position in a provided node.

    :param pymel.PyNode node: The node to save the position to.
    :param tuple(float, float) pos: The position coordinates to save.
    """
    if not node.hasAttr(_GRAPH_POS_ATTR_NAME):
        pymel.addAttr(node, longName=_GRAPH_POS_ATTR_NAME, at='float2')
        pymel.addAttr(node, longName=_GRAPH_POS_ATTR_NAME + 'X', at='float', parent=_GRAPH_POS_ATTR_NAME)
        pymel.addAttr(node, longName=_GRAPH_POS_ATTR_NAME + 'Y', at='float', parent=_GRAPH_POS_ATTR_NAME)
        attr = node.attr(_GRAPH_POS_ATTR_NAME)
    else:
        attr = node.attr(_GRAPH_POS_ATTR_NAME)
    attr.set(pos)
