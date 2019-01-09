import abc
from omtk.nodegraph import NodeModel, PortModel, ConnectionModel
from omtk.nodegraph.signal import Signal


class ISession(object):
    """
    Interface for a session.
    A session is the link between the REGISTRY_DEFAULT and a DCC application like Maya.
    :param NodeGraphRegistry registry: A REGISTRY_DEFAULT to bind to the session.

    Signals:
    :signal onNodeAdded Called when a node is added in the scene
    :signal onNodeRemoved: Called when a node is removed from the scene
    :signal onPortAdded: Called when a port is added in the scene
    :signal portChanged: Called when a port change somehow. This can be broad.
    :signal onPortRemoved: Called when a port is removed from the scene
    :signal onConnectionAdded: Called when a connection is created in the scene
    :signal onConnectionRemoved: Called when a connection is removed from the scene.
    """
    __metaclass__ = abc.ABCMeta

    nodeAdded = Signal(NodeModel)
    nodeRemoved = Signal(NodeModel)
    portAdded = Signal(object, PortModel)
    portChanged = Signal(PortModel)
    portRemoved = Signal(PortModel)
    connectionAdded = Signal(ConnectionModel)
    connectionRemoved = Signal(ConnectionModel)

    def __init__(self, registry=None):
        super(ISession, self).__init__()  # QObject
        self._registry = None
        if registry:
            self.set_registry(registry)

    @property
    def registry(self):
        """
        Return the REGISTRY_DEFAULT associated with the session.
        :return:
        """
        return self._registry

    def set_registry(self, registry):
        """
        Self the REGISTRY_DEFAULT to notify in case something happen in the session.
        :param NodeGraphRegistry registry: The REGISTRY_DEFAULT subscribing to our events.
        """
        self._registry = registry

    def add_callbacks(self):
        """
        Add callbacks to the DCC so what we are notified of QT events.
        """
        pass

    def remove_callbacks(self):
        pass

    # TODO: Move this to MayaSession
    def add_node_callbacks(self, node):
        pass

    # TODO: Move this to MayaSession
    def remove_node_callbacks(self, node):
        pass
