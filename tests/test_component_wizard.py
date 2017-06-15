"""
Ensure Component create from existing node networks work as intended.
"""
import unittest
import pymel.core as pymel  # easy standalone initialization
from maya import cmds
from omtk.libs import libComponents


class ComponentCreationTestCase(unittest.TestCase):
    def _debug_io_attrs(self, input_attrs, output_attrs):
        print("Input attributes are: ")
        for attr in input_attrs:
            print(attr)
        print("Output attributes are:")
        for attr in output_attrs:
            print(attr)

    def _asset_io_attributes_equal(self, inn_attrs, out_attrs, expected_inn_attr_names, expected_out_attr_names):
        inn_attr_names = {attr.__melobject__() for attr in inn_attrs}
        out_attr_names = {attr.__melobject__() for attr in out_attrs}
        self.assertEqual(inn_attr_names, expected_inn_attr_names)
        self.assertEqual(out_attr_names, expected_out_attr_names)

    def test_constraint_network(self):
        """
        Ensure we are able to correctly manage a simple joint contrained to a controller.
        This highlight the issues that can arrise when using Maya constraints because of all the
        two-way connections involved.
        """
        cmds.file(new=True, force=True)
        anm = pymel.createNode('transform', name='anm')
        jnt = pymel.createNode('transform', name='jnt')
        pymel.parentConstraint(anm, jnt)

        objs = [anm, jnt]

        input_attrs, output_attrs = libComponents.identify_network_io_ports(objs)

        expected_attrs_inn = {
            'anm.parentMatrix[0]',
            'anm.rotate',
            'anm.rotateOrder',
            'anm.rotatePivot',
            'anm.rotatePivotTranslate',
            'anm.scale',
            'anm.translate',
        }
        expected_attrs_out = {
            'jnt.rotateX',
            'jnt.rotateY',
            'jnt.rotateZ',
            'jnt.translateX',
            'jnt.translateY',
            'jnt.translateZ',
        }

        self._debug_io_attrs(input_attrs, output_attrs)

        # self._asset_io_attributes_equal(input_attrs, output_attrs, expected_attrs_inn, expected_attrs_out)


if __name__ == '__main__':
    unittest.main()
