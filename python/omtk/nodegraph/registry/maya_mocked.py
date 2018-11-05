from omtk.nodegraph.registry.base import NodeGraphRegistry
from omtk_test.mock_maya.base.node import MockedNode


class MockedMayaRegistry(NodeGraphRegistry):
    """
    A MayaSession mock class to use in unittests.
    """
    def __init__(self, *args, **kwargs):
        super(MockedMayaRegistry, self).__init__(*args, **kwargs)
        self._nodes = []
        self._ports = []
        self._connections = []

    # --- Parent class implementation ---

    def _get_parent_impl(self, node):
        """
        :param MockedNode node: The node to query.
        :return: The parent node or None if there's no parent.
        :rtype: MockedNode or None
        """
        return node.parent

    def _get_children_impl(self, node):
        """
        :return: The parent node or None if there's no parent.
        :rtype: MockedNode or None
        """
        return node.children

    def _set_parent_impl(self, node, parent):
        """
        :param MockedNode child: The node to parent
        :param MockedNode parent: The parent
        """
        node.set_parent(parent)

    # --- Helper methods ---

    def create_node(self, nodetype, name, emit=True):
        """
        Create a mocked node.

        :param str nodetype: The node type (ex: "transform")
        :param str dagpath: The node dagpath (ex: "|parent|child")
        """
        node = MockedNode(self, nodetype, name)
        self._nodes.append(node)
        self._register_node(node)
        if emit:
            self.onNodeAdded.emit(node)
        return node


