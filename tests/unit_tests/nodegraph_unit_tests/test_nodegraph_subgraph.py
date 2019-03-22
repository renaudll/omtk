import pytest
from omtk.nodegraph.controller import NodeGraphController
from omtk_test import assertGraphNodeNamesEqual, assertGraphConnectionsEqual


@pytest.fixture
def schema(schema_default):
    """Use a preconfigured schema to mirror as close as possible Maya behavior."""
    return schema_default


@pytest.fixture
def ctrl(registry, model):
    """Pytest fixture for a NodegraphController. Currently return the model."""
    NodeGraphController(
        registry=registry,
        model=model,
        view=None
    )


@pytest.fixture
def preconfigured_session(session, registry, model, ctrl):
    """(unused) Pytest fixture for a pre-configured session with a float-2-float graph inside."""
    n1 = session.create_node('transform', name='n1')
    n2 = session.create_node('transform', name='n2')
    n3 = session.create_node('transform', name='n3')

    # Connect n1.tx to n2.tx
    port_src = n1.get_port_by_name('translateX')
    port_dst = n2.get_port_by_name('translateX')
    session.create_connection(port_src, port_dst)

    # Connect n2.tx to n3.tx
    port_src = n2.get_port_by_name('translateX')
    port_dst = n3.get_port_by_name('translateX')
    session.create_connection(port_src, port_dst)

    component = ctrl.group_nodes([registry.get_node(n2)])

    return n1, n2, n3, component


def test_subgraph(session, registry, model, ctrl, preconfigured_session):
    n1, n2, n3, component = preconfigured_session

    assertGraphNodeNamesEqual(model, [u'node', u'component1', u'n3'])
    assertGraphConnectionsEqual(model, [
        (u'node.translateX', u'component1.translateX'),
        (u'component1.translateX', u'n3.translateX'),
    ])

    ctrl.set_level(component)

    assertGraphNodeNamesEqual(model, [
        u'component1:inn',
        u'n2',
        u'component1:out',
    ])
    assertGraphConnectionsEqual(model, [
        (u'component1:inn.translateX', u'n2.translateX'),
        (u'n2.translateX', u'component1:out.translateX'),
    ])
