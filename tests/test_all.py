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
