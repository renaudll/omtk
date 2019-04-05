from omtk.nodegraph.models import NodeModel, PortModel
from maya_mock import MockedNode, MockedPort, MockedSession, MockedPymelNode, MockedPymelPort
from omtk.nodegraph.adaptors.node.mocked import NodeGraphMockedNodeAdaptor
from omtk.nodegraph.adaptors.node.component import NodeGraphComponentNodeAdaptor
from omtk.nodegraph.adaptors.port.mocked import NodeGraphMockedPortImpl
from omtk.nodegraph.registry.base import NodeGraphRegistry


class MockedMayaRegistry(NodeGraphRegistry):
    """
    A MayaSession mock class to use in unittests.
    """
    def __init__(self, session):
        assert session is not None

        self._session = None
        self.__nodes = set()
        self.__ports = set()
        self.__connections = set()

        self.set_session(session)

        super(MockedMayaRegistry, self).__init__()

    def __del__(self):
        if self.session is not None:
            self._disconnect_session(self._session)

    @property
    def session(self):
        """
        :rtype: MockedSession
        """
        return self._session

    def set_session(self, session):
        """
        Set the session linked to the component_registry.

        :param MockedSession session: The new session associated with the REGISTRY_DEFAULT.
        """
        old_session = self._session
        if old_session is not None:
            self._disconnect_session(old_session)

        self._session = session

        if session is not None:
            self._connect_session(session)

    def _connect_session(self, session):
        """
        Connect all signals from this session to a component_registry object signal.

        :param maya_mock.MockedSession session: The component_registry to connect.
        """
        session.onNodeAdded.connect(self._callback_node_added)
        session.onNodeRemoved.connect(self._callback_node_removed)
        session.onPortAdded.connect(self._callback_port_added)
        session.onPortRemoved.connect(self._callback_port_removed)
        session.onConnectionAdded.connect(self._callback_connection_added)
        session.onConnectionRemoved.connect(self._callback_connection_removed)

    def _disconnect_session(self, session):
        """
        Disconnect all signals from this session to a (previously connected) component_registry object.

        :param maya_mock.MockedSession session: The session to disconnect.
        """
        session.onNodeAdded.disconnect(self._callback_node_added)
        session.onNodeRemoved.disconnect(self._callback_node_removed)
        session.onPortAdded.connect(self._callback_port_added)
        session.onPortRemoved.disconnect(self._callback_port_removed)
        session.onConnectionAdded.disconnect(self._callback_connection_added)
        session.onConnectionRemoved.disconnect(self._callback_connection_removed)

    def __callback_node_added(self, node):
        """
        Callback when a node is added to the scene.
        :param MockedNode node: The added node.
        """
        model = self.get_node(node)  # this SHOULD register the node
        self.onNodeAdded.emit(model)

    def _callback_node_removed(self, node):
        """
        Called when a node is removed from the scene.

        :param MockedNode node: The removed node.
        """
        model = self.get_node(node)
        self.onNodeDeleted.emit(model)
        self._unregister_node(model)

    def _callback_port_added(self, port):
        """
        Called when a port is added to the scene.

        :param MockedPort port: The added port.
        """
        model = self.get_port(port)  # this will register the port
        # self._register_port(model)
        self.__ports.add(port)
        self.onPortAdded.emit(model)

    def _callback_port_removed(self, port):
        """
        Called when a port is removed from the scene.

        :param MockedPort port: The removed port.
        """
        model = self.get_port(port)
        self.onPortRemoved.emit(model)
        self._unregister_port(model)

    def _callback_connection_added(self, connection):
        """
        Called when a connection is added to the scene.

        :param MockedConnection connection: The added connection
        """
        port_src = self.get_port(connection.src)  # cast MockedPort -> PortModel
        port_dst = self.get_port(connection.dst)  # cast MockedPort -> PortModel
        model = self.get_connection(port_src, port_dst)  # this will register the connection
        self.onConnectionAdded.emit(model)

    def _callback_connection_removed(self, connection):
        """
        Called when a connection is removed from the scene.

        :param MockedConnection connection: The removed connection
        """
        assert connection.src
        assert connection.dst

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

        # str -> MockedNode
        if isinstance(key, basestring):
            new_key = self.session.get_node_by_name(key)
            if new_key is None:
                raise Exception("%r does not exist in %s" % (key, self))
            return new_key

        return key

    def _get_node(self, val):
        """
        :param MockedNode val:
        :return: A graph node model
        :rtype: NodeModel
        """
        # TODO: how do we support compound in a mocked and real environment?
        from omtk.component import Component
        assert isinstance(val, (MockedNode, Component))
        if isinstance(val, MockedNode):
            impl = NodeGraphMockedNodeAdaptor(self.session, val)  # HACK
        elif isinstance(val, Component):
            impl = NodeGraphComponentNodeAdaptor(self, val)
        return NodeModel(self, impl)

    def _conform_port_key(self, key):
        # Special case for pymel.Attribute mock
        if isinstance(key, MockedPymelPort):
            return key._node

        # str -> MockedNode
        if isinstance(key, basestring):
            new_key = self.session.get_port_by_match(key)
            if new_key is None:
                raise Exception("%r does not exist in %s" % (key, self))
            return new_key

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
        """Scan a session and register all it's nodes."""
        assert self.session is not None

        for node in self.session.nodes:
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


