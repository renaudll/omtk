import pymel.core as pymel
from maya import OpenMaya
from omtk.libs import libRigging

def create_shape_circle(size=1.0, normal=(1, 0, 0), *args, **kwargs):
    transform, make = pymel.circle(*args, **kwargs)
    make.radius.set(size)
    make.normal.set(normal)

    # Expose the rotateOrder
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

    return shape1


def create_shape_double_needle(normal=(0, 1, 0), *args, **kwargs):
    normal_inv = (normal[0] * -1, normal[1] * -1, normal[2] * -1)  # TODO: find an eleguant way
    shape1 = create_shape_needle(normal=normal, *args, **kwargs)
    shape2 = create_shape_needle(normal=normal_inv, *args, **kwargs)
    for shape in shape2.getShapes():
        shape.setParent(shape1, shape=True, relative=True)
    pymel.delete(shape2)
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
    return node


def create_shape_attrholder(size=1.0, **kwargs):
    s1 = size
    s2 = s1 * 0.7
    node = pymel.curve(d=1, p=[(0,0,s1),(0,s2,s2),(0,s1,0),(0,s2,-s2),(0,0,-s1),(0,-s2,-s2),(0,-s1,0),(0,-s2,s2),(0,0,s1),(-s2,0,s2),(-s1,0,0),(-s2,s2,0),(0,s1,0),(s2,s2,0),(s1,0,0),(s2,0,-s2),(0,0,-s1),(-s2,0,-s2),(-s1,0,0),(-s2,-s2,0),(0,-s1,0),(s2,-s2,0),(s1,0,0),(s2,0,s2),(0,0,s1),(-s2,0,s2)], k=range(26), *kwargs)
    return node


def create_shape_box(size=1.0, r=None, h=None):
    if r is None:
        r = size

    if h is None:
        h = size / 5.0

    node = pymel.curve(d=1, p=[(-r, -h, r), (-r, h, r), (r, h, r), (r, -h, r), (-r, -h, r), (-r, -h, -r), (-r, h, -r), (-r, h, r), (r, h, r), (r, h, -r), (r, -h, -r), (r, -h, r), (r, -h, -r), (-r, -h, -r), (-r, h, -r), (r, h, -r)] )
    return node

def create_shape_box_feet(refs, offset=pymel.datatypes.Vector(0,0,0), *args, **kwargs):
    dirs = [
        OpenMaya.MVector(-1,0,0),
        OpenMaya.MVector(1,0,0),
        OpenMaya.MVector(0,0,-1),
        OpenMaya.MVector(0,0,1)
    ]

    # Using all provided objects
    min_x = max_x = max_y = min_z = max_z = None
    min_y = 0
    geometries = pymel.ls(type='mesh')


    # Ray-cast
    for ref in refs:
        pos_world = ref.getTranslation(space='world')

        x = pos_world.x
        y = pos_world.y
        z = pos_world.z
        if min_x is None or x < min_x:
            min_x = x
        if max_x is None or x > max_x:
            max_x = x
        if max_y is None or y > max_y:
            max_y = y
        if min_z is None or z < min_z:
            min_z = z
        if max_z is None or z > max_z:
            max_z = z

        for dir in dirs:
            ray_cast_pos = next(iter(libRigging.ray_cast(pos_world, dir, geometries, debug=False)), None)
            if ray_cast_pos is None:
                continue

            x = ray_cast_pos.x
            y = ray_cast_pos.y
            z = ray_cast_pos.z
            if min_x is None or x < min_x:
                min_x = x
            if max_x is None or x > max_x:
                max_x = x
            if max_y is None or y > max_y:
                max_y = y
            if min_z is None or z < min_z:
                min_z = z
            if max_z is None or z > max_z:
                max_z = z

    # HACK: Apply offset since the ctrl is generally built in-place.
    # TODO: Find an elegant way
    min_x += offset.x
    max_x += offset.x
    min_y += offset.y
    max_y += offset.y
    min_z += offset.z
    max_z += offset.z

    pos1 = (min_x, min_y, min_z)
    pos2 = (min_x, min_y, max_z)
    pos3 = (min_x, max_y, min_z)
    pos4 = (min_x, max_y, max_z)
    pos5 = (max_x, min_y, min_z)
    pos6 = (max_x, min_y, max_z)
    pos7 = (max_x, max_y, min_z)
    pos8 = (max_x, max_y, max_z)
    node = pymel.curve(d=1, p=[pos2, pos4, pos8, pos6, pos2, pos1, pos3, pos4, pos8, pos7, pos5, pos6, pos5, pos1, pos3, pos7] )

    return node