"""
Various utility methods that help the job of laying out the skeletton for a Rig.
"""
import pymel.core as pymel
from omtk.animation import mirrorPose
from omtk.libs import libPymel


def mirror_jnt(obj_src, obj_dst=None):
    """
    Method to mirror joints in behavior.
    This use existing joint and doesn't break the skin or the network associated with the joints.
    """
    if obj_dst is None:
        obj_dst = mirrorPose.get_ctrl_friend(obj_src)
    if obj_src is obj_dst:
        return
    tm = obj_src.getMatrix(worldSpace=True)
    new_tm = mirrorPose.mirror_matrix(tm, mirror_x=True, flip_rot_x=True, flip_rot_y=True, flip_rot_z=True)
    obj_dst.setMatrix(new_tm, worldSpace=True)


def mirror_selected_joints():
    for obj in pymel.selected():
        mirror_jnt(obj)


def mirror_jnts_l_to_r():
    jnts = sorted(pymel.ls('L_*_Jnt', type='joint'), key=libPymel.get_num_parents)
    for jnt in jnts:
        mirror_jnt(jnt)


def mirror_jnts_r_to_l():
    jnts = sorted(pymel.ls('R_*_Jnt', type='joint'), key=libPymel.get_num_parents())
    for jnt in jnts:
        mirror_jnt(jnt)
