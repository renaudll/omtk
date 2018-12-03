from omtk.nodegraph.adaptors.node.base import NodeGraphNodeAdaptor
from omtk.vendor.mock_maya import MockedNode
from omtk.vendor.mock_maya import MockedSession


class NodeGraphMockedNodeAdaptor(NodeGraphNodeAdaptor):
    def __init__(self, session, data):
        assert isinstance(data, MockedNode)
        super(NodeGraphMockedNodeAdaptor, self).__init__(data)
        self._session = session

    @property
    def session(self):
        """
        :rtype: MockedSession
        """
        return self._session

    @property
    def node(self):
        """
        :rtype: MockedNode
        """
        return self._data

    def get_name(self):
        return self.node.name

    def get_parent(self):
        return self.node.parent

    def get_type(self):
        return self.node.nodetype

    def delete(self):
        return self.session.remove_node(self.node)
