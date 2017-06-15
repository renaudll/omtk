"""
Ensure Component create from existing node networks work as intended.
"""
import unittest
import pymel.core as pymel  # easy standalone initialization
from maya import cmds
from omtk.libs import libComponents


class ComponentCreationTestCase(unittest.TestCase):
    def test_constraint_network(self):
        cmds.file(new=True, force=True)
        anm = pymel.createNode('transform', name='anm')
        jnt = pymel.createNode('transform', name='jnt')
        constraint = pymel.parentConstraint(anm, jnt)

        objs = [anm, jnt, constraint]

        input_attrs, output_attrs = libComponents.identify_network_io_ports(objs)
        print input_attrs, output_attrs


if __name__ == '__main__':
    unittest.main()
