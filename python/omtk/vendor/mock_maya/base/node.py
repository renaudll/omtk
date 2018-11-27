

class MockedNode(object):
    """
    A mocked Maya node
    """
    def __init__(self, registry, nodetype, name):
        super(MockedNode, self).__init__()
        self._registry = registry
        self.name = name
        self.nodetype = nodetype
        self._parent = None
        self.ports = set()  # internal REGISTRY_DEFAULT of ports associated with the node
        self.children = set()

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __hash__(self):
        return hash(self.dagpath)

    def __repr__(self):
        return '<Mocked Node "{}">'.format(self.dagpath)

    def __melobject__(self):
        """ Return the node name.

        If multiple nodes exists with the same name, the dagpath will be returned instead.
        :param MockedNode node: The node to query
        :return: The node name.
        :rtype: str
        """
        registry = self._registry
        if any(n.name == self.name for n in registry.nodes if n != self):
            return self.dagpath
        return self.name

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
        # HACK: Poor-man pattern matching...
        # TODO: Make more solid
        if not pattern:
            return True
        return pattern in self.dagpath

    @property
    def dagpath(self):
        """
        In Maya, the dagpath is the unique identifier for the resource.
        Return the fully qualified dagpath.
        """
        prefix = self._parent.dagpath if self._parent else "|"
        return "{}{}".format(prefix, self.name)

    @property
    def parent(self):
        return self._parent

    def set_parent(self, parent):
        if self._parent:
            self._parent.children.remove(self)
        if parent:
            parent.children.add(self)
        self._parent = parent

    def get_port_by_name(self, name):
        for port in self.ports:
            if port.name == name:
                return port
        return None
