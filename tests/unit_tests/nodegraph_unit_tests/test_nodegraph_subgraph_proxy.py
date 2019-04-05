"""
Ensure propre behaviour or the GraphController, GraphRegistry and every related models.
"""
import logging

import pytest
from omtk.nodegraph.models.graph.subgraph_proxy_model import SubgraphProxyModel

log = logging.getLogger('omtk')


@pytest.fixture
def model(model, registry):
    """
    Wrap the model under a model that support filtering through filters.

    :rtype: GraphFilterProxyModel
    """
    proxy_model = SubgraphProxyModel(registry=registry)
    proxy_model.set_source_model(model)
    return proxy_model


def test_empty_component(session, registry, model):
    """ Ensure that as soon as we see an "inn" and "out" object inside a namespace we interpret it as a component."""
    session.create_node("transform", "component1:inn")
    session.create_node("transform", "component1:out")
    registry.scan_session()
    model.add_all()
    actual = [node.get_name() for node in model.get_nodes()]
    assert actual == ["component1"]


def test_component_with_node(session, registry, model):
    """ Ensure that we are correctly filtering nested namespaces."""
    session.create_node("transform", "component1:inn")
    session.create_node("transform", "component1:component2:inn")
    session.create_node("transform", "component1:component2:component3:inn")
    session.create_node("transform", "component1:component2:component3:out")
    session.create_node("transform", "component1:component2:out")
    session.create_node("transform", "component1:out")
    registry.scan_session()
    model.add_all()
    actual = [node.get_name() for node in model.get_nodes()]
    assert actual == ["component1"]


def test_component_with_port(session, registry, model):
    # Create session
    n1 = session.create_node("transform", "component1:inn")
    session.create_node("transform", "component1:someNode")
    session.create_node("transform", "component1:out")
    session.create_port(n1, "in1")
    session.create_port(n1, "in2")
    session.create_port(n1, "in3")

    registry.scan_session()
    model.add_all()

    expected = {
        'connections': [],
        'nodes': ['component1'],
        'ports': [
            'component1:inn.in1',
            'component1:inn.in2',
            'component1:inn.in3'
        ]
    }
    actual = model.dump()
    assert actual == expected


def test_inside_component_with_node(registry, model):
    """Ensure that we can correct navigate into a level."""
    n1 = registry.create_node("transform", "component1:inn")
    n2 = registry.create_node("transform", "component1:someNode")
    n3 = registry.create_node("transform", "component1:out")
    model.add_node(n1)
    model.add_node(n2)
    model.add_node(n3)

    component = model._get_component_by_level("component1")
    # component_node = model._get_node_from_component(registry, component)
    model.set_level("component1")
    actual = [node.get_name() for node in model.get_nodes()]
    assert actual == ["component1:inn", "component1:someNode", "component1:out"]
