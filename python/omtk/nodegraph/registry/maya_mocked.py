from omtk.nodegraph.registry.base import NodeGraphRegistry
from omtk.nodegraph import NodeModel, PortModel
from omtk.vendor.mock_maya.base import MockedNode
from omtk.vendor.mock_maya.base import MockedPort
from omtk.vendor.mock_maya.base import MockedSession
from omtk.vendor.mock_maya.pymel import MockedPymelNode
from omtk.vendor.mock_maya.pymel import MockedPymelPort
from omtk.nodegraph.adaptors.node.mocked import NodeGraphMockedNodeAdaptor
from omtk.nodegraph.adaptors.port.mocked import NodeGraphMockedPortImpl


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
        Set the DCC session associated with the REGISTRY_DEFAULT.
        Any events in the session will be forwarded to the REGISTRY_DEFAULT.

        :param MockedSession session: The new session associated with the REGISTRY_DEFAULT.
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
        session.connectionAdded.connect(self.__callback_connection_added)
        session.connectionRemoved.connect(self.__callback_connection_removed)

    def _disconnect_session(self, session):
        """
        :param MockedSession session:
        """
        session.nodeAdded.disconnect(self.__callback_node_added)
        session.nodeRemoved.disconnect(self.__callback_node_removed)
        session.portAdded.disconnect(self.__callback_port_added)
        session.portRemoved.disconnect(self.__callback_port_removed)
        session.connectionAdded.connect(self.__callback_connection_added)
        session.connectionRemoved.connect(self.__callback_connection_removed)

    def __callback_node_added(self, node):
        """
        Callback when a node is added to the scene.
        :param MockedNode node: The added node.
        """
        model = self.get_node(node)  # this will register the node
        # self._register_node(model)
        self.onNodeAdded.emit(model)

    def __callback_node_removed(self, node):
        """
        Called when a node is removed from the scene.

        :param MockedNode node: The removed node.
        """
        model = self.get_node(node)
        self.onNodeDeleted.emit(model)
        self._unregister_node(model)

    def __callback_port_added(self, port):
        """
        Called when a port is added to the scene.

        :param MockedPort port: The added port.
        """
        model = self.get_port(port)  # this will register the port
        # self._register_port(model)
        self.__ports.add(port)
        self.onPortAdded.emit(model)

    def __callback_port_removed(self, port):
        """
        Called when a port is removed from the scene.

        :param MockedPort port: The removed port.
        """
        model = self.get_port(port)
        self.onPortRemoved.emit(model)
        self._unregister_port(model)

    def __callback_connection_added(self, connection):
        """
        Called when a connection is added to the scene.

        :param MockedConnection connection: The added connection
        """
        port_src = self.get_port(connection.src)  # cast MockedPort -> PortModel
        port_dst = self.get_port(connection.dst)  # cast MockedPort -> PortModel
        model = self.get_connection(port_src, port_dst)  # this will register the connection
        self.onConnectionAdded.emit(model)

    def __callback_connection_removed(self, connection):
        """
        Called when a connection is removed from the scene.

        :param MockedConnection connection: The removed connection
        """
        model_port_src = self.get_port(connection.src)
        model_port_dst = self.get_port(connection.dst)
        model = self.get_connection(model_port_src, model_port_dst)
        self.onConnectionRemoved.emit(model)
        self._unregister_connection(model)

    # --- Parent class implementation ---

    def _conform_node_key(self, key):
        # Special case for pymel.PyNode mock
        if isinstance(key, MockedPymelNode):
            return key._node
        return key

    def _get_node(self, val):
        """
        :param MockedNode val:
        :return: A graph node model
        :rtype: NodeModel
        """
        assert isinstance(val, MockedNode)

        impl = NodeGraphMockedNodeAdaptor(val)
        return NodeModel(self, impl)

    def _conform_port_key(self, key):
        # Special case for pymel.Attribute mock
        if isinstance(key, MockedPymelPort):
            return key._node
        return key

    def _get_port(self, val):
        """
        :param MockedPort val:
        :return: A graph port model
        :rtype: PortModel
        """
        assert isinstance(val, MockedPort)
        node = val.node
        node_model = self.get_node(node)
        inst = PortModel(self, node_model, val.name)
        impl = NodeGraphMockedPortImpl(self.session, val)
        inst._impl = impl  # HACK: Clean this
        return inst

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

    def _scan_nodes(self):
        for node in self.nodes:
            self.get_node(node)

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


