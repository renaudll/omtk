from ..cmds.session import MockedCmdsSession
from .node import MockedPymelNode
from .port import MockedPymelPort


class MockedPymelSession(MockedCmdsSession):
    """
    Mock for the maya.cmds python module

    :param MockedSession session: The mocked session for this adaptor.
    """
    def __init__(self, *args, **kwargs):
        super(MockedPymelSession, self).__init__(*args, **kwargs)

        self.session.nodeAdded.connect(self.__callback_node_added)
        self.session.nodeRemoved.connect(self.__callback_node_removed)

        self.__registry = {}

    def __callback_node_added(self, node):
        """
        Called when a node is added in the scene.
        :param MockedNode node: The node added
        """
        mock = MockedPymelNode(self, node)
        self.__registry[node] = mock

    def __callback_node_removed(self, node):
        """
        Called when a node is removed from the scene.
        :param MockedNode node: The node being removed.
        """
        self.__registry.pop(node, None)

    def _attribute(self, args):
        """
        Create a mock of pymel.Attribute
        """
        return MockedPymelPort(self, args)

    def _str_to_pynode(self, val):
        """
        Convert a string to a registered MockedPymelNode instance.

        :param str val: A node name or dagpath.
        :return: A MockedPymelNode
        :rtype: MockedPymelNode
        """
        assert(isinstance(val, basestring))
        node = self.session.get_node_by_match(val)
        if not node:
            return None
        return self._node_to_pynode(node)

    def _node_to_pynode(self, node):
        """
        Get a MockedPymelNode from an MockedNode instance.
        :param MockedNode node: A mocked node
        :return: A registered MockedPymelNode instance.
        :rtype: MockedPymelNode
        :raise KeyError: If the provided MockedNode is not registered.
        """
        return self.__registry[node]

    def _to_mel(self, data):
        """
        Convert a MockedPymelNode to a fully qualified dagpath.

        :param MockedPymelNode data: A PyNode-like object.
        :return: A fully qualified dagpath.
        :rtype: str
        """
        try:
            return data.__melobject__()
        except AttributeError:
            return data

    def ls(self, *args, **kwargs):
        nodes = super(MockedPymelSession, self).ls(*args, **kwargs)
        return [self._str_to_pynode(node) for node in nodes]

    def objExists(self, args):
        names = [str(arg) for arg in args]
        return self.session.exists(names)

    def createNode(self, *args, **kwargs):
        node = super(MockedPymelSession, self).createNode(*args, **kwargs)
        return self._str_to_pynode(node)

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
