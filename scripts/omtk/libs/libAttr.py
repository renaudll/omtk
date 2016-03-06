import pymel.core as pymel

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
            if isinstance(input.node(), (pymel.nodetypes.AnimCurve, pymel.nodetypes.BlendWeighted)):
                pymel.disconnectAttr(input, attr) # disconnect the animCurve so it won't get deleted automaticly after unbuilding the rig
                return input
        return attr.get()
    return attr


def fetch_attr(source, target):
    """
    Restore a specific @attr attribute.
    Returns: the destination attribute.
    """
    if target.isLocked():
        pymel.warning("Can't fetch locked attribute {0}.".format(target.__melobject__()))
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

'''
TODO : Implement Lock Hide function
def lock_position(node, x=True, y=True, z=True):

def lock_rotation(node, x=True, y=True, z=True):

def lock_scale(node, x=True, y=True, z=True):
'''
