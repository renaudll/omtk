# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/ui/widget_welcome.ui'
#
# Created: Wed Jul 12 11:39:46 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(559, 397)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.btn_create_rig_default = QtGui.QCommandLinkButton(Form)
        self.btn_create_rig_default.setObjectName("btn_create_rig_default")
        self.verticalLayout_6.addWidget(self.btn_create_rig_default)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3)
        self.tableView_types_rig = QtGui.QTableView(Form)
        self.tableView_types_rig.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView_types_rig.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView_types_rig.setObjectName("tableView_types_rig")
        self.tableView_types_rig.horizontalHeader().setVisible(False)
        self.tableView_types_rig.horizontalHeader().setStretchLastSection(True)
        self.tableView_types_rig.verticalHeader().setVisible(False)
        self.verticalLayout_6.addWidget(self.tableView_types_rig)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.btn_create_rig_template = QtGui.QCommandLinkButton(Form)
        self.btn_create_rig_template.setObjectName("btn_create_rig_template")
        self.verticalLayout_8.addWidget(self.btn_create_rig_template)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_8.addWidget(self.label_4)
        self.tableView_types_template = QtGui.QTableView(Form)
        self.tableView_types_template.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView_types_template.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
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
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Welcome!", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_create_rig_default.setText(QtGui.QApplication.translate("Form", "Create an empty rig", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Available rigs:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_create_rig_template.setText(QtGui.QApplication.translate("Form", "Start from a template", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Available templates", None, QtGui.QApplication.UnicodeUTF8))

