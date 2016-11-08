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

def pin(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='pin'):
    points = [[0.0, 0.0, 0.0], [0.0, 3.0, 0.0], [-0.5, 4.0, -0.5], [-0.5, 4.0, 0.0], [-0.5, 4.0, 0.5], [0.0, 3.0, 0.0],
              [0.5, 4.0, 0.5], [0.5, 4.0, -0.5], [0.0, 3.0, 0.0], [0.5, 4.0, -0.5], [0.0, 4.0, -0.5], [0.0, 4.0, 0.5],
              [-0.5, 4.0, 0.5], [0.5, 4.0, 0.5], [0.5, 4.0, 0.0], [-0.5, 4.0, 0.0], [-0.5, 4.0, -0.5], [0.0, 4.0, -0.5]]
    node = pymel.curve(p=points, d=1, name=name)
    node.rotateOrder.setKeyable(True)
    return node


def sphere(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='sphere'):
    node = pymel.curve(d=1,
        p=[(0.0, 0.0, 1.0), (0.0, 0.5, 0.866025), (0.0, 0.866025, 0.5), (0.0, 1.0, 0.0), (0.0, 0.866025, -0.5),
           (0.0, 0.5, -0.866025), (0.0, 0.0, -1.0), (0.0, -0.5, -0.866025), (0.0, -0.866025, -0.5),
           (0.0, -1.0, 0.0), (0.0, -0.866025, 0.5), (0.0, -0.5, 0.866025), (0.0, 0.0, 1.0),
           (0.707107, 0.0, 0.707107), (1.0, 0.0, 0.0), (0.707107, 0.0, -0.707107), (0.0, 0.0, -1.0),
           (-0.707107, 0.0, -0.707107), (-1.0, 0.0, 0.0), (-0.866025, 0.5, 0.0), (-0.5, 0.866025, 0.0),
           (0.0, 1.0, 0.0), (0.5, 0.866025, 0.0), (0.866025, 0.5, 0.0), (1.0, 0.0, 0.0), (0.866025, -0.5, 0.0),
           (0.5, -0.866025, 0.0), (0.0, -1.0, 0.0), (-0.5, -0.866025, 0.0), (-0.866025, -0.5, 0.0),
           (-1.0, 0.0, 0.0), (-0.707107, 0.0, 0.707107), (0.0, 0.0, 1.0)])
    node.rotateOrder.setKeyable(True)
    return node


