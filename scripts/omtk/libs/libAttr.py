import logging
log = logging.getLogger('omtk')

# src: http://download.autodesk.com/us/maya/2010help/CommandsPython/addAttr.html
from pymel import core as pymel

kwargsMap = {
    'bool' : {'at':'double'},
    'long' : {'at':'long'},
    'short' : {'at':'short'},
    'byte' : {'at':'byte'},
    'char' : {'at':'char'},
    'enum' : {'at':'enum'},
    'float' : {'at':'float'},
    'double' : {'at':'double'},
    'doubleAngle' : {'at':'doubleAngle'},
    'doubleLinear' : {'at':'doubleLinear'},
    'string' : {'dt':'string'},
    'stringArray' : {'dt':'stringArray'},
    'compound' : {'at':'compound'},
    'message' : {'at':'message'},
    'time' : {'at':'time'},
    'matrix' : {'dt':'matrix'},
    'fltMatrix' : {'at':'fltMatrix'},
    'reflectanceRGB' : {'dt':'reflectanceRGB'},
    'reflectance' : {'at':'reflectance'},
    'spectrumRGB' : {'dt':'spectrumRGB'},
    'spectrum' : {'at':'spectrum'},
    'float2' : {'dt':'float2'},
    'float3' : {'dt':'float3'},
    'double2' : {'dt':'double2'},
    'double3' : {'dt':'double3'},
    'long2' : {'dt':'long2'},
    'long3' : {'dt':'long3'},
    'short2' : {'dt':'short2'},
    'short3' : {'dt':'short3'},
    'doubleArray' : {'dt':'doubleArray'},
    'Int32Array' : {'dt':'Int32Array'},
    'vectorArray' : {'dt':'vectorArray'},
    'nurbsCurve' : {'dt':'nurbsCurve'},
    'nurbsSurface' : {'dt':'nurbsSurface'},
    'mesh' : {'dt':'mesh'},
    'lattice' : {'dt':'lattice'},
    'pointArray' : {'dt':'pointArray'}
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

    a_inputs = _get_attr_inn(a)
    b_inputs = _get_attr_inn(b)
    a_outputs = _get_attr_out(a)
    b_outputs = _get_attr_out(b)

    disconnectAttr(a)
    disconnectAttr(b)

    if inputs is True:
        _set_attr_inn(a, b_inputs)
        _set_attr_inn(b, a_inputs)

    if outputs:
        _set_attr_out(a, b_outputs)
        _set_attr_out(b, a_outputs)


def sortAttr(node):
    raise NotImplementedError


# TODO: finish
def holdAttr(attr):
    data = {
        'node':attr.node(),
        'longName':attr.longName(),
        'shortName':attr.shortName(),
        'niceName': pymel.attributeName(attr),
        'inputs':attr.inputs(plugs=True),
        'outputs':attr.outputs(plugs=True),
        'isMulti': attr.isMulti(),
        'type': attr.type(),
        'locked': attr.isLocked(),
        'keyable': attr.isKeyable(),
        'hidden': attr.isHidden()
    }

    pymel.deleteAttr(attr)
    return data


def fetchAttr(data):
    node = data['node']

    kwargs = kwargsMap[data['type']]

    pymel.addAttr(node,
        longName = data['longName'],
        multi=data['isMulti'],
        niceName = data['niceName'],
        keyable = data['keyable'],
        hidden = data['hidden'],
        **kwargs
    )
    attr = node.attr(data['longName'])

    # Re-connect inputs
    if not data['isMulti']:
        inn = next(iter(data['inputs']), None)
        if inn: pymel.connectAttr(inn, attr)
    else:
        for i, inn in enumerate(data['inputs']):
            pymel.connectAttr(inn, attr[i])

    # Re-connect outputs
    for i, output in enumerate(data['outputs']):
        if output:
            pymel.connectAttr(attr[i], output)


# Normally we can use pymel.renameAttr but this work on multi-attributes also
def renameAttr(node, oldname, newname):
    assert(isinstance(node, pymel.PyNode))
    if not node.hasAttr(oldname): return
    data = holdAttr(node.attr(oldname))
    data['longName'] = newname
    data['niceName'] = newname
    data['shortName'] = newname
    fetchAttr(data)
    return True


def hold_attrs(attr):
    """
    Hold a specific @attr attribute.
    """
    if isinstance(attr, pymel.Attribute):
        for input in attr.inputs(plugs=True):
            if not attr.isLocked():
                if isinstance(input.node(), (pymel.nodetypes.AnimCurve, pymel.nodetypes.BlendWeighted)):
                    pymel.disconnectAttr(input, attr)  # disconnect the animCurve so it won't get deleted automaticly after unbuilding the rig
                    return input
            else:
                log.warning("Input have been found on attr {0}, but it's locked. "
                            "The animation curve will be lost and the current value will be used".format(attr))
        return attr.get()
    return attr


def fetch_attr(source, target):
    """
    Restore a specific @attr attribute.
    Returns: the destination attribute.
    """
    if target.isLocked():
        #pymel.warning("Can't fetch locked attribute {0}.".format(target.__melobject__()))
        return

    if source is None:
        return
    elif isinstance(source, pymel.Attribute):
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
    assert(longName)
    pymel.addAttr(node, longName=longName, *args, **kwargs)
    return node.attr(longName)


def addAttr_separator(obj, attr_name, *args, **kwargs):
    attr = addAttr(obj, longName=attr_name, niceName=attr_name, at='enum', en='------------', k=True)
    attr.lock()

#Lock/unlock Function

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

def unlock_translation(node, x=True, y=True, z=True):
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

def unlock_rotation(node, x=True, y=True, z=True):
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

def unlock_scale(node, x=True, y=True, z=True):
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

    unlock_attrs(unlock_list)

#Hide Function#

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

#Lock/Hide shortcut

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

def is_connected_to(attr_inn, attr_out, recursive=True):
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
            if is_connected_to(attr_inn, attr, recursive=recursive):
                return True

    return False

#
# get_settable_attr
#

attr_inn_by_out_by_type = {
    'reverse':{
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

