import logging
import itertools
import string

from omtk.vendor.Qt import QtCore
from omtk.vendor.mock_maya.base import MockedNode
from omtk.vendor.mock_maya.base import MockedPort


log = logging.getLogger(__name__)

# class IBinding(object):
#     """
#     Interface to interact with a DCC scene.
#     """
#     __metaclass__ = abc.ABCMeta
#
#     @abc.abstractmethod
#     def create_node(self, nodetype, name=None):
#         """
#         Create a new node in the scene.
#
#         :param str nodetype: The type of the node.
#         :param str name: The name of the node.
#         :return: The created node
#         :rtype: MockedNode
#         """
#
#         # TODO: cmds.createNode("locator") -> "locatorShape"
#         if name and not self.exists(name):
#             pass
#         else:
#             prefix = name if name else nodetype
#             prefix = prefix.rstrip(string.digits)
#             name = self._unique_name(prefix)
#
#         node = MockedNode(self, nodetype, name)
#         self.nodes.add(node)
#         self.nodeAdded.emit(node)
#         return node
#
#     def create_port(self, node, name):
#         """
#         Create a new port in the scene.
#
#         :param MockedNode node: The port parent node
#         :param name: The name of the port
#         :return: The create port
#         :rtype: MockedPort
#         """
#         port = MockedPort(node, name)
#         self.ports.add(port)
#         self.portAdded.emit(port)
#         return port
#
#     def get_selection(self):
#         return self.selection

from omtk.nodegraph.bindings.base import ISession
from omtk.nodegraph.signal import Signal

class MockedSession(ISession):
    """
    Maya mock that try to match pymel symbols.
    """
    nodeAdded = Signal(MockedNode)
    nodeRemoved = Signal(MockedNode)
    portAdded = Signal(MockedPort)
    portRemoved = Signal(MockedPort)
    connectionAdded = None  # TODO: Implement
    connectionRemoved = None  # TODO: Implement

    def __init__(self):
        super(MockedSession, self).__init__()
        self.nodes = set()
        self.ports = set()
        self.selection = set()

    def exists(self, dagpath):
        return bool(self.get_node_by_match(dagpath, strict=False))

    def _unique_name(self, prefix):
        for i in itertools.count(1):
            name = "{}{}".format(prefix, i)
            if not self.exists(name):
                return name

    def get_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def get_node_by_match(self, pattern, strict=True):
        for node in self.nodes:
            if node._match(pattern):
                return node
        if strict:
            raise ValueError("No object matches name: {}".format(pattern))
        return None

    def create_node(self, nodetype, name=None, emit=True):
        """
        Create a new node in the scene.

        :param str nodetype: The type of the node.
        :param str name: The name of the node.
        :param bool emit: If True, the `portAdded` signal will be emmited.
        :return: The created node
        :rtype: MockedNode
        """
        # TODO: cmds.createNode("locator") -> "locatorShape"
        if name and not self.exists(name):
            pass
        else:
            prefix = name if name else nodetype
            prefix = prefix.rstrip(string.digits)
            name = self._unique_name(prefix)

        node = MockedNode(self, nodetype, name)
        self.nodes.add(node)
        if emit:
            signal = self.nodeAdded
            log.debug("%s emited with %s", signal, node)
            signal.emit(node)
        return node

    def remove_node(self, node, emit=True):
        """
        Remove a node from the graph.
        :param node:
        :param bool emit: If True, the `portAdded` signal will be emmited.
        """
        self.nodes.remove(node)
        if emit:
            self.nodeRemoved.emit(node)

    def create_port(self, node, name, emit=True):
        """
        Create a new port in the scene.

        :param MockedNode node: The port parent node
        :param name: The name of the port
        :return: The create port
        :rtype: MockedPort
        """
        port = MockedPort(node, name)
        self.ports.add(port)
        if emit:
            self.portAdded.emit(port)
        return port

    def remove_port(self, port, emit=True):
        """
        Remove a port from the graph.
        :param port:
        :param emit:
        :return:
        """
        # todo: Asset port type
        self.ports.remove(port)
        if emit:
            self.portRemoved.emit(port)

    def get_selection(self):
        return self.selection
