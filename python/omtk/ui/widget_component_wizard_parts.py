# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rlessard/packages/omtk/0.4.999/python/omtk/ui/widget_component_wizard_parts.ui'
#
# Created: Mon Dec 18 13:43:36 2017
#      by: pyside2-uic  running on Qt 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets, QtCompat

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(Form)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_ctrl_add = QtWidgets.QPushButton(Form)
        self.pushButton_ctrl_add.setObjectName("pushButton_ctrl_add")
        self.horizontalLayout.addWidget(self.pushButton_ctrl_add)
        self.pushButton_ctrl_connect = QtWidgets.QPushButton(Form)
        self.pushButton_ctrl_connect.setObjectName("pushButton_ctrl_connect")
        self.horizontalLayout.addWidget(self.pushButton_ctrl_connect)
        self.pushButton_ctrl_disconnect = QtWidgets.QPushButton(Form)
        self.pushButton_ctrl_disconnect.setObjectName("pushButton_ctrl_disconnect")
        self.horizontalLayout.addWidget(self.pushButton_ctrl_disconnect)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtCompat.translate("Form", "Form", None, -1))
        self.pushButton_ctrl_add.setText(QtCompat.translate("Form", "Add", None, -1))
        self.pushButton_ctrl_connect.setText(QtCompat.translate("Form", "Connect", None, -1))
        self.pushButton_ctrl_disconnect.setText(QtCompat.translate("Form", "Disconnect", None, -1))

