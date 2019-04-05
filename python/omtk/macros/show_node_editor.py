import logging

from omtk.core.macro import BaseMacro
from omtk.nodegraph.widget import NodeGraphWidget
from omtk.qt_widgets import main_window_extended
from omtk.vendor.Qt import QtWidgets

_gui = None  # workaround garbage collection bug
log = logging.getLogger(__name__)


class ShowNodeEditor(BaseMacro):
    def run(self):
        cls = NodeGraphWidget

        global _gui
        _gui = main_window_extended.MainWindowExtended()
        _gui.setCentralWidget(cls(_gui))

        statusbar = QtWidgets.QStatusBar(_gui)
        _gui.setStatusBar(statusbar)

        _gui.set_logger(log)
        _gui.show()


def register_plugin():
    return ShowNodeEditor
