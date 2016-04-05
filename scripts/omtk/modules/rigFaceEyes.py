import pymel.core as pymel
import collections
from omtk.core.classModule import Module
from omtk.core.classCtrl import BaseCtrl
from omtk.modules.rigIK import IK
from omtk.modules.rigFK import FK
from omtk.modules import rigFaceAvarGrps
from omtk.libs import libRigging, libCtrlShapes


class CtrlEyes(BaseCtrl):
    def __createNode__(self, width=1.0, height=1.0, normal=(0,0,1), *args, **kwargs):
        p1 = [0, height, 0]
        p2 = [width*0.5, height*0.95, 0]
        p3 = [width, 0, 0]
        p4 = [width*0.5, -height*0.95, 0]
        p5 = [0, -height, 0]
        p6 = [-width*0.5, -height*0.95, 0]
        p7 = [-width, 0, 0]
        p8 = [-width*0.5, height*0.95, 0]

        node = pymel.curve(d=2, p=[p1, p2, p3, p4, p5, p6, p7, p8, p1] )
        return node

class CtrlEye(BaseCtrl):
    def __createNode__(self, normal=(0,0,1), *args, **kwargs):
        return super(CtrlEye, self).__createNode__(normal=normal, *args, **kwargs)


class FaceEyes(rigFaceAvarGrps.ModuleFace):
    IS_SIDE_SPECIFIC = False

    def __init__(self, *args, **kwargs):
        """
        Pre-declare here all the used members.
        """
        super(FaceEyes, self).__init__(*args, **kwargs)
        self.ctrls = []
        self.ctrl_all = None

    def get_distance_from_head(self, rig):
        return rig.get_head_length() * 2

    def build(self, rig, *args, **kwargs):
        if self.parent is None:
            raise Exception("Can't build FaceEyes, no parent found!")

        super(FaceEyes, self).build(rig, create_ctrls=False, parent=True, *args, **kwargs)

        nomenclature_anm = self.get_nomenclature_anm(rig)
        nomenclature_rig = self.get_nomenclature_rig(rig)
        pos_z = self.parent.getTranslation().z + self.get_distance_from_head(rig)
        num_jnts = len(self.jnts)

        # Build a grp for the upnodes
        # Upnodes are ugly, however in this case it's better than trying to guess the joint orientation.
        # We know that the upnodes of the eyes are always upp.
        grp_parent_name = nomenclature_rig.resolve('parentGrp')
        grp_parent = pymel.createNode('transform', name=grp_parent_name)
        grp_parent.setParent(self.grp_rig)

        # TODO: Don't parent if we are in pre-deform!
        if self.parent:
            pymel.parentConstraint(self.parent, grp_parent)
            pymel.scaleConstraint(self.parent, grp_parent)

        # Resolve average position of each ctrls.
        # This is used as the position of the main ctrl.
        ctrl_default_size = 1  # TODO: Compute automatically
        ctrl_pos_average = pymel.datatypes.Vector()
        ctrl_positions = []
        x_min = None
        x_max = None
        y_min = None
        y_max = None
        for jnt in self.jnts:
            pos = jnt.getTranslation(space='world')
            pos.z = pos_z
            ctrl_positions.append(pos)
            ctrl_pos_average += pos
            if x_min is None or pos.x < x_min:
                x_min = pos.x
            if x_max is None or pos.x > x_max:
                x_max = pos.x
            if y_min is None or pos.y < y_min:
                y_min = pos.y
            if y_max is None or pos.y > y_max:
                y_max = pos.y
        ctrl_pos_average /= len(self.jnts)
        width = max(ctrl_default_size, abs(x_max - x_min)) + ctrl_default_size
        height = max(ctrl_default_size, abs(y_max - y_min)) + ctrl_default_size

        # Define main ctrl
        if not isinstance(self.ctrl_all, CtrlEyes):
            self.ctrl_all = CtrlEyes()
        ctrl_all_name = nomenclature_anm.resolve()
        self.ctrl_all.build(width=width, height=height)
        self.ctrl_all.setTranslation(ctrl_pos_average)
        self.ctrl_all.create_spaceswitch(rig, self.parent, add_default=True, default_name='Head', add_world=True)
        self.ctrl_all.rename(ctrl_all_name)
        self.ctrl_all.setParent(self.grp_anm)

        # Define ctrls
        ctrls = [None] * num_jnts
        if self.ctrls:
            for i, ctrl in enumerate(self.ctrls):
                ctrls[i] = ctrl
        self.ctrls = ctrls
        for i, ctrl in enumerate(self.ctrls):
            if not isinstance(ctrl, CtrlEye):
                self.ctrls[i] = CtrlEye()

        # Build ctrls
        for jnt, ctrl, ctrl_pos, avar, in zip(self.jnts, self.ctrls, ctrl_positions, self.avars):
            jnt_name = jnt.name()
            jnt_pos = jnt.getTranslation(space='world')
            nomenclature_jnt_anm = nomenclature_anm.rebuild(jnt_name)
            nomenclature_jnt_rig = nomenclature_rig.rebuild(jnt_name)

            # Build ctrl
            ctrl_name = nomenclature_jnt_anm.resolve()
            ctrl.build(size=ctrl_default_size)
            ctrl.rename(ctrl_name)
            ctrl.setTranslation(ctrl_pos)
            ctrl.setParent(self.ctrl_all)

            # Build an aim node
            # This separated node allow the joints to be driven by the avars.
            looknode_offset_name = nomenclature_jnt_rig.resolve('looknode_offset')
            looknode_offset = pymel.createNode('transform', name=looknode_offset_name)
            #looknode_offset.setTranslation(jnt_pos)
            looknode_offset.setParent(grp_parent)


            looknode_name = nomenclature_jnt_rig.resolve('looknode')
            looknode = pymel.createNode('transform', name=looknode_name)
            #looknode.setTranslation(jnt_pos)
            looknode.setParent(looknode_offset)

            looknode_offset.setTranslation(jnt_pos, space='world')

            # Build an upnode for the eyes.
            # I'm not a fan of upnodes but in this case it's better to guessing the joint orient.
            upnode_name = nomenclature_jnt_rig.resolve('upnode')
            upnode_pos = jnt_pos + pymel.datatypes.Vector(0, 1, 0)
            upnode = pymel.createNode('transform', name=upnode_name)
            upnode.setTranslation(upnode_pos)
            upnode.setParent(grp_parent)

            pymel.aimConstraint(ctrl, looknode,
                                maintainOffset=True,
                                upVector=(0.0, 1.0, 0.0),
                                worldUpObject=upnode,
                                worldUpType='object'
                                )

            # Convert the rotation to avars to additional values can be added.
            avar.connect_matrix(looknode.matrix)


        # TODO: Connect jnts to avars

    def unbuild(self):
        """
        If you are using sub-modules, you might want to clean them here.
        :return:
        """
        super(FaceEyes, self).unbuild()
