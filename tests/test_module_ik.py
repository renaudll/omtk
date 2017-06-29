import unittest
import pymel.core as pymel


class ModuleIkTest(unittest.TestCase):
    def test_3jnt_ik(self):
        import omtk
        from omtk.modules.module_ik import IK

        pymel.select(clear=True)
        jnt_1 = pymel.joint(position=(0, 0, 0))
        jnt_2 = pymel.joint(position=(0, 2, 0))
        jnt_3 = pymel.joint(position=(3, 0, 0))
        rig = omtk.create()
        module = IK([jnt_1, jnt_2, jnt_3])
        rig.add_module(module)
        module.build()

        module.ctrl_ik.setTranslation((5, 0, 0), space='world')
        self.assertEqual(jnt_1.getTranslation(space='world'), pymel.datatypes.Vector(0, 0, 0))
        self.assertEqual(jnt_2.getTranslation(space='world'), pymel.datatypes.Vector(2, 0, 0))
        self.assertEqual(jnt_3.getTranslation(space='world'), pymel.datatypes.Vector(5, 0, 0))


if __name__ == '__main__':
    unittest.main()
