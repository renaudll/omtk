class MockedConnection(object):
    """
    Pymel.Attribute mock.
    """

    def __init__(self, port_src, port_dst):
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
        """
        return self._port_src

    @property
    def dst(self):
        """
        :return: The connection destination port.
        """
        return self._port_dst
