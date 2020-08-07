"""
Mocked for the pymel package.
"""
import six

from .node import MockedPymelNode
from .port import MockedPymelPort
from ..cmds.session import MockedCmdsSession


class MockedPymelSession(MockedCmdsSession):
    """
    Mock for the maya.cmds python module

    :param maya_mock.MockedSession session: The mocked session for this adaptor.
    """

    def __init__(self, session):
        super(MockedPymelSession, self).__init__(session)

        self.session.onNodeAdded.connect(self.__callback_node_added)
        self.session.onNodeRemoved.connect(self.__callback_node_removed)
        self.session.onPortAdded.connect(self.__callback_port_added)
        self.session.onPortRemoved.connect(self.__callback_port_removed)

        self._registry = {}

        # pymel.core.PyNode
        self.PyNode = MockedPymelNode  # pylint: disable=invalid-name

        # pymel.core.Attribute
        self.Attribute = MockedPymelPort  # pylint: disable=invalid-name

        # Register all existing node
        for node in session.nodes:
            self.__callback_node_added(node)

        # Register all existing port
        for port in session.ports:
            self.__callback_port_added(port)

    def __callback_node_added(self, node):
        """
        Called when a node is added in the scene.
        :param MockedNode node: The node added
        """
        mock = MockedPymelNode(self, node)
        self._registry[node] = mock

    def __callback_node_removed(self, node):
        """
        Called when a node is removed from the scene.
        :param MockedNode node: The node being removed.
        """
        self._registry.pop(node, None)

    def __callback_port_added(self, port):
        mock = MockedPymelPort(self.session, port)
        self._registry[port] = mock

    def __callback_port_removed(self, port):
        self._registry.pop(port, None)

    def _str_to_pynode(self, val):
        """
        Convert a string to a registered MockedPymelNode instance.

        :param str val: A node name or dagpath.
        :return: A MockedPymelNode
        :rtype: MockedPymelNode
        """
        assert isinstance(val, six.string_types)
        node = self.session.get_node_by_match(val)
        if not node:
            return None
        return self.node_to_pynode(node)

    def node_to_pynode(self, node):
        """
        Get a MockedPymelNode from an MockedNode instance.

        :param MockedNode node: A mocked node
        :return: A registered MockedPymelNode instance.
        :rtype: MockedPymelNode
        :raise KeyError: If the provided MockedNode is not registered.
        """
        # TODO: Make private
        return self._registry[node]

    def port_to_attribute(self, port):
        """
        Get a MockedPymelPort from a MockedPort instance.
        :param port:
        :return:
        """
        # TODO: Make private
        return self._registry[port]

    def ls(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """
        :param tuple args: Positional arguments are passed to the session
        :param dict kwargs: Keyword arguments are passed to the session
        :return: A list of mocked pynode
        :rtype: list[maya_mock.MockedPymelNode]
        """
        nodes = super(MockedPymelSession, self).ls(*args, **kwargs)
        return [self._str_to_pynode(node) for node in nodes]

    def createNode(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """
        :param args: Positional arguments are fowarded to the parent implementation
        :param kwargs: Keyword arguments are fowarded to the parent implementation
        :return: A mocked pynode
        :rtype: MockedPymelNode
        """
        node = super(MockedPymelSession, self).createNode(*args, **kwargs)
        return self._str_to_pynode(node)

    def listAttr(self, objects, **kwargs):  # pylint: disable=arguments-differ
        """
        :param tuple[str] objects: Objects to list attributes from
        :return: A list of attribute names
        :rtype: list[str]
        """
        attrs = super(MockedPymelSession, self).listAttr(objects, **kwargs)
        return [MockedPymelPort(self, attr) for attr in attrs]

    def addAttr(self, *objects, **kwargs):  # pylint: disable=arguments-differ
        objects = [_to_mel(object_) for object_ in objects]
        super(MockedPymelSession, self).addAttr(*objects, **kwargs)

    def select(self, names, **kwargs):  # pylint: disable=arguments-differ
        super(MockedPymelSession, self).select(names, **kwargs)
        return self.ls(selection=True)  # TODO: Validate cmds really don't return anything

    def parent(self, *objects, **kwargs):  # pylint: disable=arguments-differ
        names = [_to_mel(object_) for object_ in objects]
        super(MockedPymelSession, self).parent(*names, **kwargs)

    def connectAttr(self, src, dst, **kwargs):  # pylint: disable=arguments-differ
        src = _to_mel(src)
        dst = _to_mel(dst)
        super(MockedPymelSession, self).connectAttr(src, dst, **kwargs)

    def disconnectAttr(self, src, dst, **kwargs):  # pylint: disable=arguments-differ
        src = _to_mel(src)
        dst = _to_mel(dst)
        super(MockedPymelSession, self).disconnectAttr(src, dst, **kwargs)


def _to_mel(data):
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
