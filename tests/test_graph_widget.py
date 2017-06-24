import unittest

from omtk.qt_widgets.nodegraph_widget.nodegraph_widget import NodeGraphWidget
from omtk.vendor.Qt import QtWidgets


class GraphWidgetTest(unittest.TestCase):
    def test_creation(self):
        """Ensure we are able to create a NodeGraphWidget"""

        # Initialize QApplication if needed
        print '1', QtWidgets.QApplication.instance()
        if not QtWidgets.QApplication.instance():
            QtWidgets.QApplication([])
        # win = QtWidgets.QMainWindow()
        wid = NodeGraphWidget()
        # win.setCentralWidget(wid)
        # win.show()


if __name__ == '__main__':
    unittest.main()