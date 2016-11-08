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
        (0, -s1, s1),
        (0, -s1, s2),
        (0, s1, s2),
        (0, s1, s1),
        (0, s2, s1),
        (0, s2, -s1),
        (0, s1, -s1),
        (0, s1, -s2),
        (0, -s1, -s2),
        (0, -s1, -s1),
        (0, -s2, -s1),
        (0, -s2, s1),
        (0, -s1, s1)
    ], **kwargs)

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node


def create_shape_attrholder(size=1.0, **kwargs):
    s1 = size
    s2 = s1 * 0.7
    node = pymel.curve(d=1,
                       p=[(0, 0, s1), (0, s2, s2), (0, s1, 0), (0, s2, -s2), (0, 0, -s1), (0, -s2, -s2), (0, -s1, 0),
                          (0, -s2, s2), (0, 0, s1), (-s2, 0, s2), (-s1, 0, 0), (-s2, s2, 0), (0, s1, 0), (s2, s2, 0),
                          (s1, 0, 0), (s2, 0, -s2), (0, 0, -s1), (-s2, 0, -s2), (-s1, 0, 0), (-s2, -s2, 0), (0, -s1, 0),
                          (s2, -s2, 0), (s1, 0, 0), (s2, 0, s2), (0, 0, s1), (-s2, 0, s2)], k=range(26), *kwargs)

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node


def create_shape_box(size=1.0, r=None, h=None):
    if r is None:
        r = size

    if h is None:
        h = size / 5.0

    node = pymel.curve(d=1, p=[(-r, -h, r), (-r, h, r), (r, h, r), (r, -h, r), (-r, -h, r), (-r, -h, -r), (-r, h, -r),
                               (-r, h, r), (r, h, r), (r, h, -r), (r, -h, -r), (r, -h, r), (r, -h, -r), (-r, -h, -r),
                               (-r, h, -r), (r, h, -r)])

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node


def _get_bounds_using_raycast(positions, dirs, geometries, parent_tm=None, filter=None):
    min_x = max_x = min_y = max_y = min_z = max_z = None
    parent_tm_inv = parent_tm.inverse()

    # Ray-cast
    for pos in positions:
        # x = pos.x
        # y = pos.y
        # z = pos.z

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
        0, 0, 0, 1
    )
    x_pos = ref.getTranslation(space='world').x
    dirs = [
        OpenMaya.MPoint(0, -1, 0) * dir_offset_tm,
        OpenMaya.MPoint(0, 1, 0) * dir_offset_tm,
        OpenMaya.MPoint(0, 0, -1) * dir_offset_tm,
        OpenMaya.MPoint(0, 0, 1) * dir_offset_tm
    ]
    # HACK : Check the x_position to know in which direction we need to do the raycast
    if x_pos >= 0.0:
        dirs.append(
            OpenMaya.MPoint(1, 0, 0) * dir_offset_tm,
        )
    else:
        dirs.append(
            OpenMaya.MPoint(-1, 0, 0) * dir_offset_tm,
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
    # min_x = 0

    pos1 = pymel.datatypes.Point(min_x, min_y, min_z)
    pos2 = pymel.datatypes.Point(min_x, min_y, max_z)
    pos3 = pymel.datatypes.Point(min_x, max_y, min_z)
    pos4 = pymel.datatypes.Point(min_x, max_y, max_z)
    pos5 = pymel.datatypes.Point(max_x, min_y, min_z)
    pos6 = pymel.datatypes.Point(max_x, min_y, max_z)
    pos7 = pymel.datatypes.Point(max_x, max_y, min_z)
    pos8 = pymel.datatypes.Point(max_x, max_y, max_z)

    node = pymel.curve(d=1, p=[pos2, pos4, pos8, pos6, pos2, pos1, pos3, pos4, pos8, pos7, pos5, pos6, pos5, pos1, pos3,
                               pos7])

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
        OpenMaya.MVector(-1, 0, 0),
        OpenMaya.MVector(1, 0, 0),
        OpenMaya.MVector(0, 0, -1),
        OpenMaya.MVector(0, 0, 1)
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
    min_x, max_x, min_y, max_y, min_z, max_z = _get_bounds_using_raycast(positions, dirs, filtered_geometries,
                                                                         parent_tm=ref_tm)
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

    node = pymel.curve(d=1, p=[pos2, pos4, pos8, pos6, pos2, pos1, pos3, pos4, pos8, pos7, pos5, pos6, pos5, pos1, pos3,
                               pos7])

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

    node = pymel.curve(d=1, p=[pos1, pos2, pos3, pos4, pos5])

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node


def create_triangle_upp():
    p1 = [0, 0.577, 0]
    p2 = [-0.5, -0.288, 0]
    p3 = [0.5, -0.288, 0]
    node = pymel.curve(d=1, p=[p1, p2, p3, p1])

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node


def create_triangle_low():
    p1 = [0, -0.577, 0]
    p2 = [-0.5, 0.288, 0]
    p3 = [0.5, 0.288, 0]
    node = pymel.curve(d=1, p=[p1, p2, p3, p1])

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node


def create_triangle_left():
    p1 = [0.577, 0, 0]
    p2 = [-0.288, -0.5, 0]
    p3 = [-0.288, 0.5, 0]
    node = pymel.curve(d=1, p=[p1, p2, p3, p1])

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node


def create_triangle_right():
    p1 = [-0.577, 0, 0]
    p2 = [0.288, -0.5, 0]
    p3 = [0.288, 0.5, 0]
    node = pymel.curve(d=1, p=[p1, p2, p3, p1])

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)


#
# JG implement from fSanges controler shape bank
#
'''def create_shape_cross(size=1.0, **kwargs):
    s1 = size * 0.5
    s2 = size
    node = pymel.curve(d=1, p=[
        (0, -s1, s1),
        (0, -s1, s2),
        (0, s1, s2),
        (0, s1, s1),
        (0, s2, s1),
        (0, s2, -s1),
        (0, s1, -s1),
        (0, s1, -s2),
        (0, -s1, -s2),
        (0, -s1, -s1),
        (0, -s2, -s1),
        (0, -s2, s1),
        (0, -s1, s1)
    ], **kwargs)

    # Expose the rotateOrder
    node.rotateOrder.setKeyable(True)

    return node'''


def pin(scale=(1, 1, 1), **kwargs):
    points = [[0.0, 0.0, 0.0], [0.0, 3.0, 0.0], [-0.5, 4.0, -0.5], [-0.5, 4.0, 0.0], [-0.5, 4.0, 0.5], [0.0, 3.0, 0.0],
              [0.5, 4.0, 0.5], [0.5, 4.0, -0.5], [0.0, 3.0, 0.0], [0.5, 4.0, -0.5], [0.0, 4.0, -0.5], [0.0, 4.0, 0.5],
              [-0.5, 4.0, 0.5], [0.5, 4.0, 0.5], [0.5, 4.0, 0.0], [-0.5, 4.0, 0.0], [-0.5, 4.0, -0.5], [0.0, 4.0, -0.5]]
    node = pymel.curve(p=points, d=1)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    node.rotateOrder.setKeyable(True)
    return node


def sphere(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(0.0, 0.0, 1.0), (0.0, 0.5, 0.866025), (0.0, 0.866025, 0.5), (0.0, 1.0, 0.0),
                          (0.0, 0.866025, -0.5),
                          (0.0, 0.5, -0.866025), (0.0, 0.0, -1.0), (0.0, -0.5, -0.866025), (0.0, -0.866025, -0.5),
                          (0.0, -1.0, 0.0), (0.0, -0.866025, 0.5), (0.0, -0.5, 0.866025), (0.0, 0.0, 1.0),
                          (0.707107, 0.0, 0.707107), (1.0, 0.0, 0.0), (0.707107, 0.0, -0.707107), (0.0, 0.0, -1.0),
                          (-0.707107, 0.0, -0.707107), (-1.0, 0.0, 0.0), (-0.866025, 0.5, 0.0), (-0.5, 0.866025, 0.0),
                          (0.0, 1.0, 0.0), (0.5, 0.866025, 0.0), (0.866025, 0.5, 0.0), (1.0, 0.0, 0.0),
                          (0.866025, -0.5, 0.0),
                          (0.5, -0.866025, 0.0), (0.0, -1.0, 0.0), (-0.5, -0.866025, 0.0), (-0.866025, -0.5, 0.0),
                          (-1.0, 0.0, 0.0), (-0.707107, 0.0, 0.707107), (0.0, 0.0, 1.0)])

    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    node.rotateOrder.setKeyable(True)

    return node


