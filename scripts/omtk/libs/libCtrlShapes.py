import pymel.core as pymel
from maya import OpenMaya
from maya import cmds
from omtk.libs import libRigging

def create_shape_circle(size=1.0, normal=(1, 0, 0), *args, **kwargs):
    transform, make = pymel.circle(*args, **kwargs)
    make.radius.set(size)
    make.normal.set(normal)

    # Expose the rotateOrder
    transform.rotateOrder.setKeyable(True)

    make.radius.set(size)
    make.degree.set(1)
    make.sections.set(8)
    return transform, make


def create_shape_needle(size=1, length=None, radius=None, name=None, normal=(0, 1, 0), *args, **kwargs):
    # TODO: docstring
    # Resolve length
    # Default length is 4x the provided size
    if length is None:
        length = size * 1.0

    # Resolve radius
    if radius is None:
        radius = size * 0.25
    radius_mid = radius * 0.75

    y_circle_mid_max = length + radius_mid
    y_circle_mid_min = length - radius_mid
    y_circle_min = length - radius
    y_circle_max = length + radius
    xz_circle_rad = radius
    xz_circle_mid_rad = xz_circle_rad * 0.75

    shape1 = pymel.curve(d=1, p=[
        (0.0, 0.0, 0.0),
        (0.0, y_circle_min, 0.0)
    ])
    shape2 = pymel.curve(d=1, p=[
        (0.0, y_circle_max, -0.0),
        (0.0, y_circle_max, 0.0),
        (xz_circle_mid_rad, y_circle_mid_max, 0.0),
        (xz_circle_rad, length, 0.0),
        (xz_circle_mid_rad, y_circle_mid_min, 0.0),
        (0.0, y_circle_min, 0),
        (-xz_circle_mid_rad, y_circle_mid_min, -0.0),
        (-xz_circle_rad, length, 0.0),
        (-xz_circle_mid_rad, y_circle_mid_max, 0.0),
        (0.0, y_circle_max, 0.0),
        (xz_circle_mid_rad, y_circle_mid_max, 0.0)
    ])
    shape3 = pymel.curve(d=1, p=[
        (-xz_circle_mid_rad, length, -xz_circle_mid_rad),
        (-xz_circle_rad, length, 0.0),
        (-xz_circle_mid_rad, length, xz_circle_mid_rad),
        (0.0, length, xz_circle_rad),
        (xz_circle_mid_rad, length, xz_circle_mid_rad),
        (xz_circle_rad, length, 0.0),
        (xz_circle_mid_rad, length, -xz_circle_mid_rad),
        (0.0, length, -xz_circle_rad),
        (-xz_circle_mid_rad, length, -xz_circle_mid_rad),
        (-xz_circle_rad, length, 0.0),
        (-xz_circle_rad, length, 0.0)
    ])
    shape2.getShape().setParent(shape1, shape=True, relative=True)
    shape3.getShape().setParent(shape1, shape=True, relative=True)
    pymel.delete(shape2)
    pymel.delete(shape3)

    # Apply normal parameter
    # TODO: Find a better way
    need_identity = True
    normal_x, normal_y, normal_z = normal
    if normal_x:
        if normal_x < 0:
            shape1.rotateZ.set(90)
        else:
            shape1.rotateZ.set(-90)
    elif normal_y:
        if normal_y < 0:
            shape1.rotateX.set(180)
        else:
            need_identity = False
    elif normal_z:
        if normal_z < 0:
            shape1.rotateX.set(-90)
        else:
            shape1.rotateX.set(90)
    if need_identity:
        pymel.makeIdentity(shape1, apply=True, rotate=True)

    if name:
        shape1.rename(name)

    # Expose the rotateOrder
    shape1.rotateOrder.setKeyable(True)

    return shape1


def create_shape_double_needle(normal=(0, 1, 0), *args, **kwargs):
    normal_inv = (normal[0] * -1, normal[1] * -1, normal[2] * -1)  # TODO: find an eleguant way
    shape1 = create_shape_needle(normal=normal, *args, **kwargs)
    shape2 = create_shape_needle(normal=normal_inv, *args, **kwargs)
    for shape in shape2.getShapes():
        shape.setParent(shape1, shape=True, relative=True)
    pymel.delete(shape2)

    # Expose the rotateOrder
    shape1.rotateOrder.setKeyable(True)

    return shape1


def create_shape_cross(size=1.0, **kwargs):
    s1 = size * 0.5
    s2 = size
    node = pymel.curve(d=1, p=[
        (0,-s1,s1),
        (0,-s1,s2),
        (0,s1,s2),
        (0,s1,s1),
        (0,s2,s1),
        (0,s2,-s1),
        (0,s1,-s1),
        (0,s1,-s2),
        (0,-s1,-s2),
        (0,-s1,-s1),
        (0,-s2,-s1),
        (0,-s2,s1),
        (0,-s1,s1)
    ], **kwargs)

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node


