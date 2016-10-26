import functools

class decorator_uiexpose(object):
    """
    Use this decorator to expose instance method to the GUI.
    """
    def __init__(self, flags=None):
        if flags is None:
            flags = []
        self.flags = flags
    def __call__(self, fn, *args, **kwargs):
        def wrapped_f(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapped_f.__can_show__ = self.__can_show__
        wrapped_f._flags = self.flags
        return wrapped_f
    def __get__(self, inst, owner):
        fn = functools.partial(self.__call__, inst)
        fn.__can_show__ = self.__can_show__  # todo: necessary?
        fn._flags = self.flags  # todo: necessary?
        return fn
    def __can_show__(self):
        """
        This method is used for duck-typing by the interface.
        """
        return True