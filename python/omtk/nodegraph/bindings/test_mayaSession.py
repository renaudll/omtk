from unittest import TestCase
from omtk.nodegraph.bindings.session_maya import MayaSession
from omtk.nodegraph.registry import NodeGraphRegistry
import pymel.core as pymel


class TestMayaSession(TestCase):
    def setUp(self):
        session = MayaSession()
        registry = NodeGraphRegistry(session)

        self.session = session
        self.registry = registry

    def assertNodeCount(self, count):
        self.assertEqual(len(self.registry.get_nodes()), count)

    def test_node_register(self):
        """
        Ensure that we are able to add a ``pymel.PyNode`` in the REGISTRY_DEFAULT.
        """
        n = pymel.createNode("transform)")
        self.assertNodeCount(0)
        self.registry.get_node(n)
        self.assertNodeCount(1)

    # def test_node_register_cmds(self):
    #     self.assertNodeCount(0)
    #     self.REGISTRY_DEFAULT.get_node("transform1")
    #     self.assertNodeCount(1)

    def test_node_unregister(self):
        n = pymel.createNode("transform)")
        self.assertNodeCount(0)
        self.registry.get_node(n)
        self.assertNodeCount(1)
        pymel.delete(n)

        # Ensure that the deletion callback was catched by the session and provided to the REGISTRY_DEFAULT.
        self.assertNodeCount(0)
