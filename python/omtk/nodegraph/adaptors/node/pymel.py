import pymel.core as pymel
from omtk.nodegraph.adaptors.node.base import NodeGraphNodeAdaptor


class NodeGraphNodePymelAdaptor(NodeGraphNodeAdaptor):
    def __init__(self, data):
        assert (isinstance(data, pymel.PyNode))
        super(NodeGraphNodePymelAdaptor, self).__init__(data)

    @property
    def data(self):
        """
        :rtype: pymel.PyNode
        """

    def get_name(self):
        return self.data.nodeName()

    def get_type(self):
        return self.data.nodeType()

    def get_parent(self):
        return self.data.getParent()
