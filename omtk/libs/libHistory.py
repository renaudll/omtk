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

def _iter_history(shape, key=None, **kwargs):
    for hist in shape.listHistory(**kwargs):
        if hist == shape:
            continue
        if _filter_shape(hist, key):
            yield hist

def iter_history_foward(shape, key=None):
    for hist in _iter_history(shape, key=key, future=True):
        yield hist

def iter_history_backward(shape, key=None):
    for hist in _iter_history(shape, key=key):
        yield hist

def get_history_farthest_sibling(shape, key=None):
    i = iter_history_foward(shape, key=key)
    return next(reversed(list(i)), None)

def get_history_previous_sibling(shape, key=None):
    i = iter_history_backward(shape, key=key)
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
