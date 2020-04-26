import unittest
import pymel.core as pymel
import omtk
import omtk_test


class SampleTests(omtk_test.TestCase):
    def test_create(self):
        rig_name = "TestRig"
        rig = omtk.create(name=rig_name)
        self.assertTrue(isinstance(rig, omtk.core.classRig.Rig))
        self.assertTrue(rig.name == rig_name)

    def test_plugins(self):
        """
        Ensure that the basic built-in plugins are successfully loaded.
        """
        from omtk.core import plugin_manager

        pm = plugin_manager.plugin_manager

        loaded_plugin_names = [
            plugin.cls.__name__ for plugin in pm.get_loaded_plugins_by_type("modules")
        ]

        builtin_plugin_names = (
            "Arm",
            "FK",
            "AdditiveFK",
            "AvarGrpOnSurface",
            "FaceBrow",
            "FaceEyeLids",
            "FaceEyes",
            "FaceJaw",
            "FaceLips",
            "FaceNose",
            "FaceSquint",
            "Hand",
            "Head",
            "IK",
            "InteractiveFK",
            "Leg",
            "LegQuad",
            "Limb",
            "Neck",
            "Ribbon",
            "SplineIK",
            "Twistbone",
        )

        for plugin_name in builtin_plugin_names:
            self.assertIn(plugin_name, loaded_plugin_names)

    @omtk_test.open_scene("./resources/test_lips.ma")
    def test_avar_connection_persistence(self):
        """Validate connection between avars is conserved between rebuilds."""
        import omtk
        from omtk.modules import rigHead
        from omtk.modules import rigFaceJaw
        from omtk.modules import rigFaceLips
        from omtk.libs import libRigging

        # Create a base rig
        rig = omtk.create()
        rig.add_module(rigHead.Head([pymel.PyNode("jnt_head")]))
        module_jaw = rig.add_module(
            rigFaceJaw.FaceJaw([pymel.PyNode("jnt_jaw"), pymel.PyNode("pSphereShape1")])
        )
        module_lips = rig.add_module(
            rigFaceLips.FaceLips(
                pymel.ls("jnt_lip*", type="joint") + [pymel.PyNode("pSphereShape1")]
            )
        )
        rig.build(strict=True)

        # Connect some avars
        avar_src = next(iter(module_jaw.avars), None).attr_ud
        for avar in module_lips.avars:
            avar_dst = avar.attr_ud
            libRigging.connectAttr_withLinearDrivenKeys(avar_src, avar_dst)

        # Re-build the rig
        rig.unbuild(strict=True)
        rig.build(strict=True)

        # Ensure the avars are still connected.
        avar_src = next(iter(module_jaw.avars), None).attr_ud
        avar_src.set(1.0)
        for avar in module_lips.avars:
            avar_dst = avar.attr_ud
            self.assertAlmostEqual(avar_dst.get(), 1.0)

    def _get_scene_surface_count(self):
        """
        :return: The number of non-intermediate surfaces in the scene.
        """
        surface_shapes = [
            shape
            for shape in pymel.ls(type="nurbsSurface")
            if not shape.intermediateObject.get()
        ]
        return len(surface_shapes)

    @omtk_test.open_scene("./resources/test_lips.ma")
    def test_avargrp_withsurface(self):
        import omtk
        from omtk.modules import rigHead
        from omtk.modules import rigFaceJaw
        from omtk.modules import rigFaceLips

        # Create a base rig
        rig = omtk.create()
        rig.add_module(rigHead.Head([pymel.PyNode("jnt_head")]))
        rig.add_module(
            rigFaceJaw.FaceJaw(
                [pymel.PyNode("jnt_jaw")]
                + [pymel.PyNode("surface_lips"), pymel.PyNode("pSphereShape1")]
            )
        )
        rig.add_module(
            rigFaceLips.FaceLips(
                pymel.ls("jnt_lip*", type="joint")
                + [pymel.PyNode("surface_lips"), pymel.PyNode("pSphereShape1")]
            )
        )

        rig.build(strict=True)
        rig.unbuild(strict=True)
        rig.build(strict=True)

    @omtk_test.open_scene("./resources/test_lips.ma")
    def test_avargrp_areaonsurface_withsurface(self):
        """
        Ensure there's always a nurbsSurface created for an AvarGrpOnSurface and that it is correctly propageted
        to it's child avars.        :return:
        """
        import omtk
        from omtk.modules import rigHead
        from omtk.modules import rigFaceAvarGrps

        # Create a base rig
        rig = omtk.create()
        rig.add_module(rigHead.Head([pymel.PyNode("jnt_head")]))
        rig.add_module(
            rigFaceAvarGrps.AvarGrpOnSurface(
                pymel.ls("jnt_lip*", type="joint")
                + [pymel.PyNode("surface_lips"), pymel.PyNode("pSphereShape1")]
            )
        )

        # Validate the state of the scene before testing.
        self.assertEqual(self._get_scene_surface_count(), 1)

        rig.build(strict=True)
        rig.unbuild(strict=True)

        # Ensure there's still one nurbsSurface in the scene.
        self.assertEqual(self._get_scene_surface_count(), 1)

        # Remove all surfaces
        pymel.delete(pymel.ls(type="nurbsSurface"))
        self.assertEqual(self._get_scene_surface_count(), 0)

        # Re-created the rig and ensure the new surface was correctly created.
        rig.build(strict=True)

    @omtk_test.open_scene("../examples/rig_rlessard_template01.ma")
    def test_rig_rlessard(self):
        self._build_unbuild_build_all(
            test_translate=True, test_rotate=True, test_scale=True
        )

    @omtk_test.open_scene("./resources/test_interactivefk01.ma")
    def test_interactivefk01(self):
        self._build_unbuild_build_all(
            test_translate=False, test_rotate=False, test_scale=False
        )  # todo: re-enabled test t/r/s

    @omtk_test.open_scene("./resources/test_interactivefk02.ma")
    def test_interactivefk02(self):
        self._build_unbuild_build_all(
            test_translate=False, test_rotate=False, test_scale=False
        )  # todo: re-enabled test t/r/s

    @omtk_test.open_scene("./resources/test_interactivefk03.ma")
    def test_interactivefk03(self):
        self._build_unbuild_build_all(
            test_translate=False, test_rotate=False, test_scale=False
        )  # todo: re-enabled test t/r/s

    @unittest.skip(
        "Disabled since break when the default rig is not the standard. Need to extend omtk.create."
    )
    def test_ctrl_space_index_preservation(self):
        """
        Check that after a ctrl have been built once, if we change it's hierarchy's and
        rebuild it, we will keep the old index.
        This ensure any rig update will never break an old animation.
        """
        from omtk.modules import rigFK

        def check_targets_index_match(ctrl):
            self.assertEqual(len(ctrl.targets), len(ctrl.targets_indexes))
            attr_space = ctrl.node.space
            for target, target_index in attr_space.getEnums().iteritems():
                if target == "Local":
                    continue
                target = pymel.PyNode(target)
                self.assertIn(target, ctrl.targets)  # Ensure the target is stored
                logical_index = ctrl.targets.index(target)
                self.assertEqual(target_index, ctrl.targets_indexes[logical_index])

        # Create a simple influence hierarhy
        inf_a = pymel.createNode("joint")
        inf_b = pymel.createNode("joint", parent=inf_a)
        inf_c = pymel.createNode("joint", parent=inf_b)
        inf_d = pymel.createNode("joint", parent=inf_c)

        # Create a simple rig
        r = omtk.create()
        mod_a = r.add_module(rigFK.FK([inf_a]))
        mod_b = r.add_module(rigFK.FK([inf_b]))
        mod_c = r.add_module(rigFK.FK([inf_c]))
        mod_d = r.add_module(rigFK.FK([inf_d]))

        # Build the last module
        mod_d.build()

        # Analyse the indexes
        c = mod_d.ctrls[0]
        old_targets = c.targets
        old_targets_indexes = c.targets_indexes
        check_targets_index_match(c)

        # Unbulid the last module, change the hierarchy and rebuilt it
        mod_d.unbuild()
        inf_d.setParent(inf_b)
        mod_d.build()

        # Analyse the indexes
        c = mod_d.ctrls[0]
        new_targets = c.targets
        new_targets_indexes = c.targets_indexes
        check_targets_index_match(c)

        self.assertListEqual(old_targets, new_targets)
        self.assertListEqual(old_targets_indexes, new_targets_indexes)


if __name__ == "__main__":
    unittest.main()
