import os, types, imp, logging, re
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

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
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

import time, functools, collections

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
        # Monkey-patch _cache attribute
        # Note that we can't use the try/catch approch since shotgun.BaseEntity overwride __getattr__.
        if not '_cache' in inst.__dict__:
            inst._cache = {}
        cache = inst._cache

        if self.__name__ not in cache:
            st = time.time()
            cache[self.__name__] = self.fget(inst)
            et = time.time() - st
            if (et-st) > 1: # 1 second
                print '[cached_properties] Updating took {0:02.4f} seconds: {1}.{2}'.format(et, inst.__class__.__name__, self.__name__)

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
       '''Return the function's docstring.'''
       return self.func.__doc__
    def __get__(self, obj, objtype):
       '''Support instance methods.'''
       return functools.partial(self.__call__, obj)


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
            pProf.print_stats()
    return runProfile

def log_execution_time(NAME):
    def deco_retry(f):
        def run(*args, **kwargs):
            m_NAME = NAME # make mutable
            st = time.time()
            rv = f(*args, **kwargs)
            print('Process {0} took {1:2.3f} seconds to execute.'.format(m_NAME, time.time()-st))
            return rv
        return run
    return deco_retry