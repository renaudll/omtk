import pytest


@pytest.fixture
def node(session):
    return session.create_node('transform')


@pytest.fixture
def port(session, node):
    return session.create_port(node, 'testPort')


@pytest.fixture
def connection(session, port):
    return session.create_connection(port, port)


@pytest.fixture
def node_model(node, registry):
    return registry.get_node(node)


@pytest.fixture
def port_model(port, registry):
    return registry.get_port(port)


@pytest.fixture
def connection_model(connection, registry):
    port_src = registry.get_port(connection.src)
    port_dst = registry.get_port(connection.dst)
    return registry.get_connection(port_src, port_dst)


def test_reset(model):
    pass


def test_get_set_registry(registry, model):
    """Validate we can set and get the registry associated with the model."""
    model.set_registry(registry)
    assert model.get_registry() is registry


def test_add_node(model, node_model):
    """Validate we can add node to the graph."""
    model.add_node(node_model)
    assert model.get_nodes() == {node_model}


def test_remove_node(model, node_model):
    """Validate we can remove a node from the graph."""
    model.add_node(node_model)
    model.remove_node(node_model)
    assert model.get_nodes() == set()


def test_is_node_visible(model, node_model):
    """Validate that by default an added node is visible."""
    model.add_node(node_model)
    assert model.is_node_visible(node_model)


def test_get_set_node_position(model, node_model):
    """Validate that we can get and set the position of a node in the graph."""
    pos = (1.2, 3.4)
    model.add_node(node_model)
    model.set_node_position(node_model, pos)
    assert model.get_node_position(node_model) == pos


def test_add_port(model, port_model):
    """Validate that we can add a port to the graph."""
    model.add_port(port_model)
    assert model.get_ports() == {port_model}


def test_add_port_automatically_add_node(model, node_model, port_model):
    """Validate that when we add a port to the graph it's node is also added."""
    model.add_port(port_model)
    assert model.get_nodes() == {node_model}


def test_remove_port(model, port_model):
    """Validate that we can remove a port from the graph."""
    model.add_port(port_model)
    model.remove_port(port_model)
    assert model.get_ports() == set()


def test_get_node_ports(model, node_model, port_model):
    """Validate we can access the ports associated with a node."""
    model.add_port(port_model)
    assert model.get_node_ports(node_model) == {port_model}


def test_is_port_visible(model, port_model):
    """Validate a port we add is visible by default."""
    model.add_port(port_model)
    assert model.is_port_visible(port_model)


def test_add_connection(model, connection_model):
    """Validate we can add a connection to the graph."""
    model.add_connection(connection_model)
    assert model.get_connections() == {connection_model}


def test_add_connection_automatically_add_port(model, connection_model, port_model):
    """Validate when we add a connection to the graph the port is added."""
    model.add_connection(connection_model)
    assert model.get_ports() == {port_model}


def test_add_connection_automatically_add_node(model, connection_model, node_model):
    """Validate when we add a connection to the graph the node is added."""
    model.add_connection(connection_model)
    assert model.get_nodes() == {node_model}


def test_remove_connection(model, connection_model):
    """Validate we can remove a connection from the graph."""
    model.add_connection(connection_model)
    model.remove_connection(connection_model)
    assert model.get_connections() == set()


def test_is_connection_visible(model, connection_model):
    """Validate that by default a connection added to the graph is visible."""
    model.add_connection(connection_model)
    assert model.is_connection_visible(connection_model)


def test_on_node_unexpectedly_deleted(session, model, node, node_model):
    """Validate that when a node is removed from the session it is removed from the graph."""
    model.add_node(node_model)
    session.remove_node(node)
    assert model.get_nodes() == set()


def test_on_attribute_unexpectedly_added(model, node_model):
    """Validate that when a node is added to the session nothing happen."""
    assert model.get_nodes() == set()


def test_on_attribute_unexpectedly_removed(session, model, port, port_model):
    """Validate that when a port is removed from the session it is removed from the graph."""
    model.add_port(port_model)
    session.remove_port(port)
    assert model.get_ports() == set()


def test_on_connection_unexpectedly_added(model, port_model):
    """Validate that when a port is added to the session nothing happen."""
    assert model.get_ports() == set()


def test_on_connection_unexpectedly_removed(session, model, connection, connection_model):
    """Validate that when a connection is removed from the session it is removed from the graph."""
    model.add_connection(connection_model)
    session.remove_connection(connection)
    assert model.get_connections() == set()


def test_expand_node_ports(model, node_model, port_model):
    """Validate that we can automatically add node ports when calling `expand_node_ports`."""
    model.add_node(node_model)
    model.expand_node_ports(node_model)
    assert model.get_ports() == {port_model}


def test_expand_node_connections(model, node_model, port_model, connection_model):
    """Validate that we can automatically add node connection when calling `expand_node_connections`."""
    model.add_port(port_model)
    model.expand_node_connections(node_model)
    assert model.get_connections() == {connection_model}


def test_add_all(model, node_model, port_model, connection_model):
    """Ensure that we can add all registered node, port and connection."""
    model.add_all()
    assert model.get_nodes() == {node_model}
    assert model.get_ports() == {port_model}
    assert model.get_connections() == {connection_model}
