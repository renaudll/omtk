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
    This use existing joint and doesn't break the skin or the network associated with the joints.
    """
    from omtk.animation import mirrorPose
    if obj_dst is None:
        obj_dst = mirrorPose.get_ctrl_friend(obj_src)
    if obj_src is obj_dst:
        return False
    tm = obj_src.getMatrix(worldSpace=True)
    new_tm = mirrorPose.mirror_matrix(tm, mirror_x=True, flip_rot_x=True, flip_rot_y=True, flip_rot_z=True)
    obj_dst.setMatrix(new_tm, worldSpace=True)
    return obj_dst

def transfer_rotation_to_joint_orient(obj):
    """
    In Maya it is not possible to do a "makeIdentity" command on a joint that is bound to a skinCluster.
    This method bypass this limitation.
    """
    mfn = obj.__apimfn__()

    rotation_orig = OpenMaya.MEulerRotation()
    mfn.getRotation(rotation_orig)
    rotation_xyz = rotation_orig.reorder(OpenMaya.MEulerRotation.kXYZ)

    # Apply existing jointOrient values
    orientation_orig = OpenMaya.MEulerRotation()
    mfn.getOrientation(orientation_orig)
    rotation_xyz *= orientation_orig

    def is_attr_accessible(attr):
        return not attr.isFreeToChange() == OpenMaya.MPlug.kFreeToChange

    if is_attr_accessible(obj.rotateX) or is_attr_accessible(obj.rotateY) or is_attr_accessible(obj.rotateZ):
        pymel.warning("Can't transfer rotation to joint orient. {0} rotation is locked.".format(obj.name()))
        return

    if is_attr_accessible(obj.jointOrientX) or is_attr_accessible(obj.jointOrientY) or is_attr_accessible(obj.jointOrientZ):
        pymel.warning("Can't transfer rotation to joint orient. {0} jointOrient is locked.".format(obj.name()))
        return

    obj.jointOrientX.set(math.degrees(rotation_xyz.x))
    obj.jointOrientY.set(math.degrees(rotation_xyz.y))
    obj.jointOrientZ.set(math.degrees(rotation_xyz.z))
    obj.rotateX.set(0)
    obj.rotateY.set(0)
    obj.rotateZ.set(0)


def mirror_jnt(obj_src, handle_joint_orient=True, create_missing=True):
    from omtk.animation import mirrorPose
    obj_dst = mirrorPose.get_ctrl_friend(obj_src)
    if obj_dst is None:
        src_name = obj_src.name()
        dst_name = mirrorPose.get_name_friend(src_name)
        if src_name == dst_name:
            return False

        obj_dst = pymel.createNode('joint')
        obj_dst.rename(dst_name)

        obj_src_parent = obj_src.getParent()
        if obj_src_parent:
            obj_dst_parent = mirrorPose.get_ctrl_friend(obj_src_parent)
            if obj_dst_parent:
                obj_dst.setParent(obj_dst_parent)

    mirror_obj(obj_src, obj_dst)
    if handle_joint_orient and isinstance(obj_src, pymel.nodetypes.Joint) and isinstance(obj_dst, pymel.nodetypes.Joint):
        transfer_rotation_to_joint_orient(obj_dst)
        obj_dst.radius.set(obj_src.radius.get())
    return obj_dst

def mirror_jnts(objs, **kwargs):
    # Sort objects by hyerarchy so we mirror parents before their children.
    objs = sorted(objs, key=libPymel.get_num_parents)
    with pymel.UndoChunk():
        for obj in objs:
            mirror_jnt(obj, **kwargs)

def freeze_selected_joints_rotation():
    jnts = [obj for obj in pymel.selected() if isinstance(obj, pymel.nodetypes.Joint)]
    for jnt in jnts:
        if not isinstance(jnt, pymel.nodetypes.Joint):
            pymel.warning("Skipping non-joint {0}".format(jnt))
            continue

        transfer_rotation_to_joint_orient(jnt)


