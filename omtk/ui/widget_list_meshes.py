# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/packages/omtk/9.9.9/omtk/ui/widget_list_meshes.ui'
#
# Created: Sun Oct 16 09:39:35 2016
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(316, 295)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_search = QtGui.QLineEdit(Form)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.horizontalLayout.addWidget(self.lineEdit_search)
        self.btn_update = QtGui.QPushButton(Form)
        self.btn_update.setObjectName("btn_update")
        self.horizontalLayout.addWidget(self.btn_update)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.treeWidget = QtGui.QTreeWidget(Form)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.treeWidget.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeWidget)
        self.pushButton_selectGrpMeshes = QtGui.QPushButton(Form)
        self.pushButton_selectGrpMeshes.setObjectName("pushButton_selectGrpMeshes")
        self.verticalLayout.addWidget(self.pushButton_selectGrpMeshes)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_update.setText(QtGui.QApplication.translate("Form", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_selectGrpMeshes.setText(QtGui.QApplication.translate("Form", "Select Meshes Grp", None, QtGui.QApplication.UnicodeUTF8))

