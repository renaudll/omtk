# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/ui/widget_logger.ui'
#
# Created: Wed Dec 20 20:39:32 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(435, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_log_search = QtWidgets.QLineEdit(Form)
        self.lineEdit_log_search.setObjectName("lineEdit_log_search")
        self.horizontalLayout_4.addWidget(self.lineEdit_log_search)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.comboBox_log_level = QtWidgets.QComboBox(Form)
        self.comboBox_log_level.setObjectName("comboBox_log_level")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.comboBox_log_level.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBox_log_level)
        self.pushButton_logs_save = QtWidgets.QPushButton(Form)
        self.pushButton_logs_save.setObjectName("pushButton_logs_save")
        self.horizontalLayout_4.addWidget(self.pushButton_logs_save)
        self.pushButton_logs_clear = QtWidgets.QPushButton(Form)
        self.pushButton_logs_clear.setObjectName("pushButton_logs_clear")
        self.horizontalLayout_4.addWidget(self.pushButton_logs_clear)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.tableView_logs = QtWidgets.QTableView(Form)
        self.tableView_logs.setObjectName("tableView_logs")
        self.verticalLayout.addWidget(self.tableView_logs)

        self.retranslateUi(Form)
        self.comboBox_log_level.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form"))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "Logs"))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "Search"))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "Level:"))
        self.comboBox_log_level.setItemText(0, QtWidgets.QApplication.translate("Form", "Error"))
        self.comboBox_log_level.setItemText(1, QtWidgets.QApplication.translate("Form", "Warning"))
        self.comboBox_log_level.setItemText(2, QtWidgets.QApplication.translate("Form", "Info"))
        self.comboBox_log_level.setItemText(3, QtWidgets.QApplication.translate("Form", "Debug"))
        self.pushButton_logs_save.setText(QtWidgets.QApplication.translate("Form", "Save"))
        self.pushButton_logs_clear.setText(QtWidgets.QApplication.translate("Form", "Clear"))

