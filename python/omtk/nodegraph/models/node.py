from omtk import decorators
from omtk.nodegraph.signal import Signal


class NodeModel(object):
    """Define the data model for a Node which can be used by multiple view."""

    # Signal emitted when the node is unexpectedly deleted.
    onDeleted = Signal(object)

    # Signal emitted when the node is renamed.
    onRenamed = Signal(object)

    # Signal emitted when an attribute is unexpectedly added.
    onPortAdded = Signal(object)

    # Signal emitted when an attribute is unexpectedly removed.
    onPortRemoved = Signal(str)

    def __init__(self, registry, impl):
        """
        NodeGraphNodeAdaptor
        :param registry:
        :param impl:
        """
        super(NodeModel, self).__init__()  # initialize QObject

        self._impl = impl
        self._name = self.impl.get_name()
        self._pos = None
        self._registry = registry
        self._child_nodes = set()
        self._cache_ports = set()

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self._name)

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    @property
    def impl(self):
        """
        :rtype: omtk.nodegraph.adaptors.NodeGraphNodeAdaptor
        """
        return self._impl

    def dump(self):
        """
        Convert a node to a JSON compatible data structure.
        Used for testing.
        :return: A JSON compatible data structure in the following form:
        {
            'node_name_1': ['port1_name', 'port2_name', ...],
            'node_name_2': ['port1_name', 'port2_name', ...],
            ...
        }
        :rtype: dict
        """
        ports = [str(port.get_name()) for port in self.iter_ports()]
        return {
            'ports': ports,
        }

    def get_name(self):
        return self._name

    def rename(self, new_name):
        self._name = new_name
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    @decorators.memoized_instancemethod
    def get_metadata(self):
        return None

    def get_type(self):
        """
        Get the node type as a string
        :rtype: str
        """
        return self.impl.get_type()

    def get_nodes(self):
        """
        Used for selection purpose. Return what should be selected if the node is selected.
        :return: A list of objects to select.
        """
        return None

    def get_parent(self):
        # type: () -> NodeModel
        """
        Provide access to the upper node level.
        This allow compound nesting.
        :return: A NodeModel instance.
        """
        return None

    def get_children(self):
        # type: () -> List[NodeModel]
        return self._child_nodes

    def get_position(self):
        return self._pos

    def set_position(self, pos):
        self._pos = pos

    def get_ports_metadata(self):
        # Used to invalidate cache
        return set()

    def _register_port(self, port):
        self._cache_ports.add(port)

    def _unregister_port(self, port):
        self._cache_ports.discard(port)

    def iter_ports(self):
        """
        Iterate through all the node ports.
        :return: A port generator
        :rtype: Generator[omtk.nodegraph.PortModel]
        """
        i = self.get_ports()
        for port in i:
            yield port

    def get_ports(self):
        """
        Query all the node ports.
        :return: The node ports.
        :rtype: List[PortModel]
        """
        if not self._cache_ports:
            for port in self.scan_ports():
                self._register_port(port)
        return self._cache_ports

    def get_port_by_name(self, name):
        """
        Find a port with a specific name.
        :param name: The port name we are searching for.
        :return: A port or None if nothing is found.
        :rtype omtk.nodegraph.PortModel or None
        """
        for port in self.iter_ports():
            if port.get_name() == name:
                return port

    def scan_ports(self):
        # type: () -> Generator[PortModel]
        return
        yield

    @decorators.memoized_instancemethod
    def get_input_ports(self):
        # type: () -> list[PortModel]
        return [attr for attr in self.get_ports() if attr.is_writable()]

    @decorators.memoized_instancemethod
    def get_connected_input_ports(self):
        # type: () -> list[PortModel]
        return [attr for attr in self.get_input_ports() if attr.get_input_connections()]

    @decorators.memoized_instancemethod
    def get_output_ports(self):
        # type: () -> list[PortModel]
        return [attr for attr in self.get_ports() if attr.is_readable()]

    @decorators.memoized_instancemethod
    def get_input_connections(self):
        # type: () -> list(PortModel)
        result = []
        for attr in self.get_input_ports():
            result.extend(attr.get_input_connections())
        return result

    @decorators.memoized_instancemethod
    def get_output_connections(self):
        result = []
        for attr in self.get_output_ports():
            result.extend(attr.get_output_connections())
        return result

    @decorators.memoized_instancemethod
    def get_connected_output_ports(self):
        return [attr for attr in self.get_output_ports() if attr.get_output_connections()]

    # --- View related methods

    def _get_widget_label(self):
        """
        Return the name that should be displayed in the Widget label.
        """
        return self._name

    def _get_widget_cls(self):
        """
        Return the desired Widget class.
        """
        from omtk.nodegraph.widgets.node import OmtkNodeGraphNodeWidget
        return OmtkNodeGraphNodeWidget

    def get_widget(self, graph, ctrl):
        """

        :param PyFlowgraphView graph:
        :param NodeGraphController ctrl:
        :return:
        :rtype: OmtkNodeGraphNodeWidget
        """
        node_name = self._get_widget_label()
        cls = self._get_widget_cls()
        inst = cls(graph, node_name, self, ctrl)
        return inst

    def on_added_to_scene(self):
        """
        Called when the node is added to a view (scene).
        """
        pass

    def on_removed_from_scene(self):
        """
        Called when the node is removed from the view (scene).
        """
        pass
