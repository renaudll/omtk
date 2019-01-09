import pytest

from maya_mock.decorators import mock_pymel
from omtk.nodegraph.filters.filter_intermediate_nodes import IntermediateNodeFilter
from omtk_test import assertGraphNodeNamesEqual, assertGraphConnectionsEqual


@pytest.fixture
def schema(schema_default):
    """Use a preconfigured schema to mirror as close as possible Maya behavior."""
    return schema_default


@pytest.fixture
def filter_():
    return IntermediateNodeFilter()


@pytest.fixture
def add_intermediate_decomposeMatrix(session):
    # Build stage with pymel
    with mock_pymel(session) as pymel:
        n1 = pymel.createNode('transform', name='a')
        n2 = pymel.createNode('transform', name='b')
        n3 = pymel.createNode('decomposeMatrix')

        pymel.connectAttr(n1.matrix, n3.inputMatrix, force=True)
        pymel.connectAttr(n3.outputTranslate, n2.translate, force=True)
        pymel.connectAttr(n3.outputTranslateX, n2.translateX, force=True)
        pymel.connectAttr(n3.outputTranslateY, n2.translateY, force=True)
        pymel.connectAttr(n3.outputTranslateZ, n2.translateZ, force=True)
        pymel.connectAttr(n3.outputRotate, n2.rotate, force=True)
        pymel.connectAttr(n3.outputRotateX, n2.rotateX, force=True)
        pymel.connectAttr(n3.outputRotateY, n2.rotateY, force=True)
        pymel.connectAttr(n3.outputRotateZ, n2.rotateZ, force=True)
        pymel.connectAttr(n3.outputScale, n2.scale, force=True)
        pymel.connectAttr(n3.outputScaleX, n2.scaleX, force=True)
        pymel.connectAttr(n3.outputScaleY, n2.scaleY, force=True)
        pymel.connectAttr(n3.outputScaleZ, n2.scaleZ, force=True)


@pytest.fixture
def add_intermediate_composeMatrix(session):
    with mock_pymel(session) as pymel:
        n1 = pymel.createNode('transform', name='a')
        n2 = pymel.createNode('transform', name='b')
        n3 = pymel.createNode('composeMatrix')

        pymel.connectAttr(n1.translate, n3.inputTranslate, force=True)
        pymel.connectAttr(n1.translateX, n3.inputTranslateX, force=True)
        pymel.connectAttr(n1.translateY, n3.inputTranslateY, force=True)
        pymel.connectAttr(n1.translateZ, n3.inputTranslateZ, force=True)
        pymel.connectAttr(n1.rotate, n3.inputRotate, force=True)
        pymel.connectAttr(n1.rotateX, n3.inputRotateX, force=True)
        pymel.connectAttr(n1.rotateY, n3.inputRotateY, force=True)
        pymel.connectAttr(n1.rotateZ, n3.inputRotateZ, force=True)
        pymel.connectAttr(n1.scale, n3.inputScale, force=True)
        pymel.connectAttr(n1.scaleX, n3.inputScaleX, force=True)
        pymel.connectAttr(n1.scaleY, n3.inputScaleY, force=True)
        pymel.connectAttr(n1.scaleZ, n3.inputScaleZ, force=True)

        # Note: If the composeMatrix is predictable and don't point to anything it will never be shown.
        # TODO: test this case?
        pymel.addAttr(n2, longName='test', dt='matrix')
        pymel.connectAttr(n3.outputMatrix, n2.test)


def test_predictable_decomposematrix(session, registry, model, add_intermediate_decomposeMatrix):
    """
    Ensure predictable decomposeMatrix are hidden.
    """
    # Add the 'a' and 'b' node to the model but NOT decomposeMatrix1.
    node_a = registry.get_node(session.get_node_by_name('a'))
    node_b = registry.get_node(session.get_node_by_name('b'))
    model.add_node(node_a)
    model.add_node(node_b)
    model.expand_node_connections(node_a)
    model.expand_node_connections(node_b)

    assertGraphNodeNamesEqual(model, [u'a', u'b'])
    assertGraphConnectionsEqual(model, [
        (u'a.matrix', u'b.translate'),
        (u'a.matrix', u'b.translateX'),
        (u'a.matrix', u'b.translateY'),
        (u'a.matrix', u'b.translateZ'),
        (u'a.matrix', u'b.rotate'),
        (u'a.matrix', u'b.rotateX'),
        (u'a.matrix', u'b.rotateY'),
        (u'a.matrix', u'b.rotateZ'),
        (u'a.matrix', u'b.scale'),
        (u'a.matrix', u'b.scaleX'),
        (u'a.matrix', u'b.scaleY'),
        (u'a.matrix', u'b.scaleZ'),
    ])


