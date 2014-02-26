# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Users/renaudlessardlarouche/GitHub/omtk/omtk/rigging/autorig/ui.ui'
#
# Created: Tue Feb 25 23:41:26 2014
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(597, 417)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.treeWidget = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout.addWidget(self.treeWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 597, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionBuild = QtGui.QAction(MainWindow)
        self.actionBuild.setObjectName(_fromUtf8("actionBuild"))
        self.actionUnbuild = QtGui.QAction(MainWindow)
        self.actionUnbuild.setObjectName(_fromUtf8("actionUnbuild"))
        self.actionRebuild = QtGui.QAction(MainWindow)
        self.actionRebuild.setObjectName(_fromUtf8("actionRebuild"))
        self.actionImport = QtGui.QAction(MainWindow)
        self.actionImport.setObjectName(_fromUtf8("actionImport"))
        self.actionExport = QtGui.QAction(MainWindow)
        self.actionExport.setObjectName(_fromUtf8("actionExport"))
        self.actionUpdate = QtGui.QAction(MainWindow)
        self.actionUpdate.setObjectName(_fromUtf8("actionUpdate"))
        self.actionAdd = QtGui.QAction(MainWindow)
        self.actionAdd.setObjectName(_fromUtf8("actionAdd"))
        self.toolBar.addAction(self.actionBuild)
        self.toolBar.addAction(self.actionUnbuild)
        self.toolBar.addAction(self.actionRebuild)
        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionImport)
        self.toolBar.addAction(self.actionExport)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionUpdate)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBuild.setText(QtGui.QApplication.translate("MainWindow", "Build", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUnbuild.setText(QtGui.QApplication.translate("MainWindow", "Unbuild", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRebuild.setText(QtGui.QApplication.translate("MainWindow", "Rebuild", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setText(QtGui.QApplication.translate("MainWindow", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setText(QtGui.QApplication.translate("MainWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUpdate.setText(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUpdate.setToolTip(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))

