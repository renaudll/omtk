import omtk
import pymel.core as pymel
import omtk_test
from omtk.vendor import libSerialization


class SampleTests(omtk_test.TestCase):
    def test_reload(self):
        """
        Ensure we are able to completely reload omtk.
        """
        import omtk
        omtk.reload_()

    def test_create(self):
        """
        Ensure we are able to build a Rig instance.
        :return:
        """
        from omtk.core.rig import Rig
        rig_name = 'TestRig'
        rig = omtk.create(name=rig_name)
        self.assertTrue(isinstance(rig, Rig))
        self.assertTrue(rig.name == rig_name)

    def test_plugins(self):
        """
        Ensure that the basic built-in plugins are successfully loaded.
        """
        # from omtk import plugin_manager
        from omtk.api import plugin_manager
        pm = plugin_manager.plugin_manager

        loaded_plugin_names = [plugin.cls.__name__ for plugin in pm.get_loaded_plugins_by_type('modules')]

        builtin_plugin_names = (
            'Arm',
            'FK',
            'AdditiveFK',
            'AvarGrpOnSurface',
            'FaceBrow',
            'FaceEyeLids',
            'FaceEyes',
            'FaceJaw',
            'FaceLips',
            'FaceNose',
            'FaceSquint',
            'Hand',
            'Head',
            'IK',
            'InteractiveFK',
            'Leg',
            'LegQuad',
            'Limb',
            'Neck',
            'Ribbon',
            'SplineIK',
            'Twistbone',
        )

        for plugin_name in builtin_plugin_names:
            self.assertIn(plugin_name, loaded_plugin_names)

    @omtk_test.open_scene('../examples/rig_rlessard_template01.ma')
    def test_rig_rlessard(self):
        self._build_unbuild_build_all(test_translate=True, test_rotate=True, test_scale=True)
