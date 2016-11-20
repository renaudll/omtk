from omtk.libs.libRigging import _filter_shape

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

