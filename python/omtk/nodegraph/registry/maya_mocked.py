from omtk.nodegraph.registry.base import NodeGraphRegistry
from omtk.nodegraph import NodeModel, PortModel
from omtk.vendor.mock_maya.base import MockedNode
from omtk.vendor.mock_maya.base import MockedPort
from omtk.vendor.mock_maya.base import MockedSession


class MockedMayaRegistry(NodeGraphRegistry):
    """
    A MayaSession mock class to use in unittests.
    """
    def __init__(self, session=None):
        # A MockedRegistry need a MockedSession
        if session is None:
            session = MockedSession()

        super(MockedMayaRegistry, self).__init__(session=session)

        self.__nodes = set()
        self.__ports = set()
        self.__connections = set()

    @property
    def session(self):
        """
        :rtype: MockedSession
        """
        return self._session

    def set_session(self, session):
        """
        Set the DCC session associated with the registry.
        Any events in the session will be fowarded to the registry.

        :param MockedSession session: The new session associated with the registry.
        """
        assert(session is None or isinstance(session, MockedSession))
        old_session = self._session
        if old_session:
            self._disconnect_session(old_session)
            # old_session.remove_callbacks()
            # self._session.set_registry(None)

        self._session = session

        # session.set_registry(self)
        self._connect_session(session)
        # session.add_callbacks()

    def _connect_session(self, session):
        """
        :param MockedSession session:
        """
        session.nodeAdded.connect(self.__callback_node_added)
        session.nodeRemoved.connect(self.__callback_node_removed)
        session.portAdded.connect(self.__callback_port_added)
        session.portRemoved.connect(self.__callback_port_removed)

    def _disconnect_session(self, session):
        """
        :param MockedSession session:
        """
        session.nodeAdded.disconnect(self.__callback_node_added)
        session.nodeRemoved.disconnect(self.__callback_node_removed)
        session.portAdded.disconnect(self.__callback_port_added)
        session.portRemoved.disconnect(self.__callback_port_removed)

    def __callback_node_added(self, node):
        """
        Callback when a node is added to the scene.
        :param MockedNode node: The added node.
        """
        model = self.get_node(node)
        self._register_node(model)
        self.onNodeAdded.emit(model)

    def __callback_node_removed(self, node):
        """
        Called when a node is removed from the scene.

        :param MockedNode node: The removed node.
        """
        model = self.get_node(node)
        self.onNodeDeleted.emit(model)
        self._invalidate_node(model)

    def __callback_port_added(self, port):
        """
        Called when a port is added to the scene.

        :param MockedPort port: The added port.
        """
        model = self.get_port(port)
        self._register_attribute(model)
        self.__ports.add(port)
        self.onPortAdded.emit(model)

    def __callback_port_removed(self, port):
        """
        Called when a port is removed from the scene.

        :param MockedPort port: The removed port.
        """
        model = self.get_port(port)
        self.onPortRemoved.emit(model)
        # self._invalidate_port(port)

    # --- Parent class implementation ---

    def _get_node(self, val):
        """
        :param MockedNode val:
        :return: A graph node model
        :rtype: NodeModel
        """
        assert(isinstance(val, MockedNode))
        return NodeModel(self, val.name)

    def _get_port(self, val):
        """
        :param MockedPort val:
        :return: A graph port model
        :rtype: PortModel
        """
        assert(isinstance(val, MockedPort))
        node = val.node
        node_model = self.get_node(node)
        return PortModel(self, node_model, val.name)

    def _get_parent_impl(self, node):
        """
        :param MockedNode node: The node to query.
        :return: The parent node or None if there's no parent.
        :rtype: MockedNode or None
        """
        return node.parent

    def _get_children_impl(self, node):
        """
        :return: The parent node or None if there's no parent.
        :rtype: MockedNode or None
        """
        return node.children

    def _set_parent_impl(self, node, parent):
        """
        :param MockedNode child: The node to parent
        :param MockedNode parent: The parent
        """
        node.set_parent(parent)

    # --- Helper methods ---

    def create_node(self, nodetype, name, emit=True):
        """
        Create a mocked node.

        :param str nodetype: The node type (ex: "transform")
        :param str dagpath: The node dagpath (ex: "|parent|child")
        """
        node = self.session.create_node(nodetype, name)
        model = self.get_node(node)
        return model


