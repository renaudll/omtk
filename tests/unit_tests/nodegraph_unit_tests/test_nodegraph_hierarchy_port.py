import unittest

from omtk_test import NodeGraphMockedMayaTestCase
from omtk.nodegraph.models import GraphModel
from omtk.vendor.mock_maya.cmds import MockedCmdsSession


class NodeGraphParentPortTestCase(NodeGraphMockedMayaTestCase):
    _cls_model = GraphModel

    def setUp(self, *args, **kwargs):
        super(NodeGraphParentPortTestCase, self).setUp(*args, **kwargs)

        self.cmds = MockedCmdsSession(session=self.session)

        self.n1 = self.registry.create_node("transform", name="parent")
        self.n2 = self.registry.create_node("transform", name="child")
        self.cmds.parent(self.n1, self.n2)
        self.model.add_node(self.n1)
        self.model.add_node(self.n2)

    @unittest.skip("Disabled for now")
    def test_parent_port(self):
        """
        Validate that when two DagNodes are parented, we add a 'parent' port.
        :return:
        """
        # self.session.parent(self.n1, self.n2)
        # TODO: This don't work because the hierarchy connection should be added by a GraphProxyModel!
        self.assertGraphConnectionsEqual((
            (u'parent.hierarchy', u'child.hierarchy'),
        ))
