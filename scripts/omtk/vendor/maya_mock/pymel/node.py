"""
Mock for pymel.core.PyNode
"""


class MockedPymelNode(object):
    """
    A pymel.core.PyNode mock.

    https://help.autodesk.com/cloudhelp/2018/CHS/Maya-Tech-Docs/PyMel/generated/classes/pymel.core.general/pymel.core.general.PyNode.html#pymel.core.general.PyNode
    """

    def __init__(self, pymel, node):
        """
        :param maya_mock.MockedPymelSession pymel: A mocked pymel session
        :param maya_mock.MockedNode node: A mocked node
        """
        self.__pymel = pymel
        self.__session = pymel.session
        self._node = node
        self.selected = False

    def __str__(self):
        return self.__melobject__()

    def __repr__(self):
        # We use the `u` prefix as we don't know yet
        # what this will be in a python-3 based maya.
        return "nt.%s(u%r)" % (self._node.type.title(), str(self._node.name))

    def __getattr__(self, item):
        """
        Reproduce pymel.PyNode.__getattr__ behavior which is to resolve a port by it's name.

        :param str item: The attribute name.
        :return: A mocked pymel.Attribute
        :rtype: maya_mock.MockedPymelPort
        :raise: AttributeError: If no port if found matching the name.
        """
        session = self.__session
        pymel = self.__pymel

        port = session.get_node_port_by_name(self._node, item)
        if port:
            mock = pymel.port_to_attribute(port)
            return mock

        raise AttributeError("{} has no attribute or method named '{}'".format(self, item))

    def __melobject__(self):
        return self._node.__melobject__()

    def attr(self, name):
        """
        Get an attribute from it's name.

        :param str name: An attribute name
        :return: A mocked pymel attribute
        :rtype: maya_mock.MockedPymelPort
        """
        session = self.__session
        pymel = self.__pymel

        port = session.get_node_port_by_name(self._node, name)
        return pymel.port_to_attribute(port)

    def getAttr(self, name):  # pylint: disable=invalid-name
        """
        Query the value of an attribute.

        :param str name: The dagpath of an attribute.
        :return: The value of the attribute.
        :rtype: bool
        """
        session = self.__session
        port = session.get_node_port_by_name(self._node, name)
        return port.value

    def hasAttr(self, name, checkShape=True):  # pylint: disable=invalid-name
        """
        Convenience function for determining if an object has an attribute.
        If checkShape is enabled, the shape node of a transform will
        also be checked for the attribute.

        :param str name: The name of the attribute to check.
        :param bool checkShape: Should we check if the shape of the node is a transform?
        :return: True if the object has the provided attribute. False otherwise.
        :rtype: bool
        """
        session = self.__session

        # If the node is a tranform and checkShape is True, also check it's shape.
        if self._node.type == "transform" and checkShape:
            for shape in self.getShapes():
                if session.get_node_port_by_name(shape, name):
                    return True

        return session.get_node_port_by_name(self._node, name) is not None

    def name(self):
        """
        :return: The name of the node.
        :rtype: str
        """
        return self._node.name

    def nodeName(self):  # pylint: disable=invalid-name
        """
        :return: Just the name of the node, without any dag path.
        :rtype: str
        """
        return self._node.name

    def fullPath(self):  # pylint: disable=invalid-name
        """
        :return: The full dag path to the object, including leading pipe (|).
        :rtype: str
        """
        return self._node.dagpath

    def getParent(self, generation=1):  # pylint: disable=invalid-name
        """
        Return the parent of this node.

        :param int generation: Gives the number of levels up that you wish to go for the parent.
        :return: The parent node or None if node have no parent.
        :rtype: MockedPymelNode or None
        """
        pymel = self.__pymel
        node = self._node
        for _ in range(generation):
            node = node.parent

        return pymel.node_to_pynode(node) if node else None

    def setParent(self, *args, **kwargs):  # pylint: disable=invalid-name
        """
        Reparent the current node.

        :param tuple args: Any positional argument are sent to `cmds.setParent`.
        :param dict kwargs: Any keyword arguments are sent to `cmds.setParent`.
        """
        pymel = self.__pymel
        pymel.parent(self, *args, **kwargs)

    def getChildren(self):  # pylint: disable=invalid-name
        """
        Query the children of this node.

        :return: A list of nodes
        :rtype: list(MockedPymelNode)
        """
        session = self.__session
        pymel = self.__pymel
        parent = self._node
        # TODO: Does ordering matter?
        return [pymel.node_to_pynode(node) for node in session.nodes if node.parent is parent]

    def getShapes(self):  # pylint: disable=invalid-name
        """
        Query the shapes of this node.
        This only work on transform node.

        :return: A list of nodes.
        :rtype: list(MockedPymelNode)
        """
        session = self.__session
        pymel = self.__pymel
        parent = self._node
        nodes = [
            node for node in session.nodes if node.parent is parent and session and node.is_shape()
        ]
        return [pymel.node_to_pynode(node) for node in nodes]
