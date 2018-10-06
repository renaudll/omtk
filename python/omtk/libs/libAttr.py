import itertools
import logging
from contextlib import contextmanager

from maya import OpenMaya
from maya import cmds
from omtk.libs import libPython
from pymel import core as pymel

log = logging.getLogger(__name__)

# src: http://download.autodesk.com/us/maya/2010help/CommandsPython/addAttr.html
_g_addAttr_kwargs_map = {
    'bool': {'at': 'double'},
    'long': {'at': 'long'},
    'short': {'at': 'short'},
    'byte': {'at': 'byte'},
    'char': {'at': 'char'},
    'enum': {'at': 'enum'},
    'float': {'at': 'float'},
    'double': {'at': 'double'},
    'doubleAngle': {'at': 'doubleAngle'},
    'doubleLinear': {'at': 'doubleLinear'},
    'string': {'dt': 'string'},
    'stringArray': {'dt': 'stringArray'},
    'compound': {'at': 'compound'},
    'message': {'at': 'message'},
    'time': {'at': 'time'},
    'matrix': {'dt': 'matrix'},
    'fltMatrix': {'at': 'fltMatrix'},
    'reflectanceRGB': {'dt': 'reflectanceRGB'},
    'reflectance': {'at': 'reflectance'},
    'spectrumRGB': {'dt': 'spectrumRGB'},
    'spectrum': {'at': 'spectrum'},
    'float2': {'dt': 'float2'},
    'float3': {'dt': 'float3'},
    'double2': {'dt': 'double2'},
    'double3': {'dt': 'double3'},
    'long2': {'dt': 'long2'},
    'long3': {'dt': 'long3'},
    'short2': {'dt': 'short2'},
    'short3': {'dt': 'short3'},
    'doubleArray': {'dt': 'doubleArray'},
    'Int32Array': {'dt': 'Int32Array'},
    'vectorArray': {'dt': 'vectorArray'},
    'nurbsCurve': {'dt': 'nurbsCurve'},
    'nurbsSurface': {'dt': 'nurbsSurface'},
    'mesh': {'dt': 'mesh'},
    'lattice': {'dt': 'lattice'},
    'pointArray': {'dt': 'pointArray'}
}

