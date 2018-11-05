"""
Various functions to interact with pyflowgraph GraphView.
"""
import logging

from omtk import constants
from omtk.vendor.Qt import QtCore
from omtk.libs import libMayaNodeEditor

log = logging.getLogger(__name__)

_GRAPH_POS_ATTR_NAME = constants.PyFlowGraphMetadataKeys.Position


def _walk_downstream(node):
    known = set()
    for port in node.iter_output_ports():
        connections = port.outCircle().getConnections()
        for connection in connections:
            # src = connection.getSrcPort()
            dst = connection.getDstPort()

            connected_node = dst.getNode()
            if connected_node in known:
                continue
            known.add(connected_node)

            # Ignore known nodes
            yield connected_node


def _walk_upstream(node):
    known = set()
    for port in node.iter_input_ports():
        connections = port.inCircle().getConnections()
        for connection in connections:
            src = connection.getSrcPort()
            # dst = connection.getDstPort()

            connected_node = src.getNode()
            if connected_node in known:
                continue
            known.add(connected_node)

            # Ignore known nodes
            yield connected_node


def iter_leaf_nodes(node, fn_walk, known=None):
    """Iterate recursively trough the graph upstream and yield any encountered leaf node."""
    if known is None:
        known = set()

    for sub_node in fn_walk(node):
        if sub_node in known:
            continue
        known.add(sub_node)

        is_leaf_node = True
        for child in iter_leaf_nodes(sub_node, fn_walk):
            yield child
            is_leaf_node = False
        if is_leaf_node:
            yield sub_node


def arrange_upstream(node, padding_x=32, padding_y=32):
    parent_pos = node.getGraphPos()
    parent_width = node.size().width()

    # Resolve nb of nodes on top level
    # Filter any node that don't share the same parent space.
    leaf_nodes = list(iter_leaf_nodes(node, _walk_upstream))
    children = list(_walk_upstream(node))
    if not children:
        return

    # Resolve total width
    total_width = 0
    total_height = 0
    for leaf_node in leaf_nodes:
        total_width = max(total_width, leaf_node.size().width())
        total_height += leaf_node.size().height()
    total_height += (len(leaf_nodes) - 1) * padding_y
    print total_height

    # Set start location
    pos_x = parent_pos.x() - (parent_width * 0.5) - (total_width * 0.5) - padding_x
    pos_y = parent_pos.y() - (total_height / 2.0)

    # Reposition all children
    for child, in zip(children):
        pos_y += child.size().height() * 0.5
        child.setGraphPos(QtCore.QPointF(
            pos_x - ((child.size().width() - total_width) / 2.0),
            pos_y,
        ))
        pos_y += child.size().height() * 0.5 + padding_y
        arrange_upstream(child, padding_x=padding_x, padding_y=padding_y)


def arrange_downstream(node, padding_x=32, padding_y=10):
    parent_pos = node.getGraphPos()
    parent_width = node.size().width()

    # Resolve nb of nodes on top level
    # Filter any node that don't share the same parent space.
    leaf_nodes = list(iter_leaf_nodes(node, _walk_downstream))
    children = list(_walk_downstream(node))
    if not children:
        return

    # Resolve total height
    total_width = 0
    total_height = 0
    for leaf_node in leaf_nodes:
        total_width = max(total_width, leaf_node.size().width())
        total_height += leaf_node.size().height()
    total_height += (len(leaf_nodes) - 1) * padding_y
    print total_height

    # Set start location
    pos_x = parent_pos.x() + (parent_width * 0.5) + (total_width * 0.5) + padding_x
    pos_y = parent_pos.y() - total_height * 0.5

    # Reposition all children
    known_nodes = set()
    num_children = len(children)
    # pos_y_increments = total_height / (num_children - 1)
    for i, child, in enumerate(children):
        if child in known_nodes:
            continue
        known_nodes.add(child)

        # pos_y += pos_y_increments  # child.size().height() * 0.5
        log.debug('Repositionning {} ({}) to {}, {}'.format(
            child, child.getName(), pos_x, pos_y
        ))
        child.setGraphPos(QtCore.QPointF(
            pos_x + ((child.size().width() - total_width) / 2.0),
            pos_y
        ))
        pos_y += child.size().height() + padding_y
        # pos_y += spacing_y
        arrange_downstream(child, padding_x=padding_x, padding_y=padding_y)


