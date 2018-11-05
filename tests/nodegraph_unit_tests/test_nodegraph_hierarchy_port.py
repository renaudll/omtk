from omtk_test.test_case_maya import NodeGraphUnitTestCase
from omtk.nodegraph.models import GraphModel
from omtk.nodegraph import NodeGraphController


class NodeGraphParentPortTestCase(NodeGraphUnitTestCase):
    def setUp(self, *args, **kwargs):
        super(NodeGraphParentPortTestCase, self).setUp(*args, **kwargs)

        self.registry = self.get_registry()
        self.model = GraphModel(self.registry)
        self.ctrl = NodeGraphController(self.registry, self.model)

        self.n1 = self.registry.create_node("transform", name="parent")
        self.n2 = self.registry.create_node("transform", name="child")
        self.registry.parent(self.n1, self.n2)

    def test_parent_port(self):
        """
        Validate that when two DagNodes are parented, we add a 'parent' port.
        :return:
        """
        self.registry.parent(self.n1, self.n2)
        self.assertGraphConnectionsEqual((
            (u'parent.hierarchy', u'child.hierarchy'),
        ))
