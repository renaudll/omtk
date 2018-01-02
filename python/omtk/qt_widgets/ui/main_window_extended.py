# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/ui/main_window_extended.ui'
#
# Created: Sat Dec 23 18:55:21 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(927, 592)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_logger = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_logger.setObjectName("dockWidget_logger")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_logger = WidgetLogger(self.dockWidgetContents)
        self.widget_logger.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_logger.sizePolicy().hasHeightForWidth())
        self.widget_logger.setSizePolicy(sizePolicy)
        self.widget_logger.setObjectName("widget_logger")
        self.verticalLayout_4.addWidget(self.widget_logger)
        self.dockWidget_logger.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_logger)
        self.actionUpdate = QtWidgets.QAction(MainWindow)
        self.actionUpdate.setObjectName("actionUpdate")
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionBuildAll = QtWidgets.QAction(MainWindow)
        self.actionBuildAll.setObjectName("actionBuildAll")
        self.actionUnbuildAll = QtWidgets.QAction(MainWindow)
        self.actionUnbuildAll.setObjectName("actionUnbuildAll")
        self.actionRebuildAll = QtWidgets.QAction(MainWindow)
        self.actionRebuildAll.setObjectName("actionRebuildAll")
        self.actionCreateModule = QtWidgets.QAction(MainWindow)
        self.actionCreateModule.setObjectName("actionCreateModule")
        self.actionAddNodeToModule = QtWidgets.QAction(MainWindow)
        self.actionAddNodeToModule.setObjectName("actionAddNodeToModule")
        self.actionRemoveNodeFromModule = QtWidgets.QAction(MainWindow)
        self.actionRemoveNodeFromModule.setObjectName("actionRemoveNodeFromModule")
        self.actionMirrorJntsLToR = QtWidgets.QAction(MainWindow)
        self.actionMirrorJntsLToR.setObjectName("actionMirrorJntsLToR")
        self.actionMirrorJntsRToL = QtWidgets.QAction(MainWindow)
        self.actionMirrorJntsRToL.setObjectName("actionMirrorJntsRToL")
        self.actionMirrorSelection = QtWidgets.QAction(MainWindow)
        self.actionMirrorSelection.setObjectName("actionMirrorSelection")
        self.actionShowPluginManager = QtWidgets.QAction(MainWindow)
        self.actionShowPluginManager.setObjectName("actionShowPluginManager")
        self.actionShowPreferences = QtWidgets.QAction(MainWindow)
        self.actionShowPreferences.setObjectName("actionShowPreferences")
        self.actionCreateComponent = QtWidgets.QAction(MainWindow)
        self.actionCreateComponent.setObjectName("actionCreateComponent")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Open Rigging Toolkit", None, -1))
        self.actionUpdate.setText(QtWidgets.QApplication.translate("MainWindow", "&Update All", None, -1))
        self.actionUpdate.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Update", None, -1))
        self.actionImport.setText(QtWidgets.QApplication.translate("MainWindow", "&Import", None, -1))
        self.actionExport.setText(QtWidgets.QApplication.translate("MainWindow", "&Export", None, -1))
        self.actionBuildAll.setText(QtWidgets.QApplication.translate("MainWindow", "&Build All", None, -1))
        self.actionUnbuildAll.setText(QtWidgets.QApplication.translate("MainWindow", "&Unbuild All", None, -1))
        self.actionRebuildAll.setText(QtWidgets.QApplication.translate("MainWindow", "&Rebuild All", None, -1))
        self.actionCreateModule.setText(QtWidgets.QApplication.translate("MainWindow", "&Create Module", None, -1))
        self.actionAddNodeToModule.setText(QtWidgets.QApplication.translate("MainWindow", "&Add Selection", None, -1))
        self.actionRemoveNodeFromModule.setText(QtWidgets.QApplication.translate("MainWindow", "&Remove Selection", None, -1))
        self.actionMirrorJntsLToR.setText(QtWidgets.QApplication.translate("MainWindow", "&Mirror L -> R", None, -1))
        self.actionMirrorJntsRToL.setText(QtWidgets.QApplication.translate("MainWindow", "Mirror &R -> L", None, -1))
        self.actionMirrorSelection.setText(QtWidgets.QApplication.translate("MainWindow", "Mirror &using Selection", None, -1))
        self.actionShowPluginManager.setText(QtWidgets.QApplication.translate("MainWindow", "Plugin &Manager", None, -1))
        self.actionShowPreferences.setText(QtWidgets.QApplication.translate("MainWindow", "&Preferences", None, -1))
        self.actionCreateComponent.setText(QtWidgets.QApplication.translate("MainWindow", "&Create New", None, -1))

from ..widget_logger import WidgetLogger
