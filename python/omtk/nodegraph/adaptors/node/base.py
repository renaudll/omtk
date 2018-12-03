"""
A NodeGraphNodeAdaptor is the link between a NodeModel and some internal data.
This is a case of 'composition over inheritance'.
"""
import abc


class NodeGraphNodeAdaptor(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, data):
        self._data = data

    @abc.abstractmethod
    def get_name(self):
        """
        Retrieve the node name.

        :return: The name of the node.
        :rtype: str
        """

    @abc.abstractmethod
    def get_parent(self):
        """
        Retrieve the node parent.

        :return: The parent of the node.
        :rtype: object or None
        """

    @abc.abstractmethod
    def get_type(self):
        """
        Retrieve the node type.

        :return: The type of the node
        :rtype: str
        """

    @abc.abstractmethod
    def delete(self):
        """
        Delete the node from the scene.
        """