_g_blacklisted_attr_names = {
    'caching',
    'isHistoricallyInteresting',
    'nodeState',
    'frozen',
    'isCollapsed',
    'blackBox',
    'publishedNodeInfo',
    'templateName',
    'templatePath',
    'templateVersion',
    'viewName',
    'iconName',
    'viewMode',
    'uiTreatment',
    'customTreatment',
    'creator',
    'creationDate',
    'containerType',
    'intermediateObject',
    'hyperLayout',
    'borderConnections',
    'publishedNode',
    'publishedNodeInfo.publishedNode',
    'renderLayerInfo',
    'renderLayerInfo.renderLayerId',
    'instObjGroups',
    'instObjGroups.objectGroups',
    'instObjGroups.objectGroups.objectGroupId',
    'instObjGroups.objectGroups.objectGrpColor',
    'template',
    'ghosting',
    'objectColorR',
    'objectColorG',
    'objectColorB',
    'objectColorRGB',
    'wireColorRGB',
    'wireColorR',
    'wireColorG',
    'wireColorB',
    'useObjectColor',
    'objectColor',
    'drawOverride',
    'overrideDisplayType',
    'overrideLevelOfDetail',
    'overrideShading',
    'overrideTexturing',
    'overridePlayback',
    'overrideEnabled',
    'overrideVisibility',
    'hideOnPlayback',
    'overrideRGBColors',
    'overrideColor',
    'overrideColorRGB',
    'overrideColorR',
    'overrideColorG',
    'overrideColorB',
    'lodVisibility',
    'selectionChildHighlighting',
    'renderInfo',
    'identification',
    'layerRenderable',
    'layerOverrideColor',
    'renderLayerInfo.renderLayerRenderable',
    'renderLayerInfo.renderLayerColor',
    'ghostingControl',
    'ghostCustomSteps',
    'ghostPreSteps',
    'ghostPostSteps',
    'ghostStepSize',
    'ghostFrames',
    'ghostColorPreA',
    'ghostColorPre',
    'ghostColorPreR',
    'ghostColorPreG',
    'ghostColorPreB',
    'ghostColorPostA',
    'ghostColorPost',
    'ghostColorPostR',
    'ghostColorPostG',
    'ghostColorPostB',
    'ghostRangeStart',
    'ghostRangeEnd',
    'ghostDriver',
    'Skipping ctrl.ghostDriver',
    'hiddenInOutliner',
    'useOutlinerColor',
    'outlinerColor',
    'outlinerColorR',
    'outlinerColorG',
    'outlinerColorB',
    'geometry',
    'selectHandle',
    'selectHandleX',
    'selectHandleY',
    'selectHandleZ',
    'displayHandle',
    'displayScalePivot',
    'displayRotatePivot',
    'displayLocalAxis',
    'dynamics',
    'showManipDefault',
    'specifiedManipLocation',
    'message',
    'boundingBox',
    'boundingBoxMin',
    'boundingBoxMax',
    'boundingBoxSize',
    'boundingBoxMinX',
    'boundingBoxMaxX',
    'boundingBoxMinY',
    'boundingBoxMaxY',
    'boundingBoxMinZ',
    'boundingBoxMaxZ',
    'boundingBoxSizeX',
    'boundingBoxSizeY',
    'boundingBoxSizeZ',
    'boundingBoxCenter',
    'boundingBoxCenterX',
    'boundingBoxCenterY',
    'boundingBoxCenterZ',
    'binMembership',
    'inverseScale',  # omtk does not care about segmentScaleCompensate
    'rmbCommand',
    'isHierarchicalConnection',
    'minTransLimit',
    'minTransXLimit',
    'minTransXLimitEnable',
    'minTransYLimit',
    'minTransYLimitEnable',
    'minTransZLimit',
    'minTransZLimitEnable',
    'maxTransLimit',
    'maxTransXLimit',
    'maxTransXLimitEnable',
    'maxTransYLimit',
    'maxTransYLimitEnable',
    'maxTransZLimit',
    'maxTransZLimitEnable',
    'minRotLimit',
    'minRotXLimit',
    'minRotXLimitEnable',
    'minRotYLimit',
    'minRotYLimitEnable',
    'minRotZLimit',
    'minRotZLimitEnable',
    'maxRotLimit',
    'maxRotXLimit',
    'maxRotXLimitEnable',
    'maxRotYLimit',
    'maxRotYLimitEnable',
    'maxRotZLimit',
    'maxRotZLimitEnable',
    'minScaleLimit',
    'minScaleXLimit',
    'minScaleXLimitEnable',
    'minScaleYLimit',
    'minScaleYLimitEnable',
    'minScaleZLimit',
    'minScaleZLimitEnable',
    'maxScaleLimit',
    'maxScaleXLimit',
    'maxScaleXLimitEnable',
    'maxScaleYLimit',
    'maxScaleYLimitEnable',
    'maxScaleZLimit',
    'maxScaleZLimitEnable',
}


def disconnectAttr(attr, inputs=True, outputs=True):
    attr_is_locked = attr.isLocked()
    if attr_is_locked: attr.unlock()

    if inputs:
        for attr_in in attr.inputs(plugs=True):
            pymel.disconnectAttr(attr_in, attr)
    if outputs:
        for attr_out in attr.outputs(plugs=True):
            pymel.disconnectAttr(attr, attr_out)

    if attr_is_locked: attr.lock()


# TODO: test
def swapAttr(a, b, inputs=True, outputs=True):
    def _get_attr_inn(att):
        return next(iter(att.inputs(plugs=True)), att.get())

    def _set_attr_inn(att, data):
        if isinstance(data, pymel.Attribute):
            pymel.connectAttr(data, att)
        else:
            att.set(data)

    def _get_attr_out(att):
        return att.outputs(plugs=True)

    def _set_attr_out(att, data):
        for attrOut in data:
            pymel.connectAttr(att, attrOut)

    a_node_mel = a.node().__melobject__()
    b_node_mel = b.node().__melobject__()
    a_is_readable = cmds.attributeQuery(a.longName(), node=a_node_mel, readable=True)
    b_is_readable = cmds.attributeQuery(b.longName(), node=b_node_mel, readable=True)
    a_is_writable = cmds.attributeQuery(a.longName(), node=a_node_mel, writable=True)
    b_is_writable = cmds.attributeQuery(b.longName(), node=b_node_mel, writable=True)

    # Swap inputs
    if inputs and (a_is_writable or b_is_writable):
        if a_is_writable != b_is_writable:
            log.warning("Cannot swap {0} outputs with {1}. One or the attributes is not writable.".format(
                a, b
            ))
        else:
            a_inputs = _get_attr_inn(a)
            b_inputs = _get_attr_inn(b)

            for a_input in a_inputs:
                pymel.disconnectAttr(a_input, a)
            for b_input in b_inputs:
                pymel.disconnectAttr(b_input, b)

            _set_attr_inn(a, b_inputs)
            _set_attr_inn(b, a_inputs)

    # Swap outputs
    if a_is_readable or b_is_readable:
        if a_is_readable != b_is_readable:
            log.warning("Cannot swap {0} outputs with {1}. One or the attributes is not readable.".format(
                a, b
            ))
        else:
            a_outputs = _get_attr_out(a)
            b_outputs = _get_attr_out(b)

            for a_output in a_outputs:
                pymel.disconnectAttr(a, a_output)
            for b_output in b_outputs:
                pymel.disconnectAttr(b, b_output)

            _set_attr_out(a, b_outputs)
            _set_attr_out(b, a_outputs)


