"""
Ensure we are able to reconize that a Component should be updated and to update it.
"""
import os
import shutil
import unittest
import pymel.core as pymel  # easy standalone initialization
from maya import cmds
import tempfile
from omtk.libs import libComponents
from omtk.core import component
from omtk.libs import libRigging
from omtk.core.component_definition import ComponentDefinition
from omtk.core.component_registry import ComponentRegistry


class ComponentUpdateTestCase(unittest.TestCase):
    def setUp(self):
        # Create an empty file to play with.
        # self._tmp_path = tempfile.mktemp('.ma')
        cmds.file(new=True, force=True)
        # cmds.file(rename=self._tmp_path)
        # cmds.file(save=True, force=True, type='mayaAscii')

        self._tmp_dir = tempfile.mkdtemp()

        self._registry = ComponentRegistry([self._tmp_dir])

    def tearDown(self):
        # if os.path.exists(self._tmp_path):
        #     os.remove(self._tmp_path)
        if os.path.exists(self._tmp_dir):
            shutil.rmtree(self._tmp_dir)

    def _create_multiply_component(self, multiplier=1.0):
        """Create a simple component that does a multiplication. For testing purpose."""
        u = libRigging.create_utility_node(
            'multiplyDivide',
            input2X=multiplier,
        )
        inst = component.from_attributes_map(
            {'inn': u.input1X},
            {'out': u.outputX},
        )
        return inst

    def test_component_save(self):
        # Create the first version of a component
        c1 = self._create_multiply_component(1.0)
        c1_def = ComponentDefinition(
            name='test',
            version='1',
            uid='1'
        )
        self._registry.register(c1, c1_def)
        self.assertTrue(self._registry.is_latest_component_version(c1_def))

        # Create the second version of a component
        c2 = self._create_multiply_component(2.0)
        c2_def = ComponentDefinition(
            name='test',
            version='2',
            uid='1',
        )
        self._registry.register(c2, c2_def)
        self.assertFalse(self._registry.is_latest_component_version(c1_def))
        self.assertTrue(self._registry.is_latest_component_version(c2_def))

        cmds.file(new=True, force=True)

        t1 = pymel.createNode('transform')
        t2 = pymel.createNode('transform')

        inst = c1_def.instanciate()
        t1.translateX.set(1.0)
        pymel.connectAttr(t1.translateX, inst.grp_inn.inn)
        pymel.connectAttr(inst.grp_out.out, t2.translateX)

        self.assertFalse(self._registry.is_latest_component_version(inst.get_definition()))
        old_namespace = inst.namespace
        map_inn, map_out = inst.get_connections_relative()
        inst.delete(disconnect=True)
        inst_2 = c2_def.instanciate(name=old_namespace)  # todo: rename to namespace
        for attr_name, attr_srcs in map_inn.iteritems():
            for attr_src in attr_srcs:
                inst_2.connect_to_input_attr(attr_name, attr_src)
        for attr_name, attr_dsts in map_out.iteritems():
            for attr_dst in attr_dsts:
                inst_2.connect_to_output_attr(attr_name, attr_dst)
        self.assertEqual(old_namespace, inst_2.namespace)

        self.assertEqual(2.0, t2.translateX.get())



if __name__ == '__main__':
    unittest.main()
