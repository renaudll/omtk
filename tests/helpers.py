def assertGraphNodeCountEqual(model, expected):
    """
    Ensure that the number of nodes in the graph match the provided count.

    :param int expected: The expected node counts in the graph.
    :raise Exception: If the number of nodes in the graph is incorrect.
    """
    actual = len(model.get_nodes())
    assert actual == expected


def assertGraphRegistryNodeCountEqual(registry, actual, expected):
    """
    Ensure that the number of registered nodes match the provided count.

    :param int expected: The expected node count in the REGISTRY_DEFAULT.
    :raise Exception: If the number of nodes in the REGISTRY_DEFAULT is incorrect.

    """
    assert len(registry._nodes)
    assert actual == expected


def getGraphPortCount(model):
    return len(model.get_ports())


def assertGraphPortCountEqual(model, expected):
    """
    Ensure that the number of ports visible in the graph match the expected count.

    :param int expected: The expected port count in the graph.
    :raise Exception: If the number of ports visible in the graph is incorrect.
    """
    actual = len(model.get_ports())
    assert actual == expected


def assertGraphNodePortNamesEqual(model, node, expected):
    """
    Ensure that all the current ports in a provided nodes match.

    :param omtk.nodegraph.NodeModel node: The node to retreive the port from.
    :param List[str] expected: A sorted list of names to match
    :raise Exception: If the name of any port don't match the expected value.
    """
    ports = model.get_node_ports(node)
    actual = sorted(port.get_name() for port in ports)
    assert actual == expected


def assertGraphConnectionCountEqual(model, expected):
    """
    Validate the the number of visible connections in the graph.

    :param int expected: The expected number of connections in the graph.
    :raise Exception: If the number of connections in the graph is unexpected.
    """
    actual = len(model.get_connections())
    assert actual == expected


def assertGraphNodeNamesEqual(model, expected):
    """
    Validate the name of all the graph nodes.

    :param List[str] expected: A sorted list of all the graph node names.
    :raise Exception: If any node name don't match the expected value.
    """
    nodes = model.get_nodes()
    actual = (node.get_name() for node in nodes)
    assert set(actual) == set(expected)
    # self.assertEqual(len(expected), len(actual))  # in case some item where are duplicated


def assertGraphConnectionsEqual(model, expected):
    """
    Validate the number of connections in the graph.
    :param List[Tuple(str, str)] expected: A list of 2-tuple describing connection in the graph.
    """
    connections = model.get_connections()
    actual = [connection.dump() for connection in connections]

    # Using set for comparison as we don't want the ordering to be taken in account.
    assert set(actual) == set(expected)
    # assert actual == expected


def assertGraphIsEmpty(model):
    assertGraphNodeCountEqual(model, 0)
    assertGraphPortCountEqual(model, 0)
    assertGraphConnectionCountEqual(model, 0)


def assertGraphEquals(model, expected):
    graph = model.dump()
    assert graph == expected