def sortAttr(node):
    raise NotImplementedError


# TODO: finish
def holdAttr(attr, delete=True):
    log.warning("holdAttr is deprecated, please don't use it!")

    data = {
        'node': attr.node(),
        'longName': attr.longName(),
        'shortName': attr.shortName(),
        'niceName': pymel.attributeName(attr),
        'inputs': attr.inputs(plugs=True),
        'outputs': attr.outputs(plugs=True),
        'isMulti': attr.isMulti(),
        'type': attr.type(),
        'locked': attr.isLocked(),
        'keyable': attr.isKeyable(),
        'hidden': attr.isHidden()
    }

    if delete:
        pymel.deleteAttr(attr)
    return data


def fetchAttr(data, reconnect_inputs=True, reconnect_outputs=True):
    log.warning("fetchAttr is deprecated, please don't use it!")

    # todo: add support for multi and compount attribute!
    node = data['node']

    kwargs = _g_addAttr_kwargs_map[data['type']]

    pymel.addAttr(node,
                  longName=data['longName'],
                  multi=data['isMulti'],
                  niceName=data['niceName'],
                  keyable=data['keyable'],
                  hidden=data['hidden'],
                  **kwargs
                  )
    attr = node.attr(data['longName'])

    # Re-connect inputs
    if reconnect_inputs:
        if not data['isMulti']:
            inn = next(iter(data['inputs']), None)
            if inn:
                pymel.connectAttr(inn, attr)
        else:
            for i, inn in enumerate(data['inputs']):
                pymel.connectAttr(inn, attr[i])

    # Re-connect outputs
    if reconnect_outputs:
        if not data['isMulti']:
            for i, output in enumerate(data['outputs']):
                pymel.connectAttr(attr, output)
        else:
            for i, output in enumerate(data['outputs']):
                if output:
                    pymel.connectAttr(attr[i], output)


