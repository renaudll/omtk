import pymel.core as pymel
import maya.mel as mel
from className import Name
from classCtrl import BaseCtrl
from classModule import Module
from libs import libPymel, libRigging, libSkinning

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

    def build(self, num_subdiv = 5, num_ctrl = 3, degree=1, create_ctrl=True, *args, **kwargs):
        self._chain_joints = libPymel.PyNodeChain([input for input in self.input if libPymel.isinstance_of_transform(input, pymel.nodetypes.Joint)])


        super(Ribbon, self).build(segmentScaleCompensate=False, create_grp_anm=create_ctrl, *args, **kwargs)
        self.num_ctrl = num_ctrl

        #Create the plane and align it with the selected bones
        plane_tran = next((input for input in self.input if libPymel.isinstance_of_shape(input, pymel.nodetypes.NurbsSurface)), None)
        if plane_tran is None:
            plane_name = self.name_rig.resolve("ribbonPlane")
            plane_tran = libRigging.create_nurbs_plane_from_joints(self._chain_joints, degree=degree)
            plane_tran.rename(plane_name)
            plane_tran.setParent(self.grp_rig)
            plane_shape = plane_tran.getShape()

        #Create the follicule needed for the system on the skinned bones
        for i, jnt in enumerate(self._chain_joints):
            pymel.select(jnt, plane_tran)
            mel.eval("djRivet")

        #Apply the skin on the plane and rename follicle from djRivet
        dj_rivet_grp = pymel.PyNode("djRivetX")
        follicle_grp_name = self.name_rig.resolve("follicle_grp")
        dj_rivet_grp.rename(follicle_grp_name)
        dj_rivet_grp.setParent(self.grp_rig)
        for n in dj_rivet_grp.getChildren():
            fol_name = self.name_rig.resolve("fol")
            n.rename(fol_name)

        # Create the joints that will drive the ribbon.
        # TODO: Support other shapes than straight lines...
        # TODO: Support ctrl hold/fetch when building/unbuilding.
        jnts = libRigging.create_chain_between_objects(self._chain_joints.start, self._chain_joints.end, self.num_ctrl, parented=False)

        # Group all the joints
        ribbon_chain_grp_name = self.name_rig.resolve('ribbonChain' + "_grp")
        ribbon_chain_grp = pymel.createNode('transform', name=ribbon_chain_grp_name, parent=self.grp_rig)
        for jnt in jnts:
            jnt.setParent(ribbon_chain_grp)

        #TODO - Improve skinning smoothing by setting manully the skin...
        pymel.skinCluster(jnts._list, plane_tran, dr=1.0, mi=2.0, omi=True)
        libSkinning.assign_weights_from_segments(plane_shape, jnts._list, dropoff=1.0)

        # Create the ctrls that will drive the joints that will drive the ribbon.
        if create_ctrl:
            self.ctrls = []
            for i, jnt in enumerate(jnts):
                ctrl_name = self.name_anm.resolve('fk' + str(i+1).zfill(2))
                ctrl = CtrlRibbon(name=ctrl_name, create=True)
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


    def unbuild(self):
        super(Ribbon, self).unbuild()

        self.ctrls = []