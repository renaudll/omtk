import pytest

from tests.helpers import assertGraphConnectionCountEqual
from tests.helpers import assertGraphNodeCountEqual
from tests.helpers import getGraphPortCount


@pytest.fixture
def node1(cmds):
    return cmds.createNode('transform', name='a')


@pytest.fixture
def node2(cmds):
    return cmds.createNode('transform', name='b')


def test_delete_existing_node(cmds, registry, model, node1, node2):
    """Ensure that when a node is deleted in Maya and visible in the graph, it is deleted from the graph."""
    # Add the node to the graph
    n1 = registry.get_node(node1)
    model.add_node(n1)

    assertGraphNodeCountEqual(model, 1)

    # Delete the node from the graph
    cmds.delete(node1)
    assertGraphNodeCountEqual(model, 0)


def test_delete_port(cmds, registry, model, node1):
    """Ensure that when a port is deleted in Maya and visible in the graph, it is deleted from the graph."""
    cmds.createNode('transform', name='a')
    node = registry.get_node('a')
    model.add_node(node)

    # Create attribute, ensure it is added to the graph
    # since the node is visible, this will add the port
    cmds.addAttr(node1, longName="test")
    port = registry.get_port('a.test')
    model.add_port(port)
    assert getGraphPortCount(model) == 1

    # Remove attribute from session, ensure it is removed from the graph
    cmds.deleteAttr('a.test')
    assert getGraphPortCount(model) == 0


def test_delete_connection(cmds, registry, model):
    """Ensure that when a connection is deleted in Maya and visible in the graph, it is deleted from the graph."""
    cmds.createNode('transform', name='a')
    cmds.addAttr('a', longName='testSrc')
    cmds.addAttr('a', longName='testDst')
    cmds.connectAttr('a.testSrc', 'a.testDst')

    node = registry.get_node('a')
    port_src = registry.get_port('a.testSrc')
    port_dst = registry.get_port('a.testDst')
    connection = registry.get_connection(port_src, port_dst)

    model.add_node(node)
    model.add_connection(connection)
    assertGraphConnectionCountEqual(model, 1)

    cmds.disconnectAttr('a.testSrc', 'a.testDst')
    assertGraphConnectionCountEqual(model, 0)