class AttributeData(object):
    """
    Temporary object that hold an attribute information.
    Mainly used to copy from an attribute to another.
    """

    def __init__(self):
        self.long_name = None
        self.short_name = None
        self.nice_name = None
        self.is_compound = None
        self.is_multi = None
        self.is_readable = None
        self.is_writable = None
        self.type = None
        self.locked = None
        self.keyable = None
        self.hidden = None
        self.inputs = None
        self.outputs = None
        self.node = None
        self.parent = None
        self.children = None

    def __repr__(self):
        return '<AttributeData {0}>'.format(self.long_name)

    @classmethod
    def from_pymel_attribute(cls, attr, store_inputs=False, store_outputs=False):
        """
        Create an AttributeData instance.
        :param attr: A pymel.Attribute instance.
        :return: An AttributeData instance.
        """
        inst = cls()
        inst.node = attr.node()
        inst.long_name = attr.longName()
        inst.short_name = attr.shortName()
        inst.nice_name = pymel.attributeName(attr)
        inst.is_multi = attr.isMulti()
        inst.is_compound = attr.isCompound()
        inst.type = attr.type()
        inst.locked = attr.isLocked()
        inst.keyable = attr.isKeyable()
        inst.hidden = attr.isHidden()

        # Array elements cannot be queried, we need the parent.
        ref_name = attr.array().longName() if attr.isElement() else inst.long_name
        inst.is_readable = pymel.attributeQuery(ref_name, node=inst.node, readable=True)
        inst.is_writable = pymel.attributeQuery(ref_name, node=inst.node, writable=True)

        # Use can choose to store additional information.
        # This was used a lot in the old implementation.
        if store_inputs:
            inst.inputs = attr.inputs(plugs=True)
        if store_outputs:
            inst.outputs = attr.outputs(plugs=True)

        # Support for compound attributes.
        if inst.is_compound:
            inst.children = []
            for child_attr in attr.getChildren():
                child_inst = cls.from_pymel_attribute(
                    child_attr,
                    store_inputs=store_inputs,
                    store_outputs=store_outputs
                )
                child_inst.parent = inst.long_name
                inst.children.append(child_inst)

        return inst

    def _get_addAttr_kwargs(self):
        """
        Return the argument that should be passed to addAttr to reproduce this attribute.
        No information about the node itself is returned/
        :parent: A pymel.Attribute representing the parent in case of compound attributes.
        Note that
        :return: A dict containing the keyword argument to pass to cmds.addAttr.
        """
        result = {
            'longName': self.long_name,
            'niceName': self.nice_name,
            'hidden': self.hidden,
            'keyable': self.keyable,
            'multi': self.is_multi,
        }

        result.update(_g_addAttr_kwargs_map[self.type])

        if self.is_compound:
            result.update({
                'numberOfChildren': len(self.children),
            })

            # Some compound still have type (ex: translate)
            # Creating them with 'at' will make Maya angry.
            result['at'] = result.pop('dt')

        if self.parent:
            result['parent'] = self.parent

        return result

    def rename(self, new_long_name, auto_rename_children=True):
        """
        Rename the attribute and -preferably- all it's children if the attribute is compound.
        Note that to rename the child correctly, we take in account that the name of the parent is in the child name.
        Also note that currently we don't correctly handle children short and nice name.
        # todo: properly support shortName and niceName renaming? how?
        """
        # todo: add support for new_nice_name? do we care enough?
        if auto_rename_children:
            cur_long_name_length = len(self.long_name)
            if self.children:
                for child in self.children:
                    if not child.long_name.startswith(self.long_name):
                        log.warning(
                            "Cannot automatically rename {0} definition. Long name don't start with {1}.".format(
                                child, self.long_name
                            ))
                    else:
                        # Note how do don't care that much about the short and nice name.
                        child_new_long_name = new_long_name + child.long_name[cur_long_name_length:]
                        child.long_name = child.short_name = child.nice_name = child_new_long_name
                    child.parent = new_long_name
        self.long_name = self.short_name = self.nice_name = new_long_name

    def copy_to_node(self, node):
        # type: (pymel.PyNode) -> pymel.Attribute
        """
        Create a new attribute from the stored definition, on a new node.
        :param node: A pymel.PyNode instance.
        :return: A pymel.Attribute instance.
        """

        # Note: The _fn is used to hide the parent attribute from the function signature.
        kwargs = self._get_addAttr_kwargs()
        pymel.addAttr(node, **kwargs)

        if self.is_compound:
            for child in self.children:
                child.copy_to_node(node)

        # Note that when creating compound attributes, the attribute start to exist only at the end of their definition.
        # This is why we cannot return an Attribute instance that is part of a compound.
        return node.attr(self.long_name) if not self.parent else None

    def connect_stored_inputs(self, node):
        """
        Generally, you'll want to call this after copy_to_node().
        :param node:
        :return:
        """
        attr = node.attr(self.long_name)
        if self.inputs is None:
            raise Exception("Cannot connect inputs, no inputs were stored. Use store_inputs when initializing.")

        for attr_input in self.inputs:
            if not attr_input.exists():
                continue
            pymel.connectAttr(attr_input, attr, force=True)

    def connect_stored_outputs(self, node):
        """
        Generally, you'll want to call this after copy_to_node().
        :param node:
        :return:
        """
        attr = node.attr(self.long_name)
        if self.outputs is None:
            raise Exception("Cannot connect outputs, no outputs were stored. Use store_outputs when initializing.")

        for attr_output in self.outputs:
            if not attr_output.exists():
                continue
            pymel.connectAttr(attr, attr_output, force=True)


# Normally we can use pymel.renameAttr but this work on multi-attributes also
def renameAttr(node, oldname, newname):
    assert (isinstance(node, pymel.PyNode))
    if not node.hasAttr(oldname): return
    data = holdAttr(node.attr(oldname))
    data['longName'] = newname
    data['niceName'] = newname
    data['shortName'] = newname
    fetchAttr(data)
    return True


def hold_attrs(attr, hold_curve=True):
    """
    Hold a specific @attr attribute.
    """
    if isinstance(attr, pymel.Attribute):
        if not hold_curve or attr.isLocked() or not attr.isKeyable():
            return attr.get()

        for input in attr.inputs(plugs=True):
            if isinstance(input.node(), (pymel.nodetypes.AnimCurve, pymel.nodetypes.BlendWeighted)):
                pymel.disconnectAttr(input,
                                     attr)  # disconnect the animCurve so it won't get deleted automaticly after unbuilding the rig
                return input
        return attr.get()
    return attr


def fetch_attr(source, target):
    """
    Restore a specific @attr attribute.
    Returns: the destination attribute.
    """
    if target.isLocked():
        # pymel.warning("Can't fetch locked attribute {0}.".format(target.__melobject__()))
        return

    if source is None:
        return
    elif isinstance(source, pymel.Attribute):
        if source.exists():
            pymel.connectAttr(source, target)
    else:
        target.set(source)

    return target


