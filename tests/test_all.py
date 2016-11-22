import os
import mayaunittest
from maya import cmds
import pymel.core as pymel
import omtk
import libSerialization

def open_scene(path_local):
    def deco_open(f):
        def f_open(*args, **kwargs):
            m_path_local = path_local # make mutable

            path = os.path.join(os.path.dirname(__file__), m_path_local)
            if not os.path.exists(path):
                raise Exception("File does not exist on disk! {0}".format(path))

            cmds.file(path, open=True, f=True)
            return f(*args, **kwargs)
        return f_open
    return deco_open

class SampleTests(mayaunittest.TestCase):

    def _get_holded_shapes(self):
        shapes = []
        for net in libSerialization.get_networks_from_class('BaseCtrl'):
            if net.hasAttr('shapes'):
                shapes.extend(net.shapes.inputs())
        return shapes

    def _build_unbuild_build(self):
        num_holder_shapes_before = len(self._get_holded_shapes())

        omtk.build_all(strict=True)
        omtk.unbuild_all()
        omtk.build_all(strict=True)

        # Ensure no shapes are left after a rebuild.
        num_holder_shapes_after = len(self._get_holded_shapes())
        self.assertEqual(num_holder_shapes_before, num_holder_shapes_after)

    def test_create(self):
        rig_name = 'TestRig'
        rig = omtk.create(name=rig_name)
        self.assertTrue(isinstance(rig, omtk.core.classRig.Rig))
        self.assertTrue(rig.name == rig_name)

    @open_scene('./test_lips.ma')
    def test_avar_connection_persistence(self):
        import omtk
        from omtk.modules import rigHead
        from omtk.modules import rigFaceJaw
        from omtk.modules import rigFaceLips
        from omtk.libs import libRigging

        # Create a base rig
        rig = omtk.create()
        rig.add_module(rigHead.Head([pymel.PyNode('jnt_head')]))
        module_jaw = rig.add_module(rigFaceJaw.FaceJaw([pymel.PyNode('jnt_jaw')]))
        module_lips = rig.add_module(rigFaceLips.FaceLips(pymel.ls('jnt_lip*', type='joint')))
        rig.build()

        # Connect some avars
        avar_src = next(iter(module_jaw.avars), None).attr_ud
        for avar in module_lips.avars:
            avar_dst = avar.attr_ud
            libRigging.connectAttr_withLinearDrivenKeys(avar_src, avar_dst)

        # Re-build the rig
        rig.unbuild()
        rig.build()

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
        surface_shapes = [shape for shape in pymel.ls(type='nurbsSurface') if not shape.intermediateObject.get()]
        return len(surface_shapes)

    @open_scene('./test_lips.ma')
    def test_avargrp_withsurface(self):
        import omtk
        from omtk.modules import rigHead
        from omtk.modules import rigFaceJaw
        from omtk.modules import rigFaceLips

        # Create a base rig
        rig = omtk.create()
        rig.add_module(rigHead.Head([pymel.PyNode('jnt_head')]))
        rig.add_module(rigFaceJaw.FaceJaw([pymel.PyNode('jnt_jaw')]))
        rig.add_module(rigFaceLips.FaceLips(pymel.ls('jnt_lip*', type='joint') + [pymel.PyNode('surface_lips')]))

        # Ensure there's only one nurbsSurface in the scene.
        self.assertEqual(self._get_scene_surface_count(), 1)

        rig.build()
        rig.unbuild()
        rig.build()

        # Ensure there's still only one nurbsSurface in the scene.
        self.assertEqual(self._get_scene_surface_count(), 1)

    @open_scene('./test_lips.ma')
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
        rig.add_module(rigHead.Head([pymel.PyNode('jnt_head')]))
        rig.add_module(rigFaceAvarGrps.AvarGrpAreaOnSurface(pymel.ls('jnt_lip*', type='joint') + [pymel.PyNode('surface_lips')]))

        # Validate the state of the scene before testing.
        self.assertEqual(self._get_scene_surface_count(), 1)

        rig.build()

        # Ensure there's one one nurbsSurface in the scene.
        self.assertEqual(self._get_scene_surface_count(), 1)

        rig.unbuild()

        # Ensure there's still one nurbsSurface in the scene.
        self.assertEqual(self._get_scene_surface_count(), 1)

        # Remove all surfaces
        pymel.delete(pymel.ls(type='nurbsSurface'))
        self.assertEqual(self._get_scene_surface_count(), 0)

        # Re-created the rig and ensure the new surface was correctly created.
        rig.build()

        # Ensure there's still one nurbsSurface in the scene.
        self.assertEqual(self._get_scene_surface_count(), 1)


    # @open_scene("../examples/rig_squeeze_template01.ma")
    # def test_rig_squeeze(self):
    #     self._build_unbuild_build()
    #
    # @open_scene('../examples/rig_rlessard_template01.ma')
    # def test_rig_rlessard(self):
    #     self._build_unbuild_build()

    # def test_ctrl_space_index_preservation(self):
    #     """
    #     Check that after a ctrl have been built once, if we change it's hierarchy's and
    #     rebuild it, we will keep the old index.
    #     This ensure any rig update will never break an old animation.
    #     """
    #     from omtk.modules import rigFK
    #
    #     def check_targets_index_match(ctrl):
    #         self.assertEqual(len(ctrl.targets), len(ctrl.targets_indexes))
    #         attr_space = ctrl.node.space
    #         for target, target_index in attr_space.getEnums().iteritems():
    #             self.assertIn(target, ctrl.targets)  # Ensure the target is stored
    #             logical_index = ctrl.targets.index(target)
    #             self.assertEqual(target_index, ctrl.targets_indexes[logical_index])
    #
    #     # Create a simple influence hierarhy
    #     inf_a = pymel.createNode('joint')
    #     inf_b = pymel.createNode('joint', parent=inf_a)
    #     inf_c = pymel.createNode('joint', parent=inf_b)
    #     inf_d = pymel.createNode('joint', parent=inf_c)
    #
    #     # Create a simple rig
    #     r = omtk.create()
    #     mod_a = r.add_module(rigFK.FK, [inf_a])
    #     mod_b = r.add_module(rigFK.FK, [inf_b])
    #     mod_c = r.add_module(rigFK.FK, [inf_c])
    #     mod_d = r.add_module(rigFK.FK, [inf_d])
    #
    #     # Build the last module
    #     mod_d.build()
    #
    #     # Analyse the indexes
    #     c = mod_d.ctrls[0]
    #     old_targets = c.targets
    #     old_targets_indexes = c.targets_indexes
    #     check_targets_index_match(c)
    #
    #     # Unbulid the last module, change the hierarchy and rebuilt it
    #     mod_d.unbuild()
    #     inf_d.setParent(inf_b)
    #     mod_d.build()
    #
    #     # Analyse the indexes
    #     c = mod_d.ctrls[0]
    #     new_targets = c.targets
    #     new_targets_indexes = c.targets_indexes
    #     check_targets_index_match(c)
    #
    #     self.assertListEqual(old_targets, new_targets)
    #     self.assertListEqual(old_targets_indexes, new_targets_indexes)
