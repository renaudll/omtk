"""
Help identifying datatypes for usage in factory methods.
"""
import collections

from omtk.libs import libPython
from omtk.vendor.Qt import QtGui
from pymel import core as pymel

_ENTITY_ATTR_TYPE_BY_MAYA_ATTR_TYPE = {
    'bool': bool,
    'long': int,
    'short': int,
    'byte': int,
    'char': str,
    'enum': int,
    'float': float,
    'double': float,
    'doubleAngle': float,
    'doubleLinear': float,
    'string': str,
    'stringArray': str,
    'time': float,
    'matrix': pymel.datatypes.Matrix,
    'fltMatrix': pymel.datatypes.Matrix,
    'float2': float,  # ???,  # ???
    'float3': pymel.datatypes.Vector,
    'double2': float,  # ???, # ???
    'double3': pymel.datatypes.Vector,
    'long2': int,  # ???,  # ???
    'long3': pymel.datatypes.Vector,
    'short2': pymel.datatypes.Vector,
    'short3': pymel.datatypes.Vector,
    'doubleArray': float,
    'Int32Array': int,
    'vectorArray': pymel.datatypes.Vector,
    'nurbsCurve': pymel.nodetypes.NurbsCurve,
    'nurbsSurface': pymel.nodetypes.NurbsSurface,
    'mesh': pymel.nodetypes.Mesh,
    'lattice': pymel.nodetypes.Lattice,
}


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
    AttributeFloat = 9
    AttributeInt = 10
    AttributeVector3 = 11
    AttributeVector4 = 12
    AttributeMatrix = 13
    AttributeBool = 14
    AttributeString = 15


_attr_type_by_native_type = {
    float: AttributeType.AttributeFloat,
    int: AttributeType.AttributeInt,
    pymel.datatypes.Vector: AttributeType.AttributeVector3,
    pymel.datatypes.Point: AttributeType.AttributeVector4,
    pymel.datatypes.Matrix: AttributeType.AttributeMatrix,
    str: AttributeType.AttributeString,
    bool: AttributeType.AttributeBool
}


def get_component_attribute_type(val):
    from omtk.core.classEntity import Entity
    from omtk.core.classCtrl import BaseCtrl
    from omtk.core.classNode import Node
    from omtk.core.classModule import Module
    from omtk.core.classModule2 import Module2
    from omtk.core.classRig import Rig

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
            pymel.datatypes.Matrix,
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
        native_type = get_entity_type_by_attr(val)
        return _attr_type_by_native_type[native_type]
    if isinstance(val, (Module, Module2)):
        return AttributeType.Module
    if isinstance(val, Rig):
        return AttributeType.Rig
    if isinstance(val, Entity):
        return AttributeType.Component
    raise Exception("Cannot resolve Component attribute type for {0} {1}".format(type(val), val))


@libPython.memoized
def get_icon_from_datatype(datatype):
    """
    Factory method that return an appropriate QIcon from a specific datatype.
    :param datatype:
    :return:
    """
    def _create(filename):
        return QtGui.QIcon(":/{}".format(filename))

    if datatype == AttributeType.Component:
        return QtGui.QIcon(":/out_objectSet.png")
    if datatype == AttributeType.Module:
        return _create("bevelPlus.png")
    if datatype == AttributeType.Rig:
        return QtGui.QIcon(":/addSkinInfluence.png")
    if datatype == AttributeType.Ctrl:
        return QtGui.QIcon(":/implicitSphere.svg")

    return None


@libPython.memoized
def get_node_color_from_datatype(datatype):
    if datatype in (
            AttributeType.Component,
            AttributeType.Module
    ):
        return QtGui.QColor(170, 128, 170, 255)
    if datatype in (
            AttributeType.Node,
    ):
        return QtGui.QColor(170, 170, 128, 255)
    if datatype == AttributeType.AttributeMatrix:
        return QtGui.QColor(255, 170, 128, 255)
    # todo: warning
    return QtGui.QColor(128, 170, 170, 255)


@libPython.memoized
def get_port_color_from_datatype(datatype):
    return get_node_color_from_datatype(datatype)


def get_entity_type_by_attr(attr):
    if attr.isMulti():
        attr_type = attr[0].type()  # this still work if there's no data
    else:
        attr_type = attr.type()

    native_type = _ENTITY_ATTR_TYPE_BY_MAYA_ATTR_TYPE[attr_type]
    return _attr_type_by_native_type[native_type]