def transfer_connections(attr_src, attr_dst):
    # Transfer input connections
    attr_src_inn = next(iter(attr_src.inputs(plugs=True)), None)
    if attr_src_inn:
        pymel.disconnectAttr(attr_src_inn, attr_src)
        pymel.connectAttr(attr_src_inn, attr_dst)

    # Transfer output connections
    for attr_src_out in attr_src.outputs(plugs=True):
        pymel.disconnectAttr(attr_src, attr_src_out)
        pymel.connectAttr(attr_dst, attr_src_out)


def addAttr(node, longName=None, *args, **kwargs):
    assert (longName)
    pymel.addAttr(node, longName=longName, *args, **kwargs)
    return node.attr(longName)


def addAttr_separator(obj, attr_name, *args, **kwargs):
    attr = addAttr(obj, longName=attr_name, niceName=attr_name, at='enum', en='------------', k=True)
    attr.lock()


# Lock/unlock Function

def lock_attrs(attr_list):
    for attr in attr_list:
        attr.lock()


def unlock_attrs(attr_list):
    for attr in attr_list:
        attr.unlock()


def lock_trs(node, *args, **kwargs):
    lock_translation(node, *args, **kwargs)
    lock_rotation(node, *args, **kwargs)
    lock_scale(node, *args, **kwargs)


def unlock_trs(node, *args, **kwargs):
    unlock_translation(node, *args, **kwargs)
    unlock_rotation(node, *args, **kwargs)
    unlock_scale(node, *args, **kwargs)


def lock_translation(node, x=True, y=True, z=True):
    lock_list = []
    if x:
        translate_x = node.attr('translateX')
        lock_list.append(translate_x)
    if y:
        translate_y = node.attr('translateY')
        lock_list.append(translate_y)
    if z:
        translate_z = node.attr('translateZ')
        lock_list.append(translate_z)

    lock_attrs(lock_list)


def unlock_translation(node, x=True, y=True, z=True, xyz=True):
    unlock_list = []
    if x:
        translate_x = node.attr('translateX')
        unlock_list.append(translate_x)
    if y:
        translate_y = node.attr('translateY')
        unlock_list.append(translate_y)
    if z:
        translate_z = node.attr('translateZ')
        unlock_list.append(translate_z)
    if xyz:
        translate = node.attr('translate')
        unlock_list.append(translate)

    unlock_attrs(unlock_list)


def lock_rotation(node, x=True, y=True, z=True):
    lock_list = []
    if x:
        rotate_x = node.attr('rotateX')
        lock_list.append(rotate_x)
    if y:
        rotate_y = node.attr('rotateY')
        lock_list.append(rotate_y)
    if z:
        rotate_z = node.attr('rotateZ')
        lock_list.append(rotate_z)

    lock_attrs(lock_list)


def unlock_rotation(node, x=True, y=True, z=True, xyz=True):
    unlock_list = []
    if x:
        rotate_x = node.attr('rotateX')
        unlock_list.append(rotate_x)
    if y:
        rotate_y = node.attr('rotateY')
        unlock_list.append(rotate_y)
    if z:
        rotate_z = node.attr('rotateZ')
        unlock_list.append(rotate_z)
    if xyz:
        rotate = node.attr('rotate')
        unlock_list.append(rotate)

    unlock_attrs(unlock_list)


def lock_scale(node, x=True, y=True, z=True):
    lock_list = []
    if x:
        scale_x = node.attr('scaleX')
        lock_list.append(scale_x)
    if y:
        scale_y = node.attr('scaleY')
        lock_list.append(scale_y)
    if z:
        scale_z = node.attr('scaleZ')
        lock_list.append(scale_z)

    lock_attrs(lock_list)


def unlock_scale(node, x=True, y=True, z=True, xyz=True):
    unlock_list = []
    if x:
        scale_x = node.attr('scaleX')
        unlock_list.append(scale_x)
    if y:
        scale_y = node.attr('scaleY')
        unlock_list.append(scale_y)
    if z:
        scale_z = node.attr('scaleZ')
        unlock_list.append(scale_z)
    if xyz:
        scale = node.attr('scale')
        unlock_list.append(scale)

    unlock_attrs(unlock_list)


