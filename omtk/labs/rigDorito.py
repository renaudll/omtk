import os
import pymel.core as pymel
from maya import cmds, mel  # djrivet
import omtk
from classNameMap import NameMap
from classRigCtrl import RigCtrl
from classRigPart import RigPart
from omtk.libs import libRigging

"""
A Dorito is a ctrl interface that output local coordinates while being parented to the geometry it deform.
Usefull to apply a deformation before a skinCluster while faking a parenting with the parent.
"""


def create_plane(normal=None):
    if normal is None:
        normal = [0, 1, 0]
    normal_x = normal[0]
    normal_y = normal[1]
    normal_z = normal[2]
    transform, polyPlane = pymel.polyPlane(sx=1, sy=1)
    shape = transform.getShape()

    # There's no parameter to re-orient a plane so we'll move all of it's vertices if needed.
    pymel.delete(polyPlane)
    offset_tm = None
    if normal_x != 0.0:
        offset_tm = pymel.datatypes.Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, -normal_x, 0], [0, 0, 0, 1]])  # X
    elif normal_y != 0.0:
        offset_tm = pymel.datatypes.Matrix([[normal_y, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])  # Y
    elif normal_z != 0.0:
        offset_tm = pymel.datatypes.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, -normal_z, 0, 0], [0, 0, 0, 1]])  # Z

    for v in shape.vtx:
        v.setPosition(v.getPosition() * offset_tm)

    return transform


def _reparent_djRivet_follicles(parent, delete_old_parent=True):
    if not cmds.objExists('djRivetX'):
        return

    follicles = pymel.PyNode('djRivetX').getChildren()
    for child in follicles:
        if parent:
            child.setParent(parent)
        else:
            child.setParent(world=True)

    if delete_old_parent:
        cmds.delete('djRivetX')

    return follicles


class Dorito(RigPart):
    def build(self, _bConstraint=True, *args, **kwargs):
        # If there's no input, create it
        if len(self.input) == 0:
            self.input = [pymel.createNode('transform', name='untitled')]
        input = next(iter(self.input))

        super(Dorito, self).build(create_grp_anm=True, create_grp_rig=True, *args, **kwargs)
        self.ctrl = RigCtrl()
        self.ctrl.build()

        # Hack: Include the rotatePivot in our matrix calculation
        ref_matrix = pymel.datatypes.Matrix(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,
                                            *input.rotatePivot.get()) * input.getMatrix(worldSpace=True)

        self.ctrl.offset.setMatrix(ref_matrix, worldSpace=True)
        self.ctrl.setParent(self.grp_anm)

        # Initialize self.mesh
        self.mesh = None
        # Try to guess the output geometry, if nothing is found, create a fake one.

        is_cluster = any((shape for shape in input.getShapes() if isinstance(shape, pymel.nodetypes.ClusterHandle)))

        if is_cluster:
            cluster = next(
                (hist for hist in input.listHistory(future=True) if isinstance(hist, pymel.nodetypes.Cluster)), None)

            if cluster:
                self.mesh = next(iter(cluster.outputGeometry.outputs()), None)

        if not self.mesh:
            self.mesh = create_plane()
            self.mesh.setParent(self.grp_rig)

        # djRivet is a noble tool that handle things well on it's own, we don't need to re-implement it
        path_djrivet = os.path.join('/', os.path.dirname(omtk.__file__), 'deps', 'djRivet.mel')
        mel.eval('source "{0}"'.format(path_djrivet))
        pymel.select(self.ctrl.offset, self.mesh)
        mel.eval('djRivet')

        # Create the follicle using djRivet
        follicles = _reparent_djRivet_follicles(self.grp_rig)
        for child in self.ctrl.offset.getChildren():
            if isinstance(child, pymel.nodetypes.Constraint):
                pymel.delete(child)
        # Hack: Hide follicle
        follicle = next(iter(follicles))
        follicle.setParent(self.grp_rig)

        # Create an initial pose reference since the follicle won't necessary have the same transform as the reference obj.
        ref = pymel.createNode('transform')
        ref.setMatrix(ref_matrix, worldSpace=True)
        ref.setParent(follicle)

        # Overwrite the self.ctrl.offset node with the magic
        # Compute the follicle minus the inverse of the ctrl
        # Since a matrix is computed scale first, rotate second and translate last, we need to inverse
        # it using translate first and rotation last (we don't care about conter-rigging the scale).

        att_ctrl_pos_inv = libRigging.create_utility_node(
            'multiplyDivide',
            operation=2,
            input1=self.ctrl.node.t,
            input2=[-1, -1, -1]
        ).output

        att_pos_inv = libRigging.create_utility_node(
            'composeMatrix',
            inputTranslate=att_ctrl_pos_inv
        ).outputMatrix

        att_ctrl_rot_inv = libRigging.create_utility_node(
            'multiplyDivide',
            operation=2,
            input1=self.ctrl.node.r,
            input2=[-1, -1, -1]
        ).output

        att_rot_inv = libRigging.create_utility_node(
            'composeMatrix',
            inputRotate=att_ctrl_rot_inv
        ).outputMatrix

        uMatrixSum = libRigging.create_utility_node(
            'multMatrix',
            matrixIn=[
                att_pos_inv,
                att_rot_inv,
                ref.worldMatrix
            ]
        ).matrixSum

        uResult = libRigging.create_utility_node(
            'decomposeMatrix',
            inputMatrix=uMatrixSum,
        )
        pymel.connectAttr(uResult.outputTranslate, self.ctrl.offset.t)
        pymel.connectAttr(uResult.outputRotate, self.ctrl.offset.r)

        # Connect the ctrl local coords to the deformer handle
        pymel.connectAttr(self.ctrl.t, input.t, force=True)
        pymel.connectAttr(self.ctrl.r, input.r, force=True)
        pymel.connectAttr(self.ctrl.s, input.s, force=True)

        pymel.select(self.ctrl)

    def unbuild(self, *args, **kwargs):
        super(Dorito, self).unbuild(*args, **kwargs)

        self.ctrl = None
