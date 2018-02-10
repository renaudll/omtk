import gc
import imp
import logging
import threading
import itertools
import sys

logging = logging.getLogger('libPython')
logging.setLevel(0)


def does_module_exist(module_name):
    try:
        imp.find_module(module_name)
        return True
    except ImportError:
        return False


# src: http://code.activestate.com/recipes/66472/
def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end is None:
        end = start + 0.0
        start = 0.0

    if inc is None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)

    return L


def resize_list(val, desired_size, default=None):
    list_size = len(val)
    if list_size > desired_size:
        for i in range(list_size - desired_size):
            val.pop(-1)
    elif list_size < desired_size:
        for i in range(desired_size - list_size):
            val.append(default)


#
# Taken from libSerialization
#


def get_class_namespace(classe, relative=False):
    if not isinstance(classe, object):
        return None  # Todo: throw exception
    class_name = classe.__name__
    if relative:
        tokens = class_name.split('.')
        return tokens[-1] if tokens else None
    else:
        tokens = []
        while classe is not object:
            tokens.append(class_name)
            classe = classe.__bases__[0]
        return '.'.join(reversed(tokens))


def get_class_def(class_name, base_class=object, relative=False):
    try:
        for cls in base_class.__subclasses__():
            cls_path = get_class_namespace(cls, relative=relative)
            if cls_path == class_name:
                return cls
            else:
                t = get_class_def(class_name, base_class=cls, relative=relative)
                if t is not None:
                    return t
    except Exception as e:
        pass
        # logging.warning("Error obtaining class definition for {0}: {1}".format(class_name, e))
    return None


def create_class_instance(class_name):
    cls = get_class_def(class_name)

    if cls is None:
        logging.warning("Can't find class definition '{0}'".format(class_name))
        return None

    class_def = getattr(sys.modules[cls.__module__], cls.__name__)
    assert (class_def is not None)

    try:
        return class_def()
    except Exception as e:
        logging.error("Fatal error creating '{0}' instance: {1}".format(class_name, str(e)))
        return None


def get_sub_classes(_cls):
    for subcls in _cls.__subclasses__():
        yield subcls
        for subsubcls in get_sub_classes(subcls):
            yield subsubcls


class LazySingleton(object):
    """A threadsafe singleton that initialises when first referenced."""

    def __init__(self, instance_class, *nargs, **kwargs):
        self.instance_class = instance_class
        self.nargs = nargs
        self.kwargs = kwargs
        self.lock = threading.Lock()
        self.instance = None

    def __call__(self):
        if self.instance is None:
            try:
                self.lock.acquire()
                if self.instance is None:
                    self.instance = self.instance_class(*self.nargs, **self.kwargs)
                    self.nargs = None
                    self.kwargs = None
            finally:
                self.lock.release()
        return self.instance


def get_class_parent_level(cls, level=0):
    """
    Return the highest number of sub-classes before reaching the object case class.
    """
    print cls.__name__
    next_level = level + 1
    levels = [get_class_parent_level(base_cls, level=next_level) for base_cls in cls.__bases__]
    if levels:
        return max(levels)
    else:
        return level


def objects_by_id(id_):
    for obj in gc.get_objects():
        if id(obj) == id_:
            return obj
    raise Exception("No found")


# src: https://docs.python.org/2/library/itertools.html
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


# -- Algorithms --

# http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for next in graph[start] - visited:
        dfs(graph, next, visited)
    return visited

# http://eddmann.com/posts/using-iterative-deepening-depth-first-search-in-python/
def id_dfs(puzzle, goal, get_moves, max_iteration=20, known=None):
    """
    :param puzzle:
    :param goal:
    :param get_moves:
    :param max_iteration:
    :param known: A set that will keep track of explored nodes. Created if not provided.
    :return:
    """
    import itertools
    if known is None:
        known = set()

    def dfs(route, depth):
        if depth == 0:
            return
        if goal(route[-1]):
            return route
        for move in get_moves(route[-1]):
            if move not in route and move not in known:
                known.add(move)
                next_route = dfs(route + [move], depth - 1)
                if next_route:
                    return next_route

    for depth in itertools.count(start=1):
        if max_iteration and depth > max_iteration:
            raise StopIteration("Maximum iteration limit!")
        known.clear()
        route = dfs([puzzle], depth)
        if route:
            return route