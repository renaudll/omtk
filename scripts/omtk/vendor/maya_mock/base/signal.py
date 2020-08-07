"""
Observer pattern implementation
"""
import logging
import threading

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

# TODO: Replace with https://github.com/dgovil/PySignal ?
# TODO: Implement __str__ that namespace sender?


class Signal(object):
    """
    Observer pattern implementation.
    Match QtCore.Signal interface for convenience.

    Q1: Why no use QtCore.Signal instead?
    A1: QtCore.Signal is compiled and cannot be inspected
        with breakpoints which make debugging harder.
    """

    def __init__(self, *_):
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
        LOG.debug("Connecting %s to Signal %s", func.__name__, self)
        self._funcs.add(func)

    def disconnect(self, func):
        """
        Disconnect a callable from the signal.

        :param object func: A callable object to disconnect from the signal.
        """
        LOG.debug("Disconnecting %s from Signal %s", func.__name__, self)
        self._funcs.remove(func)

    def emit(self, *args, **kwargs):
        """
        Call all functions registered to this signal.

        :param object args: Any arguments will be forwarded to the registered callable.
        :param object kwargs: Any arguments will be forwarded to the registered callable.
        """
        if self._block:
            LOG.debug("Skipping emit since block is True.")
            return

        LOG.debug("Signal %s emitted", self)
        self._mutex.acquire()
        self.block(True)
        try:
            for func in self._funcs:
                func(*args, **kwargs)
        finally:
            self._mutex.release()
            self.block(False)

    def block(self, state):
        """
        Set the "block" mutex that determine if we can emit the signal.
        :param bool state: Should we block the signal?
        """
        self._block = state
