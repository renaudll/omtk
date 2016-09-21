import pymel.core as pymel
import maya.mel as mel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule import Module
from omtk.libs import libPymel, libRigging, libSkinning

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
        self.num_ctrl = 3
        self.ctrls = []
        self.width = 1.0

    def build(self, rig, num_subdiv = 5, num_ctrl = None, degree=3, create_ctrl=True, constraint=False, rot_fol=False, *args, **kwargs):
        super(Ribbon, self).build(rig, create_grp_anm=create_ctrl, *args, **kwargs)
        if num_ctrl is not None:
            self.num_ctrl = num_ctrl

        nomenclature_anm = self.get_nomenclature_anm(rig)
        nomenclature_rig = self.get_nomenclature_rig(rig)

        #Create the plane and align it with the selected bones
        plane_tran = next((input for input in self.input if libPymel.isinstance_of_shape(input, pymel.nodetypes.NurbsSurface)), None)
        if plane_tran is None:
            plane_name = nomenclature_rig.resolve("ribbonPlane")
            plane_tran = libRigging.create_nurbs_plane_from_joints(self.chain_jnt, degree=degree, width=self.width)
            plane_tran.rename(plane_name)
            plane_tran.setParent(self.grp_rig)
        self._ribbon_shape = plane_tran.getShape()

        # TODO: Remove usage of djRivet
        #Create the follicule needed for the system on the skinned bones
        for i, jnt in enumerate(self.chain_jnt):
            pymel.select(jnt, plane_tran)
            mel.eval("djRivet")
            #TODO : Support aim constraint for bones instead of follicle rotation?

        # Apply the skin on the plane and rename follicle from djRivet
        dj_rivet_grp = pymel.PyNode("djRivetX")
        follicle_grp_name = nomenclature_rig.resolve("follicle_grp")
        dj_rivet_grp.rename(follicle_grp_name)
        dj_rivet_grp.setParent(self.grp_rig)
        self._follicles = dj_rivet_grp.getChildren()
        for n in self._follicles:
            fol_name = nomenclature_rig.resolve("fol")
            n.rename(fol_name)

        # Create the joints that will drive the ribbon.
        # TODO: Support other shapes than straight lines...
        # TODO: Support ctrl hold/fetch when building/unbuilding.
        self._ribbon_jnts = libRigging.create_chain_between_objects(
            self.chain_jnt.start, self.chain_jnt.end, self.num_ctrl, parented=False)

        # Group all the joints
        ribbon_chain_grp_name = nomenclature_rig.resolve('ribbonChain' + "_grp")
        ribbon_chain_grp = pymel.createNode('transform', name=ribbon_chain_grp_name, parent=self.grp_rig)
        align_chain = True if len(self.chain_jnt) == len(self._ribbon_jnts) else False
        for i, jnt in enumerate(self._ribbon_jnts):
            #Align the ribbon joints with the real joint to have a better rotation ctrl
            if align_chain:
                matrix = self.chain_jnt[i].getMatrix(worldSpace=True)
                jnt.setMatrix(matrix, worldSpace=True)
            jnt.setParent(ribbon_chain_grp)

        #TODO - Improve skinning smoothing by setting manully the skin...
        pymel.skinCluster(list(self._ribbon_jnts), plane_tran, dr=1.0, mi=2.0, omi=True)
        try:
            libSkinning.assign_weights_from_segments(self._ribbon_shape, self._ribbon_jnts, dropoff=1.0)
        except ZeroDivisionError, e:
            pass

        # Create the ctrls that will drive the joints that will drive the ribbon.
        if create_ctrl:
            self.ctrls = []
            for i, jnt in enumerate(self._ribbon_jnts):
                ctrl_name = nomenclature_anm.resolve('fk' + str(i+1).zfill(2))
                ctrl = CtrlRibbon(name=ctrl_name)
                ctrl.build(rig)
                ctrl.setMatrix(jnt.getMatrix(worldSpace=True))
                ctrl.setParent(self.grp_anm)

                pymel.parentConstraint(ctrl, jnt)
                pymel.connectAttr(ctrl.scaleX, jnt.scaleX)
                pymel.connectAttr(ctrl.scaleY, jnt.scaleY)
                pymel.connectAttr(ctrl.scaleZ, jnt.scaleZ)

                self.ctrls.append(ctrl)

            # Global uniform scale support
            self.globalScale.connect(ribbon_chain_grp.scaleX)
            self.globalScale.connect(ribbon_chain_grp.scaleY)
            self.globalScale.connect(ribbon_chain_grp.scaleZ)

        '''
        if constraint:
            for source, target in zip(self._ribbon_jnts, self.chain_jnt):
                print source, target
                pymel.parentConstraint(source, target, maintainOffset=True)
        '''


    def unbuild(self, rig):
        super(Ribbon, self).unbuild(rig)

        self.ctrls = []