# coding: utf-8
"""
Help identifying datatypes for usage in factory methods.
"""
import collections
import logging

from omtk import decorators
from omtk.vendor.Qt import QtGui
from pymel import core as pymel
from omtk.vendor.enum34 import Enum

log = logging.getLogger('omtk')

class AttributeType(Enum):
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
    AttributeCompound = 16
    AttributeNurbsCurve = 17
    AttributeNurbsSurface = 18
    AttributeMesh = 19
    AttributeLattice = 20
    AttributeMessage = 21
    ComponentDefinition = 22


_g_attr_type_from_maya_attribute_type_str = {
    'bool': AttributeType.AttributeBool,
    'long': AttributeType.AttributeInt,
    'short': AttributeType.AttributeInt,
    'byte': AttributeType.AttributeInt,
    'char': AttributeType.AttributeString,
    'enum': AttributeType.AttributeInt,
    'float': AttributeType.AttributeFloat,
    'double': AttributeType.AttributeFloat,
    'doubleAngle': AttributeType.AttributeFloat,
    'doubleLinear': AttributeType.AttributeFloat,
    'string': AttributeType.AttributeString,
    'stringArray': AttributeType.AttributeString,
    'time': AttributeType.AttributeFloat,
    'matrix': AttributeType.AttributeMatrix,
    'fltMatrix': AttributeType.AttributeMatrix,
    'float2': AttributeType.AttributeFloat,  # ???,  # ???
    'float3': AttributeType.AttributeVector3,
    'double2': AttributeType.AttributeFloat,  # ???, # ???
    'double3': AttributeType.AttributeVector3,
    'double4': AttributeType.AttributeVector4,
    'long2': AttributeType.AttributeInt,  # ???,  # ???
    'long3': AttributeType.AttributeVector3,
    'short2': AttributeType.AttributeVector3,
    'short3': AttributeType.AttributeVector3,
    'doubleArray': AttributeType.AttributeFloat,
    'Int32Array': AttributeType.AttributeInt,
    'vectorArray': AttributeType.AttributeVector3,
    'nurbsCurve': AttributeType.AttributeNurbsCurve,
    'nurbsSurface': AttributeType.AttributeNurbsSurface,
    'mesh': AttributeType.AttributeMesh,
    'lattice': AttributeType.AttributeLattice,
    'compound': AttributeType.AttributeCompound,
    'Tdatacompound': AttributeType.AttributeCompound,
    'geometry': AttributeType.AttributeCompound,
    'typed': AttributeType.AttributeCompound,
    'message': AttributeType.AttributeMessage
}

_attr_type_by_native_type = {
    float: AttributeType.AttributeFloat,
    int: AttributeType.AttributeInt,
    pymel.datatypes.Vector: AttributeType.AttributeVector3,
    pymel.datatypes.Point: AttributeType.AttributeVector4,
    pymel.datatypes.Matrix: AttributeType.AttributeMatrix,
    str: AttributeType.AttributeString,
    bool: AttributeType.AttributeBool,
    pymel.nodetypes.NurbsCurve: AttributeType.AttributeNurbsCurve,
}

