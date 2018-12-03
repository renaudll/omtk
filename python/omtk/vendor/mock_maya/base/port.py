from omtk.constants_maya import EnumAttrTypes


class MockedPort(object):
    """
    Pymel.Attribute mock.
    """

    def __init__(self, node, name, port_type='long', short_name=None, nice_name=None, value=0,
                 readable=True, writable=True, interesting=True):
        """
        Create a Maya port mock.

        :param MockedNode node: The node associated with the port.
        :param name: The name of the port.
        :param port_type: The type of the port. See omtk.contants_maya.EnumAttrTypes
        :param str short_name: The 'short' name of the port. (ex: transform.t)
        :param str nice_name: The 'nice' name of the port. (ex: transform.translateMcTranslate)
        :param object value: The value of the port.
        :param readable: 1
        :param writable:
        :param interesting:
        """
        super(MockedPort, self).__init__()
        self.node = node
        self.name = name
        self.short_name = short_name or name
        self.nice_name = nice_name or name
        self._type = EnumAttrTypes(port_type)
        self.value = value
        self.readable = readable
        self.writable = writable
        self.interesting = interesting

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __hash__(self):
        return hash(self.dagpath)

    def __repr__(self):
        return '<Mocked Port "{}.{}">'.format(self.node.name, self.name)

    @property
    def type(self):
        """
        rtype: EnumAttrTypes
        """
        return self._type

    def _match(self, pattern):
        """
        Check if the node match a certain pattern.
        The pattern can be a fully qualified dagpath or a name.

        - "child"
        - "child*"
        - "|child"

        :param pattern:
        :return:
        """
        if not pattern:
            return True
        return pattern in self.dagpath

    @property
    def dagpath(self):
        """
        Resolve the port dagpath.

        :return: A fully qualified dagpath to the port.
        :rtype: str
        """
        return "{}.{}".format(self.node.dagpath, self.name)