def connect_transform_attrs(src, dst, tx=True, ty=True, tz=True, rx=True, ry=True, rz=True, sx=True, sy=True, sz=True,
                            force=False):
    """
    Utility method to connect multiple attributes between two transform nodes.
    :param src: The source transform.
    :param dst: The destination transform.
    :param tx: If True, will connect the translateX attribute.
    :param ty: If True, will connect the translateY attribute.
    :param tz: If True, will connect the translateZ attribute.
    :param rx: If True, will connect the rotateX attribute.
    :param ry: If True, will connect the rotateY attribute.
    :param rz: If True, will connect the rotateZ attribute.
    :param sx: If True, will connect the scaleX attribute.
    :param sy: If True, will connect the scaleY attribute.
    :param sz: If True, will connect the scaleZ attribute.
    :param force: If True, will overwrite existing connections.
    """
    if tx:
        pymel.connectAttr(src.translateX, dst.translateX, force=force)
    if ty:
        pymel.connectAttr(src.translateY, dst.translateY, force=force)
    if tz:
        pymel.connectAttr(src.translateZ, dst.translateZ, force=force)
    if rx:
        pymel.connectAttr(src.rotateX, dst.rotateX, force=force)
    if ry:
        pymel.connectAttr(src.rotateY, dst.rotateY, force=force)
    if rz:
        pymel.connectAttr(src.rotateZ, dst.rotateZ, force=force)
    if sx:
        pymel.connectAttr(src.scaleX, dst.scaleX, force=force)
    if sy:
        pymel.connectAttr(src.scaleY, dst.scaleY, force=force)
    if sz:
        pymel.connectAttr(src.scaleZ, dst.scaleZ, force=force)


# Hide Function#

def hide_attrs(attr_list):
    for attr in attr_list:
        attr.setKeyable(False)


def unhide_attrs(attr_list):
    for attr in attr_list:
        attr.setKeyable(True)


def hide_trs(node, *args, **kwargs):
    hide_translation(node, *args, **kwargs)
    hide_rotation(node, *args, **kwargs)
    hide_scale(node, *args, **kwargs)


def unhide_trs(node, *args, **kwargs):
    unhide_translation(node, *args, **kwargs)
    unhide_rotation(node, *args, **kwargs)
    unhide_scale(node, *args, **kwargs)


def hide_translation(node, x=True, y=True, z=True):
    hide_list = []
    if x:
        translate_x = node.attr('translateX')
        hide_list.append(translate_x)
    if y:
        translate_y = node.attr('translateY')
        hide_list.append(translate_y)
    if z:
        translate_z = node.attr('translateZ')
        hide_list.append(translate_z)

    hide_attrs(hide_list)


def unhide_translation(node, x=True, y=True, z=True):
    unhide_list = []
    if x:
        translate_x = node.attr('translateX')
        unhide_list.append(translate_x)
    if y:
        translate_y = node.attr('translateY')
        unhide_list.append(translate_y)
    if z:
        translate_z = node.attr('translateZ')
        unhide_list.append(translate_z)

    unhide_attrs(unhide_list)


def hide_rotation(node, x=True, y=True, z=True):
    hide_list = []
    if x:
        rotate_x = node.attr('rotateX')
        hide_list.append(rotate_x)
    if y:
        rotate_y = node.attr('rotateY')
        hide_list.append(rotate_y)
    if z:
        rotate_z = node.attr('rotateZ')
        hide_list.append(rotate_z)

    hide_attrs(hide_list)


def unhide_rotation(node, x=True, y=True, z=True):
    unhide_list = []
    if x:
        rotate_x = node.attr('rotateX')
        unhide_list.append(rotate_x)
    if y:
        rotate_y = node.attr('rotateY')
        unhide_list.append(rotate_y)
    if z:
        rotate_z = node.attr('rotateZ')
        unhide_list.append(rotate_z)

    unhide_attrs(unhide_list)


def hide_scale(node, x=True, y=True, z=True):
    hide_list = []
    if x:
        scale_x = node.attr('scaleX')
        hide_list.append(scale_x)
    if y:
        scale_y = node.attr('scaleY')
        hide_list.append(scale_y)
    if z:
        scale_z = node.attr('scaleZ')
        hide_list.append(scale_z)

    hide_attrs(hide_list)


def unhide_scale(node, x=True, y=True, z=True):
    unhide_list = []
    if x:
        scale_x = node.attr('scaleX')
        unhide_list.append(scale_x)
    if y:
        scale_y = node.attr('scaleY')
        unhide_list.append(scale_y)
    if z:
        scale_z = node.attr('scaleZ')
        unhide_list.append(scale_z)

    unhide_attrs(unhide_list)


# Lock/Hide shortcut

def lock_hide_trs(node, *args, **kwargs):
    lock_trs(node, *args, **kwargs)
    hide_trs(node, *args, **kwargs)


def unlock_unhide_trs(node, *args, **kwargs):
    unlock_trs(node, *args, **kwargs)
    unhide_trs(node, *args, **kwargs)


