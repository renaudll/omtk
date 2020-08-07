"""A mocked Maya connection"""


class MockedConnection(object):
    """
    A mocked Maya connection.
    """

    def __init__(self, port_src, port_dst):
        """
        :param maya_mock.MockedPort port_src: The connection source port.
        :param maya_mock.MockedPort port_dst: The connection destination port.
        """
        assert port_src
        assert port_dst

        super(MockedConnection, self).__init__()

        self._port_src = port_src
        self._port_dst = port_dst

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __hash__(self):
        return hash(self.src.dagpath + self.dst.dagpath)

    def __repr__(self):
        return '<Mocked Connection "{}" "{}">'.format(self._port_src, self._port_dst)

    @property
    def src(self):
        """
        :return: This connection source port.
        :rtype: maya_mock.MockedPort
        """
        return self._port_src

    @property
    def dst(self):
        """
        :return: The connection destination port.
        :rtype: maya_mock.MockedPort
        """
        return self._port_dst
