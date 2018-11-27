from omtk.nodegraph.adaptors.node.base import NodeGraphNodeAdaptor
from omtk.vendor.mock_maya import MockedNode


class NodeGraphMockedNodeAdaptor(NodeGraphNodeAdaptor):
    def __init__(self, data):
        assert isinstance(data, MockedNode)
        super(NodeGraphMockedNodeAdaptor, self).__init__(data)

    @property
    def data(self):
        """
        :rtype: MockedNode
        """
        return self._data

    def get_name(self):
        return self.data.name

    def get_parent(self):
        return self.data.parent

    def get_type(self):
        return self.data.nodetype
