"""
Help identifying datatypes for usage in factory methods.
"""
import collections
import logging

from omtk.libs import libPython
from omtk.vendor.Qt import QtGui
from pymel import core as pymel

log = logging.getLogger('omtk')

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
    ComponentDefinition=16


_attr_type_by_native_type = {
    float: AttributeType.AttributeFloat,
    int: AttributeType.AttributeInt,
    pymel.datatypes.Vector: AttributeType.AttributeVector3,
    pymel.datatypes.Point: AttributeType.AttributeVector4,
    pymel.datatypes.Matrix: AttributeType.AttributeMatrix,
    str: AttributeType.AttributeString,
    bool: AttributeType.AttributeBool
}

# note: currently we try to use the same colors as in maya Node Editor
_g_port_color_by_datatype = {
    AttributeType.AttributeBool: QtGui.QColor(221, 135, 36, 255),
    AttributeType.AttributeFloat: QtGui.QColor(80, 230, 80, 255),
    AttributeType.AttributeInt: QtGui.QColor(0, 128, 1),
    AttributeType.AttributeMatrix: QtGui.QColor(128, 170, 170, 255),
    AttributeType.AttributeString: QtGui.QColor(10, 40, 195, 255),
    AttributeType.AttributeVector3: QtGui.QColor(0, 0, 0, 255),  # todo: define
    AttributeType.AttributeVector4: QtGui.QColor(0, 0, 0, 255),  # todo: define
}

_g_default_port_color = QtGui.QColor(0, 0, 0, 255)


def get_datatype(val):
    """
    Factory method that return an enum value for any possible value.
    Used to type metadata.
    """
    from omtk.core.entity import Entity
    from omtk.core.ctrl import BaseCtrl
    from omtk.core.node import Node
    from omtk.core.module import Module
    from omtk.core.module2 import Module2
    from omtk.core.rig import Rig
    from omtk.core.component_definition import ComponentDefinition

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
        native_type = get_attr_datatype(val)
        return _attr_type_by_native_type[native_type]
    if isinstance(val, (Module, Module2)):
        return AttributeType.Module
    if isinstance(val, Rig):
        return AttributeType.Rig
    if isinstance(val, Entity):
        return AttributeType.Component
    if isinstance(val, ComponentDefinition):
        return AttributeType.ComponentDefinition


    raise Exception("Cannot resolve Component attribute type for {0} {1}".format(type(val), val))


@libPython.memoized
def get_icon_from_datatype(data, datatype=None):
    """
    Factory method that return an appropriate QIcon from a specific datatype.
    :param datatype:
    :return:
    """
    if datatype is None:
        datatype = get_datatype(data)

    def _create(filename):
        return QtGui.QIcon(":/{}".format(filename))

    if datatype == AttributeType.Component:
        return _create("out_objectSet.png")
    if datatype == AttributeType.Module:
        return _create("bevelPlus.png")
    if datatype == AttributeType.Rig:
        return _create("addSkinInfluence.png")
    if datatype == AttributeType.Ctrl:
        return _create("implicitSphere.svg")
    if datatype == AttributeType.Node:
        if isinstance(data, pymel.nodetypes.Joint):
            return _create("/pickJointObj.png")
        elif isinstance(data, pymel.nodetypes.Transform):
            shape = data.getShape()
            if shape:
                return get_icon_from_datatype(shape)
            else:
                return _create("/transform.svg")
        else:
            return _create("/transform.svg")

    log.warning("Cannot resolve icon from datatype {0}".format(datatype))


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

    log.warning("Using default color for datatype {0}".format(datatype))
    return QtGui.QColor(128, 170, 170, 255)


@libPython.memoized
def get_port_color_from_datatype(datatype):
    color = _g_port_color_by_datatype.get(datatype)
    if color is None:
        log.warning("Cannot resolve color for datatype {0}. Using default color.")
        color = _g_default_port_color
    return color


def get_attr_datatype(attr):
    attr_type = None

    # Hack: some multi attributes will return None if we the type directly to the parent attribute.
    # For this reason we'll check a leaf first.
    if attr_type is None and attr.isMulti():
        attr_type = attr[0].type()

    if attr_type is None:
        attr_type = attr.type()

    if attr_type is None:
        log.warning("Cannot resolve attribute type from attribute {0}.".format(
            attr
        ))
        return

    native_type = _ENTITY_ATTR_TYPE_BY_MAYA_ATTR_TYPE.get(attr_type, None)
    if native_type is None:
        log.warning("Cannot resolve metatype from attribute type {0}. {1}".format(
            attr_type,
            attr
        ))
        return

    return _attr_type_by_native_type[native_type]
