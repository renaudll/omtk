# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/form_component_properties/ui/form_component_properties.ui'
#
# Created: Sat Sep 29 16:35:03 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(447, 334)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_author = QtWidgets.QLabel(self.centralwidget)
        self.label_author.setObjectName("label_author")
        self.gridLayout.addWidget(self.label_author, 1, 0, 1, 1)
        self.label_name = QtWidgets.QLabel(self.centralwidget)
        self.label_name.setObjectName("label_name")
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.label_version = QtWidgets.QLabel(self.centralwidget)
        self.label_version.setObjectName("label_version")
        self.gridLayout.addWidget(self.label_version, 2, 0, 1, 1)
        self.label_uid = QtWidgets.QLabel(self.centralwidget)
        self.label_uid.setObjectName("label_uid")
        self.gridLayout.addWidget(self.label_uid, 3, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 0, 1, 1, 1)
        self.lineEdit_author = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_author.setObjectName("lineEdit_author")
        self.gridLayout.addWidget(self.lineEdit_author, 1, 1, 1, 1)
        self.lineEdit_version = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_version.setObjectName("lineEdit_version")
        self.gridLayout.addWidget(self.lineEdit_version, 2, 1, 1, 1)
        self.lineEdit_uid = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_uid.setObjectName("lineEdit_uid")
        self.gridLayout.addWidget(self.lineEdit_uid, 3, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save.setObjectName("pushButton_save")
        self.verticalLayout.addWidget(self.pushButton_save)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 447, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Publish Component", None, -1))
        self.label_author.setText(QtWidgets.QApplication.translate("MainWindow", "Author", None, -1))
        self.label_name.setText(QtWidgets.QApplication.translate("MainWindow", "Name", None, -1))
        self.label_version.setText(QtWidgets.QApplication.translate("MainWindow", "Version", None, -1))
        self.label_uid.setText(QtWidgets.QApplication.translate("MainWindow", "UID", None, -1))
        self.pushButton_save.setText(QtWidgets.QApplication.translate("MainWindow", "Save", None, -1))

