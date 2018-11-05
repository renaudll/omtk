from omtk_test.mock_maya.cmds.session import MockedCmdsSession
from omtk_test.mock_maya.pymel.node import MockedPymelNode
from omtk_test.mock_maya.pymel.port import MockedPymelPort


class MockedPymelSession(MockedCmdsSession):
    """
    Mock for the maya.cmds python module

    :param MockedSession session: The mocked session for this adaptor.
    """
    def __init__(self, *args, **kwargs):
        super(MockedPymelSession, self).__init__(*args, **kwargs)

        self._nodes = {}

    def _node(self, val):
        """
        Create a mock of pymel.PyNode
        """
        key = MockedPymelNode(self, val)
        self._nodes[key] = val
        return key

    def _attribute(self, args):
        """
        Create a mock of pymel.Attribute
        """
        return MockedPymelPort(self, args)

    def _to_mel(self, data):
        """

        :param data:
        :return:
        """
        try:
            return data.__melobject__()
        except AttributeError:
            return data

    def _from_mel(self, mel):
        for node in self._nodes:
            if node._match(mel):
                return node
        return None

    def ls(self, *args, **kwargs):
        nodes = super(MockedPymelSession, self).ls(*args, **kwargs)
        return [self._node(node) for node in nodes]

    def objExists(self, args):
        names = [str(arg) for arg in args]
        return self.session.exists(names)

    def createNode(self, *args, **kwargs):
        node = super(MockedPymelSession, self).createNode(*args, **kwargs)
        return MockedPymelNode(self, node)

    def listAttr(self, objects):
        attrs = super(MockedPymelSession, self).listAttr(objects)
        return [MockedPymelPort(self, attr) for attr in attrs]

    def addAttr(self, *args, **kwargs):
        raise NotImplementedError
        # port = MockedPort(longName)
        # self.session.nodes.ports.add(port)

    def select(self, names):
        super(MockedPymelSession, self).select(names)
        return self.ls(selection=True)

    def parent(self, *dagnodes, **kwargs):
        names = [self._to_mel(node) for node in dagnodes]
        super(MockedPymelSession, self).parent(*names, **kwargs)
