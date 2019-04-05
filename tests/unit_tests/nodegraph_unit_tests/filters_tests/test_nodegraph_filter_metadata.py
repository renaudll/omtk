"""
Test a preconfigured filter that hide message type ports.
"""
import pytest

from omtk.nodegraph.filters.filter_metadata import NodeGraphMetadataFilter
from tests.helpers import assertGraphConnectionCountEqual
from tests.helpers import assertGraphIsEmpty


@pytest.fixture
def filter_():
    return NodeGraphMetadataFilter()


def test_hiding_network_node(session, registry, model, pymel):
    """Ensure that adding a network node to the graph don't add anything."""
    session.create_node('network')
    registry.scan_session()
    model.add_all()

    assertGraphIsEmpty(model)


def test_hiding_message_port(cmds, registry, model):
    """Ensure that adding a connection from a network node to the graph don't add anything."""
    node_src = cmds.createNode('transform', name='a')
    node_dst = cmds.createNode('transform', name='b')
    port_src = cmds.addAttr(node_src, ln='testSrc', at='message')
    port_dst = cmds.addAttr(node_dst, ln='testDst', at='message')
    cmds.connectAttr('a.testSrc', 'a.testDst')

    registry.scan_session()
    model.add_all()

    assertGraphConnectionCountEqual(model, 0)