def squareCrossDouble(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(0.0400343919558555, 1.0008597988963874, 1.0008597988963874),
                          (0.0400343919558555, 1.0008597988963874, -1.0008597988963874),
                          (0.0400343919558555, -1.0008597988963874, -1.0008597988963874),
                          (0.0400343919558555, -1.0008597988963874, 1.0008597988963874),
                          (0.0400343919558555, 1.0008597988963874, 1.0008597988963874),
                          (-0.0400343919558555, 1.0008597988963874, 1.0008597988963874),
                          (-0.0400343919558555, 1.0008597988963874, 0.0),
                          (0.0400343919558555, 1.0008597988963874, 0.0),
                          (-0.0400343919558555, 1.0008597988963874, 0.0),
                          (-0.0400343919558555, 1.0008597988963874, -1.0008597988963874),
                          (0.0400343919558555, 1.0008597988963874, -1.0008597988963874),
                          (-0.0400343919558555, 1.0008597988963874, -1.0008597988963874),
                          (-0.0400343919558555, 0.0, -1.0008597988963874),
                          (0.0400343919558555, 0.0, -1.0008597988963874),
                          (-0.0400343919558555, 0.0, -1.0008597988963874),
                          (-0.0400343919558555, -1.0008597988963874, -1.0008597988963874),
                          (0.0400343919558555, -1.0008597988963874, -1.0008597988963874),
                          (-0.0400343919558555, -1.0008597988963874, -1.0008597988963874),
                          (-0.0400343919558555, -1.0008597988963874, 0.0),
                          (0.0400343919558555, -1.0008597988963874, 0.0),
                          (-0.0400343919558555, -1.0008597988963874, 0.0),
                          (-0.0400343919558555, -1.0008597988963874, 1.0008597988963874),
                          (0.0400343919558555, -1.0008597988963874, 1.0008597988963874),
                          (-0.0400343919558555, -1.0008597988963874, 1.0008597988963874),
                          (-0.0400343919558555, 0.0, 1.0008597988963874),
                          (0.0400343919558555, 0.0, 1.0008597988963874),
                          (-0.0400343919558555, 0.0, 1.0008597988963874),
                          (-0.0400343919558555, 1.0008597988963874, 1.0008597988963874),
                          (0.0400343919558555, 1.0008597988963874, 1.0008597988963874),
                          (-0.0400343919558555, 1.0008597988963874, 1.0008597988963874),
                          (-0.0400343919558555, 1.0008597988963874, 0.0),
                          (0.0, 1.0008597988963874, 0.0),
                          (0.0, 0.0, 0.0),
                          (0.0, -1.0008597988963874, 0.0),
                          (0.0, 0.0, 0.0),
                          (0.0, 0.0, 1.0008597988963874),
                          (0.0, 0.0, 0.0),
                          (0.0, 0.0, -1.0008597988963874)])
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    node.rotateOrder.setKeyable(True)
    return node


