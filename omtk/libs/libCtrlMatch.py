"""
Library that allow facial ctrls to be matched/mirrored/baked.
Original code by Jimmy Goulet (https://github.com/goujin), thanks for the contribution!
todo: Use className to find sibling.
"""
import pymel.core as pymel
from omtk.libs import libRigging


def get_orig_shape(shape):
    return next((hist for hist in shape.listHistory()
                 if isinstance(hist, pymel.nodetypes.NurbsCurve)
                 and hist != shape
                 and hist.intermediateObject.get()), None)


def safety_check(check_object=None, check_curve_list=None):
    if check_object:
        if not isinstance(check_object, pymel.nodetypes.Transform):
            return False
    elif check_curve_list:
        for each in check_curve_list:
            if not isinstance(each, pymel.nodetypes.NurbsCurve):
                return False


def get_previous_controller_info(previous_controler):
    # this implementation assumes your only using one shape or that the the first shape of children shapes is representative of the lot
    assumed_only_shape = previous_controler.getShape()

    if assumed_only_shape.overrideEnabled.get():  # will return False if it isn't activated
        if assumed_only_shape.overrideRGBColors.get():
            rgb_color = assumed_only_shape.overrideColorRGB.get()
            color_info = [True, True, rgb_color]
        else:
            index_color = assumed_only_shape.overrideColor.get()
            color_info = [True, False, index_color]
    else:
        color_info = [False, False, []]

    if assumed_only_shape.visibility.isConnected():
        visibility_connection_info = assumed_only_shape.visibility.connections(plugs=True)[0]

    else:
        visibility_connection_info = False

    return (color_info, visibility_connection_info)


def adapt_to_orig_shape(source, target):
    """
    :param source: source shape to transfer
    :param target: target to transfer to
     This is based out of Renaud's code on shape to orig when building and unbuilding with omtk to preserve shape info.
    """

    def get_transformGeometry(shape):
        return next((hist for hist in shape.listHistory()
                     if isinstance(hist, pymel.nodetypes.TransformGeometry)), None)

    # Resolve orig shape
    shape_orig = get_orig_shape(target)

    # Resolve compensation matrix
    util_transform_geometry = get_transformGeometry(target)
    if not util_transform_geometry:
        target.warning("Skipping {}. Cannot find transformGeometry.".format(target))
        return
    attr_compensation_tm = next(iter(util_transform_geometry.transform.inputs(plugs=True)), None)

    if not attr_compensation_tm:
        target.warning("Skipping {}. Cannot find compensation matrix.".format(target))
        return

    tmp_transform_geometry = libRigging.create_utility_node(
        'transformGeometry',
        inputGeometry=source.local,
        transform=attr_compensation_tm,
        invertTransform=True
    )

    # source.getParent().setParent(grp_offset) JG modification source should already be in place
    pymel.connectAttr(tmp_transform_geometry.outputGeometry, shape_orig.create)

    # Cleanup
    pymel.refresh(force=True)  # but why do I have to refresh^!
    pymel.disconnectAttr(shape_orig.create)
    pymel.delete(tmp_transform_geometry)


def controller_matcher(selection=None, mirror_prefix=None, flip=True):
    """it will try to find it's match on the other side of the rig
    Select controls curves (ex. 'leg_front_l_ik_ctrl'), and set the mirror prefix ('_l_', '_r_')
    flip is for flipping on the X axis the shapes of the ctrl"""
    if selection is None:
        selection = pymel.selected()

    if not mirror_prefix:
        if len(selection) != 2:
            msg = """The only supported behavior when no mirror_prefix is given, is to have only two controlers selected.
            It will match the first controller to the second one."""
            pymel.warning(msg)
            return "Error"
        transfer_shape(*selection, flip=flip)

    else:

        for selected_object in selection:
            _possible_sides = list(mirror_prefix)
            skip_mechanism = False  # This is in place to protect from possible controller having no mirror prefix at all

            if mirror_prefix[0] in selected_object.name():
                current_side = _possible_sides.pop(0)

            elif mirror_prefix[1] in selected_object.name():
                current_side = _possible_sides.pop(1)

            else:
                skip_mechanism = True

            if skip_mechanism:
                pass
            else:
                target_name = selected_object.name().replace(current_side, _possible_sides[0])
                if pymel.objExists(target_name):
                    target = pymel.PyNode(selected_object.name().replace(current_side, _possible_sides[0]))
                    transfer_shape(selected_object, target, flip=True)


def transfer_shape(source, target, flip=True):
    """it will replace the shape of selected number 2 with the shapes of selected number 1"""

    target_shape = target.getShape(noIntermediate=True)
    target_shape_orig = get_orig_shape(target_shape)

    dup = pymel.duplicate(source, rc=1)[0]
    tmp = pymel.createNode('transform')
    pymel.parent(tmp, dup)
    pymel.xform(tmp, t=(0, 0, 0), ro=(0, 0, 0), scale=(1, 1, 1))
    pymel.parent(tmp, w=1)
    for sh in dup.getShapes(noIntermediate=True):
        pymel.parent(sh, tmp, r=1, s=1)

    pymel.delete(dup)
    temp_grp_negScale = pymel.createNode('transform')
    pymel.parent(tmp, temp_grp_negScale)
    if flip:
        temp_grp_negScale.scaleX.set(-1)

    pymel.parent(tmp, target)
    pymel.delete(temp_grp_negScale)

    pymel.makeIdentity(tmp, t=True)  # this brings translate values at 0 before scale freezing
    pymel.makeIdentity(tmp, apply=True, t=True, r=True, s=True)
    pymel.parent(tmp, w=1)

    color_info, vis_master = get_previous_controller_info(target)

    shapes_has_been_deleted = False
    for sh in tmp.getShapes():
        if target_shape_orig:
            adapt_to_orig_shape(sh, target.getShape())
        else:
            if not shapes_has_been_deleted:
                shapesDel = target.getShapes()
                if shapesDel: pymel.delete(shapesDel)
                shapes_has_been_deleted = True

            pymel.parent(sh, target, r=1, s=1)
            pymel.rename(sh.name(), target.name() + "Shape")

            if color_info[0]:
                if color_info[1]:
                    sh.overrideEnabled.set(True)
                    sh.overrideRGBColors.set(1)
                    sh.overrideColorRGB.set(color_info[2])

                else:
                    sh.overrideEnabled.set(True)
                    sh.overrideRGBColors.set(0)
                    sh.overrideColor.set(color_info[2])

            else:
                sh.overrideEnabled.set(False)

            if vis_master:
                vis_master.connect(sh.visibility)

    pymel.delete(tmp)
