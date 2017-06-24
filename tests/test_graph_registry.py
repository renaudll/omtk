"""
Ensure propre behaviour or the GraphController, GraphRegistry and every related models.
"""
import unittest
import logging

import pymel.core as pymel
from maya import cmds
from omtk.libs import libRigging
from omtk.libs import libComponents
from omtk.qt_widgets.nodegraph_widget.nodegraph_model import NodeGraphModel

log = logging.getLogger('omtk')
log.setLevel(logging.DEBUG)


class GraphRegistryTest(unittest.TestCase):
    def setUp(self):
        self.registry = NodeGraphModel()
        cmds.file(new=True, force=True)

    # def test_node_model_from_transform(self):
    #     """Ensure that we are able to read a simplement transform node and it's attributes."""
    #     transform_src = pymel.createNode('transform')
    #     transform_dst = pymel.createNode('transform')
    #     pymel.connectAttr(transform_src.translateX, transform_dst.translateX)
    #     node = self.registry.get_node_from_value(transform_src)
    #     attributes = node.get_connected_output_attributes()
    #     print(len(attributes))
    #     for a in sorted(attributes):
    #         print a

    def _create_simple_compound(self):
        transform_src = pymel.createNode('transform')
        transform_dst = pymel.createNode('transform')
        util_logic = libRigging.create_utility_node(
            'multiplyDivide',
            input1X=transform_src.translateX,
        )

        # todo: make this work with compound and multi attribute!
        # pymel.connectAttr(util_logic.output, transform_dst.translate)

        pymel.connectAttr(util_logic.outputX, transform_dst.translateX)

        component = libComponents.create_component_from_bounds([transform_src, transform_dst])
        return component

    def test_component_loading(self):
        """Ensure the registry is able to load a component and it's children."""
        component = self._create_simple_compound()
        node = self.registry.get_node_from_value(component)

        self.registry


if __name__ == '__main__':
    unittest.main()

    # todo: test discovery of nodes in a specific compound space
