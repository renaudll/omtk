"""
A NodeGraphNodeAdaptor is the link between a NodeModel and some internal data.
This is a case of 'composition over inheritance'.
"""
import abc
import six


@six.add_metaclass(abc.ABCMeta)
class NodeGraphNodeAdaptor(object):
    """
    NodeGraph adaptor for a node
    """

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

    def get_position(self):
        """
        Retrieve the position of the node in the graph.
        In contrary to Maya, a node can only have one position.

        :return: x,y coordinates or None
        :rtype tuple(int,int) or None
        """
        return None

    def save_position(self, pos):
        """
        Store a provided position to the node if supported.

        :param tuple(int,int)
        """
        pass
