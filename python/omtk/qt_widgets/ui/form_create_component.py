# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/ui/form_create_component.ui'
#
# Created: Wed Jul 12 15:22:43 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets, QtCompat

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_version = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_version.setObjectName("lineEdit_version")
        self.gridLayout.addWidget(self.lineEdit_version, 2, 2, 1, 1)
        self.label_name = QtWidgets.QLabel(self.centralwidget)
        self.label_name.setObjectName("label_name")
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.label_author = QtWidgets.QLabel(self.centralwidget)
        self.label_author.setObjectName("label_author")
        self.gridLayout.addWidget(self.label_author, 1, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 0, 2, 1, 1)
        self.label_version = QtWidgets.QLabel(self.centralwidget)
        self.label_version.setObjectName("label_version")
        self.gridLayout.addWidget(self.label_version, 2, 0, 1, 1)
        self.lineEdit_author = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_author.setObjectName("lineEdit_author")
        self.gridLayout.addWidget(self.lineEdit_author, 1, 2, 1, 1)
        self.label_id = QtWidgets.QLabel(self.centralwidget)
        self.label_id.setObjectName("label_id")
        self.gridLayout.addWidget(self.label_id, 3, 0, 1, 1)
        self.lineEdit_id = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.gridLayout.addWidget(self.lineEdit_id, 3, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.pushButton_resolve = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_resolve.setObjectName("pushButton_resolve")
        self.verticalLayout.addWidget(self.pushButton_resolve)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableView_attrs_inn = QtWidgets.QTableView(self.centralwidget)
        self.tableView_attrs_inn.setSortingEnabled(True)
        self.tableView_attrs_inn.setObjectName("tableView_attrs_inn")
        self.tableView_attrs_inn.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.tableView_attrs_inn)
        self.tableView_attrs_out = QtWidgets.QTableView(self.centralwidget)
        self.tableView_attrs_out.setSortingEnabled(True)
        self.tableView_attrs_out.setObjectName("tableView_attrs_out")
        self.tableView_attrs_out.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.tableView_attrs_out)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton_submit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.verticalLayout.addWidget(self.pushButton_submit)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Create Component", None, -1))
        self.label_name.setText(QtWidgets.QApplication.translate("MainWindow", "Name", None, -1))
        self.label_author.setText(QtWidgets.QApplication.translate("MainWindow", "Author", None, -1))
        self.label_version.setText(QtWidgets.QApplication.translate("MainWindow", "Version", None, -1))
        self.label_id.setText(QtWidgets.QApplication.translate("MainWindow", "Unique ID", None, -1))
        self.pushButton_resolve.setText(QtWidgets.QApplication.translate("MainWindow", "Resolve Input/Outputs", None, -1))
        self.pushButton_submit.setText(QtWidgets.QApplication.translate("MainWindow", "Register", None, -1))

