# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/ui/widget_welcome.ui'
#
# Created: Sun Jun 25 15:35:32 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(559, 397)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.btn_create_rig_default = QtWidgets.QCommandLinkButton(Form)
        self.btn_create_rig_default.setObjectName("btn_create_rig_default")
        self.verticalLayout_6.addWidget(self.btn_create_rig_default)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3)
        self.tableView_types_rig = QtWidgets.QTableView(Form)
        self.tableView_types_rig.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView_types_rig.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView_types_rig.setObjectName("tableView_types_rig")
        self.tableView_types_rig.horizontalHeader().setVisible(False)
        self.tableView_types_rig.horizontalHeader().setStretchLastSection(True)
        self.tableView_types_rig.verticalHeader().setVisible(False)
        self.verticalLayout_6.addWidget(self.tableView_types_rig)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.btn_create_rig_template = QtWidgets.QCommandLinkButton(Form)
        self.btn_create_rig_template.setObjectName("btn_create_rig_template")
        self.verticalLayout_8.addWidget(self.btn_create_rig_template)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_8.addWidget(self.label_4)
        self.tableView_types_template = QtWidgets.QTableView(Form)
        self.tableView_types_template.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView_types_template.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView_types_template.setObjectName("tableView_types_template")
        self.tableView_types_template.horizontalHeader().setVisible(False)
        self.tableView_types_template.horizontalHeader().setStretchLastSection(True)
        self.tableView_types_template.verticalHeader().setVisible(False)
        self.verticalLayout_8.addWidget(self.tableView_types_template)
        self.horizontalLayout.addLayout(self.verticalLayout_8)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Welcome!", None, -1))
        self.btn_create_rig_default.setText(QtWidgets.QApplication.translate("Form", "Create an empty rig", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "Available rigs:", None, -1))
        self.btn_create_rig_template.setText(QtWidgets.QApplication.translate("Form", "Start from a template", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "Available templates", None, -1))