# note: currently we try to use the same colors as in maya Node Editor.md
_g_port_color_by_datatype = {
    AttributeType.Basic: QtGui.QColor(0, 0, 0, 255),  # todo: define
    AttributeType.AttributeBool: QtGui.QColor(221, 135, 36, 255),
    AttributeType.AttributeFloat: QtGui.QColor(80, 230, 80, 255),
    AttributeType.AttributeInt: QtGui.QColor(0, 128, 1),
    AttributeType.AttributeMatrix: QtGui.QColor(128, 170, 170, 255),
    AttributeType.AttributeString: QtGui.QColor(10, 40, 195, 255),
    AttributeType.AttributeVector3: QtGui.QColor(0, 0, 0, 255),  # todo: define
    AttributeType.AttributeVector4: QtGui.QColor(0, 0, 0, 255),  # todo: define
    AttributeType.AttributeCompound: QtGui.QColor(0, 0, 0, 255),  # todo: define
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
    from omtk.core.entity_attribute import EntityAttribute

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

    raise Exception("Cannot resolve datatype for {0} {1}".format(type(val), val))


@decorators.memoized
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
        # return _create("out_objectSet.png")
        return _create("dagContainer.svg")
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
    if datatype == AttributeType.ComponentDefinition:
        return _create("out_objectSet.png")

    log.warning("Cannot resolve icon from datatype {0}".format(datatype))


@decorators.memoized
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


@decorators.memoized
def get_port_color_from_datatype(datatype):
    color = _g_port_color_by_datatype.get(datatype)
    if color is None:
        log.warning("Cannot resolve color for datatype {0}. Using default color.".format(datatype))
        color = _g_default_port_color
    return color

from maya import OpenMaya
import re

_g_regex_datatype_from_mel = re.compile('.*-dt "(\w*)".*')
_g_regex_attributetype_from_mel = re.compile('.*-at "(\w*)".*')

def _get_attr_datatype_from_mobject(mobject):
    """
    This is best way I've found of truly knowning the type of any attribute.
    ¯\_(ツ)_/¯
    :param mobject:
    :return:
    """
    mfn = OpenMaya.MFnAttribute(mobject)
    mel = mfn.getAddAttrCmd()
    result = _g_regex_datatype_from_mel.match(mel)
    if result:
        datatype = next(iter(result.groups()), None)
        return datatype

    result = _g_regex_attributetype_from_mel.match(mel)
    if result:
        datatype = next(iter(result.groups()), None)
        return datatype

def get_attr_datatype(attr):
    # type: (pymel.Attribute) -> AttributeType
    """
    Return the datatype associated with an Attribute.
    :param attr: The attribute to query the time from.
    :return: An enum value representing the attribute type in OMTK perspective.

    Note that we might have difficulties guessing the type of an attribute.
    This apparently simple task can be hard in Maya, mainly because some attributes that seem typed are in fact compounds.
    ex: multMatrix.matrixIn look like an

    Note 1
    ------
    We don't want to use pymel .type() method.
    For some reason, if the array attribute don't have any children, checking a leaf will temporally create and remove a '99' attribute.

    For example the following code:

        from maya import OpenMaya
        from omtk.libs import libMayaCallbacks
        def fn_callback(callback_id, plug, *args):
            print("{0}: {1}".format(plug.name(), libMayaCallbacks.debug_MNodeMessage_callback(callback_id)))

        m = pymel.createNode('multMatrix')
        OpenMaya.MNodeMessage.addAttributeChangedCallback(m.__apimobject__(), fn_callback)
        m.matrixIn.numElements()  # return 0
        m.matrixIn[0].type()  # will trigger callbacks

    Will output:

        multMatrix26.matrixIn[99]: kIncomingDirection, kAttributeArrayAdded
        multMatrix26.matrixIn[99]: kIncomingDirection, kAttributeArrayRemoved

    """
    attr_type = None

    from maya import cmds

    # The array is typed, not it's elements.
    if attr.isElement():
        return get_attr_datatype(attr.array())

    # In some situations, trying to type an array attribute will return None. (todo: provide an example?)
    # if attr_type is None and attr.isMulti():
    # log.warning("Getting a hard time typing {0}. Using sketchy method.".format(attr))

    # # An array is always typed?
    from maya import OpenMaya
    # mfn = OpenMaya.MFnTypedAttribute(attr.__apimobject__())
    # type_ = mfn.attrType()
    # if type_ == OpenMaya.MFnData.kMatrix
    # todo: FIND A BETTER WAY!

    # todo: How do we know if the attribute is typed?
    attr_type = _get_attr_datatype_from_mobject(attr.__apimobject__())

    # Method #1: Use Pymel
    # BAD because this will temporary create attribute and trigger a shitload of callbacks.
    # attr_type = attr[0].type()

    # Method #2: Use cmds
    # BAD because it can return None on attributes like multMatrix.matrixIn
    # attr_type = cmds.getAttr('{0}[0]'.format(attr.__melobject__()), type=True)

    # if attr_type is None:
    #     attr_type = attr.type()

    if attr_type is None:
        log.warning("Cannot resolve attribute type from attribute {0}.".format(
            attr
        ))
        return

    type_ = _g_attr_type_from_maya_attribute_type_str.get(attr_type)
    if type_ is None:
        log.warning("Cannot resolve metatype for {0} of type {1}.".format(attr, attr_type))
        return

    return type_
    #
    # if attr_type == 'message':
    #     return AttributeType.AttributeMessage
    #
    # if attr_type == 'TdataCompound':
    #     return AttributeType.AttributeCompound
    #
    # native_type = _ENTITY_ATTR_TYPE_BY_MAYA_ATTR_TYPE.get(attr_type, None)
    # if native_type is None:
    #     log.warning("Cannot resolve metatype from attribute type {0}. {1}".format(
    #         attr_type,
    #         attr
    #     ))
    #     return
    #
    # val = _attr_type_by_native_type[native_type]
    # if not val:
    #     log.warning("Cannot resolve attribute type from attribute {0}. Unknown datatype {1}".format(attr, native_type))
    #     return
    # return val
