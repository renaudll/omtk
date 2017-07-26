import logging

from omtk import constants
from omtk import factory_datatypes
from omtk.vendor.Qt import QtCore
from pymel import core as pymel

log = logging.getLogger('omtk')

_GRAPH_POS_ATTR_NAME = constants.PyFlowGraphMetadataKeys.Position


def _walk_downstream(node):
    known = set()
    for port in node.iter_input_ports():
        connections = port.inCircle().getConnections()
        for connection in connections:
            src = connection.getSrcPort()
            dst = connection.getDstPort()

            connected_node = src.getNode()
            if connected_node in known:
                continue
            known.add(connected_node)

            # Ignore known nodes
            yield connected_node


def _walk_upstream(node):
    known = set()
    for port in node.iter_output_ports():
        connections = port.outCircle().getConnections()
        for connection in connections:
            src = connection.getSrcPort()
            dst = connection.getDstPort()

            connected_node = dst.getNode()
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

    # Resolve nb of nodes on top level
    # Filter any node that don't share the same parent space.
    leaf_nodes = list(iter_leaf_nodes(node, _walk_upstream))
    children = list(_walk_downstream(node))
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


def arrange_downstream(node, padding_x=32, padding_y=10):
    parent_pos = node.getGraphPos()

    # Resolve nb of nodes on top level
    # Filter any node that don't share the same parent space.
    leaf_nodes = list(iter_leaf_nodes(node, _walk_downstream))
    children = list(_walk_downstream(node))
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
    pos_y = parent_pos.y() - total_height * 0.5

    # Reposition all children
    known_nodes = set()
    num_children = len(children)
    pos_y_increments = total_height / (num_children - 1)
    for i, child, in enumerate(children):
        if child in known_nodes:
            continue
        known_nodes.add(child)

        pos_y += pos_y_increments  # child.size().height() * 0.5
        log.debug('Repositionning {} ({}) to {}, {}'.format(
            child, child.getName(), pos_x, pos_y
        ))
        child.setGraphPos(QtCore.QPointF(
            pos_x - (child.size().width() * 0.5),
            pos_y
        ))
        pos_y += child.size().height() + padding_y
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


def spring_layout(nodes, nodes_to_ignore=None):
    # Step 1: Resolve nodes
    # Step 2: Resolve positions
    # Step 3: Resolve edges
    from omtk.vendor.jurij import graph

    nodes = list(nodes)

    node_positions = []
    for node in nodes:
        pos = node.getGraphPos()
        node_positions.append((pos.x(), pos.y()))

    vertices = range(len(nodes))

    edges = []
    for i, node in enumerate(nodes):
        for upstream_node in _walk_upstream(node):
            try:
                j = nodes.index(upstream_node)
            except ValueError:
                continue
            edges.append((j, i))
        for downstream_node in _walk_downstream(node):
            try:
                j = nodes.index(downstream_node)
            except ValueError:
                continue
            edges.append((i, j))

    layout = {}
    for node, position in zip(vertices, node_positions):
        layout[node] = position

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
            if u in vertices_to_ignore:
                continue
            # Compute the acceleration of u
            (x, y) = layout[u]
            (ax, ay) = (0, 0)
            for v in graph.vertices():
                if u != v:
                    (a, b) = layout[v]
                    d = max(0.001, (x - a) * (x - a) + (y - b) * (y - b))
                    # Columb's law
                    ax -= columb * (a - x) / (d * d)
                    ay -= columb * (b - y) / (d * d)
            for v in graph.adjacency[u]:
                # Hook's law
                (a, b) = layout[v]
                ax += hook * (a - x)
                ay += hook * (b - y)
            for v in graph.opposite()[u]:
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

    for node, (x, y) in zip(nodes, layout.itervalues()):
        node.setGraphPos(QtCore.QPointF(x*1000.0, y*1000.0))
