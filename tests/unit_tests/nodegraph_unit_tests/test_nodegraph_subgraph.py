import pytest

from omtk.nodegraph.controller import NodeGraphController
from tests.helpers import assertGraphNodeNamesEqual, assertGraphConnectionsEqual


@pytest.fixture
def ctrl(registry, model):
    """Pytest fixture for a NodegraphController. Currently return the model."""
    return NodeGraphController(
        registry=registry,
        model=model,
        view=None
    )


@pytest.fixture
def preconfigured_session(cmds, registry, model, ctrl):
    """(unused) Pytest fixture for a pre-configured session with a float-2-float graph inside."""
    n1 = cmds.createNode('transform', name='n1')
    n2 = cmds.createNode('transform', name='n2')
    n3 = cmds.createNode('transform', name='n3')
    cmds.addAttr(n1, longName='testA')
    cmds.addAttr(n2, longName='testB')
    cmds.addAttr(n3, longName='testC')
    cmds.connectAttr('n1.testA', 'n2.testB')
    cmds.connectAttr('n2.testB', 'n3.testC')

    registry.scan_session()
    model.add_all()

    node = registry.get_node('n2')
    assert node
    component = ctrl.group_nodes([node])

    return component


def test_subgraph(session, registry, model, ctrl, preconfigured_session):
    component = preconfigured_session

    assertGraphNodeNamesEqual(model, [u'n1', u'component1', u'n3'])
    assertGraphConnectionsEqual(model, [
        (u'n1.translateX', u'component1.translateX'),
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
