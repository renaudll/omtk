

class MockedPymelNode(object):
    """
    :param MockedNode node:

    :param REGISTRY_DEFAULT:
    :type.REGISTRY_DEFAULT: omtk_test.mock_maya.pymel.session.MockedPymelSession
    """
    def __init__(self, pymel, node):
        self.__pymel = pymel
        self.__session = pymel.session
        self._node = node
        self.selected = False

    def __repr__(self):
        return '<Mocked pymel.PyNode "{0}">'.format(self._node.dagpath)

    def __getattr__(self, item):
        """
        pymel behavior when __getattr__ is called is to try to resolve a port with the name.
        :param str item: The attribute name.
        :return:
        :raise: AttributeError: If no port if found matching the name.
        """
        session = self.__session
        pymel = self.__pymel

        port = session.get_node_port_by_name(self._node, item)
        if port:
            mock = pymel._port_to_attribute(port)
            return mock

        raise AttributeError("{} has no attribute or method named '{}'".format(self, item))

    def __melobject__(self):
        return self._node.__melobject__()

    def attr(self, name):
        session = self.__session
        pymel = self.__pymel

        port = session.get_node_port_by_name(self._node, name)
        return pymel._port_to_attribute(port)

    def hasAttr(self, name):
        return self.__session.get_node_port_by_name(self._node, name) is not None

    def name(self):
        return self._node.name

    def nodeName(self):
        return self._node.name

    def fullPath(self):
        return self._node.dagpath

    def getParent(self):
        registry = self.__registry
        parent = self._node.parent
        if parent is None:
            return None
        return registry._node_to_pynode(parent)

    def _expand(self, node):
        try:
            return node.__melobject__()
        except AttributeError:
            return node

    def setParent(self, *args, **kwargs):
        registry = self.__registry
        registry.parent(self, *args, **kwargs)

    def getChildren(self):
        raise NotImplementedError
