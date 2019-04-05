import pytest


@pytest.fixture()
def node(registry, session, model, cmds):
    return session.create_node('transform', name='a')


@pytest.fixture()
def port(session, node):
    return session.create_port(node, 'test')


@pytest.fixture()
def connection(session, node):
    port_src = session.create_port(node, 'testSrc')
    port_dst = session.create_port(node, 'testDst')
    connection = session.create_connection(port_src, port_dst)
    return connection


def assert_registry_empty(registry):
    """
    Utility method that asset that the provided registry is completely empty.

    :param registry:
    """
    assert_registry_node_empty(registry)
    assert_registry_port_empty(registry)
    assert_registry_connection_empty(registry)


def assert_registry_node_empty(registry):
    """
    Utility method that assert that no node information exist in the provided registry.

    :param registry:
    """
    assert not registry.nodes
    assert not registry.cache_nodes_by_value


def assert_registry_port_empty(registry):
    """
    Utility method that assert that no port information exist in the provided registry.

    :param registry:
    """
    assert not registry.ports
    assert not registry.cache_ports_by_value
    assert not registry.cache_ports_by_node


def assert_registry_connection_empty(registry):
    """
    Utility method that assert no connection information exist in the provided registry.

    :param registry:
    """
    assert not registry.connections
    assert not registry.cache_connections_by_port
    assert not registry.cache_connection_by_value


def test_set_session(registry, session):
    """
    Assert that we can set and unset the registry session.
    """
    registry.set_session(None)
    assert registry.session is None

    registry.set_session(session)
    assert registry.session is session


def test_create_node(node, registry):
    """
    Assert that a node model exist in the registry.
    """
    node_model = registry.get_node(node)
    assert node_model in registry.nodes


def test_delete_dagnode(registry, session, node):
    """
    Ensure that a node that is deleted in Maya is automatically remove from the registry.
    """
    node_model = registry.get_node(node)
    session.remove_node(node)

    assert node_model not in registry.nodes
    assert_registry_empty(registry)


def test_create_port(registry, port):
    """Ensure that when a port is added by Maya, it is automatically added on visible nodes."""
    port_model = registry.get_port(port)
    assert port_model in registry.ports


def test_remove_port(registry, session, port):
    """Ensure that when a port is removed by Maya, it is automatically removed from visible nodes."""
    port_model = registry.get_port(port)
    session.remove_port(port)
    assert port_model not in registry.ports


def test_register_connection(registry, connection):
    """Ensure that when a connection is registered, it is in the global list of connections."""
    port_model_src = registry.get_port(connection.src)
    port_model_dst = registry.get_port(connection.dst)
    connection_model = registry.get_connection(port_model_src, port_model_dst)
    assert connection_model in registry.connections


def test_register_connection_ports(registry, connection):
    """Ensure that when a connection is registerd, it's source and destination ports are also registered."""
    port_model_src = registry.get_port(connection.src)
    port_model_dst = registry.get_port(connection.dst)
    connection_model = registry.get_connection(port_model_src, port_model_dst)
    assert connection_model.get_source() in registry.ports
    assert connection_model.get_destination() in registry.ports


def test_unregister_connection(registry, session, connection):
    """Ensure that when a connection is removed from the scene, it is also removed from the registry."""
    port_model_src = registry.get_port(connection.src)
    port_model_dst = registry.get_port(connection.dst)
    connection_model = registry.get_connection(port_model_src, port_model_dst)
    session.remove_connection(connection)
    assert connection_model not in registry.connections


def test_unregister_connection_source_port(registry, session, connection):
    """Ensure that if a connection source port is removed from the scene, the connection is also unregistered."""
    port_model_src = registry.get_port(connection.src)
    port_model_dst = registry.get_port(connection.dst)
    connection_model = registry.get_connection(port_model_src, port_model_dst)
    session.remove_port(connection.src)
    assert connection_model.get_source() not in registry.ports
    assert connection_model.get_destination() in registry.ports
    assert connection_model not in registry.connections


def test_unregister_connection_destination_port(registry, session, connection):
    """Ensure that when a connection source port is removed from the scene, the connection is also unregistered."""
    port_model_src = registry.get_port(connection.src)
    port_model_dst = registry.get_port(connection.dst)
    connection_model = registry.get_connection(port_model_src, port_model_dst)
    session.remove_port(connection.dst)
    assert connection_model.get_source() in registry.ports
    assert connection_model.get_destination() not in registry.ports
    assert connection_model not in registry.connections


def test_cache_nodes_by_value(registry, node):
    """Assert the cache_nodes_by_value property is updated when a node is added."""
    node_model = registry.get_node(node)
    assert registry.cache_nodes_by_value.get(node) is node_model


def test_cache_ports_by_value(registry, port):
    """Assert the cache_ports_by_value property is updated when a node is added."""
    port_model = registry.get_port(port)
    assert registry.cache_ports_by_value.get(port) is port_model


def test_cache_ports_by_node(registry, node, port):
    """Assert the cache_ports_by_node property is updated when a node is added."""
    node_model = registry.get_node(node)
    port_model = registry.get_port(port)
    assert port_model in registry.cache_ports_by_node.get(node_model)


def test_cache_connections_by_port(registry, port, connection):
    """Assert the cache_connections_by_port property is updated when a node is added."""
    port_model = registry.get_port(port)
    connection_model = registry.get_connection(port_model, port_model)
    assert connection_model in registry.cache_connections_by_port.get(port_model)


def test_cache_connection_by_value(registry, port):
    """Assert the cache_connection_by_value property is updated when a node is added."""
    port_model = registry.get_port(port)
    key = (port_model, port_model)
    connection_model = registry.get_connection(*key)
    assert registry.cache_connection_by_value.get(key) is connection_model
