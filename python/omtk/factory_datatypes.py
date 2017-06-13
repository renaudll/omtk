"""
Help identifying datatypes for usage in factory methods.
"""
import collections

from omtk.core.classComponent import Component
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classNode import Node
from omtk.core.classModule import Module
from omtk.core.classRig import Rig
from omtk.libs import libPython
from omtk.vendor.Qt import QtGui
from pymel import core as pymel


class AttributeType:
    Basic = 0
    Iterable = 1
    Dictionary = 2
    Node = 3
    Ctrl = 4
    Attribute = 5
    Component = 6
    Module = 7
    Rig = 8


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
    if isinstance(val, Module):
        return AttributeType.Module
    if isinstance(val, Rig):
        return AttributeType.Rig
    if isinstance(val, Component):
        return AttributeType.Component
    raise Exception("Cannot resolve Component attribute type for {0} {1}".format(type(val), val))

@libPython.memoized
def get_icon_from_datatype(datatype):
    if datatype in (
        AttributeType.Component,
        AttributeType.Module,
        AttributeType.Rig
    ):
        return QtGui.QIcon(":/out_objectSet.png")
    return None

@libPython.memoized
def get_node_color_from_datatype(datatype):
    if datatype in (
        AttributeType.Component,
        AttributeType.Module
    ):
        return QtGui.QColor(170, 128, 170, 255)
    if datatype in (
        AttributeType.Node
    ):
        return QtGui.QColor(170, 170, 128, 255)
    # todo: warning
    return QtGui.QColor(128, 170, 170, 255)