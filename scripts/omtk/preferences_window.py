from PySide import QtCore, QtGui

from ui import preferences_window

class PreferencesWindow(QtGui.QDialog):
    searchQueryChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(PreferencesWindow, self).__init__(parent=parent)

        # Initialize GUI
        self.ui = preferences_window.Ui_Dialog()
        self.ui.setupUi(self)


gui = PreferencesWindow()
def show():
    global gui
    gui.show()