import pytest

from omtk_test import assertGraphConnectionCountEqual
from omtk_test import assertGraphNodeCountEqual
from omtk_test import assertGraphPortCountEqual
from omtk_test import getGraphPortCount


@pytest.fixture
def node1(session):
    return session.create_node('transform', name='a')


@pytest.fixture
def node2(session):
    return session.create_node('transform', name='b')


@pytest.fixture
def session(session, node1, node2):
    return session


def test_delete_existing_node(session, registry, model, node1, node2):
    """Ensure that when a node is deleted in Maya and visible in the graph, it is deleted from the graph."""
    # Add the node to the graph
    n1 = registry.get_node(node1)
    model.add_node(n1)

    assertGraphNodeCountEqual(model, 1)

    # Delete the node from the graph
    session.remove_node(node1)
    assertGraphNodeCountEqual(model, 0)


def test_delete_port(session, registry, model, pymel, node1):
    """Ensure that when a port is deleted in Maya and visible in the graph, it is deleted from the graph."""
    n1 = registry.get_node(node1)
    model.add_node(n1)

    # Validate the graph is empty
    assertGraphNodeCountEqual(model, 2)

    # Create attribute, ensure it is added to the graph
    # since the node is visible, this will add the port
    port_1 = session.create_port(node1, "test")
    assert getGraphPortCount(model) == 1

    # Remove attribute from session, ensure it is removed from the graph
    session.remove_port(port_1)
    pymel.deleteAttr(node1, attribute="test")
    assert getGraphPortCount(model) == 0


def test_delete_connection(session, registry, model, node1, node2, pymel):
    """Ensure that when a connection is deleted in Maya and visible in the graph, it is deleted from the graph."""
    model.add_node(node1)
    model.add_node(node2)

    # Validate the graph is empty
    assertGraphNodeCountEqual(model, 2)

    pymel.connectAttr(node1.t, node2.t)
    port_src = registry.get_port(node1.t)
    port_dst = registry.get_port(node2.t)
    connection = registry.get_connection(port_src, port_dst)

    model.add_connection(connection)
    assertGraphConnectionCountEqual(model, 1)

    pymel.disconnectAttr(node1.t, node2.t)
    assertGraphConnectionCountEqual(model, 0)
