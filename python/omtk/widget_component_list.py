from omtk.vendor.Qt import QtCore, QtWidget
from omtk.core import plugin_manager
from .ui import widget_component_list


class ComponentListModel(QtCore.QAbstractTableModel):
    def __init__(self, entries):
        self.__entries = entries

    def rowCount(self):
        return len(self.__entries)

    def columnCount(self):
        return 1

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            entry = self.__entries[row]
            return str(entry)


class WidgetComponentList(QtWidget):
    def __init__(self, parent):
        super(WidgetComponentList, self).__init__(parent)
        self.ui = widget_component_list.Ui_Form()
        self.ui.setupUi(self)

        plugins = plugin_manager.plugin_manager.get_plugins()
        view = self.ui.tableView
        model = ComponentListModel(plugins)
        view.setModel()