def test_predictable_decomposematrix_explicit(session, model, add_intermediate_decomposeMatrix):
    """
    Ensure predictable decomposeMatrix are NOT filtered when explicitely added.
    """
    # However, if you add the decomposeMatrix node explicitly, we want to see it!
    model.add_all()

    assertGraphNodeNamesEqual(model, [u'a', u'b', u'decomposeMatrix1'])
    assertGraphConnectionsEqual(model, [
        (u'a.matrix', u'decomposeMatrix1.inputMatrix'),
        (u'decomposeMatrix1.outputTranslate', u'b.translate'),
        (u'decomposeMatrix1.outputTranslateX', u'b.translateX'),
        (u'decomposeMatrix1.outputTranslateY', u'b.translateY'),
        (u'decomposeMatrix1.outputTranslateZ', u'b.translateZ'),
        (u'decomposeMatrix1.outputRotate', u'b.rotate'),
        (u'decomposeMatrix1.outputRotateX', u'b.rotateX'),
        (u'decomposeMatrix1.outputRotateY', u'b.rotateY'),
        (u'decomposeMatrix1.outputRotateZ', u'b.rotateZ'),
        (u'decomposeMatrix1.outputScale', u'b.scale'),
        (u'decomposeMatrix1.outputScaleX', u'b.scaleX'),
        (u'decomposeMatrix1.outputScaleY', u'b.scaleY'),
        (u'decomposeMatrix1.outputScaleZ', u'b.scaleZ'),
    ])


def test_unpredictable_decomposematrix(session, registry, model, cmds, add_intermediate_decomposeMatrix):
    """
    Ensure NodeGraphStandardFilter don't hide unpredictable decomposeMatrix.
    """
    cmds.connectAttr('decomposeMatrix1.outputTranslate', 'b.scale', force=True)

    # Add the 'a' and 'b' node to the model but NOT composeMatrix1.
    node_a = registry.get_node(session.get_node_by_name('a'))
    node_b = registry.get_node(session.get_node_by_name('b'))
    model.add_node(node_a)
    model.add_node(node_b)
    model.expand_node_connections(node_a)
    model.expand_node_connections(node_b)

    assertGraphNodeNamesEqual(model, [u'a', u'b', u'decomposeMatrix1'])
    assertGraphConnectionsEqual(model, [
        (u'a.matrix', u'decomposeMatrix1.inputMatrix'),
        (u'decomposeMatrix1.outputTranslate', u'b.scale'),
    ])


def test_predictable_composematrix(session, registry, model, add_intermediate_composeMatrix):
    # Add the 'a' and 'b' node to the model but NOT composeMatrix1.
    node_1 = session.get_node_by_name('a')
    node_2 = session.get_node_by_name('b')
    model.add_node(registry.get_node(node_1), expand=True)
    model.add_node(registry.get_node(node_2), expand=True)

    assertGraphNodeNamesEqual(model, [u'a', u'b'])
    actual = [connection.dump() for connection in model.get_connections()]
    assert actual == [
        (u'a.translate', u'b.test'),
        (u'a.translateX', u'b.test'),
        (u'a.translateY', u'b.test'),
        (u'a.translateZ', u'b.test'),
        (u'a.rotate', u'b.test'),
        (u'a.rotateX', u'b.test'),
        (u'a.rotateY', u'b.test'),
        (u'a.rotateZ', u'b.test'),
        (u'a.scale', u'b.test'),
        (u'a.scaleX', u'b.test'),
        (u'a.scaleY', u'b.test'),
        (u'a.scaleZ', u'b.test'),
    ]


def test_unpredictable_composematrix(session, registry, model, cmds, add_intermediate_composeMatrix):
    """
    Ensure unpredictable composeMatrix are NOT filtered.
    """
    cmds.connectAttr('a.translateX', 'composeMatrix1.inputScaleX', force=True)

    # Add the 'a' and 'b' node to the model but NOT composeMatrix1.
    model.add_node(registry.get_node(session.get_node_by_name('a')))
    model.add_node(registry.get_node(session.get_node_by_name('b')))

    assertGraphNodeNamesEqual(model, [u'a', u'b', u'composeMatrix1'])
    assertGraphConnectionsEqual(model, [
        (u'a.scaleX', u'composeMatrix1.inputTranslateX'),
        (u'composeMatrix1.outputMatrix', u'b.test'),
    ])
