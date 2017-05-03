"""
Modules instance can expose macro that will show in the interface.
"""
import abc


class ComponentAction(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, component):
        """
        :param component: The Component to associate the action with.
        """
        self.component = component

    def get_name(self):
        return

    def iter_flags(self):
        return
        yield

    def can_execute(self):
        return True

    def execute(self):
        raise NotImplementedError
