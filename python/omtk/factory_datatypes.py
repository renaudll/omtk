"""
Help identifying datatypes for usage in factory methods.
"""
import collections

from omtk.core.classComponent import Component
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classNode import Node
from pymel import core as pymel


class AttributeType:
    Basic = 0
    Iterable = 1
    Dictionary = 2
    Node = 3
    Ctrl = 4
    Attribute = 5
    Component = 6


def get_component_attribute_type(val):
    if val is None or isinstance(val, (
            bool,
            int,
            float,
            long,
            basestring,
            type,
            pymel.util.enum.EnumValue,
            pymel.datatypes.Vector,
            pymel.datatypes.Point,
            pymel.datatypes.Matrix
    )):
        return AttributeType.Basic
    if isinstance(val, (list, set, tuple)):
        return AttributeType.Iterable
    if isinstance(val, (dict, collections.defaultdict)):
        return AttributeType.Dictionary
    if isinstance(val, BaseCtrl):
        return AttributeType.Ctrl
    if isinstance(val, (pymel.PyNode, Node)):
        return AttributeType.Node
    if isinstance(val, pymel.Attribute):
        return AttributeType.Attribute
    if isinstance(val, Component):
        return AttributeType.Component
    raise Exception("Cannot resolve Component attribute type for {0} {1}".format(type(val), val))