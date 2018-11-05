import unittest
from omtk_test.mock_maya.base.session import MockedSession
from omtk_test.mock_maya.pymel.session import MockedPymelSession


class MockedCmdsTestCase(unittest.TestCase):
    def setUp(self):
        self._session = MockedSession()
        self.mock = MockedPymelSession(self._session)

    def _ls(self, expected, *args, **kwargs):
        """
        Run cmds.ls and assert the result.
        :param expected:
        :param args:
        :param kwargs:
        :return:
        """
        self.assertEqual(set(expected), set(self.mock.ls(*args, **kwargs)))

    def test_createNode(self):
        """
        Validate result when calling createNode without any name.
        The resulting name should have the node type as prefix and a number as suffix.
        """
        node = self.mock.createNode("transform")
        self.assertEqual("transform1", node.name())

    def test_pynode_setParent(self):
        """
        Validate that our mocked pymel.PyNode.setParent method work.
        :return:
        """
        parent = self.mock.createNode("transform", name="parent")
        child = self.mock.createNode("transform", name="child")

        child.setParent(parent)
        self.assertEqual(parent, child.getParent())

        child.setParent(world=True)
        self.assertEqual(None, child.getParent())
