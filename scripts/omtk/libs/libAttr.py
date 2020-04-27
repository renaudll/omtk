from contextlib import contextmanager
import logging

from pymel import core as pymel

log = logging.getLogger("omtk")


def disconnectAttr(attr, inputs=True, outputs=True):
    """
    Disconnect an attribute incoming and outgoing connections.

    :param attr: The attribute to disconnect
    :type attr: pymel.Attribute
    :param bool inputs: Should we disconnect input connections?
    :param bool outputs: Should we disconnect output connections?
    """
    attr_is_locked = attr.isLocked()
    if attr_is_locked:
        attr.unlock()

    if inputs:
        for attr_in in attr.inputs(plugs=True):
            pymel.disconnectAttr(attr_in, attr)
    if outputs:
        for attr_out in attr.outputs(plugs=True):
            pymel.disconnectAttr(attr, attr_out)

    if attr_is_locked:
        attr.lock()


def hold_attrs(attr, hold_curve=True):
    """
    Hold an attribute value or connection source.

    :param attr: An attribute to hold
    :type attr: pymel.Attribute
    :return: The attribute scalar value if unconnected, otherwise the connection source.
    :rtype: object or pymel.Attribute
    """
    if isinstance(attr, pymel.Attribute):
        if not hold_curve or attr.isLocked() or not attr.isKeyable():
            return attr.get()

        for input in attr.inputs(plugs=True):
            if isinstance(
                input.node(), (pymel.nodetypes.AnimCurve, pymel.nodetypes.BlendWeighted)
            ):
                pymel.disconnectAttr(
                    input, attr
                )  # disconnect the animCurve so it won't get deleted automaticly after unbuilding the rig
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
    """
    Wrapper around pymel.addAttr that return the created attribute.

    :param node: The node to add the attribute to
    :type node: pymel.nodetypes.DependNode
    :param str longName: The attribute longName
    :param tuple args: Positional arguments are forwarded to pymel.addAttr.
    :param dict kwargs: Keyword arguments are forwarded to pymel.addAttr.
    :return: The created attribute
    :rtype: pymel.Attribute
    """
    assert longName
    pymel.addAttr(node, longName=longName, *args, **kwargs)
    return node.attr(longName)


def addAttr_separator(node, attr_name, *args, **kwargs):
    """
    Add a no-op attribute that serve as a visual separator.

    :param node: The node to add the attribute to
    :type node: pymel.nodetypes.DependNode
    :param str attr_name: The attribute longName
    """
    # TODO: properly remove args and kwargs
    attr = addAttr(
        node,
        longName=attr_name,
        niceName=attr_name,
        at="enum",
        en="------------",
        k=True,
    )
    attr.lock()


# Lock/unlock Function


def lock_trs(node):
    """
    Lock a node translate, rotate and scale attributes.
    :param node: The node to lock
    """
    lock_translation(node)
    lock_rotation(node)
    lock_scale(node)


def unlock_trs(node):
    """
    Unlock a node translate, rotate and scale attributes.
    :param node: The node to unlock
    """
    unlock_translation(node)
    unlock_rotation(node)
    unlock_scale(node)


def lock_translation(node, x=True, y=True, z=True):
    if x:
        node.translateX.lock()
    if y:
        node.translateY.lock()
    if z:
        node.translateZ.lock()


def unlock_translation(node, x=True, y=True, z=True, xyz=True):
    if x:
        node.translateX.unlock()
    if y:
        node.translateY.unlock()
    if z:
        node.translateZ.unlock()
    if xyz:
        node.translate.unlock()


def lock_rotation(node, x=True, y=True, z=True):
    if x:
        node.rotateX.lock()
    if y:
        node.rotateY.lock()
    if z:
        node.rotateZ.lock()


def unlock_rotation(node, x=True, y=True, z=True, xyz=True):
    if x:
        node.rotateX.unlock()
    if y:
        node.rotateY.unlock()
    if z:
        node.rotateZ.unlock()
    if xyz:
        node.rotate.unlock()


