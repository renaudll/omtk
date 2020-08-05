


import sys
import os
# TODO: Remove this
path = os.path.abspath(os.path.join(os.path.basename(__file__), "..", "scripts"))
sys.path.append(path)
from omtk.vendor.Qt import QtWidgets
app = QtWidgets.QApplication([])
from omtk.widgets.main_window import OmtkMainWindow
app.exec_()
win = QtWidgets.QMainWindow()
wid = OmtkMainWindow(win)
win.show()
