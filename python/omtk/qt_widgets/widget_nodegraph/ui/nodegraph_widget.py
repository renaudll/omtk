# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/widget_nodegraph/ui/nodegraph_widget.ui'
#
# Created: Thu Jan  4 16:16:12 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(679, 592)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_breadcrumb = WidgetBreadcrumb(self.centralwidget)
        self.widget_breadcrumb.setObjectName("widget_breadcrumb")
        self.verticalLayout.addWidget(self.widget_breadcrumb)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 679, 20))
        self.menubar.setObjectName("menubar")
        self.menuNodes = QtWidgets.QMenu(self.menubar)
        self.menuNodes.setObjectName("menuNodes")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.widget_toolbar = WidgetToolbar(MainWindow)
        self.widget_toolbar.setObjectName("widget_toolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.widget_toolbar)
        MainWindow.insertToolBarBreak(self.widget_toolbar)
        self.actionAdd = QtWidgets.QAction(MainWindow)
        self.actionAdd.setObjectName("actionAdd")
        self.actionRemove = QtWidgets.QAction(MainWindow)
        self.actionRemove.setObjectName("actionRemove")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionExpand = QtWidgets.QAction(MainWindow)
        self.actionExpand.setObjectName("actionExpand")
        self.actionCollapse = QtWidgets.QAction(MainWindow)
        self.actionCollapse.setObjectName("actionCollapse")
        self.actionGoDown = QtWidgets.QAction(MainWindow)
        self.actionGoDown.setObjectName("actionGoDown")
        self.actionGoUp = QtWidgets.QAction(MainWindow)
        self.actionGoUp.setObjectName("actionGoUp")
        self.actionGroup = QtWidgets.QAction(MainWindow)
        self.actionGroup.setObjectName("actionGroup")
        self.actionUngroup = QtWidgets.QAction(MainWindow)
        self.actionUngroup.setObjectName("actionUngroup")
        self.actionMatchMayaEditorPositions = QtWidgets.QAction(MainWindow)
        self.actionMatchMayaEditorPositions.setObjectName("actionMatchMayaEditorPositions")
        self.actionLayoutUpstream = QtWidgets.QAction(MainWindow)
        self.actionLayoutUpstream.setObjectName("actionLayoutUpstream")
        self.actionLayoutDownstream = QtWidgets.QAction(MainWindow)
        self.actionLayoutDownstream.setObjectName("actionLayoutDownstream")
        self.actionLayoutSpring = QtWidgets.QAction(MainWindow)
        self.actionLayoutSpring.setObjectName("actionLayoutSpring")
        self.actionLayoutRecenter = QtWidgets.QAction(MainWindow)
        self.actionLayoutRecenter.setObjectName("actionLayoutRecenter")
        self.menuNodes.addAction(self.actionMatchMayaEditorPositions)
        self.menuNodes.addSeparator()
        self.menuNodes.addAction(self.actionLayoutUpstream)
        self.menuNodes.addAction(self.actionLayoutDownstream)
        self.menuNodes.addAction(self.actionLayoutSpring)
        self.menuNodes.addAction(self.actionLayoutRecenter)
        self.menubar.addAction(self.menuNodes.menuAction())
        self.toolBar.addAction(self.actionAdd)
        self.toolBar.addAction(self.actionRemove)
        self.toolBar.addAction(self.actionClear)
        self.toolBar.addAction(self.actionExpand)
        self.toolBar.addAction(self.actionCollapse)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionGoDown)
        self.toolBar.addAction(self.actionGoUp)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionGroup)
        self.toolBar.addAction(self.actionUngroup)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.menuNodes.setTitle(QtWidgets.QApplication.translate("MainWindow", "Arra&nge", None, -1))
        self.toolBar.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "toolBar", None, -1))
        self.widget_toolbar.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "toolBar_2", None, -1))
        self.actionAdd.setText(QtWidgets.QApplication.translate("MainWindow", "Add", None, -1))
        self.actionRemove.setText(QtWidgets.QApplication.translate("MainWindow", "Remove", None, -1))
        self.actionClear.setText(QtWidgets.QApplication.translate("MainWindow", "Clear", None, -1))
        self.actionExpand.setText(QtWidgets.QApplication.translate("MainWindow", "Expand", None, -1))
        self.actionCollapse.setText(QtWidgets.QApplication.translate("MainWindow", "Collapse", None, -1))
        self.actionGoDown.setText(QtWidgets.QApplication.translate("MainWindow", "Go Down", None, -1))
        self.actionGoUp.setText(QtWidgets.QApplication.translate("MainWindow", "Go Up", None, -1))
        self.actionGroup.setText(QtWidgets.QApplication.translate("MainWindow", "Group", None, -1))
        self.actionUngroup.setText(QtWidgets.QApplication.translate("MainWindow", "Ungroup", None, -1))
        self.actionMatchMayaEditorPositions.setText(QtWidgets.QApplication.translate("MainWindow", "&Set positions to Maya NodeEditor", None, -1))
        self.actionLayoutUpstream.setText(QtWidgets.QApplication.translate("MainWindow", "&Layout Upstream", None, -1))
        self.actionLayoutDownstream.setText(QtWidgets.QApplication.translate("MainWindow", "Layout &Downstream", None, -1))
        self.actionLayoutSpring.setText(QtWidgets.QApplication.translate("MainWindow", "La&yout Spring", None, -1))
        self.actionLayoutRecenter.setText(QtWidgets.QApplication.translate("MainWindow", "Recenter", None, -1))

from ...widget_breadcrumb import WidgetBreadcrumb
from ...widget_toolbar import WidgetToolbar