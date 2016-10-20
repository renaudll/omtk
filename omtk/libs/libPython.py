import imp
import logging
import threading
import time
import functools
import collections
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

# forked from: https://wiki.python.org/moin/PythonDecoratorLibrary#Cached_Properties
class cached_property(object):
    '''
    Use this decodator to cache read-only properties value.
    '''

    def __call__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__
        return self

    def __get__(self, inst, owner):
        if '_cache' not in inst.__dict__:
            inst._cache = {}
        cache = inst._cache

        if self.__name__ not in cache:
            st = time.time()
            cache[self.__name__] = self.fget(inst)
            et = time.time() - st
            if (et - st) > 1:  # 1 second
                print '[cached_properties] Updating took {0:02.4f} seconds: {1}.{2}'.format(et, inst.__class__.__name__,
                                                                                            self.__name__)

        return cache[self.__name__]


# src: https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
# modified to support kwargs
class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)

        # Include kwargs
        # src: http://stackoverflow.com/questions/6407993/how-to-memoize-kwargs
        key = (args, frozenset(kwargs.items()))
        if key in self.cache:
            return self.cache[key]
        else:
            value = self.func(*args, **kwargs)
            self.cache[key] = value
            return value

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)

# src: https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
# modified to support kwargs
class memoized_instancemethod(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def call(self, inst, cache, *args, **kwargs):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)

        # Include kwargs
        # src: http://stackoverflow.com/questions/6407993/how-to-memoize-kwargs
        key = self.func.__name__
        subkey = (args, frozenset(kwargs.items()))

        try:
            cache1 = cache[key]
        except KeyError:
            cache1 = cache[key] = {}

        try:
            val = cache1[subkey]
        except KeyError:
            val = self.func(inst, *args, **kwargs)
            cache1[subkey] = val

        return val

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, inst, owner):
        try:
            cache = inst._cache
        except AttributeError:
            cache = inst._cache = {}
        """Support instance methods."""
        new_fn = functools.partial(self.call, inst, cache)
        new_fn.__name__ = self.func.__name__  # Ensure proper 'del inst[fn.__name__] behavior'
        return new_fn


def profiler(func):
    '''
    [debug] Inject this decorator in your function to automaticly run cProfile on them.
    '''

    def runProfile(*args, **kwargs):
        import cProfile
        pProf = cProfile.Profile()
        try:
            pProf.enable()
            pResult = func(*args, **kwargs)
            pProf.disable()
            return pResult
        finally:
            pProf.print_stats(sort='cumulative')

    return runProfile


def log_execution_time(NAME):
    def deco_retry(f):
        def run(*args, **kwargs):
            m_NAME = NAME  # make mutable
            st = time.time()
            rv = f(*args, **kwargs)
            print('Process {0} took {1:2.3f} seconds to execute.'.format(m_NAME, time.time() - st))
            return rv

        return run

    return deco_retry

#
# Taken from libSerialization
#
import sys

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
        #logging.warning("Error obtaining class definition for {0}: {1}".format(class_name, e))
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
