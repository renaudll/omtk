

class MockedPymelNode(object):
    """
    :param MockedNode node:

    :param registry:
    :type.registry: omtk_test.mock_maya.pymel.session.MockedPymelSession
    """
    def __init__(self, registry, node):
        self.__registry = registry
        self.__node = node
        self.selected = False

    def __repr__(self):
        return '<Mocked pymel.PyNode "{0}">'.format(self.__node.dagpath)

    def __melobject__(self):
        return self.__node.__melobject__()

    def name(self):
        return self.__node.name

    def nodeName(self):
        return self.__node.name

    def fullPath(self):
        return self.__node.dagpath

    def getParent(self):
        registry = self.__registry
        parent = self.__node.parent
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
