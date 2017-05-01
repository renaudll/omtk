"""
Utility functions to deal with construction history.
Please learn the following used nomenclature:
- mesh: A polygonal geometry shape
- surface: A nurbs geometry shape
- shape: Any geometry shape, including mesh and surface.
"""
import pymel.core as pymel

from omtk.libs.libRigging import _filter_shape


def _is_mesh(shape):
    return isinstance(shape, pymel.nodetypes.Mesh)


def _is_surface(shape):
    return isinstance(shape, pymel.nodetypes.NurbsSurface)


#
# Utility functions that compliment pymel.listHistory.
#

def _iter_history(shape, key=None, fn_stop=None, stop_at_shape=False, **kwargs):
    """
    Go through the history of the provided shapes and yield interesting elements.
    :param shape: The starting po
    :param key:
    :param stop_at_shape: If True, we will stop iterating as soon as we encounter a shape. Note that if you provided a
    transform, it will stop at the first encounter of the main shape.
    :param kwargs:
    :return:
    """
    # Determine what condition make us stop iterating though history.
    if stop_at_shape:
        shape_start = shape.getShape() if isinstance(shape, pymel.nodetypes.Transform) else shape
        if fn_stop:
            fn_stop = lambda shape: isinstance(shape, pymel.nodetypes.Shape) and shape != shape_start or fn_stop(shape)
        else:
            fn_stop = lambda shape: isinstance(shape, pymel.nodetypes.Shape) and shape != shape_start

    for hist in shape.listHistory(**kwargs):
        if hist == shape:
            continue
        if fn_stop and fn_stop(hist):
            return
        if key and key(hist):
            yield hist


def iter_history_foward(shape, **kwargs):
    for hist in _iter_history(shape, future=True, **kwargs):
        yield hist


def iter_history_backward(shape, **kwargs):
    for hist in _iter_history(shape, **kwargs):
        yield hist


def get_history_farthest_sibling(shape, **kwargs):
    i = iter_history_foward(shape, **kwargs)
    return next(reversed(list(i)), None)


def get_history_previous_sibling(shape, **kwargs):
    i = iter_history_backward(shape, **kwargs)
    return next(i, None)


#
# Utility functions to resolve skinning shapes from influences.
#

def iter_affected_shapes(objs, key=None):
    """
    :param obj: A reference object, generally a pymel.nodetypes.Joint.
    :return: The geometries affected by the object.
    """
    known_skinClusters = []

    # Ensure objs is iterable
    if not isinstance(objs, (tuple, list)):
        objs = [objs]

    for obj in objs:
        if isinstance(obj, pymel.nodetypes.Joint):
            # Collect all geometries affected by the joint.
            for hist in obj.worldMatrix.outputs():
                if isinstance(hist, pymel.nodetypes.SkinCluster) and not hist in known_skinClusters:
                    known_skinClusters.append(hist)
                    for geometry in hist.getOutputGeometry():
                        if key is None or key(geometry):
                            yield geometry


def get_affected_shapes(objs, key=None):
    return list(iter_affected_shapes(objs, key=key))


def get_affected_meshes(objs):
    return list(iter_affected_shapes(objs, key=_is_mesh))


def get_affected_surface(objs):
    return list(iter_affected_shapes(objs, key=_is_surface))