def squareCross(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(0.0, -1.0000556035094568, 0.0),
                          (0.0, -1.0000556035094568, 1.0000556035094568),
                          (0.0, 0.0, 1.0000556035094568),
                          (0.0, 0.0, 0.0),
                          (0.0, -1.0000556035094568, 0.0),
                          (0.0, -1.0000556035094568, -1.0000556035094568),
                          (0.0, 0.0, -1.0000556035094568),
                          (0.0, 0.0, 0.0),
                          (0.0, 1.0000556035094568, 0.0),
                          (0.0, 1.0000556035094568, -1.0000556035094568),
                          (0.0, 0.0, -1.0000556035094568),
                          (0.0, 0.0, 1.0000556035094568),
                          (0.0, 1.0000556035094568, 1.0000556035094568),
                          (0.0, 1.0000556035094568, 0.0)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def doubleNail(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(18.620128438833536, 0.9926055308430259, 0.0),
                          (18.620128438833536, 0.9440237537332653, -0.30673123778574873),
                          (18.620128438833536, 0.8030340032072616, -0.5834393804767223),
                          (18.620128438833536, 0.5834393804767223, -0.8030340032072616),
                          (18.620128438833536, 0.30673123778574873, -0.9440237537332653),
                          (18.620128438833536, 0.0, -0.9926055308430259),
                          (18.620128438833536, 0.0, 0.0),
                          (18.620128438833536, 0.0, -0.9926055308430259),
                          (18.620128438833536, -0.30673123778574873, -0.9440237537332653),
                          (18.620128438833536, -0.5834393804767223, -0.8030340032072616),
                          (18.620128438833536, -0.8030340032072616, -0.5834393804767223),
                          (18.620128438833536, -0.9440237537332653, -0.30673123778574873),
                          (18.620128438833536, -0.9926055308430259, 0.0),
                          (18.620128438833536, -0.9440237537332653, 0.30673123778574873),
                          (18.620128438833536, -0.8030340032072616, 0.5834393804767223),
                          (18.620128438833536, -0.5834393804767223, 0.8030340032072616),
                          (18.620128438833536, -0.30673123778574873, 0.9440237537332653),
                          (18.620128438833536, -2.9581984252059225e-08, 0.9926055308430259),
                          (18.620128438833536, 0.0, 0.0),
                          (18.620128438833536, -2.9581984252059225e-08, 0.9926055308430259),
                          (18.620128438833536, 0.30673123778574873, 0.9440237537332653),
                          (18.620128438833536, 0.5834393804767223, 0.8030340032072616),
                          (18.620128438833536, 0.8030340032072616, 0.5834393804767223),
                          (18.620128438833536, 0.9440237537332653, 0.30673123778574873),
                          (18.620128438833536, 0.9926055308430259, 0.0),
                          (18.620128438833536, -0.9926055308430259, 0.0),
                          (18.620128438833536, 0.0, 0.0),
                          (-18.620128438833536, 0.0, 0.0),
                          (-18.620128438833536, 0.9926055308430259, 0.0),
                          (-18.620128438833536, 0.9440237537332653, -0.30673123778574873),
                          (-18.620128438833536, 0.8030340032072616, -0.5834393804767223),
                          (-18.620128438833536, 0.5834393804767223, -0.8030340032072616),
                          (-18.620128438833536, 0.30673123778574873, -0.9440237537332653),
                          (-18.620128438833536, 0.0, -0.9926055308430259),
                          (-18.620128438833536, 0.0, 0.0),
                          (-18.620128438833536, 0.0, -0.9926055308430259),
                          (-18.620128438833536, -0.30673123778574873, -0.9440237537332653),
                          (-18.620128438833536, -0.5834393804767223, -0.8030340032072616),
                          (-18.620128438833536, -0.8030340032072616, -0.5834393804767223),
                          (-18.620128438833536, -0.9440237537332653, -0.30673123778574873),
                          (-18.620128438833536, -0.9926055308430259, 0.0),
                          (-18.620128438833536, 0.0, 0.0),
                          (-18.620128438833536, -0.9926055308430259, 0.0),
                          (-18.620128438833536, -0.9440237537332653, 0.30673123778574873),
                          (-18.620128438833536, -0.8030340032072616, 0.5834393804767223),
                          (-18.620128438833536, -0.5834393804767223, 0.8030340032072616),
                          (-18.620128438833536, -0.30673123778574873, 0.9440237537332653),
                          (-18.620128438833536, -2.9581984252059225e-08, 0.9926055308430259),
                          (-18.620128438833536, 0.0, 0.0),
                          (-18.620128438833536, -2.9581984252059225e-08, 0.9926055308430259),
                          (-18.620128438833536, 0.30673123778574873, 0.9440237537332653),
                          (-18.620128438833536, 0.5834393804767223, 0.8030340032072616),
                          (-18.620128438833536, 0.8030340032072616, 0.5834393804767223),
                          (-18.620128438833536, 0.9440237537332653, 0.30673123778574873),
                          (-18.620128438833536, 0.9926055308430259, 0.0)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def belt(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=3,
                       p=[(1.0, -0.0270125, 0.9561633173795626),
                          (1.0, -0.0218525, 0.977071983697364),
                          (1.0, -0.0083475, 0.9899884834818498),
                          (1.0, 0.0083475, 0.9899884834818498),
                          (1.0, 0.0218525, 0.977071983697364),
                          (1.0, 0.0270125, 0.9561633173795626),
                          (1.0, 0.0270125, 0.04066524932149242),
                          (1.0, 0.0270125, -0.9899884834818498),
                          (0.0, 0.0270125, -0.9899884834818498),
                          (-1.0, 0.0270125, -0.9899884834818498),
                          (-1.0, 0.0270125, 0.04066524932149242),
                          (-1.0, 0.0270125, 0.9561633173795626),
                          (-1.0, 0.0270125, 0.9561633173795626),
                          (-1.0, 0.0270125, 0.9561633173795626),
                          (-1.0, 0.0270125, 0.9561633173795626),
                          (-1.0, 0.0218525, 0.977071983697364),
                          (-1.0, 0.0083475, 0.9899884834818498),
                          (-1.0, -0.0083475, 0.9899884834818498),
                          (-1.0, -0.0218525, 0.977071983697364),
                          (-1.0, -0.0270125, 0.9561633173795626),
                          (-1.0, -0.0270125, 0.9561633173795626),
                          (-1.0, -0.0270125, 0.9561633173795626),
                          (-1.0, -0.0270125, 0.04066524932149242),
                          (-1.0, -0.0270125, -0.9899884834818498),
                          (0.0, -0.0270125, -0.9899884834818498),
                          (1.0, -0.0270125, -0.9899884834818498),
                          (1.0, -0.0270125, 0.04066524932149242),
                          (1.0, -0.0270125, 0.9561633173795626),
                          (1.0, -0.0270125, 0.9561633173795626),
                          (1.0, -0.0270125, 0.9561633173795626),
                          (1.0, -0.0270125, 0.9561633173795626)])

    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def circle3D(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(8.326449999999999e-09, 0.05, 0.880094), (0.195839, 0.05, 0.858028),
                          (0.381858, 0.05, 0.792937), (0.54873, 0.05, 0.688085), (0.688085, 0.05, 0.54873),
                          (0.792937, 0.05, 0.381858), (0.858028, 0.05, 0.195839), (0.880094, 0.05, 1.42939e-08),
                          (0.880094, -0.05, 1.42939e-08), (0.880094, 0.05, 1.42939e-08), (0.858028, 0.05, -0.195839),
                          (0.792937, 0.05, -0.381858), (0.688085, 0.05, -0.548729), (0.548729, 0.05, -0.688085),
                          (0.381858, 0.05, -0.792937),
                          (0.195839, 0.05, -0.858028), (6.07841e-08, 0.05, -0.880094), (6.07841e-08, -0.05, -0.880094),
                          (6.07841e-08, 0.05, -0.880094), (-0.195839, 0.05, -0.858028), (-0.381858, 0.05, -0.792937),
                          (-0.548729, 0.05, -0.688085), (-0.688085, 0.05, -0.548729), (-0.792937, 0.05, -0.381858),
                          (-0.858028, 0.05, -0.195839), (-0.880094, 0.05, -2.5049299999999998e-08),
                          (-0.880094, -0.05, -1.84921e-08), (-0.880094, 0.05, -2.5049299999999998e-08),
                          (-0.858028, 0.05, 0.195839), (-0.792937, 0.05, 0.381858), (-0.688085, 0.05, 0.548729),
                          (-0.548729, 0.05, 0.688085), (-0.381858, 0.05, 0.792937), (-0.195839, 0.05, 0.858028),
                          (8.326449999999999e-09, 0.05, 0.880094), (8.326449999999999e-09, -0.05, 0.880094),
                          (-1.49012e-08, -0.05, 1.0), (8.326449999999999e-09, -0.05, 0.880094),
                          (-0.195839, -0.05, 0.858028), (-0.381858, -0.05, 0.792937), (-0.548729, -0.05, 0.688085),
                          (-0.688085, -0.05, 0.548729), (-0.792937, -0.05, 0.381858), (-0.858028, -0.05, 0.195839),
                          (-0.880094, -0.05, -1.84921e-08), (-0.858028, -0.05, -0.195839),
                          (-0.792937, -0.05, -0.381858),
                          (-0.688085, -0.05, -0.548729), (-0.548729, -0.05, -0.688085), (-0.381858, -0.05, -0.792937),
                          (-0.195839, -0.05, -0.858028), (6.07841e-08, -0.05, -0.880094), (0.195839, -0.05, -0.858028),
                          (0.381858, -0.05, -0.792937), (0.548729, -0.05, -0.688085), (0.688085, -0.05, -0.548729),
                          (0.792937, -0.05, -0.381858), (0.858028, -0.05, -0.195839), (0.880094, -0.05, 1.42939e-08),
                          (0.858028, -0.05, 0.195839), (0.792937, -0.05, 0.381858), (0.688085, -0.05, 0.54873),
                          (0.54873, -0.05, 0.688085), (0.381858, -0.05, 0.792937), (0.195839, -0.05, 0.858028),
                          (8.326449999999999e-09, -0.05, 0.880094), (-1.49012e-08, -0.05, 1.0),
                          (-2.98023e-08, 0.05, 1.0),
                          (8.326449999999999e-09, 0.05, 0.880094), (-2.98023e-08, 0.05, 1.0),
                          (0.222521, 0.05, 0.974928),
                          (0.433884, 0.05, 0.900969), (0.62349, 0.05, 0.781831), (0.781831, 0.05, 0.62349),
                          (0.900969, 0.05, 0.433884), (0.974928, 0.05, 0.222521), (1.0, 0.05, 5.96046e-08),
                          (0.974928, 0.05, -0.222521), (0.900968, 0.05, -0.433884), (0.781831, 0.05, -0.62349),
                          (0.62349, 0.05, -0.781831), (0.433884, 0.05, -0.900968), (0.222521, 0.05, -0.974927),
                          (4.47035e-08, 0.05, -1.0), (6.07841e-08, 0.05, -0.880094), (6.07841e-08, -0.05, -0.880094),
                          (4.47035e-08, -0.05, -1.0), (4.47035e-08, 0.05, -1.0), (-0.222521, 0.05, -0.974928),
                          (-0.433884, 0.05, -0.900968), (-0.62349, 0.05, -0.781831), (-0.781831, 0.05, -0.62349),
                          (-0.900968, 0.05, -0.433884), (-0.974928, 0.05, -0.222521), (-1.0, 0.05, -1.49012e-08),
                          (-0.880094, 0.05, -2.5049299999999998e-08), (-0.880094, -0.05, -1.84921e-08),
                          (-1.0, -0.05, -4.47035e-08), (-1.0, 0.05, -1.49012e-08), (-0.974928, 0.05, 0.222521),
                          (-0.900969, 0.05, 0.433884), (-0.781831, 0.05, 0.62349), (-0.62349, 0.05, 0.781831),
                          (-0.433884, 0.05, 0.900969), (-0.222521, 0.05, 0.974928), (-2.98023e-08, 0.05, 1.0),
                          (-1.49012e-08, -0.05, 1.0), (0.222521, -0.05, 0.974928), (0.433884, -0.05, 0.900969),
                          (0.62349, -0.05, 0.781831), (0.781831, -0.05, 0.62349), (0.900969, -0.05, 0.433884),
                          (0.974928, -0.05, 0.222521), (1.0, -0.05, 0.0), (1.0, 0.05, 5.96046e-08),
                          (0.880094, 0.05, 1.42939e-08), (0.880094, -0.05, 1.42939e-08), (1.0, -0.05, 0.0),
                          (0.974928, -0.05, -0.222521), (0.900968, -0.05, -0.433884), (0.781831, -0.05, -0.62349),
                          (0.62349, -0.05, -0.781831), (0.433884, -0.05, -0.900968), (0.222521, -0.05, -0.974927),
                          (4.47035e-08, -0.05, -1.0), (-0.222521, -0.05, -0.974928), (-0.433884, -0.05, -0.900968),
                          (-0.62349, -0.05, -0.781831), (-0.781831, -0.05, -0.62349), (-0.900968, -0.05, -0.433884),
                          (-0.974928, -0.05, -0.222521), (-1.0, -0.05, -4.47035e-08), (-0.974928, -0.05, 0.222521),
                          (-0.900969, -0.05, 0.433884), (-0.781831, -0.05, 0.62349), (-0.62349, -0.05, 0.781831),
                          (-0.433884, -0.05, 0.900969), (-0.222521, -0.05, 0.974928), (-1.49012e-08, -0.05, 1.0)]
                       )
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def circleCompass(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(-1.0158428554096877, 0.0, -5.120423080604854e-08),
                          (-0.681018134582272, 0.0, -1.938318811239675e-08),
                          (-0.6639434287466539, 0.0, -0.15154052914627025),
                          (-0.6135759095974554, 0.0, -0.29548232670069013),
                          (-0.5324412655171409, 0.0, -0.42460737145258975),
                          (-0.42460737145258975, 0.0, -0.5324412655171409),
                          (-0.29548232670069013, 0.0, -0.6135759095974554),
                          (-0.15154052914627025, 0.0, -0.6639434287466539),
                          (4.703483309085425e-08, 0.0, -0.681018134582272),
                          (2.1313436173076034e-09, 0.0, -1.0158428554096877),
                          (4.703483309085425e-08, 0.0, -0.681018134582272),
                          (0.15154052914627025, 0.0, -0.6639434287466539),
                          (0.29548232670069013, 0.0, -0.6135759095974554),
                          (0.42460737145258975, 0.0, -0.5324412655171409),
                          (0.5324412655171409, 0.0, -0.42460737145258975),
                          (0.6135759095974554, 0.0, -0.29548232670069013),
                          (0.6639434287466539, 0.0, -0.15154052914627025),
                          (0.681018134582272, 0.0, 1.1060642515351244e-08),
                          (1.0158428554096877, 0.0, 2.4481998914655333e-08),
                          (0.681018134582272, 0.0, 1.1060642515351244e-08),
                          (0.6639434287466539, 0.0, 0.15154052914627025),
                          (0.6135759095974554, 0.0, 0.29548232670069013),
                          (0.5324412655171409, 0.0, 0.42460814525417756),
                          (0.42460814525417756, 0.0, 0.5324412655171409),
                          (0.29548232670069013, 0.0, 0.6135759095974554),
                          (0.15154052914627025, 0.0, 0.6639434287466539), (6.4430202304442e-09, 0.0, 0.681018134582272),
                          (-7.35548706273645e-08, 0.0, 1.0158428554096877),
                          (6.4430202304442e-09, 0.0, 0.681018134582272),
                          (-0.15154052914627025, 0.0, 0.6639434287466539),
                          (-0.29548232670069013, 0.0, 0.6135759095974554),
                          (-0.42460737145258975, 0.0, 0.5324412655171409),
                          (-0.5324412655171409, 0.0, 0.42460737145258975),
                          (-0.6135759095974554, 0.0, 0.29548232670069013),
                          (-0.6639434287466539, 0.0, 0.15154052914627025),
                          (-0.681018134582272, 0.0, -1.938318811239675e-08),
                          (-1.0158428554096877, 0.0, -5.120423080604854e-08),
                          (-0.7544008343563589, 0.0, 0.17218710311101057),
                          (-0.6971712427268622, 0.0, 0.3357401281057415),
                          (-0.6049820691637396, 0.0, 0.48245755195547374),
                          (-0.48245755195547374, 0.0, 0.6049820691637396),
                          (-0.3357401281057415, 0.0, 0.6971712427268622),
                          (-0.17218710311101057, 0.0, 0.7544008343563589),
                          (-7.35548706273645e-08, 0.0, 1.0158428554096877),
                          (0.17218710311101057, 0.0, 0.7544008343563589), (0.3357401281057415, 0.0, 0.6971712427268622),
                          (0.48245755195547374, 0.0, 0.6049820691637396),
                          (0.6049820691637396, 0.0, 0.48245755195547374), (0.6971712427268622, 0.0, 0.3357401281057415),
                          (0.7544008343563589, 0.0, 0.17218710311101057),
                          (1.0158428554096877, 0.0, 2.4481998914655333e-08),
                          (0.7544008343563589, 0.0, -0.17218710311101057),
                          (0.6971704689252743, 0.0, -0.3357401281057415),
                          (0.6049820691637396, 0.0, -0.48245755195547374),
                          (0.48245755195547374, 0.0, -0.6049820691637396),
                          (0.3357401281057415, 0.0, -0.6971704689252743),
                          (0.17218710311101057, 0.0, -0.754400060554771),
                          (2.1313436173076034e-09, 0.0, -1.0158428554096877),
                          (-0.17218710311101057, 0.0, -0.7544008343563589),
                          (-0.3357401281057415, 0.0, -0.6971704689252743),
                          (-0.48245755195547374, 0.0, -0.6049820691637396),
                          (-0.6049820691637396, 0.0, -0.48245755195547374),
                          (-0.6971704689252743, 0.0, -0.3357401281057415),
                          (-0.7544008343563589, 0.0, -0.17218710311101057),
                          (-1.0158428554096877, 0.0, -5.120423080604854e-08)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def circleX(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(4.47035e-08, 0.0, -1.0), (-0.222521, 0.0, -0.974928), (-0.433884, 0.0, -0.900968),
                          (-0.62349, 0.0, -0.781831), (-0.781831, 0.0, -0.62349), (-0.900968, 0.0, -0.433884),
                          (-0.974928, 0.0, -0.222521), (-1.0, 0.0, -4.47035e-08), (1.0, 0.0, 0.0),
                          (0.974928, 0.0, -0.222521), (0.900968, 0.0, -0.433884), (0.781831, 0.0, -0.62349),
                          (0.62349, 0.0, -0.781831), (0.433884, 0.0, -0.900968), (0.222521, 0.0, -0.974927),
                          (4.47035e-08, 0.0, -1.0), (-1.49012e-08, 0.0, 1.0), (0.0, 0.0, 0.0), (1.0, 0.0, 0.0),
                          (0.974928, 0.0, 0.222521), (0.900969, 0.0, 0.433884), (0.781831, 0.0, 0.62349),
                          (0.62349, 0.0, 0.781831), (0.433884, 0.0, 0.900969), (0.222521, 0.0, 0.974928),
                          (-1.49012e-08, 0.0, 1.0), (-0.222521, 0.0, 0.974928), (-0.433884, 0.0, 0.900969),
                          (-0.62349, 0.0, 0.781831), (-0.781831, 0.0, 0.62349), (-0.900969, 0.0, 0.433884),
                          (-0.974928, 0.0, 0.222521), (-1.0, 0.0, -4.47035e-08)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def circleXPins(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(0.0, 0.0, 0.0), (0.776071, 0.0, 4.47035e-08), (0.974928, 0.0, -0.222521), (1.0, 0.0, 0.0),
                          (0.974928, 0.0, 0.222521), (0.776071, 0.0, 4.47035e-08), (-0.776071, 0.0, -4.47035e-08),
                          (-0.974928, 0.0, 0.222521), (-1.0, 0.0, -4.47035e-08), (-0.974928, 0.0, -0.222521),
                          (-0.776071, 0.0, -4.47035e-08), (0.0, 0.0, 0.0), (-4.47035e-08, 0.0, 0.776071),
                          (0.222521, 0.0, 0.974928), (-1.49012e-08, 0.0, 1.0), (-0.222521, 0.0, 0.974928),
                          (-4.47035e-08, 0.0, 0.776071), (4.47035e-08, 0.0, -0.776071), (0.222521, 0.0, -0.974927),
                          (4.47035e-08, 0.0, -1.0), (-0.222521, 0.0, -0.974928), (4.47035e-08, 0.0, -0.776071),
                          (-0.222521, 0.0, -0.974928), (-0.433884, 0.0, -0.900968), (-0.62349, 0.0, -0.781831),
                          (-0.781831, 0.0, -0.62349), (-0.900968, 0.0, -0.433884), (-0.974928, 0.0, -0.222521),
                          (-1.0, 0.0, -4.47035e-08), (-0.974928, 0.0, 0.222521), (-0.900969, 0.0, 0.433884),
                          (-0.781831, 0.0, 0.62349), (-0.62349, 0.0, 0.781831), (-0.433884, 0.0, 0.900969),
                          (-0.222521, 0.0, 0.974928), (-1.49012e-08, 0.0, 1.0), (0.222521, 0.0, 0.974928),
                          (0.433884, 0.0, 0.900969), (0.62349, 0.0, 0.781831), (0.781831, 0.0, 0.62349),
                          (0.900969, 0.0, 0.433884), (0.974928, 0.0, 0.222521), (1.0, 0.0, 0.0),
                          (0.974928, 0.0, -0.222521), (0.900968, 0.0, -0.433884), (0.781831, 0.0, -0.62349),
                          (0.62349, 0.0, -0.781831), (0.433884, 0.0, -0.900968), (0.222521, 0.0, -0.974927),
                          (4.47035e-08, 0.0, -1.0)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def locator(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(0.0, 0.9919077075245271, -2.3754506894637157e-09),
                          (-0.026568956451549827, 0.8856318817183276, -0.046018761021906884),
                          (0.05313791290309965, 0.8856318817183276, 0.0),
                          (0.0, 0.9919077075245271, -2.3754506894637157e-09),
                          (-0.026568956451549827, 0.8856318817183276, 0.046018761021906884),
                          (-0.026568956451549827, 0.8856318817183276, -0.046018761021906884),
                          (0.0, 0.8856318817183276, 0.0),
                          (-0.026568956451549827, 0.8856318817183276, 0.046018761021906884),
                          (0.05313791290309965, 0.8856318817183276, 0.0), (0.0, 0.8856318817183276, 0.0),
                          (0.0, -0.8856318817183276, 0.0),
                          (-0.026568956451549827, -0.8856318817183276, -0.046018761021906884),
                          (0.0, -0.9919077075245271, 2.3754506894637157e-09),
                          (0.05313791290309965, -0.8856318817183276, 0.0),
                          (-0.026568956451549827, -0.8856318817183276, -0.046018761021906884),
                          (-0.026568956451549827, -0.8856318817183276, 0.046018761021906884),
                          (0.0, -0.9919077075245271, 2.3754506894637157e-09),
                          (0.05313791290309965, -0.8856318817183276, 0.0), (0.0, -0.8856318817183276, 0.0),
                          (-0.026568956451549827, -0.8856318817183276, 0.046018761021906884),
                          (0.05313791290309965, -0.8856318817183276, 0.0), (0.0, -0.8856318817183276, 0.0),
                          (0.0, 0.0, 0.0), (-0.8856318817183276, 0.0, 0.0),
                          (-0.8856318817183276, 0.046018761021906884, -0.026568956451549827),
                          (-0.9919077075245271, 2.3754506894637157e-09, 0.0),
                          (-0.8856318817183276, 0.0, 0.05313791290309965),
                          (-0.8856318817183276, -0.046018761021906884, -0.026568956451549827),
                          (-0.8856318817183276, 0.046018761021906884, -0.026568956451549827),
                          (-0.8856318817183276, 0.0, 0.05313791290309965),
                          (-0.9919077075245271, 2.3754506894637157e-09, 0.0),
                          (-0.8856318817183276, -0.046018761021906884, -0.026568956451549827),
                          (-0.8856318817183276, 0.0, 0.0), (-0.8856318817183276, 0.0, 0.05313791290309965),
                          (-0.8856318817183276, 0.0, 0.0), (0.8856318817183276, 0.0, 0.0),
                          (0.8856318817183276, 0.046018761021906884, 0.026568956451549827),
                          (0.9919077075245271, 2.3754506894637157e-09, 0.0),
                          (0.8856318817183276, 0.0, -0.05313791290309965),
                          (0.8856318817183276, -0.046018761021906884, 0.026568956451549827),
                          (0.9919077075245271, 2.3754506894637157e-09, 0.0),
                          (0.8856318817183276, -0.046018761021906884, 0.026568956451549827),
                          (0.8856318817183276, 0.046018761021906884, 0.026568956451549827),
                          (0.8856318817183276, 0.0, -0.05313791290309965), (0.8856318817183276, 0.0, 0.0),
                          (0.8856318817183276, -0.046018761021906884, 0.026568956451549827),
                          (0.8856318817183276, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, -0.8856318817183276),
                          (0.05313791290309965, 0.0, -0.8856318817183276),
                          (0.0, -2.3754506894637157e-09, -0.9919077075245271),
                          (-0.026568956451549827, 0.046018761021906884, -0.8856318817183276),
                          (0.05313791290309965, 0.0, -0.8856318817183276),
                          (-0.026568956451549827, -0.046018761021906884, -0.8856318817183276),
                          (0.0, -2.3754506894637157e-09, -0.9919077075245271),
                          (-0.026568956451549827, 0.046018761021906884, -0.8856318817183276),
                          (-0.026568956451549827, -0.046018761021906884, -0.8856318817183276),
                          (0.0, 0.0, -0.8856318817183276),
                          (-0.026568956451549827, 0.046018761021906884, -0.8856318817183276),
                          (0.0, 0.0, -0.8856318817183276), (0.0, 0.0, 0.8856318817183276),
                          (-0.026568956451549827, 0.046018761021906884, 0.8856318817183276),
                          (-0.026568956451549827, -0.046018761021906884, 0.8856318817183276),
                          (0.0, 2.3754506894637157e-09, 0.9919077075245271),
                          (-0.026568956451549827, 0.046018761021906884, 0.8856318817183276),
                          (0.05313791290309965, 0.0, 0.8856318817183276), (0.0, 0.0, 0.8856318817183276),
                          (-0.026568956451549827, -0.046018761021906884, 0.8856318817183276),
                          (0.05313791290309965, 0.0, 0.8856318817183276),
                          (0.0, 2.3754506894637157e-09, 0.9919077075245271)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def cross(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(-0.33039471500877204, 0.0, -0.33039471500877204),
                          (-0.33039471500877204, 0.0, -0.9911841450263161),
                          (0.33039471500877204, 0.0, -0.9911841450263161),
                          (0.33039471500877204, 0.0, -0.33039471500877204),
                          (0.9911841450263161, 0.0, -0.33039471500877204),
                          (0.9911841450263161, 0.0, 0.33039471500877204),
                          (0.33039471500877204, 0.0, 0.33039471500877204),
                          (0.33039471500877204, 0.0, 0.9911841450263161),
                          (-0.33039471500877204, 0.0, 0.9911841450263161),
                          (-0.33039471500877204, 0.0, 0.33039471500877204),
                          (-0.9911841450263161, 0.0, 0.33039471500877204),
                          (-0.9911841450263161, 0.0, -0.33039471500877204),
                          (-0.33039471500877204, 0.0, -0.33039471500877204)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def arrow180(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(-0.23396981200934322, 0.0, -1.0045712258579862),
                          (-0.7100167609883725, 0.0, -0.9688586934619196),
                          (-0.45345380359580917, 0.0, -0.9201752490447295),
                          (-0.531916567256725, 0.0, -0.8766421942132373),
                          (-0.678353551630666, 0.0, -0.7662628579578492),
                          (-0.847453580154585, 0.0, -0.5445637053211132),
                          (-0.9542570317933219, 0.0, -0.2826919094911723),
                          (-0.9907479159750975, 0.0, 9.699158682827935e-09),
                          (-0.9542570317933219, 0.0, 0.2826919094911723), (-0.847453580154585, 0.0, 0.5445637053211132),
                          (-0.678353551630666, 0.0, 0.7662628579578492), (-0.531916567256725, 0.0, 0.8766421942132373),
                          (-0.45345380359580917, 0.0, 0.9201752490447295),
                          (-0.7100167609883725, 0.0, 0.9688586934619196),
                          (-0.23396981200934322, 0.0, 1.0045712258579862),
                          (-0.4649805762259414, 0.0, 0.5614537790027819),
                          (-0.41026102565730005, 0.0, 0.832544455730932),
                          (-0.48123436945601156, 0.0, 0.7931619740736282),
                          (-0.6137838668505218, 0.0, 0.693259447970099),
                          (-0.7667205045493773, 0.0, 0.49272060369841164),
                          (-0.8633886350082397, 0.0, 0.2557581805421561),
                          (-0.8963789889507868, 0.0, 8.77530260620295e-09),
                          (-0.8633886350082397, 0.0, -0.2557581805421561),
                          (-0.7667205045493773, 0.0, -0.49272060369841164),
                          (-0.6137838668505218, 0.0, -0.693259447970099),
                          (-0.48123436945601156, 0.0, -0.7931619740736282),
                          (-0.41026102565730005, 0.0, -0.832544455730932),
                          (-0.4649805762259414, 0.0, -0.5614537790027819),
                          (-0.23396981200934322, 0.0, -1.0045712258579862)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def angle(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(0.008711764241016717, 0.0, -1.0022087884573279),
                          (1.0106852522470122, 0.0, -1.0022087884573279), (1.0106852522470122, 0.0, 1.001738187554663),
                          (-0.9932617237649788, 0.0, 1.001738187554663),
                          (-0.9932617237649788, 0.0, -0.00023530045133235422),
                          (0.008711764241016717, 0.0, -0.00023530045133235422),
                          (0.008711764241016717, 0.0, -1.0022087884573279)])

    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def crossArrow(scale=(1, 1, 1), **kwargs):
    node = pymel.core(d=1,
                      p=[(0.0, 0.0, -0.9957517155269755), (0.33191723850899185, 0.0, -0.8297930962724797),
                         (0.16595861925449593, 0.0, -0.8297930962724797),
                         (0.16595861925449593, 0.0, -0.16595861925449593),
                         (0.8297930962724797, 0.0, -0.16595861925449593),
                         (0.8297930962724797, 0.0, -0.33191723850899185), (0.9957517155269755, 0.0, 0.0),
                         (0.8297930962724797, 0.0, 0.33191723850899185), (0.8297930962724797, 0.0, 0.16595861925449593),
                         (0.16595861925449593, 0.0, 0.16595861925449593),
                         (0.16595861925449593, 0.0, 0.8297930962724797), (0.33191723850899185, 0.0, 0.8297930962724797),
                         (0.0, 0.0, 0.9957517155269755), (-0.33191723850899185, 0.0, 0.8297930962724797),
                         (-0.16595861925449593, 0.0, 0.8297930962724797),
                         (-0.16595861925449593, 0.0, 0.16595861925449593),
                         (-0.8297930962724797, 0.0, 0.16595861925449593),
                         (-0.8297930962724797, 0.0, 0.33191723850899185), (-0.9957517155269755, 0.0, 0.0),
                         (-0.8297930962724797, 0.0, -0.33191723850899185),
                         (-0.8297930962724797, 0.0, -0.16595861925449593),
                         (-0.16595861925449593, 0.0, -0.16595861925449593),
                         (-0.16595861925449593, 0.0, -0.8297930962724797),
                         (-0.33191723850899185, 0.0, -0.8297930962724797), (0.0, 0.0, -0.9957517155269755)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def dir1Arrow(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(0.0, 0.0, -1.0106488071645405), (-1.002558231449136, 0.0, 0.14061417856157238),
                          (-0.334186077149712, 0.0, 0.14061417856157238), (-0.334186077149712, 0.0, 1.004061417856157),
                          (0.334186077149712, 0.0, 1.004061417856157), (0.334186077149712, 0.0, 0.14061417856157238),
                          (1.002558231449136, 0.0, 0.14061417856157238), (0.0, 0.0, -1.0106488071645405)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def dir2Arrow(scale=(1, 1, 1), **kwargs):
    pymel.curve(d=1,
                p=[(0.0, 0.0, -1.0083199931523783), (-1.005919279470972, 0.0, -0.43213713992244784),
                   (-0.335306426490324, 0.0, -0.43213713992244784), (-0.335306426490324, 0.0, 0.43213713992244784),
                   (-1.005919279470972, 0.0, 0.43213713992244784), (0.0, 0.0, 1.0083199931523783),
                   (1.005919279470972, 0.0, 0.43213713992244784), (0.335306426490324, 0.0, 0.43213713992244784),
                   (0.335306426490324, 0.0, -0.43213713992244784), (1.005919279470972, 0.0, -0.43213713992244784),
                   (0.0, 0.0, -1.0083199931523783)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def trident(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(0.10758603459519833, 0.0, 8.2738118369164e-09),
                          (0.14059191859120068, 0.0, 0.24114211857060067),
                          (0.2373055551163532, 0.0, 0.4645626192184933), (0.39031418701578213, 0.0, 0.6536410747379391),
                          (0.5229260814607631, 0.0, 0.7478343738304346), (0.5939328356261839, 0.0, 0.784966226431508),
                          (0.5391875260873036, 0.0, 0.5293678327754782), (0.7703070375311449, 0.0, 0.9471620150915623),
                          (0.2940359916970857, 0.0, 0.9134903815850468), (0.5507197248912631, 0.0, 0.8675890974064151),
                          (0.4722200252545763, 0.0, 0.8265438684809385), (0.32571410636119624, 0.0, 0.7224724877156466),
                          (0.156534474796739, 0.0, 0.5134429925933289), (0.0496807459370896, 0.0, 0.26653663946531575),
                          (0.021741644630343004, 0.0, 0.0605167237478767),
                          (-0.7442292750390158, 0.0, 0.0605167237478767),
                          (-0.6384487642278265, 0.0, 0.2715129771930592), (-1.0004654455370499, 0.0, 0.0),
                          (-0.6384487642278265, 0.0, -0.2715129771930592),
                          (-0.7442292750390158, 0.0, -0.0605167237478767),
                          (0.021741644630343004, 0.0, -0.0605167237478767),
                          (0.0496807459370896, 0.0, -0.26653663946531575),
                          (0.156534474796739, 0.0, -0.5134429925933289),
                          (0.32571410636119624, 0.0, -0.7224724877156466),
                          (0.4722200252545763, 0.0, -0.8265438684809385),
                          (0.5507197248912631, 0.0, -0.8675890974064151),
                          (0.2940359916970857, 0.0, -0.9134903815850468),
                          (0.7703070375311449, 0.0, -0.9471620150915623),
                          (0.5391875260873036, 0.0, -0.5293678327754782), (0.5939328356261839, 0.0, -0.784966226431508),
                          (0.5229260814607631, 0.0, -0.7478343738304346),
                          (0.39031418701578213, 0.0, -0.6536410747379391),
                          (0.2373055551163532, 0.0, -0.4645626192184933),
                          (0.14059191859120068, 0.0, -0.24114211857060067),
                          (0.10758603459519833, 0.0, 8.2738118369164e-09)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def pyramid(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1, p=[(1.3674676855125205, -0.9669454363473031, 0.0),
                               (-0.6837338427562603, -0.9669454363473031, -1.1842623066705815),
                               (0.0, 0.9669454363473031, 0.0), (1.3674676855125205, -0.9669454363473031, 0.0),
                               (-0.6837338427562603, -0.9669454363473031, 1.1842623066705815),
                               (0.0, 0.9669454363473031, 0.0),
                               (-0.6837338427562603, -0.9669454363473031, -1.1842623066705815),
                               (-0.6837338427562603, -0.9669454363473031, 1.1842623066705815)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def prism(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(0.0, -0.8970344394661268, 0.0), (0.9909826622682584, 0.0, -0.9909826622682584),
                          (0.9909826622682584, 0.0, 0.9909826622682584), (-0.9909826622682584, 0.0, 0.9909826622682584),
                          (-0.9909826622682584, 0.0, -0.9909826622682584),
                          (0.9909826622682584, 0.0, -0.9909826622682584), (0.0, 0.8970344394661268, 0.0),
                          (-0.9909826622682584, 0.0, 0.9909826622682584), (0.0, -0.8970344394661268, 0.0),
                          (0.9909826622682584, 0.0, 0.9909826622682584), (0.0, 0.8970344394661268, 0.0),
                          (-0.9909826622682584, 0.0, -0.9909826622682584), (0.0, -0.8970344394661268, 0.0)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def openCube(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(0.0, -0.9078636604654428, 0.0), (1.0029460493847893, 0.0, -1.0029460493847893),
                          (1.0029460493847893, 0.0, 1.0029460493847893), (-1.0029460493847893, 0.0, 1.0029460493847893),
                          (-1.0029460493847893, 0.0, -1.0029460493847893),
                          (1.0029460493847893, 0.0, -1.0029460493847893), (0.0, 0.9078636604654428, 0.0),
                          (-1.0029460493847893, 0.0, 1.0029460493847893), (0.0, -0.9078636604654428, 0.0),
                          (1.0029460493847893, 0.0, 1.0029460493847893), (0.0, 0.9078636604654428, 0.0),
                          (-1.0029460493847893, 0.0, -1.0029460493847893), (0.0, -0.9078636604654428, 0.0)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def arrowSphere(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(0.0, 0.35, -1.001567), (-0.336638, 0.677886, -0.751175), (-0.0959835, 0.677886, -0.751175),
                          (-0.0959835, 0.850458, -0.500783), (-0.0959835, 0.954001, -0.0987656),
                          (-0.500783, 0.850458, -0.0987656), (-0.751175, 0.677886, -0.0987656),
                          (-0.751175, 0.677886, -0.336638), (-1.001567, 0.35, 0.0), (-0.751175, 0.677886, 0.336638),
                          (-0.751175, 0.677886, 0.0987656), (-0.500783, 0.850458, 0.0987656),
                          (-0.0959835, 0.954001, 0.0987656), (-0.0959835, 0.850458, 0.500783),
                          (-0.0959835, 0.677886, 0.751175), (-0.336638, 0.677886, 0.751175), (0.0, 0.35, 1.001567),
                          (0.336638, 0.677886, 0.751175), (0.0959835, 0.677886, 0.751175),
                          (0.0959835, 0.850458, 0.500783), (0.0959835, 0.954001, 0.0987656),
                          (0.500783, 0.850458, 0.0987656), (0.751175, 0.677886, 0.0987656),
                          (0.751175, 0.677886, 0.336638), (1.001567, 0.35, 0.0), (0.751175, 0.677886, -0.336638),
                          (0.751175, 0.677886, -0.0987656), (0.500783, 0.850458, -0.0987656),
                          (0.0959835, 0.954001, -0.0987656), (0.0959835, 0.850458, -0.500783),
                          (0.0959835, 0.677886, -0.751175), (0.336638, 0.677886, -0.751175), (0.0, 0.35, -1.001567)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def cubeBevel(scale=(1, 1, 1), **kwargs):
    node = pymel.curve(d=1,
                       p=[(-0.9046436824953905, -0.9046436824953905, -0.9046436824953905),
                          (-0.8605132209141688, -0.8605132209141688, -0.9929006340552978),
                          (0.8605132209141688, -0.8605132209141688, -0.9929006340552978),
                          (0.9046436824953905, -0.9046436824953905, -0.9046436824953905),
                          (0.8605132209141688, -0.9929006340552978, -0.8605132209141688),
                          (-0.8605132209141688, -0.9929006340552978, -0.8605132209141688),
                          (-0.8605132209141688, -0.9929006340552978, 0.8605132209141688),
                          (0.8605132209141688, -0.9929006340552978, 0.8605132209141688),
                          (0.8605132209141688, -0.9929006340552978, -0.8605132209141688),
                          (0.9046436824953905, -0.9046436824953905, -0.9046436824953905),
                          (0.9929006340552978, -0.8605132209141688, -0.8605132209141688),
                          (0.9929006340552978, 0.8605132209141688, -0.8605132209141688),
                          (0.9929006340552978, 0.8605132209141688, 0.8605132209141688),
                          (0.9929006340552978, -0.8605132209141688, 0.8605132209141688),
                          (0.9929006340552978, -0.8605132209141688, -0.8605132209141688),
                          (0.9046436824953905, -0.9046436824953905, -0.9046436824953905),
                          (0.8605132209141688, -0.8605132209141688, -0.9929006340552978),
                          (0.8605132209141688, 0.8605132209141688, -0.9929006340552978),
                          (-0.8605132209141688, 0.8605132209141688, -0.9929006340552978),
                          (-0.8605132209141688, -0.8605132209141688, -0.9929006340552978),
                          (-0.9046436824953905, -0.9046436824953905, -0.9046436824953905),
                          (-0.8605132209141688, -0.9929006340552978, -0.8605132209141688),
                          (-0.9046436824953905, -0.9046436824953905, -0.9046436824953905),
                          (-0.9929006340552978, -0.8605132209141688, -0.8605132209141688),
                          (-0.9929006340552978, -0.8605132209141688, 0.8605132209141688),
                          (-0.9929006340552978, 0.8605132209141688, 0.8605132209141688),
                          (-0.9929006340552978, 0.8605132209141688, -0.8605132209141688),
                          (-0.9929006340552978, -0.8605132209141688, -0.8605132209141688),
                          (-0.9929006340552978, 0.8605132209141688, -0.8605132209141688),
                          (-0.9046436824953905, 0.9046436824953905, -0.9046436824953905),
                          (-0.8605132209141688, 0.8605132209141688, -0.9929006340552978),
                          (-0.9046436824953905, 0.9046436824953905, -0.9046436824953905),
                          (-0.8605132209141688, 0.9929006340552978, -0.8605132209141688),
                          (0.8605132209141688, 0.9929006340552978, -0.8605132209141688),
                          (0.8605132209141688, 0.9929006340552978, 0.8605132209141688),
                          (-0.8605132209141688, 0.9929006340552978, 0.8605132209141688),
                          (-0.8605132209141688, 0.9929006340552978, -0.8605132209141688),
                          (0.8605132209141688, 0.9929006340552978, -0.8605132209141688),
                          (0.9046436824953905, 0.9046436824953905, -0.9046436824953905),
                          (0.8605132209141688, 0.8605132209141688, -0.9929006340552978),
                          (0.9046436824953905, 0.9046436824953905, -0.9046436824953905),
                          (0.9929006340552978, 0.8605132209141688, -0.8605132209141688),
                          (0.9046436824953905, 0.9046436824953905, -0.9046436824953905),
                          (0.8605132209141688, 0.9929006340552978, -0.8605132209141688),
                          (0.8605132209141688, 0.9929006340552978, 0.8605132209141688),
                          (0.9046436824953905, 0.9046436824953905, 0.9046436824953905),
                          (0.9929006340552978, 0.8605132209141688, 0.8605132209141688),
                          (0.9046436824953905, 0.9046436824953905, 0.9046436824953905),
                          (0.8605132209141688, 0.8605132209141688, 0.9929006340552978),
                          (0.8605132209141688, -0.8605132209141688, 0.9929006340552978),
                          (0.9046436824953905, -0.9046436824953905, 0.9046436824953905),
                          (0.9929006340552978, -0.8605132209141688, 0.8605132209141688),
                          (0.9046436824953905, -0.9046436824953905, 0.9046436824953905),
                          (0.8605132209141688, -0.9929006340552978, 0.8605132209141688),
                          (0.9046436824953905, -0.9046436824953905, 0.9046436824953905),
                          (0.8605132209141688, -0.8605132209141688, 0.9929006340552978),
                          (-0.8605132209141688, -0.8605132209141688, 0.9929006340552978),
                          (-0.9046436824953905, -0.9046436824953905, 0.9046436824953905),
                          (-0.8605132209141688, -0.9929006340552978, 0.8605132209141688),
                          (-0.9046436824953905, -0.9046436824953905, 0.9046436824953905),
                          (-0.9929006340552978, -0.8605132209141688, 0.8605132209141688),
                          (-0.9046436824953905, -0.9046436824953905, 0.9046436824953905),
                          (-0.8605132209141688, -0.8605132209141688, 0.9929006340552978),
                          (-0.8605132209141688, 0.8605132209141688, 0.9929006340552978),
                          (-0.9046436824953905, 0.9046436824953905, 0.9046436824953905),
                          (-0.9929006340552978, 0.8605132209141688, 0.8605132209141688),
                          (-0.9046436824953905, 0.9046436824953905, 0.9046436824953905),
                          (-0.8605132209141688, 0.9929006340552978, 0.8605132209141688),
                          (-0.9046436824953905, 0.9046436824953905, 0.9046436824953905),
                          (-0.8605132209141688, 0.8605132209141688, 0.9929006340552978),
                          (0.8605132209141688, 0.8605132209141688, 0.9929006340552978)])
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def square3D(scale=(1, 1, 1), **kwargs):
    points = [(-3.216419737012196e-14, -0.9264947566117914, -0.9264947566117914),
              (-2.118130070715349e-14, -0.895193770803716, -0.9890939112378139),
              (2.1685617390657142e-14, -0.895193770803716, -0.9890939112378139),
              (3.250040849245773e-14, -0.9264947566117914, -0.9264947566117914),
              (2.1685617390657142e-14, -0.9890939112378139, -0.895193770803716),
              (-2.118130070715349e-14, -0.9890939112378139, -0.895193770803716),
              (-2.118130070715349e-14, -0.9890939112378139, 0.895193770803716),
              (2.1685617390657142e-14, -0.9890939112378139, 0.895193770803716),
              (2.1685617390657142e-14, -0.9890939112378139, -0.895193770803716),
              (3.250040849245773e-14, -0.9264947566117914, -0.9264947566117914),
              (0.05494798926941951, -0.895193770803716, -0.895193770803716),
              (0.05494798926941951, 0.895193770803716, -0.895193770803716),
              (0.05494798926941951, 0.895193770803716, 0.895193770803716),
              (0.05494798926941951, -0.895193770803716, 0.895193770803716),
              (0.05494798926941951, -0.895193770803716, -0.895193770803716),
              (3.250040849245773e-14, -0.9264947566117914, -0.9264947566117914),
              (2.1685617390657142e-14, -0.895193770803716, -0.9890939112378139),
              (2.1685617390657142e-14, 0.895193770803716, -0.9890939112378139),
              (-2.118130070715349e-14, 0.895193770803716, -0.9890939112378139),
              (-2.118130070715349e-14, -0.895193770803716, -0.9890939112378139),
              (-3.216419737012196e-14, -0.9264947566117914, -0.9264947566117914),
              (-2.118130070715349e-14, -0.9890939112378139, -0.895193770803716),
              (-3.216419737012196e-14, -0.9264947566117914, -0.9264947566117914),
              (-0.05494798926941968, -0.895193770803716, -0.895193770803716),
              (-0.05494798926941968, -0.895193770803716, 0.895193770803716),
              (-0.05494798926941968, 0.895193770803716, 0.895193770803716),
              (-0.05494798926941968, 0.895193770803716, -0.895193770803716),
              (-0.05494798926941968, -0.895193770803716, -0.895193770803716),
              (-0.05494798926941968, 0.895193770803716, -0.895193770803716),
              (-3.216419737012196e-14, 0.9264947566117914, -0.9264947566117914),
              (-2.118130070715349e-14, 0.895193770803716, -0.9890939112378139),
              (-3.216419737012196e-14, 0.9264947566117914, -0.9264947566117914),
              (-2.118130070715349e-14, 0.9890939112378139, -0.895193770803716),
              (2.1685617390657142e-14, 0.9890939112378139, -0.895193770803716),
              (2.1685617390657142e-14, 0.9890939112378139, 0.895193770803716),
              (-2.118130070715349e-14, 0.9890939112378139, 0.895193770803716),
              (-2.118130070715349e-14, 0.9890939112378139, -0.895193770803716),
              (2.1685617390657142e-14, 0.9890939112378139, -0.895193770803716),
              (3.250040849245773e-14, 0.9264947566117914, -0.9264947566117914),
              (2.1685617390657142e-14, 0.895193770803716, -0.9890939112378139),
              (3.250040849245773e-14, 0.9264947566117914, -0.9264947566117914),
              (0.05494798926941951, 0.895193770803716, -0.895193770803716),
              (3.250040849245773e-14, 0.9264947566117914, -0.9264947566117914),
              (2.1685617390657142e-14, 0.9890939112378139, -0.895193770803716),
              (2.1685617390657142e-14, 0.9890939112378139, 0.895193770803716),
              (3.250040849245773e-14, 0.9264947566117914, 0.9264947566117914),
              (0.05494798926941951, 0.895193770803716, 0.895193770803716),
              (3.250040849245773e-14, 0.9264947566117914, 0.9264947566117914),
              (2.1685617390657142e-14, 0.895193770803716, 0.9890939112378139),
              (2.1685617390657142e-14, -0.895193770803716, 0.9890939112378139),
              (3.250040849245773e-14, -0.9264947566117914, 0.9264947566117914),
              (0.05494798926941951, -0.895193770803716, 0.895193770803716),
              (3.250040849245773e-14, -0.9264947566117914, 0.9264947566117914),
              (2.1685617390657142e-14, -0.9890939112378139, 0.895193770803716),
              (3.250040849245773e-14, -0.9264947566117914, 0.9264947566117914),
              (2.1685617390657142e-14, -0.895193770803716, 0.9890939112378139),
              (-2.118130070715349e-14, -0.895193770803716, 0.9890939112378139),
              (-3.216419737012196e-14, -0.9264947566117914, 0.9264947566117914),
              (-2.118130070715349e-14, -0.9890939112378139, 0.895193770803716),
              (-3.216419737012196e-14, -0.9264947566117914, 0.9264947566117914),
              (-0.05494798926941968, -0.895193770803716, 0.895193770803716),
              (-3.216419737012196e-14, -0.9264947566117914, 0.9264947566117914),
              (-2.118130070715349e-14, -0.895193770803716, 0.9890939112378139),
              (-2.118130070715349e-14, 0.895193770803716, 0.9890939112378139),
              (-3.216419737012196e-14, 0.9264947566117914, 0.9264947566117914),
              (-0.05494798926941968, 0.895193770803716, 0.895193770803716),
              (-3.216419737012196e-14, 0.9264947566117914, 0.9264947566117914),
              (-2.118130070715349e-14, 0.9890939112378139, 0.895193770803716),
              (-3.216419737012196e-14, 0.9264947566117914, 0.9264947566117914),
              (-2.118130070715349e-14, 0.895193770803716, 0.9890939112378139),
              (2.1685617390657142e-14, 0.895193770803716, 0.9890939112378139)]

    node = pymel.curve(p=points, d=1)
    node.rotateOrder.setKeyable(True)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node


def locatorCross(scale=(1, 1, 1), **kwargs):
    points = [(1.3691100802194696e-09, 1.0088945440442032, -0.0024406720551346287),
              (0.017489007842741898, 0.9685053927462611, -0.012537959879620066),
              (4.663418676956993e-10, 0.9685053927462611, 0.017753903593836266),
              (1.3691100802194696e-09, 1.0088945440442032, -0.0024406720551346287),
              (-0.017489006910058138, 0.9685053927462611, -0.012537959879620066),
              (0.017489007842741898, 0.9685053927462611, -0.012537959879620066),
              (4.663418676956993e-10, 0.9685053927462611, -0.0024406720551346226),
              (-0.017489006910058138, 0.9685053927462611, -0.012537959879620066),
              (4.663418676956993e-10, 0.9685053927462611, 0.017753903593836266),
              (4.663418676956993e-10, 0.9685053927462611, -0.0024406720551346226),
              (4.663418796568728e-10, 0.016689417101063305, 2.7067783779580325e-16),
              (0.009034275776548983, 0.016689417101063305, -0.00521594371421531),
              (1.1669914191963584e-25, -2.1928331163204315e-16, 2.731251961845537e-16),
              (4.663418796568728e-10, 0.016689417101063305, 0.010431887428431435),
              (0.009034275776548983, 0.016689417101063305, -0.00521594371421531),
              (-0.009034274843865223, 0.016689417101063305, -0.00521594371421531),
              (1.1669914191963584e-25, -2.1928331163204315e-16, 2.731251961845537e-16),
              (4.663418796568728e-10, 0.016689417101063305, 0.010431887428431435),
              (4.663418796568728e-10, 0.016689417101063305, 2.7067783779580325e-16),
              (-0.009034274843865223, 0.016689417101063305, -0.00521594371421531),
              (4.663418796568728e-10, 0.016689417101063305, 0.010431887428431435),
              (4.663418796568728e-10, 0.016689417101063305, 2.7067783779580325e-16),
              (2.9667138764489707e-10, 0.8044032904929627, -1.4977833339152946e-15),
              (0.0024406725214767984, 0.804403290492948, -0.16410210225331265),
              (0.01253796034596226, 0.8218922978693483, -0.16410210225331265),
              (0.0024406725214767984, 0.8044032913957164, -0.2044912535512545),
              (-0.017753903127494083, 0.804403290492948, -0.16410210225331265),
              (0.01253796034596226, 0.7869142831165481, -0.16410210225331265),
              (0.01253796034596226, 0.8218922978693483, -0.16410210225331265),
              (-0.017753903127494083, 0.804403290492948, -0.16410210225331265),
              (0.0024406725214767984, 0.8044032913957164, -0.2044912535512545),
              (0.01253796034596226, 0.7869142831165481, -0.16410210225331265),
              (0.0024406725214767984, 0.804403290492948, -0.16410210225331265),
              (-0.017753903127494083, 0.804403290492948, -0.16410210225331265),
              (0.0024406725214767984, 0.804403290492948, -0.16410210225331265),
              (-0.0024406715887930644, 0.804403290492948, 0.16410210225331334),
              (-0.012537959413278498, 0.8218922978693483, 0.16410210225331334),
              (-0.0024406715887930644, 0.8044032913957164, 0.2044912535512551),
              (0.017753904060177843, 0.804403290492948, 0.16410210225331334),
              (-0.012537959413278498, 0.7869142831165481, 0.16410210225331334),
              (-0.0024406715887930644, 0.8044032913957164, 0.2044912535512551),
              (-0.012537959413278498, 0.7869142831165481, 0.16410210225331334),
              (-0.012537959413278498, 0.8218922978693483, 0.16410210225331334),
              (0.017753904060177843, 0.804403290492948, 0.16410210225331334),
              (-0.0024406715887930644, 0.804403290492948, 0.16410210225331334),
              (-0.012537959413278498, 0.7869142831165481, 0.16410210225331334),
              (-0.0024406715887930644, 0.804403290492948, 0.16410210225331334),
              (2.9667138764489707e-10, 0.8044032904929627, -1.4977833339152946e-15),
              (0.4986534124025141, 0.804403290492963, -0.002440672055151107),
              (0.4986534124025141, 0.804403290492963, 0.01775390359381978),
              (0.5316398312779885, 0.8044032895901946, -0.002440672055151107),
              (0.4986534124025141, 0.8218922978693627, -0.012537959879636662),
              (0.4986534124025141, 0.804403290492963, 0.01775390359381978),
              (0.4986534124025141, 0.7869142831165632, -0.012537959879636434),
              (0.5316398312779885, 0.8044032895901946, -0.002440672055151107),
              (0.4986534124025141, 0.8218922978693627, -0.012537959879636662),
              (0.4986534124025141, 0.7869142831165632, -0.012537959879636434),
              (0.4986534124025141, 0.804403290492963, -0.002440672055151107),
              (0.4986534124025141, 0.8218922978693627, -0.012537959879636662),
              (0.4986534124025141, 0.804403290492963, -0.002440672055151107),
              (-0.4986534118091724, 0.804403290492963, -0.002440672055151107),
              (-0.4986534118091724, 0.8218922978693627, -0.012537959879636662),
              (-0.4986534118091724, 0.7869142831165632, -0.012537959879636434),
              (-0.5316398306846459, 0.8044032913957313, -0.002440672055151107),
              (-0.4986534118091724, 0.8218922978693627, -0.012537959879636662),
              (-0.4986534118091724, 0.804403290492963, 0.01775390359381978),
              (-0.4986534118091724, 0.804403290492963, -0.002440672055151107),
              (-0.4986534118091724, 0.7869142831165632, -0.012537959879636434),
              (-0.4986534118091724, 0.804403290492963, 0.01775390359381978),
              (-0.5316398306846459, 0.8044032913957313, -0.002440672055151107)]
    node = pymel.curve(d=1, p=points)
    node.rotateOrder.setKeyable(True)
    node = pymel.curve(p=points, d=1)
    node.scale.set(scale)
    pymel.makeIdentity(a=True, s=True)
    return node
