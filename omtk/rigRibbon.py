import pymel.core as pymel
import maya.mel as mel
from className import Name
from classCtrl import BaseCtrl
from classModule import Module
from libs import libRigging

class CtrlRibbon(BaseCtrl):
    def build(self, *args, **kwargs):
        super(CtrlRibbon, self).build(*args, **kwargs)
        make = self.node.getShape().create.inputs()[0]
        make.radius.set(2)
        make.degree.set(1)
        make.sections.set(4)
        return self.node

class Ribbon(Module):
    def __init__(self, *args, **kwargs):
        super(Ribbon, self).__init__(*args, **kwargs)
        self.num_subdiv = None
        self.num_ctrl = None
        self.ctrls = []

    def build(self, num_subdiv = 5, num_ctrl = 3, create_ctrl=True, *args, **kwargs):
        super(Ribbon, self).build(*args, **kwargs)
        self.num_subdiv = num_subdiv
        self.num_ctrl = num_ctrl

        distance = self.chain.length()
        
        #Create the plane and align it with the selected bones
        plane_tran, plane_shape = pymel.nurbsPlane()
        plane_name = self.name_rig.resolve("ribbonPlane")
        plane_tran.rename(plane_name)
        start_matrix = self.chain.start.getMatrix(worldSpace=True)
        y_aligned_mat = pymel.datatypes.Matrix(start_matrix[1], start_matrix[0], -start_matrix[2], start_matrix[3])
        plane_tran.setMatrix(y_aligned_mat, worldSpace=True)

        #Place the plane between the start and end bone
        t_plane = plane_tran.getTranslation(space="world")
        between_pos = pymel.datatypes.Vector(t_plane.x, (t_plane.y + distance/2), t_plane.z)
        aligned_trans = between_pos * y_aligned_mat

        #Set the length and number of subdivision for the place
        plane_tran.setTranslation(aligned_trans, space="object")
        plane_shape.lengthRatio.set(distance)
        plane_shape.patchesV.set(self.num_subdiv)
        plane_grp_name = self.name_rig.resolve("ribbonPlane" + "_grp")
        plane_grp = pymel.createNode('transform', name=plane_grp_name, parent=self.grp_rig)
        plane_grp.setMatrix(plane_tran.getMatrix(worldSpace=True))
        plane_tran.setParent(plane_grp)

        #Create the joints that will be used to skin the plane
        a_ribbon_jnt = libRigging.create_chain_between_objects(self.chain.start,
                                                               self.chain.end, self.num_ctrl, parented=False)
        ribbon_chain_grp_name = self.name_rig.resolve('ribbonChain' + "_grp")
        ribbon_chain_grp = pymel.createNode('transform', name=ribbon_chain_grp_name, parent=self.grp_rig)
        ribbon_chain_grp.setMatrix(start_matrix)
        pymel.parentConstraint(ribbon_chain_grp, self.chain[0], maintainOffset=True)
        self.globalScale.connect(ribbon_chain_grp.scaleX)
        self.globalScale.connect(ribbon_chain_grp.scaleY)
        self.globalScale.connect(ribbon_chain_grp.scaleZ)
        for i,n in enumerate(a_ribbon_jnt):
            n.segmentScaleCompensate.set(False)
            n.setParent(ribbon_chain_grp)
            n.radius.set(1.0)
            jnt_name = self.name_rig.resolve("jnt" + str(i+1).zfill(2))
            n.rename(jnt_name)

            #Create ctrl if needed
            if create_ctrl:
                ctrl_name = self.name_anm.resolve('fk' + str(i+1).zfill(2))
                ctrl = CtrlRibbon(name=ctrl_name, create=True)
                ctrl.setMatrix(n.getMatrix(worldSpace=True))
                ctrl.setParent(self.grp_anm)
                self.ctrls.append(ctrl)

                #Constraint ctrl to ribbon jnt
                pymel.parentConstraint(ctrl, n)
                pymel.connectAttr(ctrl.scaleX, n.scaleX)
                pymel.connectAttr(ctrl.scaleY, n.scaleY)
                pymel.connectAttr(ctrl.scaleZ, n.scaleZ)

        #Create the joint that will be constrained to the plane with djRivet
        #TODO - Should we parent the joint together ? If yes, it cause some flipping du to the parent rotation
        a_skin_jnt = libRigging.create_chain_between_objects(self.chain.start, self.chain.end,
                                                             self.num_subdiv, parented=False)
        for i,n in enumerate(a_skin_jnt):
            n.segmentScaleCompensate.set(False)
            n.setParent(self.chain.start)
            jnt_name = self.name_jnt.resolve(str(i+1).zfill(2))
            n.rename(jnt_name)
            #Create the follicule needed for the system on the skinned bones
            pymel.select(n, plane_tran)
            mel.eval("djRivet")

        #Apply the skin on the plane and rename follicle from djRivet
        dj_rivet_grp = pymel.PyNode("djRivetX")
        follicle_grp_name = self.name_rig.resolve("follicle_grp")
        dj_rivet_grp.rename(follicle_grp_name)
        dj_rivet_grp.setParent(self.grp_rig)
        for n in dj_rivet_grp.getChildren():
            fol_name = self.name_rig.resolve("fol")
            n.rename(fol_name)

        #TODO - Improve skinning smoothing by setting manully the skin...
        pymel.skinCluster(a_ribbon_jnt.chain, plane_tran, dr=1.0, mi=2.0, omi=True)


    def unbuild(self):
        super(Ribbon, self).unbuild()

        self.ctrls = []