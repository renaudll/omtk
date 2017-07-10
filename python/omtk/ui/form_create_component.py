# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/ui/form_create_component.ui'
#
# Created: Sun Jun 25 15:35:32 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(627, 480)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_version = QtWidgets.QLineEdit(Form)
        self.lineEdit_version.setObjectName("lineEdit_version")
        self.gridLayout.addWidget(self.lineEdit_version, 2, 2, 1, 1)
        self.label_name = QtWidgets.QLabel(Form)
        self.label_name.setObjectName("label_name")
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.label_author = QtWidgets.QLabel(Form)
        self.label_author.setObjectName("label_author")
        self.gridLayout.addWidget(self.label_author, 1, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(Form)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 0, 2, 1, 1)
        self.label_version = QtWidgets.QLabel(Form)
        self.label_version.setObjectName("label_version")
        self.gridLayout.addWidget(self.label_version, 2, 0, 1, 1)
        self.lineEdit_author = QtWidgets.QLineEdit(Form)
        self.lineEdit_author.setObjectName("lineEdit_author")
        self.gridLayout.addWidget(self.lineEdit_author, 1, 2, 1, 1)
        self.label_id = QtWidgets.QLabel(Form)
        self.label_id.setObjectName("label_id")
        self.gridLayout.addWidget(self.label_id, 3, 0, 1, 1)
        self.lineEdit_id = QtWidgets.QLineEdit(Form)
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.gridLayout.addWidget(self.lineEdit_id, 3, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.pushButton_resolve = QtWidgets.QPushButton(Form)
        self.pushButton_resolve.setObjectName("pushButton_resolve")
        self.verticalLayout.addWidget(self.pushButton_resolve)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableView_attrs_inn = QtWidgets.QTableView(Form)
        self.tableView_attrs_inn.setObjectName("tableView_attrs_inn")
        self.horizontalLayout.addWidget(self.tableView_attrs_inn)
        self.tableView_attrs_out = QtWidgets.QTableView(Form)
        self.tableView_attrs_out.setObjectName("tableView_attrs_out")
        self.horizontalLayout.addWidget(self.tableView_attrs_out)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton_submit = QtWidgets.QPushButton(Form)
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.verticalLayout.addWidget(self.pushButton_submit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Create Component", None))
        self.label_name.setText(QtWidgets.QApplication.translate("Form", "Name", None))
        self.label_author.setText(QtWidgets.QApplication.translate("Form", "Author", None))
        self.label_version.setText(QtWidgets.QApplication.translate("Form", "Version", None))
        self.label_id.setText(QtWidgets.QApplication.translate("Form", "Unique ID", None))
        self.pushButton_resolve.setText(QtWidgets.QApplication.translate("Form", "Resolve Input/Outputs", None))
        self.pushButton_submit.setText(QtWidgets.QApplication.translate("Form", "Register", None))

