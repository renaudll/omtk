# TODO: Merge with the newest test
import pytest


@pytest.fixture
def graph(model):  # alias
    """
    :rtype: omtk.nodegraph.GraphModel
    """
    return model


@pytest.fixture
def node(session):
    """
    Simple fixture for a mocked Maya node.
    :rtype: maya_mock.MockedNode
    """
    return session.create_node('transform')


@pytest.fixture
def node_model(session, registry, node):
    """
    Simple fixture for a registered graph node.
    :rtype: omtk.nodegraph.NodeModel
    """
    return registry.get_node(node)


@pytest.fixture
def port(session, node):
    """
    Simple fixture for a port.
    :rtype: maya_mock.MockedPort
    """
    return session.create_port(node, 'foo')


@pytest.fixture
def port_model(session, registry, port):
    """
    Simple fixture for a registered graph port.
    :rtype: omtk.nodegraph.PortModel
    """
    return registry.get_port(port)


@pytest.fixture
def connection(session, node):
    """
    Simple fixture for a connection.
    :rtype: maya_mock.MockedConnection
    """
    port_src = session.create_port(node, 'src')
    port_dst = session.create_port(node, 'dst')
    return session.create_connection(port_src, port_dst)


@pytest.fixture
def connection_model(session, registry, connection):
    """
    Simple fixture for a registered graph connection.
    :rtype: omtk.nodegraph.ConnectionModel
    """
    port_src = connection.src
    port_dst = connection.dst
    port_src_model = registry.get_port(port_src)
    port_dst_model = registry.get_port(port_dst)
    return registry.get_connection(port_src_model, port_dst_model)


def test_get_set_registry(registry, graph):
    """Assert we are able to access the registry from the graph model."""
    assert graph.get_registry() is registry
    graph.set_registry(None)
    assert graph.get_registry() is None
    graph.set_registry(registry)
    assert graph.get_registry() is registry


def test_add_node(session, registry, graph, node_model):
    """Assert that we can add nodes to the graph."""
    graph.add_node(node_model)
    assert graph.get_nodes() == {node_model}


def test_add_redundant_node(session, registry, graph, node_model):
    """Assert that when trying to add a node that is already in the graph, nothing happen."""
    graph.add_node(node_model)
    graph.add_node(node_model)
    assert graph.get_nodes() == {node_model}


def test_add_all_nodes(session, registry, graph, node_model):
    """Assert that `add_all_nodes` add all registered nodes to the graph."""
    graph.add_all_nodes()
    assert graph.get_nodes() == {node_model}


def test_remove_node(session, graph, node_model):
    """Assert that we can remove a node from the graph by calling `remove_node`."""
    graph.add_all_nodes()
    graph.remove_node(node_model)
    assert not graph.get_nodes()


def test_remove_unexisting_node(session, graph, node_model):
    """Assert that when trying to remove a node that is NOT in the graph, nothing happen."""
    graph.remove_node(node_model)
    assert not graph.get_nodes()


def test_add_port(session, registry, graph, port_model):
    """Assert that we can add ports to the graph by calling `add_port`."""
    graph.add_port(port_model)
    assert graph.get_ports() == {port_model}


def test_add_redundant_port(session, registry, graph, port_model):
    """Assert that when trying to add a port that is already in the graph, nothing happen."""
    graph.add_port(port_model)
    graph.add_port(port_model)
    assert graph.get_ports() == {port_model}


def test_remove_port(session, registry, graph, port_model):
    """Assert that we can remove a port from the graph by calling `remove_port`."""
    graph.add_port(port_model)
    graph.remove_port(port_model)
    assert not graph.get_ports()


def test_remove_unexistant_port(graph, port_model):
    """Assert that when trying to remove a port that is NOT in the graph, nothing happen."""
    graph.remove_port(port_model)
    assert not graph.get_ports()


def test_add_connection(session, registry, graph, connection_model):
    """Assert that we can add a connection to the graph by calling `add_connection`."""
    graph.add_connection(connection_model)
    assert graph.get_connections() == {connection_model}


def test_add_redundant_connection(session, registry, graph, connection_model):
    """Assert that when trying to add a connection that is already in the graph, nothing happen."""
    graph.add_connection(connection_model)
    graph.add_connection(connection_model)
    assert graph.get_connections() == {connection_model}


def test_remove_connection(session, registry, graph, connection_model):
    """Assert that we can remove a connection from the graph by calling `remove_connection`."""
    graph.add_connection(connection_model)
    graph.remove_connection(connection_model)
    assert not graph.get_connections()


def test_remove_unexistant_connection(graph, connection_model):
    """Assert that when trying to remove a connection that is NOT in the graph, nothing happen."""
    graph.remove_connection(connection_model)
    assert not graph.get_connections()


def test_reset(session, registry, graph, node_model):
    """Assert that when we reset the graph, it remove any node, port and connections."""
    graph.add_all_nodes()
    graph.reset()
    assert not graph.get_nodes()
    assert not graph.get_ports()
    assert not graph.get_connections()


def test_registry_on_attribute_unexpectedly_added(session, registry, graph, node, node_model):
    """Assert that when a node is added to the registry it is NOT added to the graph."""
    assert node_model not in graph.get_nodes()


def test_registry_on_node_unexpectedly_removed(session, registry, graph, node):
    """Assert that when a node is removed from the registry it is removed from the graph."""
    session.remove_node(node)
    assert not graph.get_nodes()


def test_registry_on_port_unexpectedly_added(session, registry, graph, port_model):
    """Assert that when a port is added to the registry, it is NOT added to the graph."""
    assert port_model not in graph.get_ports()


def test_registry_on_port_unexpectedly_removed(session, registry, graph, port, port_model):
    """Assert that when a port is removed from the registry it is removed from the graph."""
    graph.add_port(port_model)
    session.remove_port(port)
    assert not graph.get_ports()


def test_registry_on_connection_unexpectedly_added(session, registry, graph, connection_model):
    """Assert that when a connection is added to the registry, it is NOT added to the graph."""
    assert not graph.get_connections()


def test_registry_on_connection_unexpectedly_removed(session, registry, graph, connection, connection_model):
    """Assert that when a connection is removed from the registry, it is removed from the graph."""
    graph.add_connection(connection_model)
    session.remove_connection(connection)
    assert not graph.get_connections()
