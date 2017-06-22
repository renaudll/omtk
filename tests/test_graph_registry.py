"""
Ensure propre behaviour or the GraphController, GraphRegistry and every related models.
"""
import unittest

import pymel.core as pymel
from maya import cmds
from omtk.qt_widgets.node_editor_widget.graph_model_registry import GraphRegistry


class GraphRegistryTest(unittest.TestCase):
    def setUp(self):
        self.registry = GraphRegistry()
        cmds.file(new=True, force=True)

    def test_node_model_from_transform(self):
        """Ensure that we are able to read a simplement transform node and it's attributes."""
        transform_src = pymel.createNode('transform')
        transform_dst = pymel.createNode('transform')
        pymel.connectAttr(transform_src.translateX, transform_dst.translateX)
        node = self.registry.get_node_from_value(transform_src)
        attributes = node.get_connected_output_attributes()
        print(len(attributes))
        for a in sorted(attributes):
            print a

if __name__ == '__main__':
    unittest.main()
