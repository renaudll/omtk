# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/outliner/ui/widget_list_componentdef.ui'
#
# Created: Tue Apr  3 21:09:17 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_search = QtWidgets.QLineEdit(Form)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.verticalLayout.addWidget(self.lineEdit_search)
        self.tableView = QtWidgets.QTableView(Form)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))