def lock_scale(node, x=True, y=True, z=True):
    if x:
        node.scaleX.lock()
    if y:
        node.scaleY.lock()
    if z:
        node.scaleZ.lock()


def unlock_scale(node, x=True, y=True, z=True, xyz=True):
    if x:
        node.scaleX.unlock()
    if y:
        node.scaleY.unlock()
    if z:
        node.scaleZ.unlock()
    if xyz:
        node.scale.unlock()


def connect_transform_attrs(
    src,
    dst,
    tx=True,
    ty=True,
    tz=True,
    rx=True,
    ry=True,
    rz=True,
    sx=True,
    sy=True,
    sz=True,
    force=False,
):
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


def hide_trs(node):
    """
    Hide a node translate, rotate and scale attribute.

    :param node: The node to hide
    :type node: pymel.nodetypes.DependNode
    """
    hide_translation(node)
    hide_rotation(node)
    hide_scale(node)


def unhide_trs(node):
    """
    Unhide a node translate, rotate and scale attribute.

    :param node: The node to unhide
    :type node: pymel.nodetypes.DependNode
    """
    unhide_translation(node)
    unhide_rotation(node)
    unhide_scale(node)


def hide_translation(node, x=True, y=True, z=True):
    if x:
        node.translateX.setKeyable(False)
    if y:
        node.translateY.setKeyable(False)
    if z:
        node.translateZ.setKeyable(False)


def unhide_translation(node, x=True, y=True, z=True):
    if x:
        node.translateX.setKeyable(True)
    if y:
        node.translateY.setKeyable(True)
    if z:
        node.translateZ.setKeyable(True)


def hide_rotation(node, x=True, y=True, z=True):
    if x:
        node.rotateX.setKeyable(False)
    if y:
        node.rotateY.setKeyable(False)
    if z:
        node.rotateZ.setKeyable(False)


def unhide_rotation(node, x=True, y=True, z=True):
    if x:
        node.rotateX.setKeyable(True)
    if y:
        node.rotateY.setKeyable(True)
    if z:
        node.rotateZ.setKeyable(True)


def hide_scale(node, x=True, y=True, z=True):
    if x:
        node.scaleX.setKeyable(False)
    if y:
        node.scaleY.setKeyable(False)
    if z:
        node.scaleZ.setKeyable(False)


def unhide_scale(node, x=True, y=True, z=True):
    if x:
        node.scaleX.setKeyable(True)
    if y:
        node.scaleY.setKeyable(True)
    if z:
        node.scaleZ.setKeyable(True)


# Lock/Hide shortcut


def lock_hide_trs(node):
    lock_trs(node)
    hide_trs(node)


def unlock_unhide_trs(node):
    unlock_trs(node)
    unhide_trs(node)


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
        if "[" in attr.name():
            continue

        if attr == attr_inn:
            return True
        else:
            if depth >= max_depth:
                return False
            if is_connected_to(
                attr_inn,
                attr,
                recursive=recursive,
                max_depth=max_depth,
                depth=depth + 1,
            ):
                return True

    return False


#
# get_settable_attr
#

attr_inn_by_out_by_type = {
    "reverse": {"outputX": "inputX", "outputY": "inputY", "outputZ": "inputZ"}
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
        if any(True for token in classification if "utility" in token):
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
    A context (use with the 'with' statement) to apply instruction while
    ensuring the provided attributes are disconnected temporarily.
    :param attrs: Redirected to hold_connections.
    """
    data = hold_connections(attrs, hold_inputs=hold_inputs, hold_outputs=hold_outputs)
    yield True
    fetch_connections(data)


def disconnect_trs(obj, inputs=True, outputs=True):
    attr_names = ["t", "tx", "ty", "tz", "r", "rx", "ry", "rz", "s", "sx", "sy", "sz"]
    for attr_name in attr_names:
        attr = obj.attr(attr_name)
        disconnectAttr(attr, inputs=inputs, outputs=outputs)
