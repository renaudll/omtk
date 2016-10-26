import os
import mayaunittest
from maya import cmds
import pymel.core as pymel
import omtk
import omtk
import libSerialization
from omtk.libs import libRigging
from omtk.modules.rigArm import Arm
from omtk.animation import ikfkTools
from omtk.animation import ikfkTools

class SampleTests(mayaunittest.TestCase):

    def _create_simple_arm_build_and_export(self):
        jnt_1 = pymel.joint(position=[0,0,0])
        jnt_2 = pymel.joint(position=[10,0,10])
        jnt_3 = pymel.joint(position=[20,0,0])

        rig = omtk.create()
        module = Arm([jnt_1, jnt_2, jnt_3])
        rig.add_module(module)
        rig.build()
        libSerialization.export_network(rig)

        return rig, module

    def _verify_ik_fk_match(self, module):
        ctrl_ik = module.sysIK.ctrl_ik.node
        ctrl_swivel = module.sysIK.ctrl_swivel.node
        ctrl_fk_01 = module.sysFK.ctrls[0].node
        ctrl_fk_02 = module.sysFK.ctrls[1].node
        ctrl_fk_03 = module.sysFK.ctrls[2].node

        ctrl_ik_pos = ctrl_ik.getTranslation(space='world')
        ctrl_swivel_pos = ctrl_swivel.getTranslation(space='world')
        ctrl_fk_01_pos = ctrl_fk_01.getTranslation(space='world')
        ctrl_fk_02_pos = ctrl_fk_02.getTranslation(space='world')
        ctrl_fk_03_pos = ctrl_fk_03.getTranslation(space='world')

        # Verify IK ctrl
        self.assertAlmostEqual((ctrl_ik_pos - ctrl_fk_03_pos).length(), 0, places=3)

        # Verify IK swivel
        look_vec = ctrl_fk_03_pos - ctrl_fk_01_pos
        upp_vec = ctrl_fk_02_pos - ctrl_fk_01_pos
        tm = libRigging.get_matrix_from_direction(look_vec, upp_vec,
            look_axis=pymel.datatypes.Vector.xAxis,
            upp_axis=pymel.datatypes.Vector.zAxis
        )
        distorsion = (ctrl_swivel_pos * tm.inverse()).y
        self.assertAlmostEqual(distorsion, 0)

    def test_ikfk_switch(self):
        rig, module = self._create_simple_arm_build_and_export()

        ctrl_ik = module.sysIK.ctrl_ik.node

        ctrl_fk_01 = module.sysFK.ctrls[0].node
        ctrl_fk_02 = module.sysFK.ctrls[1].node
        ctrl_fk_03 = module.sysFK.ctrls[2].node

        # Do a brainless IK->FK->IK switch to ensure nothing is moving.
        pymel.select(ctrl_ik)
        ikfkTools.switchToFk()
        self._verify_ik_fk_match(module)
        ikfkTools.switchToIk()
        self._verify_ik_fk_match(module)

        # Modify IK pose and perform an IK-FK switch
        ctrl_ik.setTranslation([10,0,0], space='world')
        pymel.select(ctrl_ik)
        ikfkTools.switchToFk()
        self._verify_ik_fk_match(module)

        # Modify FK pose and perform an FK->IK switch
        ctrl_fk_01.rotateX.set(45)
        ctrl_fk_02.rotateY.set(-45)
        pymel.select(ctrl_fk_02)
        ikfkTools.switchToIk()
        self._verify_ik_fk_match(module)
