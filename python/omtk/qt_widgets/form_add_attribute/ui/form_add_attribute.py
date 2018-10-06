# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/form_add_attribute/ui/form_add_attribute.ui'
#
# Created: Sat Sep 29 16:35:03 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(383, 252)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_name = QtWidgets.QLabel(self.centralwidget)
        self.label_name.setObjectName("label_name")
        self.gridLayout_2.addWidget(self.label_name, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.rb_message = QtWidgets.QRadioButton(self.centralwidget)
        self.rb_message.setObjectName("rb_message")
        self.gridLayout.addWidget(self.rb_message, 1, 1, 1, 1)
        self.rb_float = QtWidgets.QRadioButton(self.centralwidget)
        self.rb_float.setObjectName("rb_float")
        self.gridLayout.addWidget(self.rb_float, 1, 0, 1, 1)
        self.rb_integer = QtWidgets.QRadioButton(self.centralwidget)
        self.rb_integer.setObjectName("rb_integer")
        self.gridLayout.addWidget(self.rb_integer, 1, 2, 1, 1)
        self.rb_string = QtWidgets.QRadioButton(self.centralwidget)
        self.rb_string.setObjectName("rb_string")
        self.gridLayout.addWidget(self.rb_string, 2, 1, 1, 1)
        self.rb_matrix = QtWidgets.QRadioButton(self.centralwidget)
        self.rb_matrix.setObjectName("rb_matrix")
        self.gridLayout.addWidget(self.rb_matrix, 2, 0, 1, 1)
        self.rb_boolean = QtWidgets.QRadioButton(self.centralwidget)
        self.rb_boolean.setObjectName("rb_boolean")
        self.gridLayout.addWidget(self.rb_boolean, 2, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout_2.addWidget(self.lineEdit_name, 0, 1, 1, 1)
        self.label_value = QtWidgets.QLabel(self.centralwidget)
        self.label_value.setObjectName("label_value")
        self.gridLayout_2.addWidget(self.label_value, 2, 0, 1, 1)
        self.lineEdit_value = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_value.setObjectName("lineEdit_value")
        self.gridLayout_2.addWidget(self.lineEdit_value, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 383, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Add Attribute", None, -1))
        self.label_name.setText(QtWidgets.QApplication.translate("MainWindow", "Name", None, -1))
        self.rb_message.setText(QtWidgets.QApplication.translate("MainWindow", "Message", None, -1))
        self.rb_float.setText(QtWidgets.QApplication.translate("MainWindow", "Float", None, -1))
        self.rb_integer.setText(QtWidgets.QApplication.translate("MainWindow", "Integer", None, -1))
        self.rb_string.setText(QtWidgets.QApplication.translate("MainWindow", "String", None, -1))
        self.rb_matrix.setText(QtWidgets.QApplication.translate("MainWindow", "Matrix", None, -1))
        self.rb_boolean.setText(QtWidgets.QApplication.translate("MainWindow", "Boolean", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Type", None, -1))
        self.label_value.setText(QtWidgets.QApplication.translate("MainWindow", "Value", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "Create", None, -1))