def lock_hide_translation(node, x=True, y=True, z=True):
    lock_translation(node, x, y, z)
    hide_translation(node, x, y, z)


def unlock_unhide_translation(node, x=True, y=True, z=True):
    unlock_translation(node, x, y, z)
    unhide_translation(node, x, y, z)


def lock_hide_rotation(node, x=True, y=True, z=True):
    lock_rotation(node, x, y, z)
    hide_rotation(node, x, y, z)


def unlock_unhide_rotation(node, x=True, y=True, z=True):
    unlock_rotation(node, x, y, z)
    unhide_rotation(node, x, y, z)


def lock_hide_scale(node, x=True, y=True, z=True):
    lock_scale(node, x, y, z)
    hide_scale(node, x, y, z)


def unlock_unhide_scale(node, x=True, y=True, z=True):
    unlock_scale(node, x, y, z)
    unhide_scale(node, x, y, z)


def is_connected_to(attr_inn, attr_out, recursive=True, max_depth=None, depth=0):
    # TODO: Benchmark this function
    # TODO: Implement key for performance
    node = next(iter(attr_out.inputs()), None)
    if not node:
        return False

    for attr in node.listAttr(connectable=True, hasData=True):
        # HACK: Skip problematic avars...
        # TODO: Find a better way
        if '[' in attr.name():
            continue

        if attr == attr_inn:
            return True
        else:
            if depth >= max_depth:
                return False
            if is_connected_to(attr_inn, attr, recursive=recursive, max_depth=max_depth, depth=depth + 1):
                return True

    return False


#
# get_settable_attr
#

attr_inn_by_out_by_type = {
    'reverse': {
        'outputX': 'inputX',
        'outputY': 'inputY',
        'outputZ': 'inputZ'
    }
}


def get_input_attr_from_output_attr(attr_out):
    node = attr_out.node()
    node_type = node.type()
    association_dict = attr_inn_by_out_by_type.get(node_type, None)
    if association_dict:
        attr_out_name = attr_out.longName()
        attr_inn_name = association_dict.get(attr_out_name, None)
        if attr_inn_name:
            return node.attr(attr_inn_name)

    return next(iter(attr_out.inputs(plugs=True)), None)


def get_settable_attr(attr):
    """
    If attr is not settable, navigate upp in the connection hierarchy until we find the settable attribute.
    For example, in RigSqueeze, the ikFk state attribute will be redirected to the root ctrl.
    Note that in some case the attribute might have been piped in an utility node, if necessary we'll try to
    follow the connections through the utility node.
    """

    def is_attr_interesting(attr):
        if not attr:
            return True

        if not attr.isSettable() or not attr.isKeyable():
            return False

        classification = pymel.getClassification(attr.node().type())
        if any(True for token in classification if 'utility' in token):
            return False

        return True

    while not is_attr_interesting(attr):
        attr = get_input_attr_from_output_attr(attr)
    return attr


#
# Connection holding
#

def hold_connections(attrs, hold_inputs=True, hold_outputs=True):
    """
    Disconnect all inputs from the provided attributes but keep their in memory for ulterior re-connection.
    :param attrs: A list of pymel.Attribute instances.
    :return: A list of tuple containing the origin source and destination attribute for each entries.
    """
    result = []
    for attr in attrs:
        if hold_inputs:
            attr_src = next(iter(attr.inputs(plugs=True)), None)
            if attr_src:
                pymel.disconnectAttr(attr_src, attr)
                result.append((attr_src, attr))
        if hold_outputs:
            for attr_dst in attr.outputs(plugs=True):
                pymel.disconnectAttr(attr, attr_dst)
                result.append((attr, attr_dst))

    return result


def fetch_connections(data):
    """
    Reconnect all attributes using returned data from the hold_connections function.
    :param data: A list of tuple of size-two containing pymel.Attribute instances.
    """
    for attr_src, attr_dst in data:
        pymel.connectAttr(attr_src, attr_dst)


@contextmanager
def context_disconnected_attrs(attrs, hold_inputs=True, hold_outputs=True):
    """
    A context (use with the 'with' statement) to apply instruction while ensuring the provided attributes are disconnected temporarily.
    :param attrs: Redirected to hold_connections.
    """
    data = hold_connections(attrs, hold_inputs=hold_inputs, hold_outputs=hold_outputs)
    yield True
    fetch_connections(data)


def iter_leaf_attributes(obj, **kwargs):
    """
    Iter all the leaf nodes (including compounds and array attributes) recursively using pymel awesome
    iterDescendants method. Note that since the leavesOnly flag is not provided by the listAttr method
    we need to go through the top level Attributes first.
    :param obj:
    :return:
    """
    # todo: this is awfully slow, how can we make it better?
    for attr in obj.listAttr(descendants=True, **kwargs):
        yield attr


