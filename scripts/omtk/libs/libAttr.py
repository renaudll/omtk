from contextlib import contextmanager
import logging
import re


# src: http://download.autodesk.com/us/maya/2010help/CommandsPython/addAttr.html
from pymel import core as pymel

log = logging.getLogger('omtk')


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


def hold_attrs(attr, hold_curve=True):
    """
    Hold a specific @attr attribute.
    """
    if isinstance(attr, pymel.Attribute):
        if not hold_curve or attr.isLocked() or not attr.isKeyable():
            return attr.get()

        for input in attr.inputs(plugs=True):
            if isinstance(input.node(),
                          (pymel.nodetypes.AnimCurve, pymel.nodetypes.BlendWeighted)):
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
    attr = addAttr(obj, longName=attr_name, niceName=attr_name, at='enum',
                   en='------------', k=True)
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


def connect_transform_attrs(src, dst, tx=True, ty=True, tz=True, rx=True, ry=True,
                            rz=True, sx=True, sy=True, sz=True,
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
            if is_connected_to(attr_inn, attr, recursive=recursive, max_depth=max_depth,
                               depth=depth + 1):
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


def connect_t_to_avar():
    """
    Will always call connect_to_avar with the specific needed dict 
    
    :param ctrl: The ctrl we want that will control the fb, ud and lr avar
    :param avar_node: The node on which we can find the avar we want to control
    """

    ctrl = pymel.selected()[0]
    avar_node = pymel.selected()[1]

    avar_info = {"avar_ud": "ty", "avar_fb": "tz", "avar_lr": "tx"}
    connect_to_avar(ctrl, avar_node, avar_info)


def connect_r_to_avar():
    """
    Will always call connect_to_avar with the specific needed dict 

    :param ctrl: The ctrl we want that will control the fb, ud and lr avar
    :param avar_node: The node on which we can find the avar we want to control
    """

    ctrl = pymel.selected()[0]
    avar_node = pymel.selected()[1]

    avar_info = {"avar_yw": "ry", "avar_rl": "rz", "avar_pt": "rx"}
    connect_to_avar(ctrl, avar_node, avar_info)


def connect_to_avar(ctrl, avar_node, mapping_dict):
    """
    Connect the translate attribute of a controller on the specific avar of the avar_node.
    Take into consideration that the calibration should be done done to match 1 at the maximum displacement
    
    :param ctrl: The ctrl we want that will control the fb, ud and lr avar
    :param avar_node: The node on which we can find the avar we want to control
    :param mapping_dict: Dictionary in which the key represent the avar attribute name and the value the ctrl attribute
                         that will drive this avar
    """
    regex_input_idx = "^input[[]{1}(\d)[]]{1}$"

    # First get the weightBlended from the needed avar
    for avar_name, ctrl_attr_name in mapping_dict.iteritems():
        bw_list = avar_node.attr(avar_name).listConnections(c=False, d=False,
                                                            t="blendWeighted")
        if len(bw_list) != 1:
            raise (
                "Could not connect ctrl {0} translation in avar node {1}".format(ctrl,
                                                                                 avar_node))
        match = re.search(regex_input_idx, bw_list[0].input.elements()[-1])
        input_idx = int(match.group(1)) + 1
        pymel.connectAttr(ctrl.attr(ctrl_attr_name), bw_list[0].input[input_idx])

    pymel.select(ctrl)


def connect_attr_to_visibility(input_attr_name):
    """
    This function will connect the input attribute into the visibility attribute of the selected objects.
    If the output attribute is already connected, the function will try to see if it can be plugged
    in parallel with it by using a multiple divide. If a multiple divide is found, the function will connect
    to the next available input in it
     
    At the moment, the function only support attribute that can be connected in a multiple divide
    
    :param input_attr_name: The attribute which will serve as an input to drive the output attr. It need to be pass
                       with it's full path (ex: Ctrl_Grp.visibility)
    """

    vis_attr_string = "visibility"
    in_attr = pymel.Attribute(input_attr_name)
    # in_attr_node = in_attr.node()
    cur_sel = pymel.selected()

    for sel in cur_sel:
        if not sel.hasAttr(vis_attr_string):
            continue
        vis_attr = sel.attr(vis_attr_string)
        con = vis_attr.listConnections(c=False, d=False, p=True)
        num_con = len(con)
        if num_con > 1:
            # More than one connection ?? Should not happen
            continue
        elif num_con == 0:
            # Do the direct connection
            pymel.connectAttr(in_attr, vis_attr)
        # prevent some useless node to be in the scene
        else:
            # TODO - Find a better way to detect if the attr is already connected or not. This one can possibly
            # not work since listHistory is not specific to the attribute
            '''
            # If the selected node already have a connection to the input attribute, skip it
            vis_hist = vis_attr.listHistory()
            if in_attr_node in vis_hist:
                continue
            '''
            # Keep the current connected attr, and setup multipleDoubleLinear
            cur_con = con[0]
            mdl = pymel.createNode("multDoubleLinear")
            pymel.connectAttr(cur_con, mdl.input1)
            pymel.connectAttr(in_attr, mdl.input2)
            # Force the connection
            pymel.connectAttr(mdl.output, vis_attr, force=True)


def disconnect_trs(obj, inputs=True, outputs=True):
    attr_names = ['t', 'tx', 'ty', 'tz', 'r', 'rx', 'ry', 'rz', 's', 'sx', 'sy', 'sz']
    for attr_name in attr_names:
        attr = obj.attr(attr_name)
        disconnectAttr(attr, inputs=inputs, outputs=outputs)
