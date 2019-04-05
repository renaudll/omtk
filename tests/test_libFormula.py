import itertools
import math

import pymel.core as pymel
import pytest
from pymel.core.datatypes import Matrix, Vector, Quaternion
from pymel.core.general import Attribute

from omtk.libs import libFormula
from omtk.libs.libPython import grouper


def _create_pymel_attributes(**kwargs):
    result = {}
    attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']

    iterator = grouper(len(attrs), kwargs.iteritems())  # group kwargs by number of available attributes
    attr_iterator = itertools.cycle(attrs)
    for keyvals in iterator:
        node = pymel.createNode('transform')
        for keyval in keyvals:
            key, val = keyval
            attr_name = next(attr_iterator)
            attr = node.attr(attr_name)
            attr.set(val)
            result[key] = attr

    return result


@pytest.mark.parametrize('formula,vars,expected', (
        ('2+3', {}, 5),  # int addition
        ('5-3', {}, 2),  # int subtraction
        ('2*3', {}, 6),  # int multiplication
        ('6/2', {}, 3),  # int division
        ('2^3', {}, 8),  # int pow
        ('1=1', {}, True),  # equal -> True
        ('1=2', {}, False),  # equal -> False
        ('1!=2', {}, True),  # not equal -> True
        ('1!=1', {}, False),  # not equal -> False
        ('2>1', {}, True),  # greater -> True
        ('1>2', {}, False),  # greater -> False
        ('1>1', {}, False),  # greater -> False (equal)
        ('1<2', {}, True),  # less -> True
        ('2<1', {}, False),  # less -> False
        ('1<1', {}, False),  # less -> False (equal)
        ('2>=1', {}, True),  # greater or equal -> True (greater)
        ('1>=2', {}, False),  # greater or equal-> False (less)
        ('1>=1', {}, True),  # greater or equal-> False (equal)
        ('1<=2', {}, True),  # less or equal -> True (less)
        ('2<=1', {}, False),  # less or equal -> False (greater)
        ('1<=1', {}, True),  # less or equal -> False (equal)

        # weird stuff:
        ('-2^1.0*-1.0+3.3', {}, 5.3),
        ('-2*(1.0-(3^(3*-1.0)))', {}, -1.925925925925926),
        ("a+3*(6+(3*b))", {'a': 4, 'b': 7}, 85),
))
def test_execute_with_variables(formula, vars, expected):
    """ Validate formula parsing with external variables
    """
    actual = libFormula.parse(formula, **vars)
    assert actual == expected


@pytest.mark.parametrize('formula,vars,expected', (
        ('a~b', {'a': pymel.createNode('transform'), 'b': pymel.createNode('transform')}, 0.0),  # matrix distance
        ('a~b', {'a': Matrix(), 'b': Matrix()}, 0.0),  # matrix distance
        ('a~b', {'a': Vector(), 'b': Vector()}, 0.0),  # vector distance
        ('a~0', {'a': Matrix()}, 0.0),  # matrix distance from unit
        ('a~0', {'a': Vector()}, 0.0),  # vector distance from unit
))
def test_parse_with_variables_attrs(formula, vars, expected):
    """ Validate formula parsing with external variables
    """
    actual = libFormula.parse(formula, **vars)
    assert isinstance(actual, Attribute)


@pytest.mark.parametrize('formula,vars,expected', (
        ('a~b', {'a': Quaternion(), 'b': Quaternion()}, 0.0),  # quaternion distance
))
def test_parse_with_variables_attrs_not_implemented(formula, vars, expected):
    """ Assert that some datatypes are not yet implemented for the distance operator.
    """
    with pytest.raises(TypeError):
        libFormula.parse(formula, **vars)


@pytest.mark.parametrize('formula,vars,expected', (
        ('a+b', {'a': 1, 'b': 2}, 3),  # int addition
        ('a-b', {'a': 8, 'b': 2}, 6),  # int subtraction
        ('a*b', {'a': 2, 'b': 3}, 6),  # int multiplication
        ('a/b', {'a': 4, 'b': 2}, 2),  # int division
))
def test_parse_with_attribute_variables(formula, vars, expected):
    vars = _create_pymel_attributes(**vars)
    actual = libFormula.parse(formula, **vars)
    assert actual.get() == expected


def test_squash():
    """Create a bell-curve type squash step."""
    transform, shape = pymel.sphere()
    stretch = transform.sy
    squash = libFormula.parse("1 / (e^(x^2))", x=stretch)
    pymel.connectAttr(squash, transform.sx)
    pymel.connectAttr(squash, transform.sz)
    return True


def test_squash2(step_size=10):
    """Create a cylinder bell-curve joint rig setup"""
    root = pymel.createNode('transform', name='root')
    pymel.addAttr(root, longName='amount', defaultValue=1.0, k=True)
    pymel.addAttr(root, longName='shape', defaultValue=math.e, k=True)
    pymel.addAttr(root, longName='offset', defaultValue=0.0, k=True)
    attAmount = root.attr('amount')
    attShape = root.attr('shape')
    attOffset = root.attr('offset')
    attInput = libFormula.parse("amount^2", amount=attAmount)
    for i in range(0, 100, step_size):
        cyl, make = pymel.cylinder()
        cyl.rz.set(90)
        cyl.ty.set(i + step_size / 2)
        make.heightRatio.set(step_size)
        attSquash = libFormula.parse(
            "amount^(1/(shape^((x+offset)^2)))", x=(i - 50) / 50.0,
            amount=attInput,
            shape=attShape,
            offset=attOffset
        )
        pymel.connectAttr(attSquash, cyl.sy)
        pymel.connectAttr(attSquash, cyl.sz)
