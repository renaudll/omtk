# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/packages/omtk/9.9.9/omtk/ui/pluginmanager_window.ui'
#
# Created: Sun Oct 16 11:09:23 2016
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(485, 391)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_search = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.verticalLayout.addWidget(self.lineEdit_search)
        self.tableView = QtGui.QTableView(self.centralwidget)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_reload = QtGui.QPushButton(self.centralwidget)
        self.pushButton_reload.setObjectName("pushButton_reload")
        self.horizontalLayout.addWidget(self.pushButton_reload)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 485, 28))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.actionReload = QtGui.QAction(mainWindow)
        self.actionReload.setObjectName("actionReload")
        self.actionSearchQueryChanged = QtGui.QAction(mainWindow)
        self.actionSearchQueryChanged.setObjectName("actionSearchQueryChanged")

        self.retranslateUi(mainWindow)
        QtCore.QObject.connect(self.pushButton_reload, QtCore.SIGNAL("released()"), self.actionReload.trigger)
        QtCore.QObject.connect(self.lineEdit_search, QtCore.SIGNAL("textChanged(QString)"), self.actionSearchQueryChanged.trigger)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QtGui.QApplication.translate("mainWindow", "OMTK - Plugin Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_reload.setText(QtGui.QApplication.translate("mainWindow", "Reload", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReload.setText(QtGui.QApplication.translate("mainWindow", "Reload", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSearchQueryChanged.setText(QtGui.QApplication.translate("mainWindow", "SearchQueryChanged", None, QtGui.QApplication.UnicodeUTF8))

