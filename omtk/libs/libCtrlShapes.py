import pymel.core as pymel


def create_shape_needle(size=1, length=None, *args, **kwargs):
    """
    :param size:
    :param length:
    :param args:
    :param kwargs:
    :return:
    """
    # Default length is 2x the provided size
    if length is None:
        length = size * 4.0

    n = 1.195
    m = 0.195
    c = 1.275
    d = 0.275
    f = 0.805
    e = 0.725

    shape1 = pymel.curve(d=1, p=[
        (0.0, 0.0, 0.0),
        (0.0, 0.750, 0.0)
    ])
    shape2 = pymel.curve(d=1, p=[
        (-m, n, -0.0),
        (0.0, c, 0.0),
        (m, n, 0.0),
        (d, 1.0, 0.0),
        (m, f, 0.0),
        (0.0, e, 0),
        (-m, f, -0.0),
        (-d, 1.0, 0.0),
        (-m, n, 0.0),
        (0.0, c, 0.0),
        (m, n, 0.0)
    ])
    shape3 = pymel.curve(d=1, p=[
        (-m, 1.0, -m),
        (-d, 1.0, 0.0),
        (-m, 1.0, m),
        (-0.0, 1.0, d),
        (m, 1.0, m),
        (d, 1.0, 0.0),
        (m, 1.0, -m),
        (0.0, 1.0, -d),
        (-m, 1.0, -m),
        (-d, 1.0, 0.0),
        (-m, 1.0, m)
    ])
    shape2.getShape().setParent(shape1, shape=True, relative=True)
    shape3.getShape().setParent(shape1, shape=True, relative=True)
    pymel.delete(shape2)
    pymel.delete(shape3)
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
