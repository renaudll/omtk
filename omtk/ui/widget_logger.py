# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/packages/omtk/9.9.9/omtk/ui/widget_logger.ui'
#
# Created: Sun Oct 16 09:39:35 2016
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(435, 300)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_log_search = QtGui.QLineEdit(Form)
        self.lineEdit_log_search.setObjectName("lineEdit_log_search")
        self.horizontalLayout_4.addWidget(self.lineEdit_log_search)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.comboBox_log_level = QtGui.QComboBox(Form)
        self.comboBox_log_level.setObjectName("comboBox_log_level")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_log_level)
        self.pushButton_logs_save = QtGui.QPushButton(Form)
        self.pushButton_logs_save.setObjectName("pushButton_logs_save")
        self.horizontalLayout_4.addWidget(self.pushButton_logs_save)
        self.pushButton_logs_clear = QtGui.QPushButton(Form)
        self.pushButton_logs_clear.setObjectName("pushButton_logs_clear")
        self.horizontalLayout_4.addWidget(self.pushButton_logs_clear)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.tableView_logs = QtGui.QTableView(Form)
        self.tableView_logs.setObjectName("tableView_logs")
        self.verticalLayout.addWidget(self.tableView_logs)

        self.retranslateUi(Form)
        self.comboBox_log_level.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Logs", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Level:", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_log_level.setItemText(0, QtGui.QApplication.translate("Form", "Error", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_log_level.setItemText(1, QtGui.QApplication.translate("Form", "Warning", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_log_level.setItemText(2, QtGui.QApplication.translate("Form", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_log_level.setItemText(3, QtGui.QApplication.translate("Form", "Debug", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_logs_save.setText(QtGui.QApplication.translate("Form", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_logs_clear.setText(QtGui.QApplication.translate("Form", "Clear", None, QtGui.QApplication.UnicodeUTF8))

