"""
Ensure Component create from existing node networks work as intended.
"""
import unittest

import pymel.core as pymel  # easy standalone initialization
from maya import cmds
from omtk.core import component
from omtk.core.component import Component

class ComponentCreationTestCase(unittest.TestCase):
    def _debug_io_attrs(self, input_attrs, output_attrs):
        print("Input attributes are: ")
        for attr in input_attrs:
            print(attr)
        print("Output attributes are:")
        for attr in output_attrs:
            print(attr)

    def _asset_io_attributes_equal(self, inn_attrs, expected_inn_attr_names):
        inn_attr_names = {attr.__melobject__() for attr in inn_attrs}
        self.assertEqual(inn_attr_names, expected_inn_attr_names)

    def test_create_empty_component(self):
        """Ensure we are able to create an empty component."""
        namespace = 'component'
        inst = component.create_empty(namespace=namespace)

        cmpt_namespace = inst.get_namespace()
        cmds.namespace(setNamespace=cmpt_namespace)

        n1 = pymel.createNode('transform', name='n1')

        self.assertIn(n1, inst)

    def test_create_component_from_objects(self):
        cmds.file(new=True, force=True)
        obj = pymel.createNode('transform')

        namespace = 'component'
        inst = component.from_nodes([obj], namespace=namespace)

        self.assertEqual(namespace, inst.get_namespace())
        self.assertEqual(namespace, obj.namespace().strip(':'))

    def test_create_component_from_attributes(self):
        """
        Ensure we are able to create a component by manually specifying the attributes we want.
        """
        cmds.file(new=True, force=True)
        src = pymel.createNode('transform')
        dst = pymel.createNode('transform')
        pymel.connectAttr(src.tx, dst.tx)

        namespace = 'component'
        inst = component.from_attributes(
            {'innVal': src.tx}, {'outVal': dst.tx}, namespace=namespace
        )

        # Validate that the attributes have been included in the component.
        self.assertEqual(inst.grp_inn.attr('innVal').inputs(plugs=True), [])
        self.assertEqual(inst.grp_inn.attr('innVal').outputs(plugs=True), [src.tx])
        self.assertEqual(inst.grp_out.attr('outVal').inputs(plugs=True), [dst.tx])
        self.assertEqual(inst.grp_out.attr('outVal').outputs(plugs=True), [])

        # Validate that the objects are under a namespace.
        for obj in [src, dst, inst.grp_inn, inst.grp_out]:
            self.assertEqual(namespace, obj.namespace().strip(':'))

    def test_create_component_from_compound_attributes(self):
        """
        Ensure we are able to create a component by manually specifying the attribute we want.
        This time using compound attribute types.
        """
        cmds.file(new=True, force=True)
        src = pymel.createNode('transform')
        dst = pymel.createNode('transform')

        pymel.connectAttr(src.tx, dst.tx)

        inst = component.from_attributes(
            {'innVal': src.t}, {'outVal': dst.rx}
        )

        self.assertEqual(inst.grp_inn.attr('innVal').inputs(plugs=True), [])
        self.assertEqual(inst.grp_inn.attr('innVal').outputs(plugs=True), [src.t])
        self.assertEqual(inst.grp_out.attr('outVal').inputs(plugs=True), [dst.rx])
        self.assertEqual(inst.grp_out.attr('outVal').outputs(plugs=True), [])


if __name__ == '__main__':
    unittest.main()
