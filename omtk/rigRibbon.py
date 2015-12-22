import pymel.core as pymel
import maya.mel as mel
from className import Name
from classCtrl import BaseCtrl
from classModule import Module
from libs import libRigging

class Ribbon(Module):
    def __init__(self, *args, **kwargs):
        super(Ribbon, self).__init__(*args, **kwargs)
        self.num_subdiv = None
        self.num_ctrl = None

    def build(self, num_subdiv = 5, num_ctrl = 3, *args, **kwargs):
        super(Ribbon, self).build(*args, **kwargs)
        #TODO - Improve naming

        self.num_subdiv = num_subdiv
        self.num_ctrl = num_ctrl

        distance = self.chain.length()
        
        #Create the plane and align it with the selected bones
        plane_tran, plane_shape = pymel.nurbsPlane()
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

        #Create the joints that will be used to skin the plane
        a_ribbon_jnt = libRigging.create_chain_between_objects(self.chain.start, self.chain.end, self.num_ctrl)
        for n in a_ribbon_jnt:
            jnt_name = self.name_rig.resolve("jnt")
            n.rename(jnt_name)

        #Create the joint that will be constrained to the plane with djRivet
        a_skin_jnt = libRigging.create_chain_between_objects(self.chain.start, self.chain.end, self.num_subdiv)

        for n in a_skin_jnt:
            jnt_name = self.name_rig.resolve("toskin")
            n.rename(jnt_name)
            #Create the follicule needed for the system on the skinned bones
            pymel.select(n, plane_tran)
            mel.eval("djRivet")

        #Apply the skin on the plane and rename follicle from djRivet
        dj_rivet_grp = pymel.PyNode("djRivetX")
        follicle_grp_name = self.name_rig.resolve("follicle_grp")
        dj_rivet_grp.rename(follicle_grp_name)
        for n in dj_rivet_grp.getChildren():
            fol_name = self.name_rig.resolve("fol")
            n.rename(fol_name)

        #TODO - Improve skinning smoothing
        pymel.skinCluster(a_ribbon_jnt.pynodes, plane_tran, dr=(distance/self.num_ctrl), ih=True)


    def unbuild(self):
        raise NotImplementedError