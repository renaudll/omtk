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

def align_joints_to_view(joints, cam):
    cam_tm = cam.getMatrix()
    sel = pymel.selected()

    transforms = []
    parentdir = pymel.datatypes.Matrix()
    for i in range(len(sel)-1):
        s = sel[i].getTranslation(space='world')
        e = sel[i+1].getTranslation(space='world')
        x_axis = pymel.datatypes.Vector(s[0]-e[0], s[1]-e[1], s[2]-e[2])
        x_axis.normalize()
        #cam_tm = cam_tm * parentdir
        y_axis = pymel.datatypes.Vector(cam_tm.data[2][0], cam_tm.data[2][1], cam_tm.data[2][2]).normal()
        z_axis = pymel.datatypes.Vector(x_axis).cross(y_axis)
        y_axis = x_axis.cross(z_axis)

        transforms.append(matrix_from_normal(
            (e - s),
            y_axis
        ))

    for transform, node in zip(transforms, pymel.selected()):
        node.setParent(world=True)
        node.setMatrix(transform, worldSpace=True)

def align_selected_joints_to_persp ():
    sel = pymel.selected()
    cam = pymel.PyNode('persp')
    align_joints_to_view(sel, cam)


