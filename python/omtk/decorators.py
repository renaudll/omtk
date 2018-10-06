import contextlib
import logging
import os
import sys

import collections
import datetime
import functools
import time

log = logging.getLogger(__name__)


def decorator(decorator):
    """
    This decorator can be used to turn simple functions
    into well-behaved decorators, so long as the decorators
    are fairly simple. If a decorator expects a function and
    returns a function (no descriptors), and if it doesn't
    modify function attributes or docstring, then it is
    eligible to use this. Simply apply @simple_decorator to
    your decorator and it will automatically preserve the
    docstring and function attributes of functions to which
    it is applied.
    """

    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g

    # Now a few lines needed to make simple_decorator itself
    # be a well-behaved decorator.
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator


@decorator
def log_info(func):
    def subroutine(*args, **kwargs):
        log.info('calling {}'.format(func.__name__))
        return func(*args, **kwargs)

    return subroutine


@decorator
def log_warning(func):
    def subroutine(*args, **kwargs):
        log.warning('calling {}'.format(func.__name__))
        return func(*args, **kwargs)

    return subroutine


@contextlib.contextmanager
def pymel_preserve_selection():
    import pymel.core as pymel
    from omtk.libs import libPymel

    sel = pymel.selected()
    yield True
    sel = filter(libPymel.is_valid_PyNode, sel)
    if sel:
        pymel.select(sel)
    else:
        pymel.select(clear=True)


@decorator
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
            log.info('Process {0} took {1:2.3f} seconds to execute.'.format(m_NAME, time.time() - st))
            return rv

        return run

    return deco_retry


class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).

    src: https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    modified to support kwargs
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


class memoized_instancemethod(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).

    src: https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    modified to support kwargs
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


class cached_property(object):
    '''
    Use this decodator to cache read-only properties value.

    forked from: https://wiki.python.org/moin/PythonDecoratorLibrary#Cached_Properties
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
                log.info(
                    '[cached_properties] Updating took {0:02.4f} seconds: {1}.{2}'.format(et, inst.__class__.__name__,
                                                                                          self.__name__))

        return cache[self.__name__]


def open_scene(path):
    """
    Decorator for opening a Maya file.
    The provided path can be related to the file the function is defined.
    :param str path: A relative path to the function location.
    :return A decorator function
    :rtype: type
    """

    def deco_open(f):
        def f_open(*args, **kwargs):
            from maya import cmds
            path_ = os.path.abspath(os.path.join(os.path.dirname(sys.modules[f.__module__].__file__), path))
            cmds.file(path_, open=True, f=True)
            return f(*args, **kwargs)

        return f_open

    return deco_open


@decorator
def save_on_assert():
    """
    Backup the current scene if an exception is raise. Let the exception propagate afteward.
    """

    def deco(f):
        try:
            f()
        except Exception:
            from maya import cmds
            current_path = cmds.file(q=True, sn=True)
            if current_path:
                dirname = os.path.dirname(current_path)
                basename = os.path.basename(current_path)
                filename, ext = os.path.splitext(basename)

                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
                destination_path = os.path.join(dirname, '{}_{}{}'.format(filename, timestamp, ext))
                print("Saving scene to {}".format(destination_path))
                cmds.file(rename=destination_path)
                cmds.file(save=True, type='mayaAscii')
            raise

    return deco
