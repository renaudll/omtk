# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/omtk/ui/pluginmanager_window.ui'
#
# Created: Sat Apr 29 23:30:58 2017
#      by: pyside2-uic  running on Qt 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets, QtCompat

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(485, 391)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.verticalLayout.addWidget(self.lineEdit_search)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_reload = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reload.setObjectName("pushButton_reload")
        self.horizontalLayout.addWidget(self.pushButton_reload)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 485, 28))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.actionReload = QtWidgets.QAction(mainWindow)
        self.actionReload.setObjectName("actionReload")
        self.actionSearchQueryChanged = QtWidgets.QAction(mainWindow)
        self.actionSearchQueryChanged.setObjectName("actionSearchQueryChanged")

        self.retranslateUi(mainWindow)
        QtCore.QObject.connect(self.pushButton_reload, QtCore.SIGNAL("released()"), self.actionReload.trigger)
        QtCore.QObject.connect(self.lineEdit_search, QtCore.SIGNAL("textChanged(QString)"), self.actionSearchQueryChanged.trigger)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QtCompat.translate("mainWindow", "OMTK - Plugin Manager", None, -1))
        self.pushButton_reload.setText(QtCompat.translate("mainWindow", "Reload", None, -1))
        self.actionReload.setText(QtCompat.translate("mainWindow", "Reload", None, -1))
        self.actionSearchQueryChanged.setText(QtCompat.translate("mainWindow", "SearchQueryChanged", None, -1))

