from decorators import memoized
from .core import get_class_namespace, get_class_module_root

def iter_subclasses_recursive(cls):
    yield cls

    try:
        for sub_cls in cls.__subclasses__():
            for x in iter_subclasses_recursive(sub_cls):
                yield x
    except TypeError:  # This will fail when encountering the 'type' datatype.
        pass

def iter_module_subclasses_recursive(module_root, cls):
    for sub_cls in iter_subclasses_recursive(cls):
        cur_module_root = get_class_module_root(sub_cls)
        if module_root == cur_module_root:
            yield sub_cls

class Cache(object):
    def __init__(self):
        self.classes = None
        self._cache_import_by_id = {}
        self._cache_networks_by_id = {}  # todo: merge with _cache_import_by_id

    @memoized
    def _get_cls_cache_by_module(self, module_name, base_class=object):
        i = iter_module_subclasses_recursive(module_name, base_class)
        result = {}
        for cls in i:
            result[cls.__name__] = cls
        return result

    @memoized
    def _get_cls_cache(self, base_class=object):
        i = iter_subclasses_recursive(base_class)
        result = {}
        for cls in i:
            result[cls.__name__] = cls
        return result

    def get_class_by_name(self, cls_name, module_name=None, base_class=object):
        if module_name is None:
            cache = self._get_cls_cache(base_class=base_class)
        else:
            cache = self._get_cls_cache_by_module(module_name=module_name, base_class=base_class)
        return cache.get(cls_name, None)

    def get_class_by_namespace(self, cls_namespace, module_name=None, base_class=object):
        if module_name is None:
            cache = self._get_cls_cache(base_class=base_class)
        else:
            cache = self._get_cls_cache_by_module(base_class=base_class)
        for cls in cache.values():
            cur_namespace = get_class_namespace(cls)
            if cls_namespace == cur_namespace:
                return cls

    def get_import_value_by_id(self, id, default=None):
        return self._cache_import_by_id.get(id, default)

    def set_import_value_by_id(self, id, val):
        self._cache_import_by_id[id] = val

    def get_network_by_id(self, id, default=None):
        return self._cache_networks_by_id.get(id, default)

    def set_network_by_id(self, id, net):
        self._cache_networks_by_id[id] = net