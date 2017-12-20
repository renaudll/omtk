from omtk.core import plugin_manager
from omtk.qt_widgets.ui import pluginmanager_window
from omtk.vendor.Qt import QtCore, QtWidgets


class PluginListModel(QtCore.QAbstractTableModel):
    """
    QTableModel that list attributes.
    # TODO: Benchmark pymel.Attribute vs lazy proxy class.
    """
    HEADER = ('Name', 'Type', 'Status', 'Location', 'Description')

    ROW_NAME = 0
    ROW_TYPE = 1
    ROW_STAT = 2
    ROW_LOCA = 3
    ROW_DESC = 4

    def __init__(self, parent, data, *args):
        super(PluginListModel, self).__init__(parent, *args)
        self.items = data
        self.header = self.HEADER

    def rowCount(self, parent):
        return len(self.items)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole:
            plugin = self.items[index.row()]
            col_index = index.column()
            if col_index == self.ROW_NAME:
                return plugin.name
            elif col_index == self.ROW_TYPE:
                return plugin.type_name.title()
            elif col_index == self.ROW_STAT:
                return plugin.status
            elif col_index == self.ROW_LOCA:
                return plugin.module.__file__ if plugin.module else 'n/a'
            elif col_index == self.ROW_DESC:
                return plugin.description
            return ''
        elif role == QtCore.Qt.BackgroundColorRole:
            plugin = self.items[index.row()]
            if plugin.status == plugin_manager.PluginStatus.Failed:
                return QtCore.Qt.red
            return None

        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def reset(self):
        """Backport of Qt4 .reset method()"""
        self.beginResetModel()
        self.endResetModel()


class PluginListFilterProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent):
        super(PluginListFilterProxyModel, self).__init__(parent)
        self._search_query = None

    def set_search_query(self, search_query, update=True):
        self._search_query = search_query
        if update:
            self.reset()

    def filterAcceptsRow(self, row, index):
        if not self._search_query:
            return True

        model = self.sourceModel()
        item = model.items[row]
        return self._search_query in item.module_name

    def reset(self):
        """Backport of Qt4 .reset method()"""
        self.beginResetModel()
        self.endResetModel()


class PluginManagerWindow(QtWidgets.QMainWindow):
    searchQueryChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(PluginManagerWindow, self).__init__(parent=parent)

        # Initialize GUI
        self.ui = pluginmanager_window.Ui_mainWindow()
        self.ui.setupUi(self)

        # Initialize MVC
        self._data = plugin_manager.plugin_manager.get_plugins()
        self._model = PluginListModel(self, self._data)
        self._proxy_model = PluginListFilterProxyModel(self)
        self._proxy_model.setSourceModel(self._model)
        self._proxy_model.setDynamicSortFilter(False)
        self.ui.tableView.setModel(self._proxy_model)

        # Connect actions
        self.ui.actionReload.triggered.connect(self.on_reload)
        self.ui.actionSearchQueryChanged.triggered.connect(self.on_searchquery_changed)

    def iter_selected_plugins(self):
        for row in self.ui.tableView.selectionModel().selectedRows():
            plugin = self._data[row.row()]
            yield plugin

    def get_selected_plugins(self):
        return list(self.iter_selected_plugins())

    def on_reload(self):
        for plugin in self.iter_selected_plugins():
            plugin.load(force=True)
        self._proxy_model.reset()

    def on_searchquery_changed(self, *args, **kwargs):
        query = self.ui.lineEdit_search.text()
        self._proxy_model.set_search_query(query)


gui = PluginManagerWindow()


def show():
    global gui
    gui.show()
