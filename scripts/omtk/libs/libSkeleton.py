"""
Various utility methods that help the job of laying out the skeletton for a Rig.
"""
import pymel.core as pymel
from omtk.libs import libPymel
from maya import OpenMaya
import math


def mirror_obj(obj_src, obj_dst=None):
    """
    Method to mirror joints in behavior.
    This use existing joint and doesn't break the skin or
    the network associated with the joints.
    """
    from omtk.animation import mirrorPose

    if obj_dst is None:
        obj_dst = mirrorPose.get_ctrl_friend(obj_src)
    if obj_src is obj_dst:
        return False
    tm = obj_src.getMatrix(worldSpace=True)
    new_tm = mirrorPose.mirror_matrix(
        tm, mirror_x=True, flip_rot_x=True, flip_rot_y=True, flip_rot_z=True
    )
    obj_dst.setMatrix(new_tm, worldSpace=True)
    return obj_dst


def _check_joint_rotation_attributes(obj):
    """
    Validate the rotation attributes of a joint are free to change
    :param pymel.nodetypes.Joint obj: A joint
    :raises ValueError: If a rotation attribute is not free to change
    """
    for attr in (
        obj.rotateX,
        obj.rotateY,
        obj.rotateZ,
        obj.jointOrientX,
        obj.jointOrientY,
        obj.jointOrientZ,
    ):
        if attr.isFreeToChange() != OpenMaya.MPlug.kFreeToChange:
            raise ValueError(
                "Can't transfer rotation to joint orient. %r is locked." % attr
            )


def transfer_rotation_to_joint_orient(obj):
    """
    Convert ajoint rotation values to orient.

    In Maya it is not possible to do a "makeIdentity" command on a joint
    that is bound to a skin_clusters. This method bypass this limitation.

    :param obj: The joints to act on
    :rtype obj: pymel.nodetypes.Joint
    """
    try:
        _check_joint_rotation_attributes(obj)
    except ValueError as error:
        pymel.warning(error)
        return

    mfn = obj.__apimfn__()

    # Get current rotation
    rotation = OpenMaya.MEulerRotation()
    mfn.getRotation(rotation)

    # Get current joint orient
    joint_orient = OpenMaya.MEulerRotation()
    mfn.getOrientation(joint_orient)

    # Compute new rotation
    result = rotation.reorder(OpenMaya.MEulerRotation.kXYZ) * joint_orient

    obj.jointOrientX.set(math.degrees(result.x))
    obj.jointOrientY.set(math.degrees(result.y))
    obj.jointOrientZ.set(math.degrees(result.z))
    obj.rotateX.set(0.0)
    obj.rotateY.set(0.0)
    obj.rotateZ.set(0.0)


def transfer_joint_orient_to_rotation(obj):
    """
    Convert a joint orient values to rotation.
    
    :param pymel.nodetypes.Joint obj: A joint
    """
    try:
        _check_joint_rotation_attributes(obj)
    except ValueError as error:
        pymel.warning(error)
        return

    mfn = obj.__apimfn__()

    # Get current rotation
    rotation = OpenMaya.MEulerRotation()
    mfn.getRotation(rotation)
    rotation_order = mfn.rotationOrder()

    # Get current joint orient
    joint_orient = OpenMaya.MEulerRotation()
    mfn.getOrientation(joint_orient)

    # Compute new rotation
    result = rotation * joint_orient.reorder(rotation_order)

    obj.jointOrientX.set(0.0)
    obj.jointOrientY.set(0.0)
    obj.jointOrientZ.set(0.0)
    obj.rotateX.set(math.degrees(result.x))
    obj.rotateY.set(math.degrees(result.y))
    obj.rotateZ.set(math.degrees(result.z))


def mirror_jnt(obj_src):
    """
    Mirror a a joint transform from one side to another.
    For example, mirroring a jnt_arm_l to a jnt_arm_r.
    This will create the other joint if needed, otherwise it will re-use it.

    :param obj_src: The joint to mirror
    :type obj_src: pymel.nodetypes.Joint
    :return: The mirrored joint
    :rtype: pymel.nodetypes.Joint
    """
    from omtk.animation import mirrorPose

    obj_dst = mirrorPose.get_ctrl_friend(obj_src)
    if obj_dst is None:
        src_name = obj_src.name()
        dst_name = mirrorPose.get_name_friend(src_name)
        if src_name == dst_name:
            return False

        obj_dst = pymel.createNode("joint")
        obj_dst.rename(dst_name)

        obj_src_parent = obj_src.getParent()
        if obj_src_parent:
            obj_dst_parent = mirrorPose.get_ctrl_friend(obj_src_parent)
            if obj_dst_parent:
                obj_dst.setParent(obj_dst_parent)

    mirror_obj(obj_src, obj_dst)
    if isinstance(obj_src, pymel.nodetypes.Joint) and isinstance(
        obj_dst, pymel.nodetypes.Joint
    ):
        transfer_rotation_to_joint_orient(obj_dst)
        obj_dst.radius.set(obj_src.radius.get())

    return obj_dst


def mirror_jnts(objs):
    """
    Mirror a a joint transform from one side to another.
    For example, mirroring a jnt_arm_l to a jnt_arm_r.
    This will create the other joint if needed, otherwise it will re-use it.

    :param objs: The joints to mirror
    :type: objs: list of pymel.nodetypes.Joint
    """
    # Sort objects by hierarchy so we mirror parents before their children.
    objs = sorted(objs, key=libPymel.get_num_parents)
    with pymel.UndoChunk():
        for obj in objs:
            mirror_jnt(obj)