def squareCrossDouble(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None,
                      name='squareCrossDouble'):
    node = mel.eval(
        'curve -d 1 -p 0.02 0.5 0.5 -p 0.02 0.5 -0.5 -p 0.02 -0.5 -0.5 -p 0.02 -0.5 0.5 -p 0.02 0.5 0.5 -p -0.02 0.5 0.5 -p -0.02 0.5 0 -p 0.02 0.5 0 -p -0.02 0.5 0 -p -0.02 0.5 -0.5 -p 0.02 0.5 -0.5 -p -0.02 0.5 -0.5 -p -0.02 0 -0.5 -p 0.02 0 -0.5 -p -0.02 0 -0.5 -p -0.02 -0.5 -0.5 -p 0.02 -0.5 -0.5 -p -0.02 -0.5 -0.5 -p -0.02 -0.5 0 -p 0.02 -0.5 0 -p -0.02 -0.5 0 -p -0.02 -0.5 0.5 -p 0.02 -0.5 0.5 -p -0.02 -0.5 0.5 -p -0.02 0 0.5 -p 0.02 0 0.5 -p -0.02 0 0.5 -p -0.02 0.5 0.5 -p 0.02 0.5 0.5 -p -0.02 0.5 0.5 -p -0.02 0.5 0 -p 0 0.5 0 -p 0 0 0 -p 0 -0.5 0 -p 0 0 0 -p 0 0 0.5 -p 0 0 0 -p 0 0 -0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def squareCross(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='squareCross'):
    node = mel.eval(
        'curve -d 1 -p 0 -0.5 0 -p 0 -0.5 0.5 -p 0 0 0.5 -p 0 0 0 -p 0 -0.5 0 -p 0 -0.5 -0.5 -p 0 0 -0.5 -p 0 0 0 -p 0 0.5 0 -p 0 0.5 -0.5 -p 0 0 -0.5 -p 0 0 0.5 -p 0 0.5 0.5 -p 0 0.5 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def doubleNail(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='doubleNail'):
    node = mel.eval(
        'curve -d 1 -p 1 0.0533082 0 -p 1 0.0506991 -0.0164731 -p 1 0.0431272 -0.0313338 -p 1 0.0313338 -0.0431272 -p 1 0.0164731 -0.0506991 -p 1 0 -0.0533082 -p 1 0 0 -p 1 0 -0.0533082 -p 1 -0.0164731 -0.0506991 -p 1 -0.0313338 -0.0431272 -p 1 -0.0431272 -0.0313338 -p 1 -0.0506991 -0.0164731 -p 1 -0.0533082 0 -p 1 -0.0506991 0.0164731 -p 1 -0.0431272 0.0313338 -p 1 -0.0313338 0.0431272 -p 1 -0.0164731 0.0506991 -p 1 -1.58871e-09 0.0533082 -p 1 0 0 -p 1 -1.58871e-09 0.0533082 -p 1 0.0164731 0.0506991 -p 1 0.0313338 0.0431272 -p 1 0.0431272 0.0313338 -p 1 0.0506991 0.0164731 -p 1 0.0533082 0 -p 1 -0.0533082 0 -p 1 0 0 -p -1 0 0 -p -1 0.0533082 0 -p -1 0.0506991 -0.0164731 -p -1 0.0431272 -0.0313338 -p -1 0.0313338 -0.0431272 -p -1 0.0164731 -0.0506991 -p -1 0 -0.0533082 -p -1 0 0 -p -1 0 -0.0533082 -p -1 -0.0164731 -0.0506991 -p -1 -0.0313338 -0.0431272 -p -1 -0.0431272 -0.0313338 -p -1 -0.0506991 -0.0164731 -p -1 -0.0533082 0 -p -1 0 0 -p -1 -0.0533082 0 -p -1 -0.0506991 0.0164731 -p -1 -0.0431272 0.0313338 -p -1 -0.0313338 0.0431272 -p -1 -0.0164731 0.0506991 -p -1 -1.58871e-09 0.0533082 -p -1 0 0 -p -1 -1.58871e-09 0.0533082 -p -1 0.0164731 0.0506991 -p -1 0.0313338 0.0431272 -p -1 0.0431272 0.0313338 -p -1 0.0506991 0.0164731 -p -1 0.0533082 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -k 53 -k 54 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def belt(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 3 -p 1 -0.0270125 0.7262 -p 1 -0.0218525 0.74208 -p 1 -0.0083475 0.75189 -p 1 0.0083475 0.75189 -p 1 0.0218525 0.74208 -p 1 0.0270125 0.7262 -p 1 0.0270125 0.030885 -p 1 0.0270125 -0.75189 -p 0 0.0270125 -0.75189 -p -1 0.0270125 -0.75189 -p -1 0.0270125 0.030885 -p -1 0.0270125 0.7262 -p -1 0.0270125 0.7262 -p -1 0.0270125 0.7262 -p -1 0.0270125 0.7262 -p -1 0.0218525 0.74208 -p -1 0.0083475 0.75189 -p -1 -0.0083475 0.75189 -p -1 -0.0218525 0.74208 -p -1 -0.0270125 0.7262 -p -1 -0.0270125 0.7262 -p -1 -0.0270125 0.7262 -p -1 -0.0270125 0.030885 -p -1 -0.0270125 -0.75189 -p 0 -0.0270125 -0.75189 -p 1 -0.0270125 -0.75189 -p 1 -0.0270125 0.030885 -p 1 -0.0270125 0.7262 -p 1 -0.0270125 0.7262 -p 1 -0.0270125 0.7262 -p 1 -0.0270125 0.7262 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 28 -k 28 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def circle3D(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p 8.32645e-09 0.05 0.880094 -p 0.195839 0.05 0.858028 -p 0.381858 0.05 0.792937 -p 0.54873 0.05 0.688085 -p 0.688085 0.05 0.54873 -p 0.792937 0.05 0.381858 -p 0.858028 0.05 0.195839 -p 0.880094 0.05 1.42939e-08 -p 0.880094 -0.05 1.42939e-08 -p 0.880094 0.05 1.42939e-08 -p 0.858028 0.05 -0.195839 -p 0.792937 0.05 -0.381858 -p 0.688085 0.05 -0.548729 -p 0.548729 0.05 -0.688085 -p 0.381858 0.05 -0.792937 -p 0.195839 0.05 -0.858028 -p 6.07841e-08 0.05 -0.880094 -p 6.07841e-08 -0.05 -0.880094 -p 6.07841e-08 0.05 -0.880094 -p -0.195839 0.05 -0.858028 -p -0.381858 0.05 -0.792937 -p -0.548729 0.05 -0.688085 -p -0.688085 0.05 -0.548729 -p -0.792937 0.05 -0.381858 -p -0.858028 0.05 -0.195839 -p -0.880094 0.05 -2.50493e-08 -p -0.880094 -0.05 -1.84921e-08 -p -0.880094 0.05 -2.50493e-08 -p -0.858028 0.05 0.195839 -p -0.792937 0.05 0.381858 -p -0.688085 0.05 0.548729 -p -0.548729 0.05 0.688085 -p -0.381858 0.05 0.792937 -p -0.195839 0.05 0.858028 -p 8.32645e-09 0.05 0.880094 -p 8.32645e-09 -0.05 0.880094 -p -1.49012e-08 -0.05 1 -p 8.32645e-09 -0.05 0.880094 -p -0.195839 -0.05 0.858028 -p -0.381858 -0.05 0.792937 -p -0.548729 -0.05 0.688085 -p -0.688085 -0.05 0.548729 -p -0.792937 -0.05 0.381858 -p -0.858028 -0.05 0.195839 -p -0.880094 -0.05 -1.84921e-08 -p -0.858028 -0.05 -0.195839 -p -0.792937 -0.05 -0.381858 -p -0.688085 -0.05 -0.548729 -p -0.548729 -0.05 -0.688085 -p -0.381858 -0.05 -0.792937 -p -0.195839 -0.05 -0.858028 -p 6.07841e-08 -0.05 -0.880094 -p 0.195839 -0.05 -0.858028 -p 0.381858 -0.05 -0.792937 -p 0.548729 -0.05 -0.688085 -p 0.688085 -0.05 -0.548729 -p 0.792937 -0.05 -0.381858 -p 0.858028 -0.05 -0.195839 -p 0.880094 -0.05 1.42939e-08 -p 0.858028 -0.05 0.195839 -p 0.792937 -0.05 0.381858 -p 0.688085 -0.05 0.54873 -p 0.54873 -0.05 0.688085 -p 0.381858 -0.05 0.792937 -p 0.195839 -0.05 0.858028 -p 8.32645e-09 -0.05 0.880094 -p -1.49012e-08 -0.05 1 -p -2.98023e-08 0.05 1 -p 8.32645e-09 0.05 0.880094 -p -2.98023e-08 0.05 1 -p 0.222521 0.05 0.974928 -p 0.433884 0.05 0.900969 -p 0.62349 0.05 0.781831 -p 0.781831 0.05 0.62349 -p 0.900969 0.05 0.433884 -p 0.974928 0.05 0.222521 -p 1 0.05 5.96046e-08 -p 0.974928 0.05 -0.222521 -p 0.900968 0.05 -0.433884 -p 0.781831 0.05 -0.62349 -p 0.62349 0.05 -0.781831 -p 0.433884 0.05 -0.900968 -p 0.222521 0.05 -0.974927 -p 4.47035e-08 0.05 -1 -p 6.07841e-08 0.05 -0.880094 -p 6.07841e-08 -0.05 -0.880094 -p 4.47035e-08 -0.05 -1 -p 4.47035e-08 0.05 -1 -p -0.222521 0.05 -0.974928 -p -0.433884 0.05 -0.900968 -p -0.62349 0.05 -0.781831 -p -0.781831 0.05 -0.62349 -p -0.900968 0.05 -0.433884 -p -0.974928 0.05 -0.222521 -p -1 0.05 -1.49012e-08 -p -0.880094 0.05 -2.50493e-08 -p -0.880094 -0.05 -1.84921e-08 -p -1 -0.05 -4.47035e-08 -p -1 0.05 -1.49012e-08 -p -0.974928 0.05 0.222521 -p -0.900969 0.05 0.433884 -p -0.781831 0.05 0.62349 -p -0.62349 0.05 0.781831 -p -0.433884 0.05 0.900969 -p -0.222521 0.05 0.974928 -p -2.98023e-08 0.05 1 -p -1.49012e-08 -0.05 1 -p 0.222521 -0.05 0.974928 -p 0.433884 -0.05 0.900969 -p 0.62349 -0.05 0.781831 -p 0.781831 -0.05 0.62349 -p 0.900969 -0.05 0.433884 -p 0.974928 -0.05 0.222521 -p 1 -0.05 0 -p 1 0.05 5.96046e-08 -p 0.880094 0.05 1.42939e-08 -p 0.880094 -0.05 1.42939e-08 -p 1 -0.05 0 -p 0.974928 -0.05 -0.222521 -p 0.900968 -0.05 -0.433884 -p 0.781831 -0.05 -0.62349 -p 0.62349 -0.05 -0.781831 -p 0.433884 -0.05 -0.900968 -p 0.222521 -0.05 -0.974927 -p 4.47035e-08 -0.05 -1 -p -0.222521 -0.05 -0.974928 -p -0.433884 -0.05 -0.900968 -p -0.62349 -0.05 -0.781831 -p -0.781831 -0.05 -0.62349 -p -0.900968 -0.05 -0.433884 -p -0.974928 -0.05 -0.222521 -p -1 -0.05 -4.47035e-08 -p -0.974928 -0.05 0.222521 -p -0.900969 -0.05 0.433884 -p -0.781831 -0.05 0.62349 -p -0.62349 -0.05 0.781831 -p -0.433884 -0.05 0.900969 -p -0.222521 -0.05 0.974928 -p -1.49012e-08 -0.05 1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -k 53 -k 54 -k 55 -k 56 -k 57 -k 58 -k 59 -k 60 -k 61 -k 62 -k 63 -k 64 -k 65 -k 66 -k 67 -k 68 -k 69 -k 70 -k 71 -k 72 -k 73 -k 74 -k 75 -k 76 -k 77 -k 78 -k 79 -k 80 -k 81 -k 82 -k 83 -k 84 -k 85 -k 86 -k 87 -k 88 -k 89 -k 90 -k 91 -k 92 -k 93 -k 94 -k 95 -k 96 -k 97 -k 98 -k 99 -k 100 -k 101 -k 102 -k 103 -k 104 -k 105 -k 106 -k 107 -k 108 -k 109 -k 110 -k 111 -k 112 -k 113 -k 114 -k 115 -k 116 -k 117 -k 118 -k 119 -k 120 -k 121 -k 122 -k 123 -k 124 -k 125 -k 126 -k 127 -k 128 -k 129 -k 130 -k 131 -k 132 -k 133 -k 134 -k 135 -k 136 -k 137 -k 138 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def circleCompass(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p -1.312795 0.00 -6.61723e-08 -p -0.880094 0.00 -2.50493e-08 -p -0.858028 0.00 -0.195839 -p -0.792937 0.00 -0.381858 -p -0.688085 0.00 -0.548729 -p -0.548729 0.00 -0.688085 -p -0.381858 0.00 -0.792937 -p -0.195839 0.00 -0.858028 -p 6.07841e-08 0.00 -0.880094 -p 2.75438e-09 0.00 -1.312795 -p 6.07841e-08 0.00 -0.880094 -p 0.195839 0.00 -0.858028 -p 0.381858 0.00 -0.792937 -p 0.548729 0.00 -0.688085 -p 0.688085 0.00 -0.548729 -p 0.792937 0.00 -0.381858 -p 0.858028 0.00 -0.195839 -p 0.880094 0.00 1.42939e-08 -p 1.312795 0.00 3.16386e-08 -p 0.880094 0.00 1.42939e-08 -p 0.858028 0.00 0.195839 -p 0.792937 0.00 0.381858 -p 0.688085 0.00 0.54873 -p 0.54873 0.00 0.688085 -p 0.381858 0.00 0.792937 -p 0.195839 0.00 0.858028 -p 8.32645e-09 0.00 0.880094 -p -9.50565e-08 0.00 1.312795 -p 8.32645e-09 0.00 0.880094 -p -0.195839 0.00 0.858028 -p -0.381858 0.00 0.792937 -p -0.548729 0.00 0.688085 -p -0.688085 0.00 0.548729 -p -0.792937 0.00 0.381858 -p -0.858028 0.00 0.195839 -p -0.880094 0.00 -2.50493e-08 -p -1.312795 0.00 -6.61723e-08 -p -0.974928 0.00 0.222521 -p -0.900969 0.00 0.433884 -p -0.781831 0.00 0.62349 -p -0.62349 0.00 0.781831 -p -0.433884 0.00 0.900969 -p -0.222521 0.00 0.974928 -p -9.50565e-08 0.00 1.312795 -p 0.222521 0.00 0.974928 -p 0.433884 0.00 0.900969 -p 0.62349 0.00 0.781831 -p 0.781831 0.00 0.62349 -p 0.900969 0.00 0.433884 -p 0.974928 0.00 0.222521 -p 1.312795 0.00 3.16386e-08 -p 0.974928 0.00 -0.222521 -p 0.900968 0.00 -0.433884 -p 0.781831 0.00 -0.62349 -p 0.62349 0.00 -0.781831 -p 0.433884 0.00 -0.900968 -p 0.222521 0.00 -0.974927 -p 2.75438e-09 0.00 -1.312795 -p -0.222521 0.00 -0.974928 -p -0.433884 0.00 -0.900968 -p -0.62349 0.00 -0.781831 -p -0.781831 0.00 -0.62349 -p -0.900968 0.00 -0.433884 -p -0.974928 0.00 -0.222521 -p -1.312795 0.00 -6.61723e-08 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -k 53 -k 54 -k 55 -k 56 -k 57 -k 58 -k 59 -k 60 -k 61 -k 62 -k 63 -k 64 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def circleX(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p 4.47035e-08 0 -1 -p -0.222521 0 -0.974928 -p -0.433884 0 -0.900968 -p -0.62349 0 -0.781831 -p -0.781831 0 -0.62349 -p -0.900968 0 -0.433884 -p -0.974928 0 -0.222521 -p -1 0 -4.47035e-08 -p 1 0 0 -p 0.974928 0 -0.222521 -p 0.900968 0 -0.433884 -p 0.781831 0 -0.62349 -p 0.62349 0 -0.781831 -p 0.433884 0 -0.900968 -p 0.222521 0 -0.974927 -p 4.47035e-08 0 -1 -p -1.49012e-08 0 1 -p 0 0 0 -p 1 0 0 -p 0.974928 0 0.222521 -p 0.900969 0 0.433884 -p 0.781831 0 0.62349 -p 0.62349 0 0.781831 -p 0.433884 0 0.900969 -p 0.222521 0 0.974928 -p -1.49012e-08 0 1 -p -0.222521 0 0.974928 -p -0.433884 0 0.900969 -p -0.62349 0 0.781831 -p -0.781831 0 0.62349 -p -0.900969 0 0.433884 -p -0.974928 0 0.222521 -p -1 0 -4.47035e-08 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def circleXPins(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p 0 0 0 -p 0.776071 0 4.47035e-08 -p 0.974928 0 -0.222521 -p 1 0 0 -p 0.974928 0 0.222521 -p 0.776071 0 4.47035e-08 -p -0.776071 0 -4.47035e-08 -p -0.974928 0 0.222521 -p -1 0 -4.47035e-08 -p -0.974928 0 -0.222521 -p -0.776071 0 -4.47035e-08 -p 0 0 0 -p -4.47035e-08 0 0.776071 -p 0.222521 0 0.974928 -p -1.49012e-08 0 1 -p -0.222521 0 0.974928 -p -4.47035e-08 0 0.776071 -p 4.47035e-08 0 -0.776071 -p 0.222521 0 -0.974927 -p 4.47035e-08 0 -1 -p -0.222521 0 -0.974928 -p 4.47035e-08 0 -0.776071 -p -0.222521 0 -0.974928 -p -0.433884 0 -0.900968 -p -0.62349 0 -0.781831 -p -0.781831 0 -0.62349 -p -0.900968 0 -0.433884 -p -0.974928 0 -0.222521 -p -1 0 -4.47035e-08 -p -0.974928 0 0.222521 -p -0.900969 0 0.433884 -p -0.781831 0 0.62349 -p -0.62349 0 0.781831 -p -0.433884 0 0.900969 -p -0.222521 0 0.974928 -p -1.49012e-08 0 1 -p 0.222521 0 0.974928 -p 0.433884 0 0.900969 -p 0.62349 0 0.781831 -p 0.781831 0 0.62349 -p 0.900969 0 0.433884 -p 0.974928 0 0.222521 -p 1 0 0 -p 0.974928 0 -0.222521 -p 0.900968 0 -0.433884 -p 0.781831 0 -0.62349 -p 0.62349 0 -0.781831 -p 0.433884 0 -0.900968 -p 0.222521 0 -0.974927 -p 4.47035e-08 0 -1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def arrowCircle(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p -0.251045 0 -1.015808 -p -0.761834 0 -0.979696 -p -0.486547 0 -0.930468 -p -0.570736 0 -0.886448 -p -0.72786 0 -0.774834 -p -0.909301 0 -0.550655 -p -1.023899 0 -0.285854 -p -1.063053 0 9.80765e-009 -p -1.023899 0 0.285854 -p -0.909301 0 0.550655 -p -0.72786 0 0.774834 -p -0.570736 0 0.886448 -p -0.486547 0 0.930468 -p -0.761834 0 0.979696 -p -0.251045 0 1.015808 -p -0.498915 0 0.567734 -p -0.440202 0 0.841857 -p -0.516355 0 0.802034 -p -0.658578 0 0.701014 -p -0.822676 0 0.498232 -p -0.926399 0 0.258619 -p -0.961797 0 8.87346e-009 -p -0.926399 0 -0.258619 -p -0.822676 0 -0.498232 -p -0.658578 0 -0.701014 -p -0.516355 0 -0.802034 -p -0.440202 0 -0.841857 -p -0.498915 0 -0.567734 -p -0.251045 0 -1.015808 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def circle(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval('circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 0 -n "' + name + '";')[0]
    return node


# node.rotateOrder.setKeyable(True)


def square(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p 1 0 -1 -p -1 0 -1 -p -1 0 1 -p 1 0 1 -p 1 0 -1 -k 0 -k 1 -k 2 -k 3 -k 4 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def locator(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p 0 1.12 -2.68221e-09 -p -0.03 1 -0.0519615 -p 0.06 1 0 -p 0 1.12 -2.68221e-09 -p -0.03 1 0.0519615 -p -0.03 1 -0.0519615 -p 0 1 0 -p -0.03 1 0.0519615 -p 0.06 1 0 -p 0 1 0 -p 0 -1 0 -p -0.03 -1 -0.0519615 -p 0 -1.12 2.68221e-09 -p 0.06 -1 0 -p -0.03 -1 -0.0519615 -p -0.03 -1 0.0519615 -p 0 -1.12 2.68221e-09 -p 0.06 -1 0 -p 0 -1 0 -p -0.03 -1 0.0519615 -p 0.06 -1 0 -p 0 -1 0 -p 0 0 0 -p -1 0 0 -p -1 0.0519615 -0.03 -p -1.12 2.68221e-09 0 -p -1 0 0.06 -p -1 -0.0519615 -0.03 -p -1 0.0519615 -0.03 -p -1 0 0.06 -p -1.12 2.68221e-09 0 -p -1 -0.0519615 -0.03 -p -1 0 0 -p -1 0 0.06 -p -1 0 0 -p 1 0 0 -p 1 0.0519615 0.03 -p 1.12 2.68221e-09 0 -p 1 0 -0.06 -p 1 -0.0519615 0.03 -p 1.12 2.68221e-09 0 -p 1 -0.0519615 0.03 -p 1 0.0519615 0.03 -p 1 0 -0.06 -p 1 0 0 -p 1 -0.0519615 0.03 -p 1 0 0 -p 0 0 0 -p 0 0 -1 -p 0.06 0 -1 -p 0 -2.68221e-09 -1.12 -p -0.03 0.0519615 -1 -p 0.06 0 -1 -p -0.03 -0.0519615 -1 -p 0 -2.68221e-09 -1.12 -p -0.03 0.0519615 -1 -p -0.03 -0.0519615 -1 -p 0 0 -1 -p -0.03 0.0519615 -1 -p 0 0 -1 -p 0 0 1 -p -0.03 0.0519615 1 -p -0.03 -0.0519615 1 -p 0 2.68221e-09 1.12 -p -0.03 0.0519615 1 -p 0.06 0 1 -p 0 0 1 -p -0.03 -0.0519615 1 -p 0.06 0 1 -p 0 2.68221e-09 1.12 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -k 53 -k 54 -k 55 -k 56 -k 57 -k 58 -k 59 -k 60 -k 61 -k 62 -k 63 -k 64 -k 65 -k 66 -k 67 -k 68 -k 69 -n "' + name + '"')
    # node.rotateOrder.setKeyable(True)
    return node


def cross(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p -1 0 -1 -p -1 0 -3 -p 1 0 -3 -p 1 0 -1 -p 3 0 -1 -p 3 0 1 -p 1 0 1 -p 1 0 3 -p -1 0 3 -p -1 0 1 -p -3 0 1 -p -3 0 -1 -p -1 0 -1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12  -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def arrow180(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p -0.251045 0 -1.015808 -p -0.761834 0 -0.979696 -p -0.486547 0 -0.930468 -p -0.570736 0 -0.886448 -p -0.72786 0 -0.774834 -p -0.909301 0 -0.550655 -p -1.023899 0 -0.285854 -p -1.063053 0 9.80765e-009 -p -1.023899 0 0.285854 -p -0.909301 0 0.550655 -p -0.72786 0 0.774834 -p -0.570736 0 0.886448 -p -0.486547 0 0.930468 -p -0.761834 0 0.979696 -p -0.251045 0 1.015808 -p -0.498915 0 0.567734 -p -0.440202 0 0.841857 -p -0.516355 0 0.802034 -p -0.658578 0 0.701014 -p -0.822676 0 0.498232 -p -0.926399 0 0.258619 -p -0.961797 0 8.87346e-009 -p -0.926399 0 -0.258619 -p -0.822676 0 -0.498232 -p -0.658578 0 -0.701014 -p -0.516355 0 -0.802034 -p -0.440202 0 -0.841857 -p -0.498915 0 -0.567734 -p -0.251045 0 -1.015808 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def triangle(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p -1.03923 0 0.6 -p 1.03923 0 0.6 -p 0 0 -1.2 -p -1.03923 0 0.6 -k 0 -k 1 -k 2 -k 3 -n "' + name + '"')
    # node.rotateOrder.setKeyable(True)
    return node


def angle(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p -1 0 -3 -p 1 0 -3 -p 1 0 1 -p -3 0 1 -p -3 0 -1 -p -1 0 -1 -p -1 0 -3 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def cube(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p -0.5 0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 0.5 0.5 -p -0.5 0.5 0.5 -p -0.5 0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 -0.5 0.5 -p 0.5 -0.5 0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 0.5 0.5 -p 0.5 -0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 0.5 0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def crossArrow(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p 0 0 -1.5 -p 0.5 0 -1.25 -p 0.25 0 -1.25 -p 0.25 0 -0.25 -p 1.25 0 -0.25 -p 1.25 0 -0.5 -p 1.5 0 0 -p 1.25 0 0.5 -p 1.25 0 0.25 -p 0.25 0 0.25 -p 0.25 0 1.25 -p 0.5 0 1.25 -p 0 0 1.5 -p -0.5 0 1.25 -p -0.25 0 1.25 -p -0.25 0 0.25 -p -1.25 0 0.25 -p -1.25 0 0.5 -p -1.5 0 0 -p -1.25 0 -0.5 -p -1.25 0 -0.25 -p -0.25 0 -0.25 -p -0.25 0 -1.25 -p -0.5 0 -1.25 -p 0 0 -1.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def dir1Arrow(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p 0 0 -1.32 -p -0.99 0 0 -p -0.33 0 0 -p -0.33 0 0.99 -p 0.33 0 0.99 -p 0.33 0 0 -p 0.99 0 0 -p 0 0 -1.32 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -n "' + name + '" ;')
    # node.rotateOrder.setKeyable(True)
    return node


def dir2Arrow(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p 0 0 -2.31 -p -0.99 0 -0.99 -p -0.33 0 -0.99 -p -0.33 0 0.99 -p -0.99 0 0.99 -p 0 0 2.31 -p 0.99 0 0.99 -p 0.33 0 0.99 -p 0.33 0 -0.99 -p 0.99 0 -0.99 -p 0 0 -2.31 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def trident(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p -0.961797 0 8.87346e-09 -p -0.926399 0 0.258619 -p -0.822676 0 0.498232 -p -0.658578 0 0.701014 -p -0.516355 0 0.802034 -p -0.440202 0 0.841857 -p -0.498915 0 0.567734 -p -0.251045 0 1.015808 -p -0.761834 0 0.979696 -p -0.486547 0 0.930468 -p -0.570736 0 0.886448 -p -0.72786 0 0.774834 -p -0.909301 0 0.550655 -p -1.023899 0 0.285854 -p -1.053863 0 0.0649027 -p -1.875348 0 0.0649027 -p -1.761901 0 0.291191 -p -2.150155 0 0 -p -1.761901 0 -0.291191 -p -1.875348 0 -0.0649027 -p -1.053863 0 -0.0649027 -p -1.023899 0 -0.285854 -p -0.909301 0 -0.550655 -p -0.72786 0 -0.774834 -p -0.570736 0 -0.886448 -p -0.486547 0 -0.930468 -p -0.761834 0 -0.979696 -p -0.251045 0 -1.015808 -p -0.498915 0 -0.567734 -p -0.440202 0 -0.841857 -p -0.516355 0 -0.802034 -p -0.658578 0 -0.701014 -p -0.822676 0 -0.498232 -p -0.926399 0 -0.258619 -p -0.961797 0 8.87346e-09 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def pyramid(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p 0.57735 -0.408248 0 -p -0.288675 -0.408248 -0.5 -p 0 0.408248 0 -p 0.57735 -0.408248 0 -p -0.288675 -0.408248 0.5 -p 0 0.408248 0 -p -0.288675 -0.408248 -0.5 -p -0.288675 -0.408248 0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -n "' + name + '" ;')
    # node.rotateOrder.setKeyable(True)
    return node


def prism(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p 0 -0.360988 0 -p 0.398795 0 -0.398795 -p 0.398795 0 0.398795 -p -0.398795 0 0.398795 -p -0.398795 0 -0.398795 -p 0.398795 0 -0.398795 -p 0 0.360988 0 -p -0.398795 0 0.398795 -p 0 -0.360988 0 -p 0.398795 0 0.398795 -p 0 0.360988 0 -p -0.398795 0 -0.398795 -p 0 -0.360988 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -n "' + name + '" ;')
    # node.rotateOrder.setKeyable(True)
    return node


def openCube(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p -0.5 0.5 0.5 -p -0.5 0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 0.5 0.5 -p 0.5 -0.5 0.5 -p 0.5 -0.5 -0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 -0.5 -0.5 -p -0.5 -0.5 0.5 -p -0.5 0.5 0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -n "' + name + '" ;')
    # node.rotateOrder.setKeyable(True)
    return node


def arrowSphere(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='controlCurve'):
    node = mel.eval(
        'curve -d 1 -p 0 0.35 -1.001567 -p -0.336638 0.677886 -0.751175 -p -0.0959835 0.677886 -0.751175 -p -0.0959835 0.850458 -0.500783 -p -0.0959835 0.954001 -0.0987656 -p -0.500783 0.850458 -0.0987656 -p -0.751175 0.677886 -0.0987656 -p -0.751175 0.677886 -0.336638 -p -1.001567 0.35 0 -p -0.751175 0.677886 0.336638 -p -0.751175 0.677886 0.0987656 -p -0.500783 0.850458 0.0987656 -p -0.0959835 0.954001 0.0987656 -p -0.0959835 0.850458 0.500783 -p -0.0959835 0.677886 0.751175 -p -0.336638 0.677886 0.751175 -p 0 0.35 1.001567 -p 0.336638 0.677886 0.751175 -p 0.0959835 0.677886 0.751175 -p 0.0959835 0.850458 0.500783 -p 0.0959835 0.954001 0.0987656 -p 0.500783 0.850458 0.0987656 -p 0.751175 0.677886 0.0987656 -p 0.751175 0.677886 0.336638 -p 1.001567 0.35 0 -p 0.751175 0.677886 -0.336638 -p 0.751175 0.677886 -0.0987656 -p 0.500783 0.850458 -0.0987656 -p 0.0959835 0.954001 -0.0987656 -p 0.0959835 0.850458 -0.500783 -p 0.0959835 0.677886 -0.751175 -p 0.336638 0.677886 -0.751175 -p 0 0.35 -1.001567 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def cubeBevel(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='cuveBevel'):
    node = mel.eval(
        'curve -d 1 -p -0.455556 -0.455556 -0.455556 -p -0.433333 -0.433333 -0.5 -p 0.433333 -0.433333 -0.5 -p 0.455556 -0.455556 -0.455556 -p 0.433333 -0.5 -0.433333 -p -0.433333 -0.5 -0.433333 -p -0.433333 -0.5 0.433333 -p 0.433333 -0.5 0.433333 -p 0.433333 -0.5 -0.433333 -p 0.455556 -0.455556 -0.455556 -p 0.5 -0.433333 -0.433333 -p 0.5 0.433333 -0.433333 -p 0.5 0.433333 0.433333 -p 0.5 -0.433333 0.433333 -p 0.5 -0.433333 -0.433333 -p 0.455556 -0.455556 -0.455556 -p 0.433333 -0.433333 -0.5 -p 0.433333 0.433333 -0.5 -p -0.433333 0.433333 -0.5 -p -0.433333 -0.433333 -0.5 -p -0.455556 -0.455556 -0.455556 -p -0.433333 -0.5 -0.433333 -p -0.455556 -0.455556 -0.455556 -p -0.5 -0.433333 -0.433333 -p -0.5 -0.433333 0.433333 -p -0.5 0.433333 0.433333 -p -0.5 0.433333 -0.433333 -p -0.5 -0.433333 -0.433333 -p -0.5 0.433333 -0.433333 -p -0.455556 0.455556 -0.455556 -p -0.433333 0.433333 -0.5 -p -0.455556 0.455556 -0.455556 -p -0.433333 0.5 -0.433333 -p 0.433333 0.5 -0.433333 -p 0.433333 0.5 0.433333 -p -0.433333 0.5 0.433333 -p -0.433333 0.5 -0.433333 -p 0.433333 0.5 -0.433333 -p 0.455556 0.455556 -0.455556 -p 0.433333 0.433333 -0.5 -p 0.455556 0.455556 -0.455556 -p 0.5 0.433333 -0.433333 -p 0.455556 0.455556 -0.455556 -p 0.433333 0.5 -0.433333 -p 0.433333 0.5 0.433333 -p 0.455556 0.455556 0.455556 -p 0.5 0.433333 0.433333 -p 0.455556 0.455556 0.455556 -p 0.433333 0.433333 0.5 -p 0.433333 -0.433333 0.5 -p 0.455556 -0.455556 0.455556 -p 0.5 -0.433333 0.433333 -p 0.455556 -0.455556 0.455556 -p 0.433333 -0.5 0.433333 -p 0.455556 -0.455556 0.455556 -p 0.433333 -0.433333 0.5 -p -0.433333 -0.433333 0.5 -p -0.455556 -0.455556 0.455556 -p -0.433333 -0.5 0.433333 -p -0.455556 -0.455556 0.455556 -p -0.5 -0.433333 0.433333 -p -0.455556 -0.455556 0.455556 -p -0.433333 -0.433333 0.5 -p -0.433333 0.433333 0.5 -p -0.455556 0.455556 0.455556 -p -0.5 0.433333 0.433333 -p -0.455556 0.455556 0.455556 -p -0.433333 0.5 0.433333 -p -0.455556 0.455556 0.455556 -p -0.433333 0.433333 0.5 -p 0.433333 0.433333 0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 -k 29 -k 30 -k 31 -k 32 -k 33 -k 34 -k 35 -k 36 -k 37 -k 38 -k 39 -k 40 -k 41 -k 42 -k 43 -k 44 -k 45 -k 46 -k 47 -k 48 -k 49 -k 50 -k 51 -k 52 -k 53 -k 54 -k 55 -k 56 -k 57 -k 58 -k 59 -k 60 -k 61 -k 62 -k 63 -k 64 -k 65 -k 66 -k 67 -k 68 -k 69 -k 70 -n "' + name + '";')
    # node.rotateOrder.setKeyable(True)
    return node


def square3D(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='square3D'):
    points = [[-1.5931700403370996e-14, -0.4589151321818673, -0.4589151321818673],
              [-1.049160758270773e-14, -0.44341100122265187, -0.4899219987773481],
              [1.074140776324839e-14, -0.44341100122265187, -0.4899219987773481],
              [1.609823385706477e-14, -0.4589151321818673, -0.4589151321818673],
              [1.074140776324839e-14, -0.4899219987773481, -0.44341100122265187],
              [-1.049160758270773e-14, -0.4899219987773481, -0.44341100122265187],
              [-1.049160758270773e-14, -0.4899219987773481, 0.44341100122265187],
              [1.074140776324839e-14, -0.4899219987773481, 0.44341100122265187],
              [1.074140776324839e-14, -0.4899219987773481, -0.44341100122265187],
              [1.609823385706477e-14, -0.4589151321818673, -0.4589151321818673],
              [0.027217060408329302, -0.44341100122265187, -0.44341100122265187],
              [0.027217060408329302, 0.44341100122265187, -0.44341100122265187],
              [0.027217060408329302, 0.44341100122265187, 0.44341100122265187],
              [0.027217060408329302, -0.44341100122265187, 0.44341100122265187],
              [0.027217060408329302, -0.44341100122265187, -0.44341100122265187],
              [1.609823385706477e-14, -0.4589151321818673, -0.4589151321818673],
              [1.074140776324839e-14, -0.44341100122265187, -0.4899219987773481],
              [1.074140776324839e-14, 0.44341100122265187, -0.4899219987773481],
              [-1.049160758270773e-14, 0.44341100122265187, -0.4899219987773481],
              [-1.049160758270773e-14, -0.44341100122265187, -0.4899219987773481],
              [-1.5931700403370996e-14, -0.4589151321818673, -0.4589151321818673],
              [-1.049160758270773e-14, -0.4899219987773481, -0.44341100122265187],
              [-1.5931700403370996e-14, -0.4589151321818673, -0.4589151321818673],
              [-0.027217060408329385, -0.44341100122265187, -0.44341100122265187],
              [-0.027217060408329385, -0.44341100122265187, 0.44341100122265187],
              [-0.027217060408329385, 0.44341100122265187, 0.44341100122265187],
              [-0.027217060408329385, 0.44341100122265187, -0.44341100122265187],
              [-0.027217060408329385, -0.44341100122265187, -0.44341100122265187],
              [-0.027217060408329385, 0.44341100122265187, -0.44341100122265187],
              [-1.5931700403370996e-14, 0.4589151321818673, -0.4589151321818673],
              [-1.049160758270773e-14, 0.44341100122265187, -0.4899219987773481],
              [-1.5931700403370996e-14, 0.4589151321818673, -0.4589151321818673],
              [-1.049160758270773e-14, 0.4899219987773481, -0.44341100122265187],
              [1.074140776324839e-14, 0.4899219987773481, -0.44341100122265187],
              [1.074140776324839e-14, 0.4899219987773481, 0.44341100122265187],
              [-1.049160758270773e-14, 0.4899219987773481, 0.44341100122265187],
              [-1.049160758270773e-14, 0.4899219987773481, -0.44341100122265187],
              [1.074140776324839e-14, 0.4899219987773481, -0.44341100122265187],
              [1.609823385706477e-14, 0.4589151321818673, -0.4589151321818673],
              [1.074140776324839e-14, 0.44341100122265187, -0.4899219987773481],
              [1.609823385706477e-14, 0.4589151321818673, -0.4589151321818673],
              [0.027217060408329302, 0.44341100122265187, -0.44341100122265187],
              [1.609823385706477e-14, 0.4589151321818673, -0.4589151321818673],
              [1.074140776324839e-14, 0.4899219987773481, -0.44341100122265187],
              [1.074140776324839e-14, 0.4899219987773481, 0.44341100122265187],
              [1.609823385706477e-14, 0.4589151321818673, 0.4589151321818673],
              [0.027217060408329302, 0.44341100122265187, 0.44341100122265187],
              [1.609823385706477e-14, 0.4589151321818673, 0.4589151321818673],
              [1.074140776324839e-14, 0.44341100122265187, 0.4899219987773481],
              [1.074140776324839e-14, -0.44341100122265187, 0.4899219987773481],
              [1.609823385706477e-14, -0.4589151321818673, 0.4589151321818673],
              [0.027217060408329302, -0.44341100122265187, 0.44341100122265187],
              [1.609823385706477e-14, -0.4589151321818673, 0.4589151321818673],
              [1.074140776324839e-14, -0.4899219987773481, 0.44341100122265187],
              [1.609823385706477e-14, -0.4589151321818673, 0.4589151321818673],
              [1.074140776324839e-14, -0.44341100122265187, 0.4899219987773481],
              [-1.049160758270773e-14, -0.44341100122265187, 0.4899219987773481],
              [-1.5931700403370996e-14, -0.4589151321818673, 0.4589151321818673],
              [-1.049160758270773e-14, -0.4899219987773481, 0.44341100122265187],
              [-1.5931700403370996e-14, -0.4589151321818673, 0.4589151321818673],
              [-0.027217060408329385, -0.44341100122265187, 0.44341100122265187],
              [-1.5931700403370996e-14, -0.4589151321818673, 0.4589151321818673],
              [-1.049160758270773e-14, -0.44341100122265187, 0.4899219987773481],
              [-1.049160758270773e-14, 0.44341100122265187, 0.4899219987773481],
              [-1.5931700403370996e-14, 0.4589151321818673, 0.4589151321818673],
              [-0.027217060408329385, 0.44341100122265187, 0.44341100122265187],
              [-1.5931700403370996e-14, 0.4589151321818673, 0.4589151321818673],
              [-1.049160758270773e-14, 0.4899219987773481, 0.44341100122265187],
              [-1.5931700403370996e-14, 0.4589151321818673, 0.4589151321818673],
              [-1.049160758270773e-14, 0.44341100122265187, 0.4899219987773481],
              [1.074140776324839e-14, 0.44341100122265187, 0.4899219987773481]]

    node = pymel.curve(p=points, d=1, name=name)
    node.rotateOrder.setKeyable(True)
    return node


def locatorCross(scale=(1, 1, 1), orientation=(0, 0, 0), offset=(0, 0, 0), color=17, mirror=None, name='locatorCross'):
    points = [[3.032641500666399e-10, 0.22347475986546647, -0.0005406200327391884],
              [0.003873895295612548, 0.21452837796583143, -0.0027772155076479284],
              [1.0329685844147403e-10, 0.21452837796583143, 0.003932570917078296],
              [3.032641500666399e-10, 0.22347475986546647, -0.0005406200327391884],
              [-0.0038738950890188258, 0.21452837796583143, -0.0027772155076479284],
              [0.003873895295612548, 0.21452837796583143, -0.0027772155076479284],
              [1.0329685844147403e-10, 0.21452837796583143, -0.000540620032739187],
              [-0.0038738950890188258, 0.21452837796583143, -0.0027772155076479284],
              [1.0329685844147403e-10, 0.21452837796583143, 0.003932570917078296],
              [1.0329685844147403e-10, 0.21452837796583143, -0.000540620032739187],
              [1.0329686109092872e-10, 0.00369678228608928, 5.99563801384484e-17],
              [0.0020011334402004932, 0.00369678228608928, -0.0011553554094301706],
              [2.5849394142282115e-26, -4.85722573273506e-17, 6.049848122469115e-17],
              [1.0329686109092872e-10, 0.00369678228608928, 0.0023107108188605216],
              [0.0020011334402004932, 0.00369678228608928, -0.0011553554094301706],
              [-0.002001133233606771, 0.00369678228608928, -0.0011553554094301706],
              [2.5849394142282115e-26, -4.85722573273506e-17, 6.049848122469115e-17],
              [1.0329686109092872e-10, 0.00369678228608928, 0.0023107108188605216],
              [1.0329686109092872e-10, 0.00369678228608928, 5.99563801384484e-17],
              [-0.002001133233606771, 0.00369678228608928, -0.0011553554094301706],
              [1.0329686109092872e-10, 0.00369678228608928, 0.0023107108188605216],
              [1.0329686109092872e-10, 0.00369678228608928, 5.99563801384484e-17],
              [6.571407041923037e-11, 0.178179011115784, -3.3176586478056436e-16],
              [0.0005406201360361137, 0.17817901111578074, -0.03634936685005059],
              [0.002777215610944859, 0.18205290630809648, -0.03634936685005059],
              [0.0005406201360361137, 0.17817901131574806, -0.045295748749685574],
              [-0.003932570813781368, 0.17817901111578074, -0.03634936685005059],
              [0.002777215610944859, 0.17430511592346506, -0.03634936685005059],
              [0.002777215610944859, 0.18205290630809648, -0.03634936685005059],
              [-0.003932570813781368, 0.17817901111578074, -0.03634936685005059],
              [0.0005406201360361137, 0.17817901131574806, -0.045295748749685574],
              [0.002777215610944859, 0.17430511592346506, -0.03634936685005059],
              [0.0005406201360361137, 0.17817901111578074, -0.03634936685005059],
              [-0.003932570813781368, 0.17817901111578074, -0.03634936685005059],
              [0.0005406201360361137, 0.17817901111578074, -0.03634936685005059],
              [-0.0005406199294423972, 0.17817901111578074, 0.036349366850050746],
              [-0.0027772154043511363, 0.18205290630809648, 0.036349366850050746],
              [-0.0005406199294423972, 0.17817901131574806, 0.04529574874968571],
              [0.00393257102037509, 0.17817901111578074, 0.036349366850050746],
              [-0.0027772154043511363, 0.17430511592346506, 0.036349366850050746],
              [-0.0005406199294423972, 0.17817901131574806, 0.04529574874968571],
              [-0.0027772154043511363, 0.17430511592346506, 0.036349366850050746],
              [-0.0027772154043511363, 0.18205290630809648, 0.036349366850050746],
              [0.00393257102037509, 0.17817901111578074, 0.036349366850050746],
              [-0.0005406199294423972, 0.17817901111578074, 0.036349366850050746],
              [-0.0027772154043511363, 0.17430511592346506, 0.036349366850050746],
              [-0.0005406199294423972, 0.17817901111578074, 0.036349366850050746],
              [6.571407041923037e-11, 0.178179011115784, -3.3176586478056436e-16],
              [0.11045401350477006, 0.17817901111578405, -0.0005406200327428384],
              [0.11045401350477006, 0.17817901111578405, 0.003932570917074644],
              [0.11776065628575764, 0.17817901091581673, -0.0005406200327428384],
              [0.11045401350477006, 0.18205290630809967, -0.0027772155076516043],
              [0.11045401350477006, 0.17817901111578405, 0.003932570917074644],
              [0.11045401350477006, 0.17430511592346842, -0.002777215507651554],
              [0.11776065628575764, 0.17817901091581673, -0.0005406200327428384],
              [0.11045401350477006, 0.18205290630809967, -0.0027772155076516043],
              [0.11045401350477006, 0.17430511592346842, -0.002777215507651554],
              [0.11045401350477006, 0.17817901111578405, -0.0005406200327428384],
              [0.11045401350477006, 0.18205290630809967, -0.0027772155076516043],
              [0.11045401350477006, 0.17817901111578405, -0.0005406200327428384],
              [-0.11045401337334215, 0.17817901111578405, -0.0005406200327428384],
              [-0.11045401337334215, 0.18205290630809967, -0.0027772155076516043],
              [-0.11045401337334215, 0.17430511592346842, -0.002777215507651554],
              [-0.11776065615432954, 0.17817901131575137, -0.0005406200327428384],
              [-0.11045401337334215, 0.18205290630809967, -0.0027772155076516043],
              [-0.11045401337334215, 0.17817901111578405, 0.003932570917074644],
              [-0.11045401337334215, 0.17817901111578405, -0.0005406200327428384],
              [-0.11045401337334215, 0.17430511592346842, -0.002777215507651554],
              [-0.11045401337334215, 0.17817901111578405, 0.003932570917074644],
              [-0.11776065615432954, 0.17817901131575137, -0.0005406200327428384]]

    node = pymel.curve(p=points, d=1, name=name)
    node.rotateOrder.setKeyable(True)
    return node
