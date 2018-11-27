"""
A PortAdaptor is the link between a Port model and it's internal data.
This is a case of 'composition over inheritance'.
"""
import abc


class NodeGraphPortImpl(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, data):
        self._data = data

    def get_metadata(self):  # TODO: Deprecate
        return self._data

    def get_metatype(self):  # TODO: Deprecate
        from omtk.factories import factory_datatypes
        return factory_datatypes.get_attr_datatype(self._data)

    @abc.abstractmethod
    def is_source(self):
        """
        Determine if the port is the source of a connection.

        :return: True if the port is the source of a connection. False otherwise.
        :rtype: bool
        """

    @abc.abstractmethod
    def is_destination(self):
        """
        Determine if the port is the destination of a connection.

        :return: True if the port is the destination of a connection. False otherwise.
        :rtype: bool
        """

    @abc.abstractmethod
    def get_inputs(self):
        """
        Get the ports of each input connections to this port.

        :return: A set of port.
        :rtype: set[object]
        """

    @abc.abstractmethod
    def get_outputs(self):
        """
        Get the ports of each output connections from this port.

        :return: A set of port.
        :rtype: set[object]
        """

    @abc.abstractmethod
    def is_readable(self):
        """
        Determine if a port is readable.
        A readable port can be the source of a connection.

        :return: True if the port is readable. False otherwise.
        :rtype: bool
        """

    @abc.abstractmethod
    def is_writable(self):
        """
        Determine if a port is writable.
        A writable port can be the destination of a connection.

        :return: True if the port is writable. False otherwise.
        :rtype: bool
        """

    @abc.abstractmethod
    def is_interesting(self):
        """
        Determine if the port is interesting.
        There's an internal algorithm in Maya that determine if a node can be displayed in the NodeEditor by default.
        It's not perfect but it's worth implementing.
        see https://around-the-corner.typepad.com/adn/2013/09/maya-node-editor-and-attributes.html

        :return: True if the port is interesting. False otherwise
        :rtype: bool
        """

    @abc.abstractmethod
    def connect_from(self, val):
        """
        Create a connection from another port to this port.
        :param val: The source port of the connection.
        """

    @abc.abstractmethod
    def connect_to(self, val):
        """
        Create a connection from this port to another port.
        :param val: The destination port of the connection.
        """

    @abc.abstractmethod
    def disconnect_from(self, val):
        """
        Disconnect a connection from another port to this port.
        :param val: The source port of the connection.
        """

    @abc.abstractmethod
    def disconnect_to(self):
        """
        Disconnect a connection from this port to another port.
        :param val: The destination port of the connection.
        """


