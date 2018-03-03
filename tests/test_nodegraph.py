import unittest
import pymel.core as pymel
from omtk.qt_widgets.widget_nodegraph import NodeGraphModel, NodeGraphController, NodeGraphView, NodeGraphControllerFilter
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class TestNodeGraph(unittest.TestCase):
    def setUp(self):
        # if QtWidgets.qApp is None:
        #     app = QtWidgets.QApplication([])
        self._registry = NodeGraphModel()
        # self._view = NodeGraphView()
        self._filter = NodeGraphControllerFilter(self._registry)

        self._controller = NodeGraphController(self._registry)
        # self._controller.set_view(self._view)

    def test_transform(self):
        """Ensure that we are able to represent a single transform."""
        obj = pymel.createNode('transform')
        model = self._controller.get_node_model_from_value(obj)
        self._controller.add_node(model)

    def test_simple_connection(self):
        """Ensure that we are able to represent a single connection."""

    def test_create_compound(self):
        """Ensure that we are able to create a compound."""


if __name__ == '__main__':
    unittest.main()