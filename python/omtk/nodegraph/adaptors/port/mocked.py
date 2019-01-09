from omtk.nodegraph.adaptors.port.base import NodeGraphPortImpl
from maya_mock import MockedSession, MockedPort


class NodeGraphMockedPortImpl(NodeGraphPortImpl):
    """
    omtk.nodegraph.PortModel interface for maya_mock.MockedPort.
    """
    def __init__(self, session, *args, **kwargs):
        self._session = session
        super(NodeGraphMockedPortImpl, self).__init__(*args, **kwargs)

    @property
    def session(self):
        """
        :rtype: MockedSession
        """
        return self._session

    @property
    def data(self):
        """
        :rtype: MockedPort
        """
        return self._data

    def get_metatype(self):
        return self.data.type

    def is_source(self):
        return self.session.port_is_source(self.data)

    def is_destination(self):
        return self.session.port_is_destination(self.data)

    def get_inputs(self):
        return self.session.get_port_inputs(self.data)

    def get_outputs(self):
        return self.session.get_port_outputs(self.data)

    def is_readable(self):
        return self.data.readable

    def is_writable(self):
        return self.data.writable

    def is_interesting(self):
        return self.data.interesting

    def connect_from(self, val):
        pass

    def connect_to(self, val):
        pass

    def disconnect_from(self, val):
        pass

    def disconnect_to(self):
        pass
