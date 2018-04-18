"""
A PortAdaptor is the link between a Port model and it's internal data.
This is a case of 'composition over inheritance'.
"""
import abc

from omtk.factories import factory_datatypes


class NodeGraphPortImpl(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, data):
        self._data = data

    def get_metadata(self):
        return self._data

    def get_metatype(self):
        return factory_datatypes.get_attr_datatype(self._data)

    def is_source(self):
        raise NotImplementedError

    def is_destination(self):
        raise NotImplementedError

    def get_inputs(self):
        return set()

    def get_outputs(self):
        return set()

    @abc.abstractmethod
    def is_readable(self):
        pass

    @abc.abstractmethod
    def is_writable(self):
        raise NotImplementedError

    @abc.abstractmethod
    def is_interesting(self):
        raise NotImplementedError

    @abc.abstractmethod
    def connect_from(self, val):
        raise NotImplementedError

    @abc.abstractmethod
    def connect_to(self, val):
        raise NotImplementedError

    # @abc.abstractmethod
    def disconnect_from(self, val):
        raise NotImplementedError

    # @abc.abstractmethod
    def disconnect_to(self):
        raise NotImplementedError