def iter_contributing_attributes(obj):
    """
    Yield all attributes contributing to the provided object.
    :param OpenMaya.MFnDependencyNode obj: A pymel.PyNode instance.
    # :yield: pymel.Attribute instances.
    :return: A plug generator
    :rtype: Generator[OpenMaya.MPlug]
    """
    def _iter_plug_children(plug_):
        yield plug_
        if plug_.isArray():
            num_elements = plug_.numElements()
            for i in xrange(num_elements):
                child = plug_.elementByLogicalIndex(i)
                for yielded in _iter_plug_children(child):
                    yield yielded
            return

        if plug_.isCompound():
            num_children = plug_.numChildren()
            for i in xrange(num_children):
                child = plug_.child(i)
                for yielded in _iter_plug_children(child):
                    yield yielded

    mfn = obj.__apimfn__()
    num_attributes = mfn.attributeCount()
    for j in xrange(num_attributes):
        mo_attr = mfn.attribute(j)
        plug = mfn.findPlug(mo_attr)

        # We will ignore any child attribute since we want to explore them
        # ourself. This is because some attributes like renderLayerInfo[-1].renderLayerId don't really exist.
        if plug.isChild():
            continue

        for yielded in _iter_plug_children(plug):
            yield pymel.Attribute(yielded)


def iter_contributing_attributes_openmaya2(dagpath):
    from maya.api import OpenMaya as om2

    sel = om2.MSelectionList()
    sel.add(dagpath)
    obj = sel.getDependNode(0)
    mfn = om2.MFnDependencyNode(obj)

    # mfn = om2.MFnDependencyNode(dagpath)
    for j in xrange(mfn.attributeCount()):
        a = mfn.attribute(j)
        amfn = om2.MFnAttribute(a)
        yield pymel.Attribute(dagpath + '.' + amfn.name)
        # yield amfn


def iter_network_contributing_attributes(network):
    global _g_blacklisted_attr_names
    # for attr in iter_contributing_attributes(network):
    for attr in iter_contributing_attributes_openmaya2(network.__melobject__()):
        if attr.name in _g_blacklisted_attr_names:
            continue
        # if attr.longName() in _g_blacklisted_attr_names:
        #     continue
        yield attr


# def iter_contributing_attributes(obj):
#     """
#     Extend pymel.listAttr by implementing recursivity
#     :param obj: A pymel.nodetypes.DagNode that contain attribute to explore.
#     :param read: If True, output attributes will be yielded.
#     :param write: If True, input attributes will be yielded.
#     :yield: pymel.Attribute instances.
#     """
#     for attr in iter_leaf_attributes(obj):
#         attr_name = attr.longName()
#
#         # Ignore some known attributes by name
#         if attr_name in _blacklisted_attr_names:
#             continue
#
#         yield attr


def get_unique_attr_name(obj, attr_name, str_format='{0}{1:02d}', start=1):
    if not obj.hasAttr(attr_name):
        return attr_name
    for i in itertools.count(start=start):
        new_attr_name = str_format.format(attr_name, i)
        if not obj.hasAttr(new_attr_name):
            return new_attr_name


def escape_attr_name(attr_name):
    return attr_name.replace('[', '_').replace(']', '_').replace('.', '_')


def _wip_explore_input_dependencies(node):
    """
    Similar to listConnection but take in account indirect relationships (like ikHandles).
    """
    # todo: add support for ikHandles?
    children = pymel.listConnections(node, source=True, destination=False, skipConversionNodes=True)

    # ikHandle are a special case, they are not bound by connections.
    # It seem the message connection is important though, if removed the handle don't work...
    for node in node.message.outputs():
        if node.type() == 'ikHandle':
            children.append(node)

    return children


def _wip_explore_input_dependencies_recursive(start_node):
    known = set()

    def _fake_goal(_):
        return False

    libPython.id_dfs(start_node, _fake_goal, _wip_explore_input_dependencies, max_iteration=200, known=known)
    return known


def _wip_explore_output_dependencies(node):
    children = pymel.listConnections(node, source=False, destination=True, skipConversionNodes=True)

    # ikHandle are a special case, they are not bound by connections.
    # It seem the message connection is important though, if removed the handle don't work...
    if node.type() == 'ikHandle':
        children.extend(node.startJoint.inputs())
        children.extend(node.endEffector.inputs())

    return children


def _wip_explore_output_dependencies_recursive(start_node):
    known = set()

    def _fake_goal(_):
        return False

    libPython.id_dfs(start_node, _fake_goal, _wip_explore_output_dependencies, max_iteration=200, known=known)
    return known
