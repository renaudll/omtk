"""
Ensure Component create from existing node networks work as intended.
"""
import unittest

import pymel.core as pymel  # easy standalone initialization
from maya import cmds
from omtk import component
from omtk.libs import libRigging


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

        n1 = pymel.createNode('transform', name='node')

        self.assertIn(n1, inst)

    def test_create_component_from_objects(self):
        cmds.file(new=True, force=True)
        obj = pymel.createNode('transform')

        namespace = 'component'
        inst = component.from_nodes([obj], namespace=namespace)

        self.assertEqual('component1', inst.get_namespace())
        self.assertEqual('component1', obj.namespace().strip(':'))

    def test_create_component_from_objects_nested(self):
        """
        Ensure desired behavior when creating a component sandwitched between existing connections.
        """
        cmds.file(new=True, force=True)
        n1 = pymel.createNode('transform')
        n2 = pymel.createNode('transform')
        n3 = pymel.createNode('transform')
        n4 = pymel.createNode('transform')
        n5 = pymel.createNode('transform')
        pymel.connectAttr(n1.tx, n2.tx)
        pymel.connectAttr(n2.tx, n3.tx)
        pymel.connectAttr(n3.tx, n4.tx)
        pymel.connectAttr(n4.tx, n5.tx)

        # Create first component
        namespace = 'component'
        c1 = component.from_nodes([n2, n3, n4], namespace=namespace)

        self.assertEqual(c1.grp_inn.longName(), 'component1:inn')
        self.assertEqual(c1.grp_out.longName(), 'component1:out')

        # Validate connections
        # Note that for now, create a component from nodes don't populate the hubs automatically.
        # This might be something that we are interested to do but I'm scared atm haha.
        # self.assertEqual(c1.grp_inn.attr('innVal').inputs(plugs=True), [node.tx])
        # self.assertEqual(c1.grp_inn.attr('innVal').outputs(plugs=True), [n2.tx])
        # self.assertEqual(c1.grp_out.attr('outVal').inputs(plugs=True), [n4.tx])
        # self.assertEqual(c1.grp_out.attr('outVal').outputs(plugs=True), [n5.tx])

        # Validate namespaces
        self.assertEqual('', self._get_namespace(n1))
        self.assertEqual('component1', self._get_namespace(n2))
        self.assertEqual('component1', self._get_namespace(n3))
        self.assertEqual('component1', self._get_namespace(n4))
        self.assertEqual('', self._get_namespace(n5))
        self.assertEqual('component1', self._get_namespace(c1.grp_inn))
        self.assertEqual('component1', self._get_namespace(c1.grp_out))

        # Create a second component under the first component
        namespace = 'component'
        c2 = component.from_nodes([n3], namespace=namespace)

        # Validate connections
        # node -> c1 -> n2 -> c2 -> n3 -> c2 -> n4 -> c1 -> n5
        # self.assertEqual(c1.grp_inn.attr('innVal').inputs(plugs=True), [node.tx])
        # self.assertEqual(c1.grp_inn.attr('innVal').outputs(plugs=True), [n2.tx])
        # self.assertEqual(c2.grp_inn.attr('innVal').inputs(plugs=True), [n2.tx])
        # self.assertEqual(c2.grp_inn.attr('innVal').outputs(plugs=True), [n3.tx])
        # self.assertEqual(c2.grp_out.attr('outVal').inputs(plugs=True), [n3.tx])
        # self.assertEqual(c2.grp_out.attr('outVal').outputs(plugs=True), [n4.tx])
        # self.assertEqual(c1.grp_out.attr('outVal').inputs(plugs=True), [n4.tx])
        # self.assertEqual(c1.grp_out.attr('outVal').outputs(plugs=True), [n5.tx])

        # Validate namespaces
        self.assertEqual('', self._get_namespace(n1))
        self.assertEqual('component1', self._get_namespace(n2))
        self.assertEqual('component1:component1', self._get_namespace(n3))
        self.assertEqual('component1', self._get_namespace(n4))
        self.assertEqual('', self._get_namespace(n5))
        self.assertEqual('component1', self._get_namespace(c1.grp_inn))
        self.assertEqual('component1', self._get_namespace(c1.grp_out))
        self.assertEqual('component1:component1', self._get_namespace(c2.grp_inn))
        self.assertEqual('component1:component1', self._get_namespace(c2.grp_out))

    def test_create_component_from_attributes(self):
        """
        Ensure we are able to create a component by manually specifying the attributes we want.
        """
        cmds.file(new=True, force=True)
        src = pymel.createNode('transform')
        dst = pymel.createNode('transform')
        pymel.connectAttr(src.tx, dst.tx)

        namespace = 'component'
        expected_namespace = 'component1'
        inst = component.from_attributes_map(
            {'innVal': src.tx}, {'outVal': dst.tx}, namespace=namespace
        )

        # Validate that the attributes have been included in the component.
        self.assertEqual(inst.grp_inn.attr('innVal').inputs(plugs=True), [])
        self.assertEqual(inst.grp_inn.attr('innVal').outputs(plugs=True), [src.tx])
        self.assertEqual(inst.grp_out.attr('outVal').inputs(plugs=True), [dst.tx])
        self.assertEqual(inst.grp_out.attr('outVal').outputs(plugs=True), [])

        # Validate that the objects are under a namespace.
        for obj in [src, dst, inst.grp_inn, inst.grp_out]:
            self.assertEqual(expected_namespace, obj.namespace().strip(':'))

    @staticmethod
    def _get_namespace(obj):
        return obj.namespace().strip(':')

    def test_create_component_from_attributes_nested(self):
        """
        Ensure desired behavior when creating a component sandwitched between existing connections.
        """
        # Create a 5-daisy-chain of nodes
        # node.tx -> n2.tx -> n3.tx -> n4.tx -> n5.tx
        cmds.file(new=True, force=True)
        n1 = pymel.createNode('transform')
        n2 = pymel.createNode('transform')
        n3 = pymel.createNode('transform')
        n4 = pymel.createNode('transform')
        n5 = pymel.createNode('transform')
        pymel.connectAttr(n1.tx, n2.tx)
        pymel.connectAttr(n2.tx, n3.tx)
        pymel.connectAttr(n3.tx, n4.tx)
        pymel.connectAttr(n4.tx, n5.tx)

        # Create first component
        # node.tx -> ( n2.tx -> n3.tx -> n4.tx ) -> n5.tx
        namespace = 'component'
        c1 = component.from_attributes_map(
            {'innVal': n2.tx}, {'outVal': n4.tx}, namespace=namespace
        )

        # Validate connections
        self.assertEqual(c1.grp_inn.attr('innVal').inputs(plugs=True), [n1.tx])
        self.assertEqual(c1.grp_inn.attr('innVal').outputs(plugs=True), [n2.tx])
        self.assertEqual(c1.grp_out.attr('outVal').inputs(plugs=True), [n4.tx])
        self.assertEqual(c1.grp_out.attr('outVal').outputs(plugs=True), [n5.tx])

        # Validate namespaces
        self.assertEqual('', self._get_namespace(n1))
        self.assertEqual('component1', self._get_namespace(n2))
        self.assertEqual('component1', self._get_namespace(n3))
        self.assertEqual('component1', self._get_namespace(n4))
        self.assertEqual('', self._get_namespace(n5))
        self.assertEqual('component1', self._get_namespace(c1.grp_inn))
        self.assertEqual('component1', self._get_namespace(c1.grp_out))

        # Create a second component inside the first component
        # node -> ( n2 -> ( n3.tx ) -> n4 ) -> c5
        namespace = 'component'
        c2 = component.from_attributes_map(
            {'innVal': n3.tx}, {'outVal': n3.tx}, namespace=namespace
        )

        # Validate connections
        self.assertEqual(c1.grp_inn.attr('innVal').inputs(plugs=True), [n1.tx])
        self.assertEqual(c1.grp_inn.attr('innVal').outputs(plugs=True), [n2.tx])
        self.assertEqual(c2.grp_inn.attr('innVal').inputs(plugs=True), [n2.tx])
        self.assertEqual(c2.grp_inn.attr('innVal').outputs(plugs=True), [n3.tx])
        self.assertEqual(c2.grp_out.attr('outVal').inputs(plugs=True), [n3.tx])
        self.assertEqual(c2.grp_out.attr('outVal').outputs(plugs=True), [n4.tx])
        self.assertEqual(c1.grp_out.attr('outVal').inputs(plugs=True), [n4.tx])
        self.assertEqual(c1.grp_out.attr('outVal').outputs(plugs=True), [n5.tx])

        # Validate namespaces
        self.assertEqual('', self._get_namespace(n1))
        self.assertEqual('component1', self._get_namespace(n2))
        self.assertEqual('component1:component1', self._get_namespace(n3))
        self.assertEqual('component1', self._get_namespace(n4))
        self.assertEqual('', self._get_namespace(n5))
        self.assertEqual('component1', self._get_namespace(c1.grp_inn))
        self.assertEqual('component1', self._get_namespace(c1.grp_out))
        self.assertEqual('component1:component1', self._get_namespace(c2.grp_inn))
        self.assertEqual('component1:component1', self._get_namespace(c2.grp_out))

    def test_create_component_from_compound_attributes(self):
        """
        Ensure we are able to create a component by manually specifying the attribute we want.
        This time using compound attribute types.
        """
        cmds.file(new=True, force=True)
        src = pymel.createNode('transform')
        dst = pymel.createNode('transform')

        pymel.connectAttr(src.tx, dst.tx)

        inst = component.from_attributes_map(
            {'innVal': src.t}, {'outVal': dst.rx}
        )

        self.assertEqual(inst.grp_inn.attr('innVal').inputs(plugs=True), [])
        self.assertEqual(inst.grp_inn.attr('innVal').outputs(plugs=True), [src.t])
        self.assertEqual(inst.grp_out.attr('outVal').inputs(plugs=True), [dst.rx])
        self.assertEqual(inst.grp_out.attr('outVal').outputs(plugs=True), [])

    def test_create_blend_transforms_component(self):
        """
        Test a component known to by hard to create.
        """
        cmds.file(new=True, force=True)
        n1 = pymel.createNode('transform', name='node')
        n2 = pymel.createNode('transform', name='n2')
        n3 = pymel.createNode('transform', name='n3')
        u1 = libRigging.create_utility_node(
            'blendColors',
            name='u1',
            color1=n1.t,
            color2=n2.t
        )
        pymel.connectAttr(u1.output, n3.t)
        u2 = libRigging.create_utility_node(
            'blendColors',
            name='u2',
            color1=n1.r,
            color2=n2.r,
        )
        pymel.connectAttr(u2.output, n3.r)

        inst = component.from_attributes([u1.color1, u1.color2, u2.color1, u2.color2], [u1.output, u2.output])

        # This is what it should be when called from the ui.
        # inst = component.from_nodes([u1, u2])

        print list(inst.iter_attributes())
        # self.assertEqual(inst.grp_inn.attr('innTranslate1').inputs(plugs=True), [])
        # self.assertEqual(inst.grp_inn.attr('innTranslate1').outputs(plugs=True), [node.t])


if __name__ == '__main__':
    unittest.main()
