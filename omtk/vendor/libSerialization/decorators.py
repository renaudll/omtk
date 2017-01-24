import collections
import functools

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