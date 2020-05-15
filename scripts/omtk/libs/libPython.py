import logging
import time

_LOG = logging.getLogger(__name__)


def resize_list(val, desired_size, default=None):
    list_size = len(val)
    if list_size > desired_size:
        for _ in range(list_size - desired_size):
            val.pop(-1)
    elif list_size < desired_size:
        for _ in range(desired_size - list_size):
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
            _LOG.debug("Resolved %s with %s iterations.", mid, iter_count)
            return mid

        if result_high > result_low:
            low = mid
        else:
            high = mid

        mid = (low + high) / 2.0

    _LOG.warning("Could not resolve value under %s iterations.", max_iter)
    return mid
