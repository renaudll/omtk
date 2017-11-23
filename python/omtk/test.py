# generaly loaded in maya script editor for debugging

import sys

sys.path.append('/home/rll/dev/python/omtk/python')
import omtk

reload(omtk)
omtk._reload()

from omtk.vendor.Qt import QtWidgets
from omtk.qt_widgets import widget_outliner


def test_widget(cls):
    win = QtWidgets.QMainWindow()
    wid = cls()
    win.setCentralWidget(wid)
    win.show()
    return win


w1 = w2 = w3 = w4 = None


def run():
    omtk.show()

    w1 = test_widget(widget_outliner.OmtkBaseListWidget)
    w2 = test_widget(widget_outliner.WidgetListMeshes)
    w3 = test_widget(widget_outliner.WidgetListModules)
    w4 = test_widget(widget_outliner.WidgetListComponentDefinition)