def create_shape_attrholder(size=1.0, **kwargs):
    s1 = size
    s2 = s1 * 0.7
    node = pymel.curve(d=1, p=[(0,0,s1),(0,s2,s2),(0,s1,0),(0,s2,-s2),(0,0,-s1),(0,-s2,-s2),(0,-s1,0),(0,-s2,s2),(0,0,s1),(-s2,0,s2),(-s1,0,0),(-s2,s2,0),(0,s1,0),(s2,s2,0),(s1,0,0),(s2,0,-s2),(0,0,-s1),(-s2,0,-s2),(-s1,0,0),(-s2,-s2,0),(0,-s1,0),(s2,-s2,0),(s1,0,0),(s2,0,s2),(0,0,s1),(-s2,0,s2)], k=range(26), *kwargs)

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node


def create_shape_box(size=1.0, r=None, h=None):
    if r is None:
        r = size

    if h is None:
        h = size / 5.0

    node = pymel.curve(d=1, p=[(-r, -h, r), (-r, h, r), (r, h, r), (r, -h, r), (-r, -h, r), (-r, -h, -r), (-r, h, -r), (-r, h, r), (r, h, r), (r, h, -r), (r, -h, -r), (r, -h, r), (r, -h, -r), (-r, -h, -r), (-r, h, -r), (r, h, -r)] )

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node

def _get_bounds_using_raycast(positions, dirs, geometries, parent_tm=None, filter=None):
    min_x = max_x = min_y = max_y = min_z = max_z = None
    parent_tm_inv = parent_tm.inverse()

    # Ray-cast
    for pos in positions:
        #x = pos.x
        #y = pos.y
        #z = pos.z

        # Expand bounds using starting positions.
        pos_local = pymel.datatypes.Point(pos) * parent_tm_inv if parent_tm is not None else pos
        x_local = pos_local.x
        y_local = pos_local.y
        z_local = pos_local.z
        if min_x is None or x_local < min_x:
            min_x = x_local
        if max_x is None or x_local > max_x:
            max_x = x_local
        if min_y is None or y_local < min_y:
            min_y = y_local
        if max_y is None or y_local > max_y:
            max_y = y_local
        if min_z is None or z_local < min_z:
            min_z = z_local
        if max_z is None or z_local > max_z:
            max_z = z_local

        for dir in dirs:
            ray_cast_pos = libRigging.ray_cast_nearest(pos, dir, geometries, debug=False)
            if ray_cast_pos is None:
                continue

            if parent_tm is not None:
                ray_cast_pos = ray_cast_pos * parent_tm_inv

            x = ray_cast_pos.x
            y = ray_cast_pos.y
            z = ray_cast_pos.z
            if min_x is None or x < min_x:
                min_x = x
            if max_x is None or x > max_x:
                max_x = x
            if min_y is None or y < min_y:
                min_y = y
            if max_y is None or y > max_y:
                max_y = y
            if min_z is None or z < min_z:
                min_z = z
            if max_z is None or z > max_z:
                max_z = z

    return min_x, max_x, min_y, max_y, min_z, max_z

def create_shape_box_arm(refs, geometries, epsilon=0.01, default_size=1.0):
    # TODO: Prevent crashes when there's no geometries
    ref = next(iter(refs))
    ref_tm = ref.getMatrix(worldSpace=True)
    positions = [r.getTranslation(space='world') for r in refs]

    # Resolve raycast directions
    dir_offset_tm = pymel.datatypes.Matrix(  # Remove translation from ref_tm to keep direction normalized.
        ref_tm.a00, ref_tm.a01, ref_tm.a02, ref_tm.a03,
        ref_tm.a10, ref_tm.a11, ref_tm.a12, ref_tm.a13,
        ref_tm.a20, ref_tm.a21, ref_tm.a22, ref_tm.a23,
        0,          0,          0,          1
    )
    x_pos = ref.getTranslation(space='world').x
    dirs = [
        OpenMaya.MPoint(0,-1,0) * dir_offset_tm,
        OpenMaya.MPoint(0,1,0) * dir_offset_tm,
        OpenMaya.MPoint(0,0,-1) * dir_offset_tm,
        OpenMaya.MPoint(0,0,1) * dir_offset_tm
    ]
    # HACK : Check the x_position to know in which direction we need to do the raycast
    if x_pos >= 0.0:
        dirs.append(
            OpenMaya.MPoint(1,0,0) * dir_offset_tm,
        )
    else:
        dirs.append(
            OpenMaya.MPoint(-1,0,0) * dir_offset_tm,
        )

    min_x, max_x, min_y, max_y, min_z, max_z = _get_bounds_using_raycast(positions, dirs, geometries, parent_tm=ref_tm)

    # Ensure a minimum size for the ctrl
    if (max_x - min_x) < epsilon:
        max_x = default_size
    if (max_y - min_y) < epsilon:
        min_y = -default_size * 0.5
        max_y = default_size * 0.5
    if (max_z - min_z) < epsilon:
        min_z = -default_size * 0.5
        max_z = default_size * 0.5

    # Convert our bouding box
    #min_x = 0

    pos1 = pymel.datatypes.Point(min_x, min_y, min_z)
    pos2 = pymel.datatypes.Point(min_x, min_y, max_z)
    pos3 = pymel.datatypes.Point(min_x, max_y, min_z)
    pos4 = pymel.datatypes.Point(min_x, max_y, max_z)
    pos5 = pymel.datatypes.Point(max_x, min_y, min_z)
    pos6 = pymel.datatypes.Point(max_x, min_y, max_z)
    pos7 = pymel.datatypes.Point(max_x, max_y, min_z)
    pos8 = pymel.datatypes.Point(max_x, max_y, max_z)

    node = pymel.curve(d=1, p=[pos2, pos4, pos8, pos6, pos2, pos1, pos3, pos4, pos8, pos7, pos5, pos6, pos5, pos1, pos3, pos7] )

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node


