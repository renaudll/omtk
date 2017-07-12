from omtk.libs import libPython
from omtk.qt_widgets.ui.form_create_component import Ui_Form as ui_def
from omtk.vendor.Qt import QtWidgets


class CreateComponentForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CreateComponentForm, self).__init__(parent=None)
        self.ui = ui_def()
        self.ui.setupUi(self)


@libPython.memoized
def get():
    return CreateComponentForm()


def show():
    gui = get()
    gui.show()
