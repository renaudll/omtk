# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rlessard/packages/omtk/0.4.999/omtk/ui/widget_list_meshes.ui'
#
# Created: Tue Jan 24 10:18:37 2017
#      by: pyside2-uic  running on Qt 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets, QtCompat

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(316, 295)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_search = QtWidgets.QLineEdit(Form)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.horizontalLayout.addWidget(self.lineEdit_search)
        self.btn_update = QtWidgets.QPushButton(Form)
        self.btn_update.setObjectName("btn_update")
        self.horizontalLayout.addWidget(self.btn_update)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeWidget = QtWidgets.QTreeWidget(Form)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.treeWidget.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeWidget)
        self.pushButton_selectGrpMeshes = QtWidgets.QPushButton(Form)
        self.pushButton_selectGrpMeshes.setObjectName("pushButton_selectGrpMeshes")
        self.verticalLayout.addWidget(self.pushButton_selectGrpMeshes)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtCompat.translate("Form", "Form", None, -1))
        self.btn_update.setText(QtCompat.translate("Form", "Update", None, -1))
        self.pushButton_selectGrpMeshes.setText(QtCompat.translate("Form", "Select Meshes Grp", None, -1))

