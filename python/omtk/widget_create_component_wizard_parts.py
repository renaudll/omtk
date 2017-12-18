from omtk.vendor.Qt import QtCore, QtWidgets
from ui import widget_component_wizard_parts

import pymel.core as pymel


class ComponentPartModel(QtCore.QAbstractTableModel):
    def __init__(self, entries):
        super(ComponentPartModel, self).__init__()
        self._entries = entries

    def rowCount(self, index):
        return len(self._entries)

    def columnCount(self, index):
        return 1

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            return str(self._entries[row])
        if role == QtCore.Qt.CheckStateRole:
            row = index.row()
            entry = self._entries[row]
            return entry.is_connected()

    def setData(self, index, value, role):
        if role == QtCore.Qt.CheckStateRole:
            index = index.row()
            is_checked = bool(value)
            entry = self._entries[index]
            if is_checked:
                entry.connect()
            else:
                entry.disconnect()
            return True

        return False

    def flags(self, index):
        flags = super(ComponentPartModel, self).flags(index)
        flags |= QtCore.Qt.ItemIsUserCheckable
        return flags

    def reset(self):
        self.beginResetModel()
        self.endResetModel()

    def add_entries(self, entries, update=False):
        need_update = False
        for entry in entries:
            # assert (isinstance(entry, ComponentPart))
            if not entry in self._entries:
                self._entries.append(entry)
                entry.initialize()
                entry.connect()
                need_update = True

        if need_update and update:
            self.reset()


class WidgetCreateComponentWizardParts(QtWidgets.QWidget):
    _cls = None

    # Triggered when the scene changed
    onNetworkChanged = QtCore.Signal()

    def __init__(self, parent):
        self._wizard = None
        self._cls = None

        super(WidgetCreateComponentWizardParts, self).__init__(parent)

        self.ui = widget_component_wizard_parts.Ui_Form()
        self.ui.setupUi(self)

        self.model = ComponentPartModel([])

        self.ui.tableView.setModel(self.model)

        self.ui.pushButton_ctrl_add.pressed.connect(self.on_added)
        self.ui.pushButton_ctrl_connect.pressed.connect(self.on_connect)
        self.ui.pushButton_ctrl_disconnect.pressed.connect(self.on_disconnect)

    def get_selected_entries(self):
        indexes = set(qindex.row() for qindex in self.ui.tableView.selectedIndexes())
        entries = [self.model._entries[index] for index in indexes]
        return entries

    def can_add(self, obj):
        # Prevent adding the same object twice.
        for entry in self.model._entries:
            if entry._obj == obj:
                return False
        return True

    def on_added(self):
        assert (self._cls is not None)  # ensure the class have been set
        new_entries = []
        for obj in pymel.selected():
            if self.can_add(obj):
                entry = self._cls(self._wizard, obj)
                new_entries.append(entry)

        if new_entries:
            self.model.add_entries(new_entries, update=True)
            self.onNetworkChanged.emit()

    def on_connect(self):
        need_update = False
        entries = self.get_selected_entries()
        for entry in entries:
            if not entry.is_connected():
                entry.connect()
                need_update = True
        if need_update:
            self.model.reset()

    def on_disconnect(self):
        need_update = False
        entries = self.get_selected_entries()
        for entry in entries:
            if entry.is_connected():
                entry.disconnect()
                need_update = True
        if need_update:
            self.model.reset()

    def set_entries(self, wizard, cls, entries):
        self._wizard = wizard
        self._cls = cls
        self.model._entries = entries
        self.model.reset()
