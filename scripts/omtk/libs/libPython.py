import collections
import functools
import logging
import time
import sys
import threading

logging = logging.getLogger("libPython")
logging.setLevel(0)


def resize_list(val, desired_size, default=None):
    list_size = len(val)
    if list_size > desired_size:
        for i in range(list_size - desired_size):
            val.pop(-1)
    elif list_size < desired_size:
        for i in range(desired_size - list_size):
            val.append(default)


def profiler(func):
    """
    [debug] Inject this decorator in your function to automaticly run cProfile on them.
    """

    def runProfile(*args, **kwargs):
        import cProfile

        pProf = cProfile.Profile()
        try:
            pProf.enable()
            pResult = func(*args, **kwargs)
            pProf.disable()
            return pResult
        finally:
            pProf.print_stats(sort="cumulative")

    return runProfile


def log_execution_time(NAME):
    def deco_retry(f):
        def run(*args, **kwargs):
            m_NAME = NAME  # make mutable
            st = time.time()
            rv = f(*args, **kwargs)
            print(
                "Process {0} took {1:2.3f} seconds to execute.".format(
                    m_NAME, time.time() - st
                )
            )
            return rv

        return run

    return deco_retry


#
# Taken from libSerialization
#


def get_class_namespace(classe, relative=False):
    if not isinstance(classe, object):
        return None  # Todo: throw exception
    class_name = classe.__name__
    if relative:
        tokens = class_name.split(".")
        return tokens[-1] if tokens else None
    else:
        tokens = []
        while classe is not object:
            tokens.append(class_name)
            classe = classe.__bases__[0]
        return ".".join(reversed(tokens))


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
        logging.warning("Can't find class definition %r", class_name)
        return None

    class_def = getattr(sys.modules[cls.__module__], cls.__name__)
    assert class_def is not None

    try:
        return class_def()
    except Exception as e:
        logging.error("Fatal error creating %r instance: %s", class_name, str(e))
        return None


def get_sub_classes(_cls):
    for subcls in _cls.__subclasses__():
        yield subcls
        for subsubcls in get_sub_classes(subcls):
            yield subsubcls


class LazySingleton(object):
    """A thread safe singleton that initialises when first referenced."""

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


def guess_value(
    default_low, default_high, fn_guess, max_iter=100, epsilon=0.00000000001
):
    low = default_low
    high = default_high
    mid = (low + high) / 2.0

    for iter_count in range(max_iter):
        iter_count += 1
        if iter_count > max_iter:
            raise Exception("Max iteration reached: %s" % max_iter)

        result_low = fn_guess(low)
        result_high = fn_guess(high)
        result = fn_guess(mid)

        if abs(1.0 - result) < epsilon:
            logging.debug("Resolved %s with %s iterations.", mid, iter_count)
            return mid

        if result_high > result_low:
            low = mid
        else:
            high = mid

        mid = (low + high) / 2.0

    logging.warning("Could not resolve value under %s iterations.", max_iter)
    return mid
