from omtk.widgets.ui import form_preferences
from omtk.core import plugin_manager
from omtk.core import preferences

from omtk.vendor.Qt import QtCore, QtWidgets


class PreferencesWindow(QtWidgets.QDialog):
    searchQueryChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(PreferencesWindow, self).__init__(parent=parent)

        # Initialize GUI
        self.ui = form_preferences.Ui_Dialog()
        self.ui.setupUi(self)

        # Fill the QComboBox
        self.rig_plugins = sorted(plugin_manager.plugin_manager.get_loaded_plugins_by_type("rigs"))
        rig_plugins_names = [plugin.cls.__name__ for plugin in self.rig_plugins if plugin]
        labels = ["Default"] + rig_plugins_names

        self.ui.comboBox.addItems(labels)

        # Apply old settings (default rig)
        cls = preferences.preferences.get_default_rig_class()
        if cls:
            name = cls.__name__
            if name in rig_plugins_names:
                self.ui.comboBox.setCurrentIndex(rig_plugins_names.index(cls) + 1)

        # Connect events
        self.ui.comboBox.currentIndexChanged.connect(self.on_default_rig_changed)

    def on_default_rig_changed(self, index):
        if index == 0:
            preferences.preferences.default_rig = None
        else:
            preferences.preferences.default_rig = self.rig_plugins[index - 1].cls.__name__

        preferences.preferences.save()


gui = PreferencesWindow()


def show():
    global gui
    gui.show()
