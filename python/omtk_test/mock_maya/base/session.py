import itertools
import string

from omtk_test.mock_maya.base.node import MockedNode


class MockedSession(object):
    """
    Maya mock that try to match pymel symbols.
    """
    def __init__(self):
        self.nodes = set()
        self.selection = set()

    def exists(self, dagpath):
        return any(node._match(dagpath) for node in self.nodes)

    def _unique_name(self, prefix):
        for i in itertools.count(1):
            name = "{}{}".format(prefix, i)
            if not self.exists(name):
                return name

    def get_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node

    def create_node(self, nodetype, name=None):
        # TODO: cmds.createNode("locator") -> "locatorShape"
        if name and not self.exists(name):
            pass
        else:
            prefix = name if name else nodetype
            prefix = prefix.rstrip(string.digits)
            name = self._unique_name(prefix)
        node = MockedNode(self, nodetype, name)
        self.nodes.add(node)
        return node

    def get_selection(self):
        return self.selection
