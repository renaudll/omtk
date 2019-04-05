import pymel.core as pymel

from omtk.nodegraph.adaptors.node._utils import get_node_position, save_node_position
from omtk.nodegraph.adaptors.node.base import NodeGraphNodeAdaptor


class NodeGraphNodePymelAdaptor(NodeGraphNodeAdaptor):
    """
    A NodeGraph adaptor for a `pymel.PyNode`
    """
    def __init__(self, data):
        """
        :param data: pymel.PyNode
        """
        assert (isinstance(data, pymel.PyNode))
        super(NodeGraphNodePymelAdaptor, self).__init__(data)

    @property
    def data(self):
        """
        :rtype: pymel.PyNode
        """
        return self._data

    def get_name(self):
        return self.data.nodeName()

    def get_type(self):
        return self.data.nodeType()

    def get_parent(self):
        return self.data.getParent()

    def delete(self):
        return pymel.delete(self.data)

    def get_position(self):
        return get_node_position(self.data)

    def save_position(self, pos):
        """
        :param pos: A position to save.
        :type pos: tuple(float, float) 
        """
        save_node_position(self.data, pos)
