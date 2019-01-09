"""
Ensure proper behaviour or the GraphController, GraphRegistry and every related models.
"""
import pytest

from maya_mock.decorators import mock_pymel
from omtk.nodegraph import NodeGraphFilter
from omtk_test import assertGraphNodeNamesEqual


@pytest.fixture
def session(session):
    print 'fixture session'
    """Preconfigured session that contain the default maya cameras and a transform."""
    # TODO: Push maya_mock further to diminish the amount of boilerplate
    front = session.create_node('transform', name='front')
    persp = session.create_node('transform', name='persp')
    top = session.create_node('transform', name='top')
    side = session.create_node('transform', name='side')

    # Create shapes
    frontShape = session.create_node('camera', name='frontShape')
    perspShape = session.create_node('camera', name='perspShape')
    topShape = session.create_node('camera', name='topShape')
    sideShape = session.create_node('camera', name='sideShape')

    frontShape.set_parent(front)
    perspShape.set_parent(persp)
    topShape.set_parent(top)
    sideShape.set_parent(side)

    return session


@pytest.fixture
def filter_():
    return CameraFilter()


class CameraFilter(NodeGraphFilter):
    """
    Show only camera shapes.
    """

    def intercept_node(self, node):
        node_type = node.get_type()
        if node_type != 'camera':
            return

        yield node


def test_can_show_node(registry, session, model, pymel):
    """Test a simple NodeGraphFilter that only let camera goes through."""
    registry.scan_session()
    model.add_all()

    for pynode in pymel.ls():
        node = registry.get_node(pynode)
        model.add_node(node)

    expected = [
        u'frontShape',
        u'perspShape',
        u'sideShape',
        u'topShape',
    ]
    assertGraphNodeNamesEqual(model, expected)
