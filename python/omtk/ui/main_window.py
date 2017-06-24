# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/ui/main_window.ui'
#
# Created: Tue Jun 20 21:45:39 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtWidgets

class Ui_OpenRiggingToolkit(object):
    def setupUi(self, OpenRiggingToolkit):
        OpenRiggingToolkit.setObjectName("OpenRiggingToolkit")
        OpenRiggingToolkit.resize(574, 587)
        self.centralwidget = QtWidgets.QWidget(OpenRiggingToolkit)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.page_1)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.widget_welcome = WidgetWelcome(self.page_1)
        self.widget_welcome.setObjectName("widget_welcome")
        self.verticalLayout_9.addWidget(self.widget_welcome)
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget_node_editor = NodeGraphWidget(self.page_2)
        self.widget_node_editor.setObjectName("widget_node_editor")
        self.verticalLayout_7.addWidget(self.widget_node_editor)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout_5.addWidget(self.stackedWidget)
        OpenRiggingToolkit.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(OpenRiggingToolkit)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 574, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuRig = QtWidgets.QMenu(self.menubar)
        self.menuRig.setObjectName("menuRig")
        self.menuJoint = QtWidgets.QMenu(self.menubar)
        self.menuJoint.setObjectName("menuJoint")
        self.menuInfluences = QtWidgets.QMenu(self.menubar)
        self.menuInfluences.setObjectName("menuInfluences")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuComponents = QtWidgets.QMenu(self.menubar)
        self.menuComponents.setObjectName("menuComponents")
        OpenRiggingToolkit.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(OpenRiggingToolkit)
        self.statusbar.setObjectName("statusbar")
        OpenRiggingToolkit.setStatusBar(self.statusbar)
        self.dockWidget_logger = QtWidgets.QDockWidget(OpenRiggingToolkit)
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
        OpenRiggingToolkit.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_logger)
        self.dockWidget_modules = QtWidgets.QDockWidget(OpenRiggingToolkit)
        self.dockWidget_modules.setMinimumSize(QtCore.QSize(120, 50))
        self.dockWidget_modules.setObjectName("dockWidget_modules")
        self.dockWidgetContents_modules = QtWidgets.QWidget()
        self.dockWidgetContents_modules.setObjectName("dockWidgetContents_modules")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.dockWidgetContents_modules)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_modules = WidgetListModules(self.dockWidgetContents_modules)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_modules.sizePolicy().hasHeightForWidth())
        self.widget_modules.setSizePolicy(sizePolicy)
        self.widget_modules.setObjectName("widget_modules")
        self.verticalLayout_6.addWidget(self.widget_modules)
        self.dockWidget_modules.setWidget(self.dockWidgetContents_modules)
        OpenRiggingToolkit.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_modules)
        self.dockWidget_influences = QtWidgets.QDockWidget(OpenRiggingToolkit)
        self.dockWidget_influences.setMinimumSize(QtCore.QSize(120, 50))
        self.dockWidget_influences.setObjectName("dockWidget_influences")
        self.dockWidgetContents_jnts = QtWidgets.QWidget()
        self.dockWidgetContents_jnts.setObjectName("dockWidgetContents_jnts")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.dockWidgetContents_jnts)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.widget_jnts = WidgetListInfluences(self.dockWidgetContents_jnts)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_jnts.sizePolicy().hasHeightForWidth())
        self.widget_jnts.setSizePolicy(sizePolicy)
        self.widget_jnts.setObjectName("widget_jnts")
        self.verticalLayout_8.addWidget(self.widget_jnts)
        self.dockWidget_influences.setWidget(self.dockWidgetContents_jnts)
        OpenRiggingToolkit.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_influences)
        self.dockWidget_meshes = QtWidgets.QDockWidget(OpenRiggingToolkit)
        self.dockWidget_meshes.setMinimumSize(QtCore.QSize(120, 50))
        self.dockWidget_meshes.setObjectName("dockWidget_meshes")
        self.dockWidgetContents_meshes = QtWidgets.QWidget()
        self.dockWidgetContents_meshes.setObjectName("dockWidgetContents_meshes")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.dockWidgetContents_meshes)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.widget_meshes = WidgetListMeshes(self.dockWidgetContents_meshes)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_meshes.sizePolicy().hasHeightForWidth())
        self.widget_meshes.setSizePolicy(sizePolicy)
        self.widget_meshes.setObjectName("widget_meshes")
        self.verticalLayout_10.addWidget(self.widget_meshes)
        self.dockWidget_meshes.setWidget(self.dockWidgetContents_meshes)
        OpenRiggingToolkit.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_meshes)
        self.actionUpdate = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionUpdate.setObjectName("actionUpdate")
        self.actionImport = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionImport.setObjectName("actionImport")
        self.actionExport = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionExport.setObjectName("actionExport")
        self.actionBuildAll = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionBuildAll.setObjectName("actionBuildAll")
        self.actionUnbuildAll = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionUnbuildAll.setObjectName("actionUnbuildAll")
        self.actionRebuildAll = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionRebuildAll.setObjectName("actionRebuildAll")
        self.actionCreateModule = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionCreateModule.setObjectName("actionCreateModule")
        self.actionAddNodeToModule = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionAddNodeToModule.setObjectName("actionAddNodeToModule")
        self.actionRemoveNodeFromModule = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionRemoveNodeFromModule.setObjectName("actionRemoveNodeFromModule")
        self.actionMirrorJntsLToR = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionMirrorJntsLToR.setObjectName("actionMirrorJntsLToR")
        self.actionMirrorJntsRToL = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionMirrorJntsRToL.setObjectName("actionMirrorJntsRToL")
        self.actionMirrorSelection = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionMirrorSelection.setObjectName("actionMirrorSelection")
        self.actionShowPluginManager = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionShowPluginManager.setObjectName("actionShowPluginManager")
        self.actionShowPreferences = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionShowPreferences.setObjectName("actionShowPreferences")
        self.actionCreateComponent = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionCreateComponent.setObjectName("actionCreateComponent")
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionUpdate)
        self.menuRig.addAction(self.actionBuildAll)
        self.menuRig.addAction(self.actionUnbuildAll)
        self.menuRig.addAction(self.actionRebuildAll)
        self.menuJoint.addAction(self.actionCreateModule)
        self.menuJoint.addAction(self.actionAddNodeToModule)
        self.menuJoint.addAction(self.actionRemoveNodeFromModule)
        self.menuInfluences.addAction(self.actionMirrorJntsLToR)
        self.menuInfluences.addAction(self.actionMirrorJntsRToL)
        self.menuInfluences.addAction(self.actionMirrorSelection)
        self.menuSettings.addAction(self.actionShowPreferences)
        self.menuSettings.addAction(self.actionShowPluginManager)
        self.menuComponents.addAction(self.actionCreateComponent)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuRig.menuAction())
        self.menubar.addAction(self.menuJoint.menuAction())
        self.menubar.addAction(self.menuInfluences.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuComponents.menuAction())

        self.retranslateUi(OpenRiggingToolkit)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(OpenRiggingToolkit)

    def retranslateUi(self, OpenRiggingToolkit):
        OpenRiggingToolkit.setWindowTitle(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Open Rigging Toolkit", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Fi&le", None, -1))
        self.menuRig.setTitle(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Ri&g", None, -1))
        self.menuJoint.setTitle(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Mo&dules", None, -1))
        self.menuInfluences.setTitle(QtWidgets.QApplication.translate("OpenRiggingToolkit", "I&nfluences", None, -1))
        self.menuSettings.setTitle(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Settings", None, -1))
        self.menuComponents.setTitle(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Components", None, -1))
        self.dockWidget_modules.setWindowTitle(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Modules", None, -1))
        self.dockWidget_influences.setWindowTitle(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Influences", None, -1))
        self.dockWidget_meshes.setWindowTitle(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Meshes", None, -1))
        self.actionUpdate.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "&Update All", None, -1))
        self.actionUpdate.setToolTip(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Update", None, -1))
        self.actionImport.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "&Import", None, -1))
        self.actionExport.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "&Export", None, -1))
        self.actionBuildAll.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "&Build All", None, -1))
        self.actionUnbuildAll.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "&Unbuild All", None, -1))
        self.actionRebuildAll.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "&Rebuild All", None, -1))
        self.actionCreateModule.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "&Create Module", None, -1))
        self.actionAddNodeToModule.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "&Add Selection", None, -1))
        self.actionRemoveNodeFromModule.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "&Remove Selection", None, -1))
        self.actionMirrorJntsLToR.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "&Mirror L -> R", None, -1))
        self.actionMirrorJntsRToL.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Mirror &R -> L", None, -1))
        self.actionMirrorSelection.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Mirror &using Selection", None, -1))
        self.actionShowPluginManager.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Plugin &Manager", None, -1))
        self.actionShowPreferences.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "&Preferences", None, -1))
        self.actionCreateComponent.setText(QtWidgets.QApplication.translate("OpenRiggingToolkit", "Create New", None, -1))

from omtk.qt_widgets.nodegraph_widget.nodegraph_widget import NodeGraphWidget
from ..widget_list_meshes import WidgetListMeshes
from ..widget_logger import WidgetLogger
from ..widget_list_modules import WidgetListModules
from ..widget_welcome import WidgetWelcome
from ..widget_list_influences import WidgetListInfluences
