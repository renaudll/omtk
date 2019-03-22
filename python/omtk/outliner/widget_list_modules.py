import logging

from omtk.core import manager
from omtk.factories import factory_rc_menu
from omtk.outliner import widget_list_base
from omtk.vendor.Qt import QtCore, QtWidgets, QtGui

log = logging.getLogger(__name__)


class WidgetListModules(widget_list_base.OmtkBaseListWidget):
    needExportNetwork = QtCore.Signal()
    needImportNetwork = QtCore.Signal()
    deletedRig = QtCore.Signal(object)

    def iter_values(self):
        s = manager.get_session()
        for rig in s.get_rigs():
            print rig
            yield rig

    def on_context_menu_request(self, pos):
        selected_items = self.ui.treeWidget.selectedItems()
        assert (selected_items)
        menu = QtWidgets.QMenu()
        selected_values = [item._meta_data for item in selected_items]
        menu = factory_rc_menu.get_menu(menu, selected_values, self.actionRequested.emit)
        menu.exec_(QtGui.QCursor.pos())
