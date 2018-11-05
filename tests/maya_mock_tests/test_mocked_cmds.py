import unittest
from omtk_test.mock_maya.base.session import MockedSession
from omtk_test.mock_maya.cmds.session import MockedCmdsSession


class MockedCmdsTestCase(unittest.TestCase):
    def setUp(self):
        self._session = MockedSession()
        self.mock = MockedCmdsSession(self._session)

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
        self.mock.createNode("transform")
        self._ls(["transform1"])

    def test_createNode_multi(self):
        """
        Validate result when calling createNode multiple times without any name.
        """
        self.mock.createNode("transform")
        self.mock.createNode("transform")
        self._ls(["transform1", "transform2"])

    def test_createNode_name(self):
        """
        Validate result when calling createNode and specifying a name that don't exist.
        """
        self.mock.createNode("transform", name="foo")
        self._ls(["foo"])

    def test_createNode_name_multi(self):
        """
        Validate result when calling createNode and specifying a name that exist.
        """
        self.mock.createNode("transform", name="foo")
        self.mock.createNode("transform", name="foo")
        self.mock.createNode("transform", name="foo")
        self._ls(['foo', 'foo1', 'foo2'])

    def assertSelection(self, expected):
        actual = self.mock.ls(selection=True)
        self.assertEqual(expected, actual)

    def test_selection(self):
        """
        Validate that we can access the selection.
        """
        # Assert Nothing is selected
        self.assertSelection([])

        # Create a node
        self.mock.createNode("transform", name="foo")

        # Assert the node is selected
        self.assertSelection(['foo'])

        # Clear selection
        self.mock.select([])
        self.assertSelection([])

        # Select the node
        self.mock.select(['foo'])

        # Assert the node is selected
        self.assertSelection(['foo'])
