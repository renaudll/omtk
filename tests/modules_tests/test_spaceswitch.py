import omtk
import pymel.core as pymel
import omtk_test
from omtk.vendor import libSerialization


class SampleTests(omtk_test.TestCase):
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
                if target == 'Local':
                    continue
                target = pymel.PyNode(target)
                self.assertIn(target, ctrl.targets)  # Ensure the target is stored
                logical_index = ctrl.targets.index(target)
                self.assertEqual(target_index, ctrl.targets_indexes[logical_index])

        # Create a simple influence hierarhy
        inf_a = pymel.createNode('joint')
        inf_b = pymel.createNode('joint', parent=inf_a)
        inf_c = pymel.createNode('joint', parent=inf_b)
        inf_d = pymel.createNode('joint', parent=inf_c)

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
