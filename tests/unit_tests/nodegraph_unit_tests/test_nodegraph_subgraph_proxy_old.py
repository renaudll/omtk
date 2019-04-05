"""
Ensure propre behaviour or the GraphController, GraphRegistry and every related models.
"""
import logging

from maya_mock.decorators import mock_pymel
from tests.helpers import assertGraphNodeNamesEqual, assertGraphConnectionsEqual

log = logging.getLogger(__name__)


def assertPortInfo(model, node, name, is_readable, is_writable):
    """Assert that a provided port is readable, writable or both."""

    def _get_port_by_name(name):
        for port in model.iter_node_ports(node):
            if port.get_name() == name:
                return port

    p = _get_port_by_name(name)
    assert p.is_readable() == is_readable
    assert p.is_writable() == is_writable


def test_io_subgraph(session, registry, model, ctrl):
    """Ensure that we support subgraphs networks where an attribute is both an input and an output (io)."""
    # Create network
    with mock_pymel(session) as pymel:
        n1 = pymel.createNode('transform', name='node')
        n2 = pymel.createNode('transform', name='n2')
        n3 = pymel.createNode('transform', name='n3')
        pymel.connectAttr(n1.t, n2.t)
        pymel.connectAttr(n2.t, n3.t)

    # Register network
    model.add_all_nodes()

    assertGraphNodeNamesEqual([u'node', u'n2', u'n3'])
    assertGraphConnectionsEqual(model, [
        (u'node.translate', u'n2.translate'),
        (u'n2.translate', u'n3.translate'),
    ])

    # Create a subgroup (group nodes)
    component = ctrl.group_nodes([n2])
    assertGraphNodeNamesEqual([u'node', u'component1', u'n3'])
    assertPortInfo(model, component, 'translate', is_readable=True, is_writable=True)
    assertGraphConnectionsEqual(model, [
        (u'node.translate', u'component1.translate'),
        (u'component1.translate', u'n3.translate'),
    ])

    # Enter the subgrap
    ctrl.set_level(component)
    assertGraphNodeNamesEqual(model, [u'component1:inn', u'n2', u'component1:out'])
    # assertGraphConnectionsEqual


def test_nested_subgraphs(session, registry, model, ctrl):
    """Ensure that we are able to navigate between multiple nested subgraphs."""
    # Create network
    with mock_pymel(session) as pymel:
        def _create_transform(name): return pymel.createNode('transform', name=name)

        n1 = _create_transform('node')
        n2 = _create_transform('n2')
        n3 = _create_transform('n3')
        n4 = _create_transform('n4')
        n5 = _create_transform('n5')
        pymel.connectAttr(n1.t, n2.t)
        pymel.connectAttr(n2.t, n3.t)
        pymel.connectAttr(n3.t, n4.t)
        pymel.connectAttr(n4.t, n5.t)

    registry.scan_session()
    model.add_all_nodes()

    assertGraphNodeNamesEqual(model, [u'node', u'n2', u'n3', u'n4', u'n5'])

    # Create a subgroup (group nodes)
    component_1 = ctrl.group_nodes([n2, n3, n4])
    assertGraphNodeNamesEqual(model, [u'node', u'component1', u'n5'])
    assertGraphConnectionsEqual(model, [
        (u'node.translate', u'component1.translate'),
        (u'component1.translate', u'n5.translate'),
    ])

    # Enter the subgrap
    ctrl.set_level(component_1)
    assertGraphNodeNamesEqual(model, [u'component1:inn', u'n2', u'n3', u'n4', u'component1:out'])
    assertGraphConnectionsEqual(model, [
        (u'component1:inn.translate', u'n2.translate'),
        (u'n2.translate', u'n3.translate'),
        (u'n3.translate', u'n4.translate'),
        (u'n4.translate', u'component1:out.translate'),
    ])

    # Create a new component
    component_2 = ctrl.group_nodes([n3])
    assertGraphNodeNamesEqual(model, [u'component1:inn', u'n2', u'component1:component1', u'n4', u'component1:out'])
    assertGraphConnectionsEqual(model, [
        (u'component1:inn.translate', u'n2.translate'),
        (u'n2.translate', u'component1:component1.translate'),
        (u'component1:component1.translate', u'n4.translate'),
        (u'n4.translate', u'component1:out.translate'),
    ])

    # Enter the new component
    ctrl.set_level(component_2)
    assertGraphNodeNamesEqual(model, [u'component1:component1:inn', u'n3', u'component1:component1:out'])
    assertGraphConnectionsEqual(model, [
        (u'component1:component1:inn.translate', u'n3.translate'),
        (u'n3.translate', u'component1:component1:out.translate'),
    ])

    # Exit the new component
    ctrl.set_level(component_1)
    assertGraphNodeNamesEqual(model, [u'component1:inn', u'n2', u'component1:component1', u'n4', u'component1:out'])
    assertGraphConnectionsEqual(model, [
        (u'component1:inn.translate', u'n2.translate'),
        (u'n2.translate', u'component1:component1.translate'),
        (u'component1:component1.translate', u'n4.translate'),
        (u'n4.translate', u'component1:out.translate'),
    ])

    # Return to root level
    ctrl.set_level(None)
    assertGraphNodeNamesEqual([u'node', u'component1', u'n5'])
    assertGraphConnectionsEqual(model, [
        (u'node.translate', u'component1.translate'),
        (u'component1.translate', u'n5.translate'),
    ])
