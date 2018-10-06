# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/form_component_wizard/ui/widget_component_wizard_parts.ui'
#
# Created: Sat Sep 29 16:35:03 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(Form)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_add = QtWidgets.QPushButton(Form)
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout.addWidget(self.pushButton_add)
        self.pushButton_remove = QtWidgets.QPushButton(Form)
        self.pushButton_remove.setObjectName("pushButton_remove")
        self.horizontalLayout.addWidget(self.pushButton_remove)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_connect = QtWidgets.QPushButton(Form)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.horizontalLayout_2.addWidget(self.pushButton_connect)
        self.pushButton_disconnect = QtWidgets.QPushButton(Form)
        self.pushButton_disconnect.setObjectName("pushButton_disconnect")
        self.horizontalLayout_2.addWidget(self.pushButton_disconnect)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.pushButton_add.setText(QtWidgets.QApplication.translate("Form", "Add", None, -1))
        self.pushButton_remove.setText(QtWidgets.QApplication.translate("Form", "Remove", None, -1))
        self.pushButton_connect.setText(QtWidgets.QApplication.translate("Form", "Connect", None, -1))
        self.pushButton_disconnect.setText(QtWidgets.QApplication.translate("Form", "Disconnect", None, -1))

