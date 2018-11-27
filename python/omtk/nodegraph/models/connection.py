class ConnectionModel(object):
    """
    Model for a connection.
    A connection is composed of a source port and a destination port.
    """
    def __init__(self, registry, port_src, port_dst):
        """
        :param omtk.nodegraph.NodeGraphRegistry registry: The REGISTRY_DEFAULT holding the connection.
        :param omtk.nodegraph.PortModel port_src: The source port.
        :param omtk.nodegraph.PortModel port_dst: The destination port.
        """
        self._registry = registry
        self._port_src = port_src
        self._port_dst = port_dst

    def __repr__(self):
        return '<Connection {0}.{1} to {2}.{3}>'.format(
            self._port_src.get_parent(),
            self._port_src.get_name(),
            self._port_dst.get_parent(),
            self._port_dst.get_name()
        )

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __hash__(self):
        # Previously we hashed the two ports and combined together with the ^ operator.
        # return hash(self._port_src) ^ hash(self._port_dst)
        # However this clashed, so instead we combine the paths.
        return hash(self._port_src.get_path() + self._port_dst.get_path())

    def dump(self):
        port_src = self.get_source()
        port_dst = self.get_destination()

        return (
            port_src.get_path(),
            port_dst.get_path(),
        )

    def get_source(self):
        """
        Get the port that is the source of the connection.
        :return: The source port
        :rtype: omtk.nodegraph.PortModel
        """
        return self._port_src

    def get_destination(self):
        """
        Get the port that is the destination of the connection.
        :return: The destination port
        :rtype: omtk.nodegraph.PortModel
        """
        return self._port_dst
