import math
import pymel.core as pymel

# TODO: Move to rigging???

import itertools
VALID_JOINT_ORIENTS=[
    pymel.datatypes.Vector(1,0,0),
    pymel.datatypes.Vector(-1,0,0),
    pymel.datatypes.Vector(0,1,0),
    pymel.datatypes.Vector(0,-1,0),
    pymel.datatypes.Vector(0,0,1),
    pymel.datatypes.Vector(0,0,-1)
]

JOINT_ORIENTS_FILTERS = [
    pymel.datatypes.Vector(1,0,0),
    pymel.datatypes.Vector(1,0,0),
    pymel.datatypes.Vector(0,1,0),
    pymel.datatypes.Vector(0,1,0),
    pymel.datatypes.Vector(0,0,1),
    pymel.datatypes.Vector(0,0,1)
]

# todo: use numpy?
def math_distance(pnt1, pnt2):
    dx = pnt1[0] - pnt2[0]
    dy = pnt1[1] - pnt2[1]
    dz = pnt1[2] - pnt2[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

class JointData(object):
    def __init__(self, jnt):
        self.root = jnt
        self.dir = None
        self.length = None
        self.next = None

        self.postInit(jnt)

    def __repr__(self):
        return '<JointData {0}, {1} to {2}>'.format(self.dir, self.root, self.next)

    def is_valid(self):
        return self.dir is not None

    # todo: clean
    def _get_lookat_info(self, jnt):
        """
        Get lookat node and dir.
        """
        global VALID_JOINT_ORIENTS
        index = None
        min_val = None
        parent_tm_inv = jnt.getMatrix(worldSpace=True).inverse()
        children = jnt.getChildren()
        children_tms = [child.getMatrix(worldSpace=True) for child in jnt.getChildren()]
        closest_jnt = None

        # get lookat child
        for i, orient, filter in zip(xrange(len(VALID_JOINT_ORIENTS)), VALID_JOINT_ORIENTS, JOINT_ORIENTS_FILTERS):
            for child, child_tm in zip(children, children_tms):
                local_pos = (child_tm * parent_tm_inv).translate

                plane = pymel.datatypes.Vector(1,1,1) - filter
                local_pos_plane = pymel.datatypes.Vector(local_pos.x*plane.x, local_pos.y*plane.y, local_pos.z*plane.z)
                local_length  = pymel.datatypes.Vector(local_pos.x*orient.x, local_pos.y*orient.y, local_pos.z*orient.z)


                lookaxis = local_length[0] + local_length[1] + local_length[2]
                if lookaxis > 0:

                    dot = local_pos_plane.length()

                    if not min_val or dot < min_val:
                        min_val = dot
                        index = i
                        closest_jnt = child

        if closest_jnt:
            self.next = closest_jnt
            self.dir = pymel.datatypes.Vector(VALID_JOINT_ORIENTS[index])

    def postInit(self, jnt):
        self._get_lookat_info(jnt)

        # get length
        if self.dir is not None:
            sp = jnt.getTranslation(space='world')
            ep = self.next.getTranslation(space='world')
            self.length = math_distance(sp, ep)

def create_boxes():
    boxes = []
    for jnt in pymel.ls(type='joint'):
        joint_data = JointData(jnt)
        if joint_data.is_valid():
            length = joint_data.length
            print jnt, joint_data
            transform, make = pymel.polyCube(height=length, width=length*0.33, depth=length*0.33)
            r_offset = pymel.datatypes.Matrix(0, -1.0, -0.0, 0.0, 1.0, 0, 0.0, 0.0, 0.0, -0.0, 1.0, 0.0,
                                              joint_data.dir[0]*length*0.5,
                                              joint_data.dir[1]*length*0.5,
                                              joint_data.dir[2]*length*0.5,
                                              1.0)
            cylinder_tm = r_offset
            transform.setParent(jnt)
            transform.setMatrix(cylinder_tm)
            boxes.append(transform)
    return boxes

def collect_proxy_boxes():
    return_values = []
    for obj in pymel.ls(type='transform'):
        if any((hist for hist in obj.listHistory() if isinstance(hist, pymel.nodetypes.PolyCube))):
            if isinstance(obj.getParent(), pymel.nodetypes.Joint):
                return_values.append(obj)
    return return_values

def finalize_boxes():
    # collect weights
    boxes = collect_proxy_boxes()
    jnts = [box.getParent() for box in boxes]
    weights = []
    for i, box in enumerate(boxes):
        weights.extend([i] * len(box.vtx))

    # mergeboxes
    polyUnite = pymel.createNode('polyUnite')
    itt = 0
    for box in boxes:
        for shape in box.getShapes():
            pymel.connectAttr(shape.worldMatrix, polyUnite.inputMat[itt])
            pymel.connectAttr(shape.outMesh, polyUnite.inputPoly[itt])
            itt += 1
    outputMesh = pymel.createNode('mesh')
    pymel.connectAttr(polyUnite.output, outputMesh.inMesh)
    #pymel.delete(boxes)

    # set skin weights
    pymel.skinCluster(jnts, outputMesh.getParent(), toSelectedBones=True)
    skinCluster = next((hist for hist in outputMesh.listHistory() if isinstance(hist, pymel.nodetypes.SkinCluster)), None)
    for vtx, inf in zip(iter(outputMesh.vtx), weights):
        skinCluster.setWeights(vtx, [inf], [1])

# src: http://tech-artists.org/forum/showthread.php?4384-Vector-math-and-Maya
from pymel.core.datatypes import Vector, Matrix, Point
def matrix_from_normal(up_vect, front_vect):
    # normalize first!
    up_vect.normalize()
    front_vect.normalize()

    #get the third axis with the cross vector
    side_vect = Vector.cross(up_vect, front_vect)
    #recross in case up and front were not originally orthoganl:
    front_vect = Vector.cross(side_vect, up_vect )

    #the new matrix is
    return Matrix (
        side_vect.x, side_vect.y, side_vect.z, 0,
        up_vect.x, up_vect.y, up_vect.z, 0,
        front_vect.x, front_vect.y, front_vect.z, 0,
        0,0,0,1)

from pymel.core.datatypes import Vector, Matrix

def get_matrix_from_direction(look_vec, upp_vec):
    # Ensure we deal with normalized vectors
    look_vec.normalize()
    upp_vec.normalize()

    side_vec = Vector.cross(look_vec, upp_vec)
    #recross in case up and front were not originally orthogonal:
    upp_vec = Vector.cross(side_vec, look_vec)

    #the new matrix is
    return Matrix (
        look_vec.x, look_vec.y, look_vec.z, 0,
        upp_vec.x, upp_vec.y, upp_vec.z, 0,
        side_vec.x, side_vec.y, side_vec.z, 0,
        0, 0, 0, 1)

def debug_pos(pos):
    l = pymel.spaceLocator()
    l.setTranslation(pos)

def debug_tm(tm):
    l = pymel.spaceLocator()
    l.setMatrix(tm)
    l.s.set(10,10,10)

def align_joints_to_view(joints, cam, affect_pos=True):
    """
    Align the up axis of selected joints to the look axis of a camera.
    Similar to an existing functionnality in blender.
    """

    pos_start = joints[0].getTranslation(space='world')

    # Get camera direction
    cam_tm = cam.getMatrix(worldSpace=True)
    cam_pos = cam.getTranslation(space='world')
    cam_upp = cam_pos - pos_start
    cam_upp.normalize()

    # Store original positions
    positions_orig = [joint.getTranslation(space='world') for joint in joints]

    # Compute positions that respect the plane
    positions = []
    if affect_pos:

        pos_inn = positions_orig[0]
        pos_out = positions_orig[-1]
        look_axis = pos_out - pos_inn
        ref_tm = get_matrix_from_direction(look_axis, cam_upp)
        ref_tm.translate = pos_inn
        ref_tm_inv = ref_tm.inverse()

        for i in range(len(joints)):
            joint = joints[i]
            joint_pos = positions_orig[i]
            if i == 0:
                positions.append(joint_pos)
            else:
                joint_local_pos = (joint_pos - pos_start) * ref_tm_inv
                joint_local_pos.z = 0
                new_joint_pos = (joint_local_pos * ref_tm) + pos_start
                positions.append(new_joint_pos)
    else:
        for joint in joints:
            positions.append(joint.getTranslation(space='world'))


    # Compute transforms
    transforms = []
    num_positions = len(positions)
    for i in range(num_positions):
        pos_inn = positions[i]

        # Compute rotation-only matrix
        if i < num_positions-1:
            pos_out = positions[i+1]
            # Compute look axis
            x_axis = pos_out - pos_inn
            x_axis.normalize()

            # Compute side axis
            z_axis = pymel.datatypes.Vector(x_axis).cross(cam_upp)

            # Compute up axis (corrected)
            y_axis = z_axis.cross(x_axis)

            # Next ref_y_axis will use parent correct up axis to prevent flipping
            cam_upp = y_axis

            tm = get_matrix_from_direction(x_axis, y_axis)
        else:
            tm = transforms[i-1].copy() # Last joint share the same rotation as it's parent

        # Add translation
        if affect_pos:
            tm.translate = pos_inn
        else:
            tm.translate = positions_orig[i]

        transforms.append(tm)

    # Apply transforms
    for transform, node in zip(transforms, joints):
        node.setMatrix(transform, worldSpace=True)



def align_selected_joints_to_persp ():
    sel = pymel.selected()
    cam = pymel.PyNode('persp')
    align_joints_to_view(sel, cam)
