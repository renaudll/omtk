import unittest
import pymel.core as pymel


class ModuleFkTest(unittest.TestCase):
    def test_simple_fk(self):
        import omtk
        from omtk.modules.module_fk import FK

        pymel.select(clear=True)
        jnt_1 = pymel.joint(position=(0, 0, 0))
        jnt_2 = pymel.joint(position=(0, 2, 0))
        jnt_3 = pymel.joint(position=(3, 0, 0))
        rig = omtk.create()
        module = FK([jnt_1, jnt_2, jnt_3])
        rig.add_module(module)
        module.build()



if __name__ == '__main__':
    unittest.main()