def _get_node_position(node, use_stored_pos=True, use_maya_pos=False):
    # type: (pymel.PyNode, bool, bool) -> None
    # If the node contain a saved position, use it.
    if use_stored_pos and node.hasAttr(constants.PyFlowGraphMetadataKeys.Position):
        pos = node.attr(constants.PyFlowGraphMetadataKeys.Position).get()
        # print("Getting position. {0} at {1}".format(node, pos))
        return pos
    # Otherwise use the saved position from the Maya NodeEditor.
    elif use_maya_pos:
        pos = libMayaNodeEditor.get_node_position(node)
        # print("Getting position. {0} at {1}".format(node, pos))
        return pos


def get_node_position(node, use_stored_pos=True, use_maya_pos=False):
    # type: (NodeModel, bool, bool) -> (float, float)
    from omtk.factories import factory_datatypes

    assert(use_stored_pos or use_maya_pos)
    meta_type = node.get_metatype()
    meta_data = node.get_metadata()

    if meta_type in (factory_datatypes.AttributeType.Node,):
        return _get_node_position(meta_data, use_stored_pos=use_stored_pos, use_maya_pos=use_maya_pos)
    elif meta_type in (factory_datatypes.AttributeType.Component,):
        return _get_node_position(meta_data.grp_inn, use_stored_pos=use_stored_pos, use_maya_pos=use_maya_pos)


def _save_node_position(node, pos):
    from pymel import core as pymel
    # type: (pymel.PyNode, Tuple[float,float]) -> None
    if not node.hasAttr(_GRAPH_POS_ATTR_NAME):
        pymel.addAttr(node, longName=_GRAPH_POS_ATTR_NAME, at='float2')
        pymel.addAttr(node, longName=_GRAPH_POS_ATTR_NAME + 'X', at='float', parent=_GRAPH_POS_ATTR_NAME)
        pymel.addAttr(node, longName=_GRAPH_POS_ATTR_NAME + 'Y', at='float', parent=_GRAPH_POS_ATTR_NAME)
        attr = node.attr(_GRAPH_POS_ATTR_NAME)
    else:
        attr = node.attr(_GRAPH_POS_ATTR_NAME)
    attr.set(pos)

    # print("Saving position. {0} at {1}".format(node, pos))


def save_node_position(node, pos):
    # type: (NodeModel, Tuple[float,float]) -> None
    from omtk.factories import factory_datatypes
    meta_type = node.get_metatype()
    meta_data = node.get_metadata()

    if meta_type in (factory_datatypes.AttributeType.Node,):
        _save_node_position(meta_data, pos)

    elif meta_type in (factory_datatypes.AttributeType.Component,):
        _save_node_position(meta_data.grp_inn, pos)


def pyflowgraph_to_networkxgraph(nodes):
    import networkx
    g = networkx.Graph()
    layout = {}

    # Add nodes
    g.add_nodes_from(range(len(nodes)))

    # Add edges
    for i, node in enumerate(nodes):
        for upstream_node in _walk_upstream(node):
            try:
                j = nodes.index(upstream_node)
            except ValueError:
                continue
            g.add_edge((j, i))
        for downstream_node in _walk_downstream(node):
            try:
                j = nodes.index(downstream_node)
            except ValueError:
                continue
            g.add_edge((i, j))

    # Get positions
    for i, node in enumerate(nodes):
        pos = node.getGraphPos()
        pos = (pos.x(), pos.y())
        layout[i] = pos

    return g, layout


def spring_layout2(nodes, fixed=None, **kwargs):
    import networkx
    g, layout = pyflowgraph_to_networkxgraph(nodes)
    fixed_indexes = [nodes.index(f) for f in fixed] if fixed else None
    layout = networkx.spring_layout(g, k=1, pos=layout, fixed=fixed_indexes, **kwargs)

    for i, node in enumerate(nodes):
        pos = layout[i]
        pos = QtCore.QPointF(*pos)
        node.setGraphPos(pos)


