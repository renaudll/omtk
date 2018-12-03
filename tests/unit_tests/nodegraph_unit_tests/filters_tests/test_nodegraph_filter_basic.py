"""
Ensure propre behaviour or the GraphController, GraphRegistry and every related models.
"""
import unittest

from omtk.nodegraph import NodeGraphFilter
from omtk.vendor.mock_maya.decorators import mock_pymel
from omtk_test import NodeGraphMockedMayaTestCase


class CameraFilter(NodeGraphFilter):
    """
    Show only camera shapes.
    """

    def intercept_node(self, node):
        node_type = node.get_type()
        if node_type == 'camera':
            return

        yield node


class MessageFilter(NodeGraphFilter):
    """
    Show only message type filters.
    """

    def intercept_port(self, port):
        """
        Yield port only if they are named 'message'.
        :param NodeGraphPortModel port: The port to inspect.
        :return: A port generator
        rtype: Generator[NodeGraphPortModel]
        """
        port_name = port.get_name()
        if port_name != 'message':
            return

        yield port


class NodeGraphFilterMockedMayaTestCase(NodeGraphMockedMayaTestCase):
    _cls_filter = None

    def setUp(self):
        super(NodeGraphFilterMockedMayaTestCase, self).setUp()

        filter_ = CameraFilter()
        self.model.add_filter(filter_)


class SimpleNodeGraphFilterTestCase(NodeGraphFilterMockedMayaTestCase):
    """
    Test a simple NodeGraphFilter that only let camera goes through.
    """

    def test_can_show_node(self):
        with mock_pymel(self.session) as pymel:
            for pynode in pymel.ls():
                node = self.registry.get_node(pynode)
                self.ctrl.add_node(node)

            expected = [
                'frontShape',
                'perspShape',
                'topShape',
                'sideShape',
            ]
            self.assertGraphNodeNamesEqual(expected)


class SimpleGraphPortFilterTestCase(NodeGraphMockedMayaTestCase):
    """
    Test a simple NodeGraphFilter that only let message attributes goes throught.
    """

    def test_can_shot_port(self):
        with mock_pymel(self.session) as pymel:
            pynode = pymel.PyNode('top')
            node = self.registry.get_node(pynode)
            self.model.add_node(node)
            self.assertGraphNodePortNamesEqual(node, ['message'])


if __name__ == '__main__':
    unittest.main()
