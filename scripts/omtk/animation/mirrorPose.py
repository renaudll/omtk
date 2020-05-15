"""
Pose mirroring tool.
Warning: The mirror functionality of OMTK is in alpha stage. Use it at your own risk!
"""
import itertools

import pymel.core as pymel
from maya import cmds, OpenMaya

from omtk.core import ctrl, constants
from omtk.vendor import libSerialization


def list_from_MMatrix(matrix):
    """
    Convert a matrix object to a list of float.
    :param matrix: A matrix
    :type matrix: pymel.datatypes.Matrix
    :return: A list of 16 floats
    :rtype: list or float
    """
    return [
        matrix(row, column) for row, column in itertools.product(range(4), range(4))
    ]


def mirror_matrix_axis(matrix, axis):
    """
    :param matrix: A matrix to mirror
    :type matrix: pymel.datatypes.Matrix
    """
    flip_tm = OpenMaya.MMatrix()
    if axis == constants.Axis.x:
        OpenMaya.MScriptUtil.createMatrixFromList(
            [-1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], flip_tm
        )
    elif axis == constants.Axis.y:
        OpenMaya.MScriptUtil.createMatrixFromList(
            [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], flip_tm
        )
    elif axis == constants.Axis.z:
        OpenMaya.MScriptUtil.createMatrixFromList(
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1], flip_tm
        )
    else:
        raise Exception("Unsupported axis. Got  %s" % axis)
    return matrix * flip_tm


def flip_matrix_axis_pos(m, axis):
    data = list_from_MMatrix(m)

    if axis == constants.Axis.x:
        data[12] *= -1.0
    elif axis == constants.Axis.y:
        data[13] *= -1.0
    elif axis == constants.Axis.z:
        data[14] *= -1.0
    else:
        raise Exception("Unsupported axis. Got  %s" % axis)

    OpenMaya.MScriptUtil.createMatrixFromList(data, m)
    return m


def flip_matrix_axis_rot(m, axis):
    """
    Utility function to mirror the x, y or z axis of an provided matrix.
    :param m: The pymel.datatypes.Matrix to flip.
    :param axis: The axis to flip.
    :return: The resulting pymel.datatypes.Matrix.
    """
    data = list_from_MMatrix(m)

    if axis == constants.Axis.x:
        data[0] *= -1.0
        data[1] *= -1.0
        data[2] *= -1.0
    elif axis == constants.Axis.y:
        data[4] *= -1.0
        data[5] *= -1.0
        data[6] *= -1.0
    elif axis == constants.Axis.z:
        data[8] *= -1.0
        data[9] *= -1.0
        data[10] *= -1.0
    else:
        raise Exception("Unsupported axis. Got  %s" % axis)

    OpenMaya.MScriptUtil.createMatrixFromList(data, m)
    return m


def get_name_friend(obj_src_name, separator="_"):
    tokens_side_l = ["l", "L", "lf", "LF", "left", "Left"]
    tokens_side_r = ["r", "R", "rt", "RT", "right", "Right"]

    # Resolve obj_dst_name
    tokens_src = obj_src_name.split(separator)
    tokens_dst = []

    for i, token in enumerate(tokens_src):
        for token_side_l, token_side_r in zip(tokens_side_l, tokens_side_r):
            if token == token_side_l:
                token = token_side_r
            elif token == token_side_r:
                token = token_side_l
        tokens_dst.append(token)

    obj_dst_name = separator.join(tokens_dst)

    return obj_dst_name


def get_ctrl_friend(obj_src):
    obj_src_name = obj_src.name()
    obj_dst_name = get_name_friend(obj_src_name)

    if obj_dst_name is None:
        print("Can't find ctrl friend of  %s" % obj_src_name)
        return None

    if not cmds.objExists(obj_dst_name):
        print("Can't find ctrl named  %s" % obj_dst_name)
        return None

    return pymel.PyNode(obj_dst_name)


