"""
Ensure we are able to reconize that a Component should be updated and to update it.
"""

import pymel.core as pymel  # easy standalone initialization
import pytest

from omtk import component
from omtk.component import ComponentDefinition
from omtk.component import ComponentRegistry
from omtk.libs import libRigging


def _create_multiply_component(multiplier=1.0):
    """Create a simple component that does a multiplication. For testing purpose."""
    u = libRigging.create_utility_node(
        'multiplyDivide',
        input1X=1.0,
        input2X=multiplier,
    )
    inst = component.from_attributes_map(
        {'inn': u.input1X},
        {'out': u.outputX},
    )
    return inst


@pytest.fixture()
def component_registry(tmp_path):
    paths = [str(tmp_path)]
    return ComponentRegistry(paths)


@pytest.fixture
def component_def_v1(component_registry):
    # Create the first version of a component
    c1 = _create_multiply_component(1.0)
    c1_def = ComponentDefinition(
        name='test',
        version='1',
        uid='1'
    )
    component_registry.register(c1, c1_def)
    c1.delete()
    assert component_registry.is_latest_component_version(c1_def)
    return c1_def


@pytest.fixture
def component_def_v2(component_registry):
    c2 = _create_multiply_component(2.0)
    c2_def = ComponentDefinition(
        name='test',
        version='2',
        uid='1',
    )
    component_registry.register(c2, c2_def)
    c2.delete()
    assert component_registry.is_latest_component_version(c2_def)
    return c2_def


@pytest.fixture
def component_inst_v1(component_def_v1):
    """
    Create the following schema
    |t1
    |t2
    |component

    t1.tx -> component.input
    component.output -> t2.tx

    :return:
    :rtype: omtk.component.Component
    """
    t1 = pymel.createNode('transform', name='t1')
    t2 = pymel.createNode('transform', name='t2')
    inst = component_def_v1.instanciate()
    t1.translateX.set(1.0)
    pymel.connectAttr(t1.translateX, inst.grp_inn.inn)
    pymel.connectAttr(inst.grp_out.out, t2.translateX)
    return inst


def test_is_latest(component_registry, component_inst_v1, component_def_v2):
    """
    Validate from our latest scene,
    """
    latest = component_registry.is_latest_component_version(component_inst_v1)
    assert not latest


def test_update(component_registry, component_inst_v1, component_def_v2):
    """Validate we can update a component instance from v1 to v2."""
    from maya import cmds

    old_namespace = component_inst_v1.namespace
    new_inst = component_inst_v1.update(component_def_v2)
    new_namespace = new_inst.namespace

    assert old_namespace == new_namespace

    # Validate new logic
    assert cmds.getAttr('t2.translateX') == 2.0


def test_explode(cmds, component_registry, component_inst_v1):
    """Validate we can explode a component."""
    assert cmds.connectionInfo('t1.translateX', destinationFromSource=True) == ['test:inn.inn']
    assert cmds.connectionInfo('t2.translateX', sourceFromDestination=True) == 'test:out.out'

    component_inst_v1.explode()

    assert cmds.connectionInfo('t1.translateX', destinationFromSource=True) == ['multiplyDivide1.input1X']
    assert cmds.connectionInfo('t2.translateX', sourceFromDestination=True) == 'multiplyDivide1.outputX'


# def test_component_hold_connections(component_inst_v1):
#
#     map_inn, map_out =  component_inst_v1.hold_connections()
#     map_inn = {k: v.fullPath() for k, vals in map_inn.iteritems()}
#     map_out = {k: v.fullPath() for k, vals in map_out.iteritems()}
#     assert map_inn == 1
#     assert map_out == 1