import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule import Module
from omtk.libs import libRigging
from omtk.libs import libSkinning
from omtk.libs import libPython


class CtrlRibbon(BaseCtrl):
    """
    Inherit of base Ctrl to create a specific square shaped controller
    """

    def __createNode__(self, *args, **kwargs):  # pylint: disable=arguments-differ
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
        self._surface_shape = None
        self._follicles = []
        self.ribbon_chain_grp = None

    def build(
        self,
        no_subdiv=False,
        num_ctrl=None,
        degree=3,
        create_ctrl=True,
        constraint=False,
        rot_fol=True,
        *args,
        **kwargs
    ):
        super(Ribbon, self).build(create_grp_anm=create_ctrl, *args, **kwargs)
        if num_ctrl is not None:
            self.num_ctrl = num_ctrl

        naming = self.get_nomenclature_rig()

        # Create the plane and align it with the selected bones
        surface = self.get_surface() or self._create_surface(degree, not no_subdiv)
        self._surface_shape = surface.getShape()  # TODO: Remove

        follicles_grp = pymel.createNode(
            "transform", name=naming.resolve("follicleGrp"), parent=self.grp_rig
        )
        self._follicles = self._create_follicles(follicles_grp, rot_fol)

        # Create the joints that will drive the ribbon.
        # TODO: Support other shapes than straight lines...
        self._ribbon_jnts = libRigging.create_chain_between_objects(
            self.chain_jnt.start, self.chain_jnt.end, self.num_ctrl, parented=False
        )

        # Group all the joints
        ribbon_chain_grp_name = naming.resolve("ribbonChainGrp")
        self.ribbon_chain_grp = pymel.createNode(
            "transform", name=ribbon_chain_grp_name, parent=self.grp_rig
        )
        align_chain = True if len(self.chain_jnt) == len(self._ribbon_jnts) else False
        for i, jnt in enumerate(self._ribbon_jnts):
            # Align the ribbon joints with the real joint to have a better rotation ctrl
            ribbon_jnt_name = naming.resolve("ribbonJnt{0:02d}".format(i))
            jnt.rename(ribbon_jnt_name)
            jnt.setParent(self.ribbon_chain_grp)
            if align_chain:
                matrix = self.chain_jnt[i].getMatrix(worldSpace=True)
                jnt.setMatrix(matrix, worldSpace=True)

        # TODO - Improve skinning smoothing by setting manually the skin...
        pymel.skinCluster(list(self._ribbon_jnts), surface, dr=1.0, mi=2.0, omi=True)
        try:
            libSkinning.assign_weights_from_segments(
                self._surface_shape, self._ribbon_jnts, dropoff=1.0
            )
        except ZeroDivisionError:  # TODO: When would that happen?
            pass

        # Create the ctrls that will drive the joints that will drive the ribbon.
        if create_ctrl:
            self.ctrls = self.create_ctrls(**kwargs)

            # Global uniform scale support
            self.globalScale.connect(self.ribbon_chain_grp.scaleX)
            self.globalScale.connect(self.ribbon_chain_grp.scaleY)
            self.globalScale.connect(self.ribbon_chain_grp.scaleZ)

    def unbuild(self):
        super(Ribbon, self).unbuild()

        self.ctrls = []

    def create_ctrls(
        self, ctrls=None, no_extremity=False, constraint_rot=True, **kwargs
    ):
        """
        This function can be used to create controllers on the ribbon joints.
        :param no_extremity: Tell if we want extremity ctrls
        :param constraint_rot: Tell if we constraint the bones on the controllers
        :return: nothing
        """
        ctrls = ctrls if ctrls else self.ctrls
        naming = self.get_nomenclature_anm()

        # Ensure we have as many ctrls as needed.
        desired_ctrls_count = len(self._ribbon_jnts)
        if no_extremity:
            desired_ctrls_count -= 2
        ctrls = filter(None, ctrls)
        libPython.resize_list(ctrls, desired_ctrls_count)

        real_index = 0
        for i, jnt in enumerate(self._ribbon_jnts):
            if no_extremity and (i == 0 or i == (len(self._ribbon_jnts) - 1)):
                continue
            ctrl = ctrls[real_index] if real_index < len(ctrls) else None
            ctrl_name = naming.resolve(str(real_index + 1).zfill(2))
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

    def _create_follicles(self, parent, constraint_rot=True):
        """
        Create follicle attached to the place for each input joint
        :param constraint_rot: Are the joints will be constraint in rotation on the follicle
        :return: Nothing
        """
        result = []
        for idx, jnt in enumerate(self.chain_jnt):
            # TODO: Validate that we don't need to inverse the rotation separately.
            jnt_pos = jnt.getMatrix(worldSpace=True).translate
            fol = self._create_follicle(self._surface_shape, idx, jnt_pos)
            fol.setParent(parent)
            if constraint_rot:
                pymel.parentConstraint(fol, jnt, mo=True)
            else:
                pymel.pointConstraint(fol, jnt, mo=True)

            result.append(fol)
        return result

    def _create_follicle(self, surface_shape, index, pos):
        """
        Create a follicle on a surface.
        :param surface_shape: The follicle surface
        :type surface_shape: pymel.nodetypes.NurbsSurface
        :param str index: The follicle index, for naming.
        :param pos: The position to create the follicle from
        :type pos: pymel.datatypes.Vector
        :return: The follicle transform
        :rtype: pymel.nodetypes.Transform
        """
        naming = self.get_nomenclature_rig()
        _, fol_u, fol_v = libRigging.get_closest_point_on_surface(surface_shape, pos)
        name = naming.resolve("ribbonFollicle{0:02d}".format(index))
        shape = libRigging.create_follicle(surface_shape, u=fol_u, v=fol_v)
        transform = shape.getParent()
        transform.rename(name)
        return transform

    def _create_surface(self, degree, subdiv):
        """
        Create a ribbon surface

        :param int degree: The number of degree for the surface.
        :param bool subdiv: Do we want subdivisions?
        :return: The surface transform
        :rtype: pymel.nodetypes.Transform
        """
        naming = self.get_nomenclature_rig()
        surface = libRigging.create_nurbs_plane_from_joints(
            self.chain_jnt if subdiv else [self.chain_jnt[0], self.chain_jnt[-1]],
            degree=degree if subdiv else min(degree, 2),
            width=self.width,
        )
        surface.rename(naming.resolve("ribbonPlane"))
        surface.setParent(self.grp_rig)
        return surface


def register_plugin():
    return Ribbon
