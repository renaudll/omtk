import pytest

from omtk.nodegraph.filters.filter_intermediate_nodes import IntermediateNodeFilter
from omtk_test import assertGraphNodeNamesEqual, assertGraphConnectionsEqual


@pytest.fixture
def schema(schema_default):
    return schema_default


@pytest.fixture
def filter_():
    return IntermediateNodeFilter()


def test_unitconversion_filtering(session, registry, model, pymel):
    """
    Ensure NodeGraphStandardFilter hide unitConversion nodes unless explicitly ask to.
    """
    n1 = pymel.createNode('transform', name='a')
    n2 = pymel.createNode('transform', name='b')
    pymel.connectAttr(n1.translateX, n2.rotateX)

    model.add_all()

    assertGraphNodeNamesEqual(model, [u'a', u'b'])
    assertGraphConnectionsEqual(model, [(u'a.translateX', u'b.rotateX')])

    # However, if you add the unitConversion node explicitly, we want to see it!
    n3 = n1.translateX.outputs()[0]
    m3 = registry.get_node(n3)
    model.add_node(m3)

    assertGraphNodeNamesEqual(model, [u'a', u'b', u'unitConversion1'])
    assertGraphConnectionsEqual(model, [
        (u'a.translateX', u'b.rotateX'),
        (u'a.translateX', u'unitConversion1.input'),
        (u'unitConversion1.output', u'b.rotateX'),
    ])


def test_existing_unitconversion_filtering(session, registry, model, pymel):
    """
    Ensure NodeGraphStandardFilter hide unitConversion nodes unless explicitly ask to.
    """
    n1 = pymel.createNode('transform', name='a')
    n2 = pymel.createNode('transform', name='b')
    pymel.connectAttr(n1.translateX, n2.rotateX)

    m1 = registry.get_node(n1)
    m2 = registry.get_node(n2)
    model.add_node(m1)
    # ctrl.add_node_callbacks(m2)

    assertGraphNodeNamesEqual([u'a', u'b'])
    assertGraphConnectionsEqual([(u'a.translateX', u'b.rotateX')])
