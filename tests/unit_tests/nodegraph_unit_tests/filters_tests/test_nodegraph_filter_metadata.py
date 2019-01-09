"""
Test a preconfigured filter that hide message type ports.
"""
import pytest

from omtk.nodegraph.filters.filter_metadata import NodeGraphMetadataFilter
from omtk_test import assertGraphConnectionCountEqual
from omtk_test import assertGraphIsEmpty


@pytest.fixture
def filter_():
    return NodeGraphMetadataFilter()


def test_hiding_network_node(session, registry, model, pymel):
    """Ensure that adding a network node to the graph don't add anything."""
    session.create_node('network')
    registry.scan_session()
    model.add_all()

    assertGraphIsEmpty(model)


def test_hiding_message_port(session, registry, model):
    """Ensure that adding a connection from a network node to the graph don't add anything."""
    node_src = session.create_node('transform')
    node_dst = session.create_node('transform')
    port_src = session.create_port(node_src, 'message')
    port_dst = session.create_port(node_dst, 'message')
    session.create_connection(port_src, port_dst)
    registry.scan_session()
    model.add_all()

    assertGraphConnectionCountEqual(model, 0)
