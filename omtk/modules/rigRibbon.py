import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule import Module
from omtk.libs import libPymel
from omtk.libs import libRigging
from omtk.libs import libSkinning
from omtk.libs import libPython


class CtrlRibbon(BaseCtrl):
    """
    Inherit of base Ctrl to create a specific square shaped controller
    """
    def __createNode__(self, *args, **kwargs):
        node = super(CtrlRibbon, self).__createNode__(*args, **kwargs)
        make = next(iter(node.getShape().create.inputs()), None)
        if make:
            make.degree.set(1)
            make.sections.set(4)
        return node


class Ribbon(Module):
    """
    Generic ribbon setup.
    """
    def __init__(self, *args, **kwargs):
        super(Ribbon, self).__init__(*args, **kwargs)
        self.num_ctrl = 3
        self.ctrls = []
        self.width = 1.0
        self._ribbon_jnts = []
        self._ribbon_shape = None
        self._follicles = []
        self.ribbon_chain_grp = None

    def create_ctrls(self, ctrls=None, no_extremity=False, constraint_rot=True, **kwargs):
        """
        This function can be used to create controllers on the ribbon joints.
        :param no_extremity: Tell if we want extremity ctrls
        :param constraint_rot: Tell if we constraint the bones on the controllers
        :return: nothing
        """
        ctrls = ctrls if ctrls else self.ctrls
        nomenclature_anm = self.get_nomenclature_anm()


        # Ensure we have as many ctrls as needed.
        desired_ctrls_count = len(self._ribbon_jnts)
        if no_extremity:
            desired_ctrls_count -= 2
        ctrls = filter(None, ctrls)
        libPython.resize_list(ctrls, desired_ctrls_count)

        real_index = 0
        for i, jnt in enumerate(self._ribbon_jnts):
            if no_extremity and i == 0 or i == (len(self._ribbon_jnts) - 1):
                continue
            ctrl = ctrls[real_index] if real_index < len(ctrls) else None
            ctrl_name = nomenclature_anm.resolve('fk' + str(real_index+1).zfill(2))
            # Check if we already have an instance of the ctrl
            if not isinstance(ctrl, CtrlRibbon):
                ctrl = CtrlRibbon()
                ctrls[real_index] = ctrl
            ctrl.build(name=ctrl_name, **kwargs)
            ctrl.setMatrix(jnt.getMatrix(worldSpace=True), worldSpace=True)
            ctrl.setParent(self.grp_anm)

            if constraint_rot:
                pymel.parentConstraint(ctrl, jnt, mo=True)
            else:
                pymel.pointConstraint(ctrl, jnt, mo=True)
            pymel.connectAttr(ctrl.scaleX, jnt.scaleX)
            pymel.connectAttr(ctrl.scaleY, jnt.scaleY)
            pymel.connectAttr(ctrl.scaleZ, jnt.scaleZ)

            real_index += 1

        return ctrls

    def attach_to_plane(self, constraint_rot=True):
        """
        Create follicle attached to the place for each input joint
        :param constraint_rot: Are the joints will be constraint in rotation on the follicle
        :return: Nothing
        """
        nomenclature_rig = self.get_nomenclature_rig()
        fol_v = 0.5  # Always in the center

        #split_value = 1.0 / (len(self.chain_jnt) - 1)

        for i, jnt in enumerate(self.chain_jnt):
            #fol_u = split_value * i
            # TODO: Validate that we don't need to inverse the rotation separately.
            jnt_pos = jnt.getMatrix(worldSpace=True).translate
            pos, fol_u, fol_v = libRigging.get_closest_point_on_surface(self._ribbon_shape, jnt_pos)
            fol_name = nomenclature_rig.resolve("ribbonFollicle{0:02d}".format(i))
            fol_shape = libRigging.create_follicle2(self._ribbon_shape, u=fol_u, v=fol_v)
            fol = fol_shape.getParent()
            fol.rename(fol_name)
            if constraint_rot:
                pymel.parentConstraint(fol, jnt, mo=True)
            else:
                pymel.pointConstraint(fol, jnt, mo=True)

            self._follicles.append(fol)

    def build(self, no_subdiv=False, num_ctrl = None, degree=3, create_ctrl=True, constraint=False, rot_fol=True, *args, **kwargs):
        super(Ribbon, self).build(create_grp_anm=create_ctrl, *args, **kwargs)
        if num_ctrl is not None:
            self.num_ctrl = num_ctrl

        nomenclature_rig = self.get_nomenclature_rig()

        # Create the plane and align it with the selected bones
        plane_tran = next((input for input in self.input if libPymel.isinstance_of_shape(input, pymel.nodetypes.NurbsSurface)), None)
        if plane_tran is None:
            plane_name = nomenclature_rig.resolve("ribbonPlane")
            if no_subdiv:  # We don't want any subdivision in the plane, so use only 2 bones to create it
                no_subdiv_degree = 2
                if degree < 2:
                    no_subdiv_degree = degree
                plane_tran = libRigging.create_nurbs_plane_from_joints([self.chain_jnt[0], self.chain_jnt[-1]],
                                                                       degree=no_subdiv_degree, width=self.width)
            else:
                plane_tran = libRigging.create_nurbs_plane_from_joints(self.chain_jnt, degree=degree, width=self.width)
            plane_tran.rename(plane_name)
            plane_tran.setParent(self.grp_rig)
        self._ribbon_shape = plane_tran.getShape()

        # Create the follicule needed for the system on the skinned bones
        self.attach_to_plane(rot_fol)
        # TODO : Support aim constraint for bones instead of follicle rotation?

        follicles_grp = pymel.createNode("transform")
        follicle_grp_name = nomenclature_rig.resolve("follicleGrp")
        follicles_grp.rename(follicle_grp_name)
        follicles_grp.setParent(self.grp_rig)
        for n in self._follicles:
            n.setParent(follicles_grp)

        # Create the joints that will drive the ribbon.
        # TODO: Support other shapes than straight lines...
        self._ribbon_jnts = libRigging.create_chain_between_objects(
            self.chain_jnt.start, self.chain_jnt.end, self.num_ctrl, parented=False)

        # Group all the joints
        ribbon_chain_grp_name = nomenclature_rig.resolve('ribbonChainGrp')
        self.ribbon_chain_grp = pymel.createNode('transform', name=ribbon_chain_grp_name, parent=self.grp_rig)
        align_chain = True if len(self.chain_jnt) == len(self._ribbon_jnts) else False
        for i, jnt in enumerate(self._ribbon_jnts):
            # Align the ribbon joints with the real joint to have a better rotation ctrl
            ribbon_jnt_name = nomenclature_rig.resolve('ribbonJnt{0:02d}'.format(i))
            jnt.rename(ribbon_jnt_name)
            jnt.setParent(self.ribbon_chain_grp)
            if align_chain:
                matrix = self.chain_jnt[i].getMatrix(worldSpace=True)
                jnt.setMatrix(matrix, worldSpace=True)

        # TODO - Improve skinning smoothing by setting manually the skin...
        pymel.skinCluster(list(self._ribbon_jnts), plane_tran, dr=1.0, mi=2.0, omi=True)
        try:
            libSkinning.assign_weights_from_segments(self._ribbon_shape, self._ribbon_jnts, dropoff=1.0)
        except ZeroDivisionError, e:
            pass

        # Create the ctrls that will drive the joints that will drive the ribbon.
        if create_ctrl:
            self.ctrls = self.create_ctrls(**kwargs)

            # Global uniform scale support
            self.globalScale.connect(self.ribbon_chain_grp.scaleX)
            self.globalScale.connect(self.ribbon_chain_grp.scaleY)
            self.globalScale.connect(self.ribbon_chain_grp.scaleZ)

        '''
        if constraint:
            for source, target in zip(self._ribbon_jnts, self.chain_jnt):
                print source, target
                pymel.parentConstraint(source, target, maintainOffset=True)
        '''


    def unbuild(self):
        super(Ribbon, self).unbuild()

        self.ctrls = []

def register_plugin():
    return Ribbon