def spring_layout(nodes):
    if not nodes:
        return
    
    from omtk.vendor.jurij import graph

    nodes = list(nodes)
    num_vertices = len(nodes)
    print num_vertices

    edges = []
    for i, node in enumerate(nodes):
        for upstream_node in _walk_upstream(node):
            try:
                j = nodes.index(upstream_node)
            except ValueError:
                j = len(nodes)
                nodes.append(upstream_node)
                # continue
            edges.append((j, i))
        for downstream_node in _walk_downstream(node):
            try:
                j = nodes.index(downstream_node)
            except ValueError:
                j = len(nodes)
                nodes.append(downstream_node)
                # continue
            edges.append((i, j))

    vertices = range(len(nodes))
    print len(vertices)

    node_positions = []
    for node in nodes:
        pos = node.getGraphPos()
        node_positions.append(pos)
        # node_positions.append((pos.x(), pos.y()))

    average_pos_before = QtCore.QPointF()
    for pos in node_positions:
        average_pos_before += pos
    average_pos_before /= len(nodes)

    import itertools
    bound_before_x = max(abs(a.x() - b.x()) for a, b in itertools.permutations(node_positions, 2))
    bound_before_y = max(abs(a.y() - b.y()) for a, b in itertools.permutations(node_positions, 2))

    node_positions = [(pos.x(), pos.y()) for pos in node_positions]

    layout = {}
    for i, position in enumerate(node_positions):
        layout[i] = position

    graph = graph.Graph(vertices=vertices, edges=edges)

    layout_iteration = 1000
    columb = 1.0  # Intensity of Columb's force
    hook = 0.1  # Intensity of Hook's force
    dt = 0.5  # Time step

    while layout_iteration > 0:
        layout_iteration = layout_iteration - 1
        # Compute change of layout
        kinetic = 0.0  # kinetic energy
        for u in graph.vertices():
            if u > num_vertices:
                continue
            # Compute the acceleration of u
            (x, y) = layout[u]
            (ax, ay) = (0, 0)
            for v in graph.vertices():
                # if u > num_vertices:
                #     continue
                if u != v:
                    (a, b) = layout[v]
                    d = max(0.001, (x - a) * (x - a) + (y - b) * (y - b))
                    # Columb's law
                    ax -= columb * (a - x) / (d * d)
                    ay -= columb * (b - y) / (d * d)
            for v in graph.adjacency[u]:
                # if u > num_vertices:
                #     continue
                # Hook's law
                (a, b) = layout[v]
                ax += hook * (a - x)
                ay += hook * (b - y)
            for v in graph.opposite()[u]:
                # if u > num_vertices:
                #     continue
                # Hook's law
                (a, b) = layout[v]
                ax += hook * (a - x)
                ay += hook * (b - y)
            # Update velocities
            vx = dt * ax
            vy = dt * ay
            kinetic += vx * vx + vy * vy
            x = x + dt * vx + ax * dt * dt
            y = y + dt * vy + ay * dt * dt
            layout[u] = (x, y)
        if kinetic < 1e-6:
            layout_iteration = 0
            # self._layout_worker = self.canvas.after(20, self.spring_layout_worker)

    # Adjust scale
    new_positions = [QtCore.QPointF(x, y) for i, (x, y) in zip(xrange(num_vertices), layout.itervalues())]
    bound_after_x = max(abs(a.x() - b.x()) for a, b in itertools.permutations(new_positions, 2))
    bound_after_y = max(abs(a.y() - b.y()) for a, b in itertools.permutations(new_positions, 2))
    print 'bound after', bound_after_x, bound_after_y

    ratio_x = bound_before_x / bound_after_x
    ratio_y = bound_before_y / bound_after_y
    print 'ratio', ratio_x, ratio_y
    new_positions = [QtCore.QPointF(pos.x() * ratio_x, pos.y() * ratio_y) for pos in new_positions]

    # Adjust translate
    average_pos_after = QtCore.QPointF()
    for pos in new_positions:
        average_pos_after += pos
    average_pos_after /= len(new_positions)
    print 'average_pos_after', average_pos_after

    offset = average_pos_before - average_pos_after
    print 'offset', offset
    new_positions = [pos + offset for pos in new_positions]

    for node, pos in zip(nodes, new_positions):
        # print node, pos
        node.setGraphPos(pos)


def _get_bounds_from_nodes(nodes):
    bounds = QtCore.QRectF()
    for node in nodes:
        bounds |= node.boundingRect()
    return bounds


def recenter_nodes(nodes):
    bound = _get_bounds_from_nodes(nodes)
    center = bound.center()
    for node in nodes:
        pos = node.getGraphPos()
        pos -= center
        node.setGraphPos(pos)
