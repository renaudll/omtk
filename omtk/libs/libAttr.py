import pymel.core as pymel

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
        'input':next(iter(attr.inputs(plugs=True)), None),
        'outputs':attr.outputs(plugs=True)
    }
    print 1
    pymel.deleteAttr(attr)
    print 2
    return data

def fetchAttr(data):
    node = data['node']
    pymel.addAttr(node,
        longName = data['longName']
    )
    attr = node.attr(data['longName'])

    # Re-connect inputs
    if data['input']:
        pymel.connectAttr(data['input'], attr)

    # Re-connect outputs
    for i, output in enumerate(data['outputs']):
        if output:
            pymel.connectAttr(attr[i], output)

# Normally we can use pymel.renameAttr but this work on multi-attributes also
def renameAttr(attr, new_name):
    assert(isinstance(attr, pymel.Attribute))
    node = attr.node()
    data = holdAttr(attr)
    data['longName'] = new_name
    fetchAttr(attr)

    return True

def addAttr(node, longName=None, *args, **kwargs):
    assert(longName)
    pymel.addAttr(node, longName=longName, *args, **kwargs)
    return node.attr(longName)