def create_shape_box_feet(refs, geometries, *args, **kwargs):
    ref = next(iter(refs))
    ref_pos = ref.getTranslation(space='world')
    ref_tm = pymel.datatypes.Matrix(
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        ref_pos.x, ref_pos.y, ref_pos.z, 1
    )

    positions = [ref.getTranslation(space='world') for ref in refs]
    dirs = [
        OpenMaya.MVector(-1,0,0),
        OpenMaya.MVector(1,0,0),
        OpenMaya.MVector(0,0,-1),
        OpenMaya.MVector(0,0,1)
    ]

    # Sanity check, ensure that at least one point is in the bounds of geometries.
    # This can prevent rays from being fired from outside a geometry.
    # TODO: Make it more robust.
    filtered_geometries = []
    for geometry in geometries:
        xmin, ymin, zmin, xmax, ymax, zmax = cmds.exactWorldBoundingBox(geometry.__melobject__())
        bound = pymel.datatypes.BoundingBox((xmin, ymin, zmin), (xmax, ymax, zmax))
        if any(True for pos in positions if bound.contains(pos)):
            filtered_geometries.append(geometry)


    # Using all provided objects
    min_x, max_x, min_y, max_y, min_z, max_z = _get_bounds_using_raycast(positions, dirs, filtered_geometries, parent_tm=ref_tm)
    min_y = min(min_y, - ref_pos.y)

    # If no geometry was provided, there won't be any width in the returned values.
    if not geometries:
        length = max_z - min_z
        desired_width = length * 0.25
        min_x = -desired_width
        max_x = desired_width

    pos1 = pymel.datatypes.Point(min_x, min_y, min_z)
    pos2 = pymel.datatypes.Point(min_x, min_y, max_z)
    pos3 = pymel.datatypes.Point(min_x, max_y, min_z)
    pos4 = pymel.datatypes.Point(min_x, max_y, max_z)
    pos5 = pymel.datatypes.Point(max_x, min_y, min_z)
    pos6 = pymel.datatypes.Point(max_x, min_y, max_z)
    pos7 = pymel.datatypes.Point(max_x, max_y, min_z)
    pos8 = pymel.datatypes.Point(max_x, max_y, max_z)


    # HACK: Convert to local space...
    '''
    ref = next(iter(refs))
    pos = ref.getTranslation(space='world')
    pos1 -= pos
    pos2 -= pos
    pos3 -= pos
    pos4 -= pos
    pos5 -= pos
    pos6 -= pos
    pos7 -= pos
    pos8 -= pos
    '''


    node = pymel.curve(d=1, p=[pos2, pos4, pos8, pos6, pos2, pos1, pos3, pos4, pos8, pos7, pos5, pos6, pos5, pos1, pos3, pos7] )

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node


def create_square(size=1.0, width=None, height=None, **kwargs):
    if width is None:
        width = 1.0
    if height is None:
        height = 1.0
    width *= size
    height *= size

    pos1 = pymel.datatypes.Point(-height, -width, 0)
    pos2 = pymel.datatypes.Point(-height, width, 0)
    pos3 = pymel.datatypes.Point(height, width, 0)
    pos4 = pymel.datatypes.Point(height, -width, 0)
    pos5 = pymel.datatypes.Point(-height, -width, 0)

    node = pymel.curve(d=1, p=[pos1, pos2, pos3, pos4, pos5] )

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node

def create_triangle_upp():
    p1 = [0, 0.577, 0]
    p2 = [-0.5, -0.288, 0]
    p3 = [0.5, -0.288, 0]
    node = pymel.curve(d=1, p=[p1, p2, p3, p1] )

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node

def create_triangle_low():
    p1 = [0, -0.577, 0]
    p2 = [-0.5, 0.288, 0]
    p3 = [0.5, 0.288, 0]
    node = pymel.curve(d=1, p=[p1, p2, p3, p1] )

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node

def create_triangle_left():
    p1 = [0.577, 0, 0]
    p2 = [-0.288, -0.5, 0]
    p3 = [-0.288, 0.5, 0]
    node = pymel.curve(d=1, p=[p1, p2, p3, p1] )

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node

def create_triangle_right():
    p1 = [-0.577, 0, 0]
    p2 = [0.288, -0.5, 0]
    p3 = [0.288, 0.5, 0]
    node = pymel.curve(d=1, p=[p1, p2, p3, p1] )

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node

