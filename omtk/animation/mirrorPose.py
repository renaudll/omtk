import pymel.core as pymel
from maya import cmds
from omtk.libs import libPymel

class Axis:
    x = 'X'
    y = 'Y'
    z = 'Z'


def flip_matrix_axis_pos(tm, axis):
    if axis == Axis.x:
        tm.a30 *= -1.0
    elif axis == Axis.y:
        tm.a31 *= -1.0
    elif axis == Axis.z:
        tm.a32 *= -1.0
    else:
        raise Exception("Unsupported axis. Got {0}".format(axis))


def flip_matrix_axis_rot(tm, axis):
    """
    Utility function to mirror the x, y or z axis of an provided matrix.
    :param tm: The pymel.datatypes.Matrix to flip.
    :param axis: The axis to flip.
    :return: The resulting pymel.datatypes.Matrix.
    """
    if axis == Axis.x:
        tm.a00 *= -1.0
        tm.a01 *= -1.0
        tm.a02 *= -1.0
    elif axis == Axis.y:
        tm.a10 *= -1.0
        tm.a11 *= -1.0
        tm.a12 *= -1.0
    elif axis == Axis.z:
        tm.a20 *= -1.0
        tm.a21 *= -1.0
        tm.a22 *= -1.0
    else:
        raise Exception("Unsupported axis. Got {0}".format(axis))


def get_ctrl_fiend(obj_src):
    obj_src_name = obj_src.name()

    # Resolve obj_dst_name
    obj_dst_name = None
    # TODO: find a better algorythm
    if '_l_' in obj_src_name:
        obj_dst_name = obj_src_name.replace('_l_', '_r_')
    elif '_r_' in obj_src_name:
        obj_dst_name = obj_src_name.replace('_r_', '_l_')

    if obj_dst_name is None:
        print("Can't find ctrl friend of {0}".format(obj_src_name))
        return None

    if not cmds.objExists(obj_dst_name):
        print ("Can't find ctrl named {0}".format(obj_dst_name))
        return None

    return pymel.PyNode(obj_dst_name)


def mirror_matrix(tm_inn, parent_ref=None, flip_x=True, flip_y=True, flip_z=False):
    """
    Mirror a pose using the local matrix and a flip vector.
    Note that you can store the flip vector in the BaseCtrl instance of each ctrls.
    :param tm_inn: The source object containing the pose we want to mirror.
    :param obj_dst: The target object on witch we want to mirror to.
    """

    tm_flip = pymel.datatypes.Matrix(-1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1)

    if parent_ref is None:
        parent_ref = pymel.datatypes.Matrix()

    tm = tm_inn * (tm_flip * parent_ref.inverse())

    #print "Source Matrix: {0}".format(tm)

    if flip_x:
        flip_matrix_axis_rot(tm, Axis.x)
    if flip_y:
        flip_matrix_axis_rot(tm, Axis.y)
    if flip_z:
        flip_matrix_axis_rot(tm, Axis.z)

    #print "Target Matrix: {0}".format(tm)

    return tm * parent_ref


def mirror_objs(objs):
    # Resolve desired poses without affecting anything
    tms_by_objs = {}
    for obj_dst in objs:
        # Resolve source object
        obj_src = get_ctrl_fiend(obj_dst)
        if obj_src is None:
            obj_src = obj_dst
        tm_inn = obj_dst.getMatrix(worldSpace=True)
        # HACK: Currently we are only guessing
        # TODO: Store the flip information on the nodes (when the algorithm is approved)
        if obj_src == obj_dst:
            tm_out = mirror_matrix(tm_inn, flip_x=False, flip_y=True, flip_z=False)
        else:
            tm_out = mirror_matrix(tm_inn, flip_x=True, flip_y=True, flip_z=False)

        tms_by_objs[obj_src] = tm_out

    # Apply desired poses
    objs = sorted(tms_by_objs.keys(), key=libPymel.get_num_parents)
    for obj in objs:
        tm = tms_by_objs[obj]
        obj.setMatrix(tm, worldSpace=True)



