import os
from omtk.vendor.Qt import QtCore
from omtk.core import plugin_manager

_dir_template = os.path.join(os.path.dirname(__file__), 'templates')

class RigTemplatesModel(QtCore.QAbstractTableModel):
    def __init__(self):
        filenames = os.listdir(_dir_template)
        self.entries = [filename for filename in filenames if os.path.splitext(filename)[1] == '.ma']
        super(RigTemplatesModel, self).__init__()

    def rowCount(self, index):
        return len(self.entries)

    def columnCount(self, index):
        return 1

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return str(self.entries[index.row()])
