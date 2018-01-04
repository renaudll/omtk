import logging

from omtk.core.macro import BaseMacro
from omtk.vendor.Qt import QtWidgets
from omtk.qt_widgets import widget_nodegraph
from omtk.qt_widgets import main_window_extended

_gui = None  # workaround garbage collection bug


class ShowNodeEditor(BaseMacro):
    def run(self):
        cls = widget_nodegraph.nodegraph_widget.NodeGraphWidget
        log = logging.getLogger('omtk.nodegraph')

        global _gui
        _gui = main_window_extended.MainWindowExtended()
        _gui.setCentralWidget(cls(_gui))

        statusbar = QtWidgets.QStatusBar(_gui)
        _gui.setStatusBar(statusbar)

        _gui.set_logger(log)
        _gui.show()


def register_plugin():
    return ShowNodeEditor
