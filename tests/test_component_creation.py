"""
Ensure Component create from existing node networks work as intended.
"""
import unittest

import pymel.core as pymel  # easy standalone initialization
from maya import cmds
from omtk.core import classComponent
from omtk.libs import libComponents
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

    def test_creation_manual(self):
        """Ensure we are able to create a component by manually specifying the attributes we want."""
        cmds.file(new=True, force=True)
        src = pymel.createNode('transform')
        dst = pymel.createNode('transform')

        pymel.connectAttr(src.tx, dst.tx)

        component = classComponent.Component.create(
            {'innVal': src.tx}, {'outVal': dst.tx}
        )

        self.assertEqual(component.grp_inn.attr('innVal').inputs(plugs=True), [])
        self.assertEqual(component.grp_inn.attr('innVal').outputs(plugs=True), [src.tx])
        self.assertEqual(component.grp_out.attr('outVal').inputs(plugs=True), [dst.tx])
        self.assertEqual(component.grp_out.attr('outVal').outputs(plugs=True), [])

    def test_creation_manual_component(self):
        """
        Ensure we are able to create a component by manually specifying the attribute we want.
        This time using component attribute types.
        """
        cmds.file(new=True, force=True)
        src = pymel.createNode('transform')
        dst = pymel.createNode('transform')

        pymel.connectAttr(src.tx, dst.tx)

        component = classComponent.Component.create(
            {'innVal': src.t}, {'outVal': dst.rx}
        )

        self.assertEqual(component.grp_inn.attr('innVal').inputs(plugs=True), [])
        self.assertEqual(component.grp_inn.attr('innVal').outputs(plugs=True), [src.t])
        self.assertEqual(component.grp_out.attr('outVal').inputs(plugs=True), [dst.rx])
        self.assertEqual(component.grp_out.attr('outVal').outputs(plugs=True), [])

    # the automatic detection of attribute is maybe to much foward-thinking for now,
    # let's limit ourself to something simpler
    # def test_constraint_network(self):
    #     """
    #     Ensure we are able to correctly manage a simple joint contrained to a controller.
    #     This highlight the issues that can arise when using Maya constraints because of all the
    #     two-way connections involved.
    #     """
    #     cmds.file(new=True, force=True)
    #     anm = pymel.createNode('transform', name='anm')
    #     jnt = pymel.createNode('transform', name='jnt')
    #     pymel.parentConstraint(anm, jnt)
    #
    #     objs = [anm, jnt]
    #
    #     input_attrs, output_attrs = libComponents.identify_network_io_ports(objs)
    #
    #     expected_attrs_inn = {
    #         'anm.parentMatrix[0]',
    #         'anm.rotate',
    #         'anm.rotateOrder',
    #         'anm.rotatePivot',
    #         'anm.rotatePivotTranslate',
    #         'anm.scale',
    #         'anm.translate',
    #         'jnt.rotatePivot',
    #         'jnt.rotateOrder',
    #         'jnt.rotatePivotTranslate',
    #         'jnt.parentInverseMatrix[0]',
    #     }
    #     expected_attrs_out = {
    #         'jnt.rotateX',
    #         'jnt.rotateY',
    #         'jnt.rotateZ',
    #         'jnt.translateX',
    #         'jnt.translateY',
    #         'jnt.translateZ',
    #     }
    #
    #     self._debug_io_attrs(input_attrs, output_attrs)
    #     self._asset_io_attributes_equal(input_attrs, expected_attrs_inn)
    #     self._asset_io_attributes_equal(output_attrs, expected_attrs_out)
    #
    #     component = classComponent.Component.from_attributes(input_attrs, output_attrs)
    #     hub_inn = component.grp_inn
    #     hub_out = component.grp_out
    #     for obj in objs:
    #         for attr in obj.listAttr():
    #             self.assertFalse(attr.isSource(), msg="Attribute {0} is source!".format(attr))
    #             self.assertFalse(attr.isDestination(), msg="Attribute {0} is destination!".format(attr))


if __name__ == '__main__':
    unittest.main()
