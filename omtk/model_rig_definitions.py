from omtk.vendor.Qt import QtCore
from omtk.core import plugin_manager


class RigDefinitionsModel(QtCore.QAbstractTableModel):
    def __init__(self):
        pm = plugin_manager.plugin_manager
        plugin_type = plugin_manager.RigPluginType.type_name
        plugins = sorted(pm.get_loaded_plugins_by_type(plugin_type))
        self.entries = [plugin.cls for plugin in plugins]
        super(RigDefinitionsModel, self).__init__()

    def rowCount(self, index):
        return len(self.entries)

    def columnCount(self, index):
        return 1

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return str(self.entries[index.row()].__name__)
