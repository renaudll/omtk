# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/ui/form_create_component.ui'
#
# Created: Wed Jul 12 11:39:46 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(627, 480)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_version = QtGui.QLineEdit(Form)
        self.lineEdit_version.setObjectName("lineEdit_version")
        self.gridLayout.addWidget(self.lineEdit_version, 2, 2, 1, 1)
        self.label_name = QtGui.QLabel(Form)
        self.label_name.setObjectName("label_name")
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.label_author = QtGui.QLabel(Form)
        self.label_author.setObjectName("label_author")
        self.gridLayout.addWidget(self.label_author, 1, 0, 1, 1)
        self.lineEdit_name = QtGui.QLineEdit(Form)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 0, 2, 1, 1)
        self.label_version = QtGui.QLabel(Form)
        self.label_version.setObjectName("label_version")
        self.gridLayout.addWidget(self.label_version, 2, 0, 1, 1)
        self.lineEdit_author = QtGui.QLineEdit(Form)
        self.lineEdit_author.setObjectName("lineEdit_author")
        self.gridLayout.addWidget(self.lineEdit_author, 1, 2, 1, 1)
        self.label_id = QtGui.QLabel(Form)
        self.label_id.setObjectName("label_id")
        self.gridLayout.addWidget(self.label_id, 3, 0, 1, 1)
        self.lineEdit_id = QtGui.QLineEdit(Form)
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.gridLayout.addWidget(self.lineEdit_id, 3, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.pushButton_resolve = QtGui.QPushButton(Form)
        self.pushButton_resolve.setObjectName("pushButton_resolve")
        self.verticalLayout.addWidget(self.pushButton_resolve)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableView_attrs_inn = QtGui.QTableView(Form)
        self.tableView_attrs_inn.setObjectName("tableView_attrs_inn")
        self.horizontalLayout.addWidget(self.tableView_attrs_inn)
        self.tableView_attrs_out = QtGui.QTableView(Form)
        self.tableView_attrs_out.setObjectName("tableView_attrs_out")
        self.horizontalLayout.addWidget(self.tableView_attrs_out)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton_submit = QtGui.QPushButton(Form)
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.verticalLayout.addWidget(self.pushButton_submit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Create Component", None, QtGui.QApplication.UnicodeUTF8))
        self.label_name.setText(QtGui.QApplication.translate("Form", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_author.setText(QtGui.QApplication.translate("Form", "Author", None, QtGui.QApplication.UnicodeUTF8))
        self.label_version.setText(QtGui.QApplication.translate("Form", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.label_id.setText(QtGui.QApplication.translate("Form", "Unique ID", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_resolve.setText(QtGui.QApplication.translate("Form", "Resolve Input/Outputs", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_submit.setText(QtGui.QApplication.translate("Form", "Register", None, QtGui.QApplication.UnicodeUTF8))