def mirror_matrix(
    matrix,
    mirror_x=False,
    mirror_y=False,
    mirror_z=False,
    flip_pos_x=False,
    flip_pos_y=False,
    flip_pos_z=False,
    flip_rot_x=False,
    flip_rot_y=False,
    flip_rot_z=False,
):
    """
    Mirror a pose using the local matrix and a flip vector.
    Note that you can store the flip vector in the BaseCtrl instance of each ctrls.
    """

    # Mirror axis if necessary
    # Note that in 99.9% of case we only want to mirror one axis.
    if (mirror_x or mirror_y or mirror_z) and not (
        flip_rot_x or flip_rot_y or flip_rot_z
    ):
        raise Exception(
            "When mirroring, please at least flip one axis, "
            "otherwise you might end of with a right handed matrix!"
        )
    if mirror_x:
        matrix = mirror_matrix_axis(matrix, constants.Axis.x)
    if mirror_y:
        matrix = mirror_matrix_axis(matrix, constants.Axis.y)
    if mirror_z:
        matrix = mirror_matrix_axis(matrix, constants.Axis.z)

    # Flip rotation axises if necessary
    if flip_rot_x:
        matrix = flip_matrix_axis_rot(matrix, constants.Axis.x)
    if flip_rot_y:
        matrix = flip_matrix_axis_rot(matrix, constants.Axis.y)
    if flip_rot_z:
        matrix = flip_matrix_axis_rot(matrix, constants.Axis.z)

    # Flip position if necessary
    if flip_pos_x:
        matrix = flip_matrix_axis_pos(matrix, constants.Axis.x)
    if flip_pos_y:
        matrix = flip_matrix_axis_pos(matrix, constants.Axis.y)
    if flip_pos_z:
        matrix = flip_matrix_axis_pos(matrix, constants.Axis.z)

    return matrix


def get_obj_mirror_def(obj):
    network_is_ctrl = lambda x: libSerialization.is_network_from_class(
        x, ctrl.BaseCtrl.__name__.split(".")[-1]
    )
    networks = libSerialization.get_connected_networks(
        [obj], key=network_is_ctrl, recursive=False
    )
    network = next(iter(networks), None)

    if network:
        # HACK: We read the attributes directly
        try:
            return (
                network.attr("mirror_x").get(),
                network.attr("mirror_y").get(),
                network.attr("mirror_z").get(),
                network.attr("mirror_flip_pos_x").get(),
                network.attr("mirror_flip_pos_y").get(),
                network.attr("mirror_flip_pos_z").get(),
                network.attr("mirror_flip_rot_x").get(),
                network.attr("mirror_flip_rot_y").get(),
                network.attr("mirror_flip_rot_z").get(),
            )
        except pymel.MayaAttributeError as e:
            print(str(e))

    # If we cannot resolve the ctrl data, take a guess?
    pymel.warning("Can't resolve mirror data for  %s" % obj)


def mirror_objs(objs):
    # Only work on transforms
    objs = filter(
        lambda obj: isinstance(obj, pymel.nodetypes.Transform)
        and not isinstance(obj, pymel.nodetypes.Constraint),
        objs,
    )

    # Resolve desired poses without affecting anything
    tms_by_objs = {}
    for obj_dst in objs:
        # Resolve source object
        obj_src = get_ctrl_friend(obj_dst) or obj_dst

        # Resolve mirror definition
        # If we didn't find any friend, we'll use a default mirror definition.
        data = get_obj_mirror_def(obj_dst)
        if data is None:
            continue

        matrix = obj_dst.__apimfn__().transformation().asMatrix()
        matrix = mirror_matrix(matrix, *data)
        tms_by_objs[obj_src] = OpenMaya.MTransformationMatrix(matrix)

    # Apply desired poses
    cmds.undoInfo(openChunk=True)
    for mfn_transform_src, tm in tms_by_objs.items():
        # HACK: Use cmds so undoes are working
        # mfn_transform_src.set(tm)
        cmds.xform(
            mfn_transform_src.__melobject__(), matrix=list_from_MMatrix(tm.asMatrix())
        )
    cmds.undoInfo(closeChunk=True)
