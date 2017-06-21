from omtk import factory_datatypes, constants
from omtk.vendor.Qt import QtCore
from omtk import constants
from pymel import core as pymel

_GRAPH_POS_ATTR_NAME = constants.PyFlowGraphMetadataKeys.Position

def _iter_connected_nodes(node):
    for port in node.iter_input_ports():
        connections = port.inCircle().getConnections()
        for connection in connections:
            src = connection.getSrcPort()
            dst = connection.getDstPort()

            connected_node = src.getNode()

            # Ignore known nodes
            yield connected_node


def iter_leaf_nodes(node, known=None):
    """Iterate recursively trough the graph upstream and yield any encountered leaf node."""
    if known is None:
        known = set()

    for sub_node in _iter_connected_nodes(node):
        if sub_node in known:
            continue
        known.add(sub_node)

        is_leaf_node = True
        for child in iter_leaf_nodes(sub_node):
            yield child
            is_leaf_node = False
        if is_leaf_node:
            yield sub_node


def arrange_upstream(node, padding_x=32, padding_y=32):
    parent_pos = node.getGraphPos()

    # Resolve nb of nodes on top level
    # Filter any node that don't share the same parent space.
    leaf_nodes = list(iter_leaf_nodes(node))
    children = list(_iter_connected_nodes(node))
    if not children:
        return

    # Resolve total width
    total_height = 0
    for leaf_node in leaf_nodes:
        total_height += leaf_node.size().height()
    total_height += (len(leaf_nodes) - 1) * padding_y
    print total_height

    # Set start location
    pos_x = parent_pos.x() - (node.size().width() * 0.5) - padding_x
    pos_y = parent_pos.y() - (total_height / 2.0)

    # Reposition all children
    for child, in zip(children):
        pos_y += child.size().height() * 0.5
        child.setGraphPos(QtCore.QPointF(
            pos_x + (child.size().width() * -0.5),
            pos_y + (child.size().height() * -0.5))
        )
        pos_y += child.size().height() * 0.5 + padding_y
        # pos_y += spacing_y
        arrange_upstream(child, padding_x=padding_x, padding_y=padding_y)

def arrange_downstream(node, padding_x=32, padding_y=32):
    parent_pos = node.getGraphPos()

    # Resolve nb of nodes on top level
    # Filter any node that don't share the same parent space.
    leaf_nodes = list(iter_leaf_nodes(node))
    children = list(_iter_connected_nodes(node))
    if not children:
        return

    # Resolve total width
    total_height = 0
    for leaf_node in leaf_nodes:
        total_height += leaf_node.size().height()
    total_height += (len(leaf_nodes) - 1) * padding_y
    print total_height

    # Set start location
    pos_x = parent_pos.x() - (node.size().width() * 0.5) - padding_x
    pos_y = parent_pos.y() - (total_height / 2.0)

    # Reposition all children
    for child, in zip(children):
        pos_y += child.size().height() * 0.5
        child.setGraphPos(QtCore.QPointF(
            pos_x - (child.size().width() * 0.5),
            pos_y + (child.size().height() * -0.5))
        )
        pos_y += child.size().height() * 0.5 + padding_y
        # pos_y += spacing_y
        arrange_downstream(child, padding_x=padding_x, padding_y=padding_y)

def get_node_position(node):
    meta_type = node._meta_type
    meta_data = node._meta_data

    if meta_type in (factory_datatypes.AttributeType.Node,) and meta_data.hasAttr(
            constants.PyFlowGraphMetadataKeys.Position):
        return meta_data.attr(constants.PyFlowGraphMetadataKeys.Position).get()


def save_node_position(node, pos):
    meta_type = node._meta_type
    meta_data = node._meta_data
    print node, meta_type, meta_data

    if meta_type in (factory_datatypes.AttributeType.Node,):

        if not meta_data.hasAttr(_GRAPH_POS_ATTR_NAME):
            pymel.addAttr(meta_data, longName=_GRAPH_POS_ATTR_NAME, at='float2')
            pymel.addAttr(meta_data, longName=_GRAPH_POS_ATTR_NAME + 'X', at='float', parent=_GRAPH_POS_ATTR_NAME)
            pymel.addAttr(meta_data, longName=_GRAPH_POS_ATTR_NAME + 'Y', at='float', parent=_GRAPH_POS_ATTR_NAME)
            attr = meta_data.attr(_GRAPH_POS_ATTR_NAME)
        else:
            attr = meta_data.attr(_GRAPH_POS_ATTR_NAME)
        attr.set(pos)