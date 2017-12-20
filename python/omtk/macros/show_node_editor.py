from omtk.core.macro import BaseMacro
from omtk.vendor.Qt import QtWidgets
from omtk.qt_widgets import widget_nodegraph

_gui = None  # workaround garbage collection bug


class ShowNodeEditor(BaseMacro):
    def run(self):
        cls = widget_nodegraph.nodegraph_widget.NodeGraphWidget
        global _gui
        _gui = QtWidgets.QMainWindow()
        _gui.setCentralWidget(cls(_gui))
        _gui.show()


def register_plugin():
    return ShowNodeEditor
