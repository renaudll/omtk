import sys
import os
#
# # TODO: Remove this
# path = os.path.abspath(os.path.join(os.path.basename(__file__), "..", "scripts"))
# sys.path.append(path)
# from omtk.vendor.Qt import QtWidgets
#
# app = QtWidgets.QApplication([])
#
# app.exec_()
# win = QtWidgets.QMainWindow()
# win.show()

from omtk.vendor.Qt import QtGui, QtWidgets

app = QtWidgets.QApplication([])
from omtk.widgets.main_window import OmtkMainWindow
win = OmtkMainWindow()
win.show()
app.exec_()
