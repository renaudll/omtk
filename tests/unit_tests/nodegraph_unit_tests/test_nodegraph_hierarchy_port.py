import pytest
import unittest

from omtk_test import NodeGraphMockedMayaTestCase
from omtk.nodegraph.models import GraphModel
from maya_mock import MockedCmdsSession


@pytest.fixture
def session(session, cmds):
    """
    Simple session involving a child and a parent node.
    
    :param maya_mock.MockedSession session:
    :rtype: maya_mock.MockedSession session:
    """
    n1 = session.create_node('transform', name='parent')
    n2 = session.create_node('transform', name='child')
    cmds.parent(n1, n2)


@unittest.skip("Disabled for now")
def test_parent_port(self):
    """Assert that """
    # self.session.parent(self.node, self.n2)
    # TODO: This don't work because the hierarchy connection should be added by a GraphProxyModel!
    self.assertGraphConnectionsEqual((
        (u'parent.hierarchy', u'child.hierarchy'),
    ))
