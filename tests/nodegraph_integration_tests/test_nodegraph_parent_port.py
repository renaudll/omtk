import pymel.core as pymel
from omtk_test.omtk_test import NodeGraphTestCase


class NodeGraphParentPortTestCase(NodeGraphTestCase):
    def setUp(self, *args, **kwargs):
        super(NodeGraphParentPortTestCase, self).setUp(*args, **kwargs)
        self.n1 = pymel.createNode("transform", name="parent")
        self.n2 = pymel.createNode("transform", name="child")
        self.n2.setParent(self.n1)
        self.m1 = self.registry.get_node(self.n1)
        self.m2 = self.registry.get_node(self.n2)
        self.ctrl.add_nodes(self.m1, self.m2)

    def test_parent_port(self):
        """
        Validate that when two DagNodes are parented, we add a 'parent' port.
        :return:
        """
        self.n2.setParent(self.n1)
        self.assertGraphConnectionsEqual((
            (u'parent.hierarchy', u'child.hierarchy'),
        ))
