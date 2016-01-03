import pymel.core as pymel
from maya import cmds, OpenMaya
from omtk.libs import libPymel, libPython

class Axis:
    x = 'X'
    y = 'Y'
    z = 'Z'


def list_from_MMatrix(m):
    # TODO: There's got to be a better way!
    #m = OpenMaya.MTransformationMatrix().asMatrix()
    return [
        m(0, 0),
        m(0, 1),
        m(0, 2),
        m(0, 3),
        m(1, 0),
        m(1, 1),
        m(1, 2),
        m(1, 3),
        m(2, 0),
        m(2, 1),
        m(2, 2),
        m(2, 3),
        m(3, 0),
        m(3, 1),
        m(3, 2),
        m(3, 3)
    ]


def flip_matrix_axis_pos(m, axis):
    data = list_from_MMatrix(m)

    if axis == Axis.x:
        data[12] *= -1.0
    elif axis == Axis.y:
        data[13] *= -1.0
    elif axis == Axis.z:
        data[14] *= -1.0
    else:
        raise Exception("Unsupported axis. Got {0}".format(axis))

    OpenMaya.MScriptUtil.createMatrixFromList(data, m)
    return m


def flip_matrix_axis_rot_plane(m, axis):
    data = list_from_MMatrix(m)

    if axis == Axis.x:
        data[0] *= -1.0
    elif axis == Axis.y:
        data[4] *= -1.0
    elif axis == Axis.z:
        data[8] *= -1.0
    else:
        raise Exception("Unsupported axis. Got {0}".format(axis))

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

    if axis == Axis.x:
        data[0] *= -1.0
        data[1] *= -1.0
        data[2] *= -1.0
    elif axis == Axis.y:
        data[4] *= -1.0
        data[5] *= -1.0
        data[6] *= -1.0
    elif axis == Axis.z:
        data[8] *= -1.0
        data[9] *= -1.0
        data[10] *= -1.0
    else:
        raise Exception("Unsupported axis. Got {0}".format(axis))

    OpenMaya.MScriptUtil.createMatrixFromList(data, m)
    return m


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


def mirror_matrix(m, parent_ref=None, mirror=False,
                  flip_pos_x=False, flip_pos_y=False, flip_pos_z=False,
                  flip_rot_x=False, flip_rot_y=False, flip_rot_z=False,
                  mirror_x=False, mirror_y=False, mirror_z=False):
    """
    Mirror a pose using the local matrix and a flip vector.
    Note that you can store the flip vector in the BaseCtrl instance of each ctrls.
    """
    '''

    tm_flip = OpenMaya.MTransformationMatrix(m_flip)

    if parent_ref is None:
        parent_ref = OpenMaya.MTransformationMatrix()

    tm = OpenMaya.MTransformationMatrix(tm_inn.asMatrix() * parent_ref.asMatrixInverse())
    '''

    if mirror:
        if mirror and not (flip_rot_x or flip_rot_y or flip_rot_z):
            raise Exception("When mirroring, please at least flip one axis, otherwise you might end of with a right handed matrix!")

        m_flip = OpenMaya.MMatrix()
        OpenMaya.MScriptUtil.createMatrixFromList([-1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], m_flip)
        m = m * m_flip

    if flip_pos_x:
        flip_matrix_axis_pos(m, Axis.x)
    if flip_pos_y:
        flip_matrix_axis_pos(m, Axis.y)
    if flip_pos_z:
        flip_matrix_axis_pos(m, Axis.z)

    if mirror_x:
        flip_matrix_axis_rot_plane(m, Axis.x)
    if mirror_y:
        flip_matrix_axis_rot_plane(m, Axis.y)
    if mirror_z:
        flip_matrix_axis_rot_plane(m, Axis.z)

    if flip_rot_x:
        flip_matrix_axis_rot(m, Axis.x)
    if flip_rot_y:
        flip_matrix_axis_rot(m, Axis.y)
    if flip_rot_z:
        flip_matrix_axis_rot(m, Axis.z)


# @libPython.profiler
@libPython.log_execution_time(__name__)
def mirror_objs(objs):
    # Only work on transforms
    objs = filter(lambda obj: isinstance(obj, pymel.nodetypes.Transform) and not isinstance(obj, pymel.nodetypes.Constraint), objs)

    # Resolve desired poses without affecting anything
    tms_by_objs = {}
    for obj_dst in objs:
        # Resolve source object
        obj_src = get_ctrl_fiend(obj_dst)
        if obj_src is None:
            obj_src = obj_dst
        #tm_parent = obj_dst.getParent().getMatrix(worldSpace=True) if obj_dst.getParent() else pymel.datatypes.Matrix()
        #tm_inn = obj_dst.getMatrix(worldSpace=False)

        mfn_transform_src = obj_src.__apimfn__()
        mfn_transform_dst = obj_dst.__apimfn__()
        tm_inn = mfn_transform_dst.transformation()
        m = tm_inn.asMatrix()
        # HACK: Currently we are only guessing
        # TODO: Store the flip information on the nodes (when the algorithm is approved)
        if obj_src == obj_dst:
            mirror_matrix(m, mirror=True, flip_rot_x=True)
        else:
            mirror_matrix(m, mirror=False,
                             flip_pos_x=True, flip_pos_y=True, flip_pos_z=True,
                             flip_rot_x=False, flip_rot_y=False, flip_rot_z=False,
                             mirror_x=False, mirror_y=False, mirror_z=False
                         )

        tms_by_objs[obj_src] = OpenMaya.MTransformationMatrix(m)

    # Apply desired poses
    cmds.undoInfo(openChunk=True)
    for mfn_transform_src in tms_by_objs.keys():
        tm = tms_by_objs[mfn_transform_src]
        # HACK: Use cmds so undoes are working
        # mfn_transform_src.set(tm)
        cmds.xform(mfn_transform_src.__melobject__(), matrix=list_from_MMatrix(tm.asMatrix()))
    cmds.undoInfo(closeChunk=True)



