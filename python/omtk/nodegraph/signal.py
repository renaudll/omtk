import logging
import threading

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# TODO: Replace with https://github.com/dgovil/PySignal ?
# TODO: Implement __str__ that query sender?


class Signal(object):
    """
    Observer pattern implementation that match QtCore.Signal interface.

    Q1: Why no use QtCore.Signal instead?
    A1: QtCore.Signal is compiled and cannot be inspected with breakpoints which make debugging harder.

    :param args: The signature of the signal. This is the type of argument that we expect to pass. Unused
    """
    def __init__(self, *args):
        self._mutex = threading.RLock()
        self._funcs = set()
        self._block = False

    def __repr__(self):
        # TODO: Retrieve sender name?
        return "<Signal {}>".format(self.__class__)

    def connect(self, func):
        """
        Connect a callable to the signal.

        :param object func: A callable object to connect to the signal.
        """
        log.debug("Connecting %s to Signal %s", func.__name__, self)
        self._funcs.add(func)

    def disconnect(self, func):
        """
        Disconnect a callable from the signal.

        :param object func: A callable object to disconnect from the signal.
        """
        log.debug("Disconnecting %s from Signal %s", func.__name__, self)
        self._funcs.remove(func)

    def emit(self, *args, **kwargs):
        """
        Call all functions registered to this signal.

        :param object args: Any arguments will be forwarded to the registered callable.
        :param object kwargs: Any arguments will be forwarded to the registered callable.
        """
        if self._block:
            log.debug("Skipping emit since block is True.")
            return

        log.debug("Signal %s emitted", self)
        self._mutex.acquire()
        self.block(True)
        try:
            for func in self._funcs:
                log.debug(" Calling %s.%s", func.im_class.__name__, func.im_func.__name__)
                func(*args, **kwargs)
        finally:
            self._mutex.release()
            self.block(False)

    def block(self, state):
        self._block = state
