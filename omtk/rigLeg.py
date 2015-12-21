import pymel.core as pymel
from classNode import Node
from rigArm import Arm
from libs import libRigging


class Leg(Arm):
    def build(self, *args, **kwargs):
        super(Leg, self).build(orient_ik_ctrl=False, *args, **kwargs)

        # Hack: Ensure the ctrlIK is looking in the right direction
        oMake = self.sysIK.ctrlIK.getShape().create.inputs()[0]
        oMake.normal.set((0, 1, 0))

        self.create_footroll()

    # TODO: Support foot that is not aligned to world plane
    def create_footroll(self):
        jnt_foot = self.sysIK._chain_ik[self.iCtrlIndex]
        jnt_toes = self.sysIK._chain_ik[self.iCtrlIndex + 1]
        jnt_tip = self.sysIK._chain_ik[self.iCtrlIndex + 2]

        # Create FootRoll
        p3Foot = jnt_foot.getTranslation(space='world')
        p3Toes = jnt_toes.getTranslation(space='world')

        offset_f = 5
        offset_b = offset_f * 0.25

        # Create pivots; TODO: Create side pivots
        obj_pivot_m = Node()
        obj_pivot_m.build()
        obj_pivot_m.rename(self._name_rig.resolve('pivotM'))
        obj_pivot_m.t.set(p3Toes)

        obj_pivot_f = Node()
        obj_pivot_f.build()
        obj_pivot_f.rename(self._name_rig.resolve('pivotF'))
        obj_pivot_f.t.set(p3Foot + [0, 0, offset_f])

        obj_pivot_b = Node()
        obj_pivot_b.build()
        obj_pivot_b.rename(self._name_rig.resolve('pivotB'))
        obj_pivot_b.t.set(p3Foot + [0, 0, -offset_b])

        footRoll_root = Node()
        footRoll_root.build()
        footRoll_root.rename(self._name_rig.resolve('footRoll'))

        # Create hyerarchy
        obj_pivot_m.setParent(obj_pivot_f)
        obj_pivot_f.setParent(obj_pivot_b)
        obj_pivot_b.setParent(footRoll_root)
        footRoll_root.setParent(self.grp_rig)
        pymel.parentConstraint(self.sysIK.ctrlIK, footRoll_root, maintainOffset=True)

        # Create attributes
        oAttHolder = self.sysIK.ctrlIK
        pymel.addAttr(oAttHolder, longName='footRoll', k=True)
        pymel.addAttr(oAttHolder, longName='footRollThreshold', k=True, defaultValue=45)
        attFootRoll = oAttHolder.attr('footRoll')
        attFootRollThreshold = oAttHolder.attr('footRollThreshold')

        attr_roll_f = libRigging.create_utility_node('condition', operation=2,
                                                     firstTerm=attFootRoll, secondTerm=attFootRollThreshold,
                                                     colorIfFalseR=0,
                                                     colorIfTrueR=(
                                                         libRigging.create_utility_node('plusMinusAverage', operation=2,
                                                                                        input1D=[attFootRoll,
                                                                                                 attFootRollThreshold]).output1D)).outColorR  # Substract
        attr_roll_m = libRigging.create_utility_node('condition', operation=2, firstTerm=attFootRoll,
                                                     secondTerm=attFootRollThreshold, colorIfTrueR=attFootRollThreshold,
                                                     colorIfFalseR=attFootRoll).outColorR  # Less
        attr_roll_b = libRigging.create_utility_node('condition', operation=2, firstTerm=attFootRoll, secondTerm=0.0,
                                                     colorIfTrueR=0, colorIfFalseR=attFootRoll).outColorR  # Greater
        pymel.connectAttr(attr_roll_m, obj_pivot_m.rotateX)
        pymel.connectAttr(attr_roll_f, obj_pivot_f.rotateX)
        pymel.connectAttr(attr_roll_b, obj_pivot_b.rotateX)

        pymel.parentConstraint(self.sysIK.ctrlIK, self.sysIK.ctrl_swivel,
                               maintainOffset=True)  # TODO: Implement SpaceSwitch

        # Create ikHandles
        ikHandle_foot, ikEffector_foot = pymel.ikHandle(startJoint=jnt_foot, endEffector=jnt_toes, solver='ikSCsolver')
        ikHandle_foot.rename(self._name_rig.resolve('ikHandle', 'foot'))
        ikHandle_foot.setParent(footRoll_root)
        ikHandle_toes, ikEffector_toes = pymel.ikHandle(startJoint=jnt_toes, endEffector=jnt_tip, solver='ikSCsolver')
        ikHandle_toes.rename(self._name_rig.resolve('ikHandle', 'ties'))
        ikHandle_toes.setParent(footRoll_root)

        # Connect ikHandles
        pymel.delete([o for o in self.sysIK._ik_handle.getChildren() if
                      isinstance(o, pymel.nodetypes.Constraint) and not isinstance(o,
                                                                                   pymel.nodetypes.PoleVectorConstraint)])
        pymel.parentConstraint(obj_pivot_m, self.sysIK._ik_handle, maintainOffset=True)
        pymel.parentConstraint(obj_pivot_f, ikHandle_foot, maintainOffset=True)
        pymel.parentConstraint(obj_pivot_b, ikHandle_toes, maintainOffset=True)

        # Handle globalScale
        pymel.connectAttr(self.grp_rig.globalScale, footRoll_root.scaleX)
        pymel.connectAttr(self.grp_rig.globalScale, footRoll_root.scaleY)
        pymel.connectAttr(self.grp_rig.globalScale, footRoll_root.scaleZ)
