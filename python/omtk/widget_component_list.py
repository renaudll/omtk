from omtk.vendor.Qt import QtCore, QtWidgets, QtCore
from omtk.core import plugin_manager
from .ui import widget_component_list
from omtk.libs import libComponents

class ComponentDefinitionTableModel(QtCore.QAbstractTableModel):
    def __init__(self, entries):
        super(ComponentDefinitionTableModel, self).__init__()
        self.__entries = entries

    def rowCount(self, index):
        return len(self.__entries)

    def columnCount(self, index):
        return 1

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            entry = self.__entries[row]
            return str(entry)


class WidgetComponentList(QtWidgets.QWidget):
    def __init__(self, parent):
        super(WidgetComponentList, self).__init__(parent)
        self.ui = widget_component_list.Ui_Form()
        self.ui.setupUi(self)

        plugins = plugin_manager.plugin_manager.get_plugins()
        view = self.ui.tableView

        # Configure headers
        horizontal_header = view.horizontalHeader()
        horizontal_header.setSectionResizeMode(horizontal_header.Stretch)
        view.verticalHeader().hide()

        defs = list(libComponents.walk_available_component_definitions())
        model = ComponentDefinitionTableModel(defs)
        view.setModel(model)
        # view.resizeColumnsToContents()
