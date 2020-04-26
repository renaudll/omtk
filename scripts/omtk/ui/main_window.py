# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rlessard/packages/omtk/0.4.999/python/omtk/ui/main_window.ui'
#
# Created: Tue Feb 20 10:34:54 2018
#      by: pyside2-uic  running on Qt 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets, QtCompat


class Ui_OpenRiggingToolkit(object):
    def setupUi(self, OpenRiggingToolkit):
        OpenRiggingToolkit.setObjectName("OpenRiggingToolkit")
        OpenRiggingToolkit.resize(787, 658)
        self.centralwidget = QtWidgets.QWidget(OpenRiggingToolkit)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_modules = QtWidgets.QLabel(self.layoutWidget)
        self.label_modules.setObjectName("label_modules")
        self.verticalLayout.addWidget(self.label_modules)
        self.widget_modules = WidgetListModules(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.widget_modules.sizePolicy().hasHeightForWidth()
        )
        self.widget_modules.setSizePolicy(sizePolicy)
        self.widget_modules.setObjectName("widget_modules")
        self.verticalLayout.addWidget(self.widget_modules)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_jnts = QtWidgets.QLabel(self.layoutWidget1)
        self.label_jnts.setObjectName("label_jnts")
        self.verticalLayout_2.addWidget(self.label_jnts)
        self.widget_jnts = WidgetListInfluences(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_jnts.sizePolicy().hasHeightForWidth())
        self.widget_jnts.setSizePolicy(sizePolicy)
        self.widget_jnts.setObjectName("widget_jnts")
        self.verticalLayout_2.addWidget(self.widget_jnts)
        self.layoutWidget2 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.layoutWidget2)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.widget_meshes = WidgetListMeshes(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.widget_meshes.sizePolicy().hasHeightForWidth()
        )
        self.widget_meshes.setSizePolicy(sizePolicy)
        self.widget_meshes.setObjectName("widget_meshes")
        self.verticalLayout_3.addWidget(self.widget_meshes)
        self.verticalLayout_5.addWidget(self.splitter)
        OpenRiggingToolkit.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(OpenRiggingToolkit)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 787, 19))
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
        OpenRiggingToolkit.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(OpenRiggingToolkit)
        self.statusbar.setObjectName("statusbar")
        OpenRiggingToolkit.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(OpenRiggingToolkit)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_logger = WidgetLogger(self.dockWidgetContents)
        self.widget_logger.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.widget_logger.sizePolicy().hasHeightForWidth()
        )
        self.widget_logger.setSizePolicy(sizePolicy)
        self.widget_logger.setObjectName("widget_logger")
        self.verticalLayout_4.addWidget(self.widget_logger)
        self.dockWidget.setWidget(self.dockWidgetContents)
        OpenRiggingToolkit.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget)
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
        self.actionAddSelectedInfluencesToModule = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionAddSelectedInfluencesToModule.setObjectName(
            "actionAddSelectedInfluencesToModule"
        )
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
        self.actionAddSelectedMeshesToModule = QtWidgets.QAction(OpenRiggingToolkit)
        self.actionAddSelectedMeshesToModule.setObjectName(
            "actionAddSelectedMeshesToModule"
        )
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionUpdate)
        self.menuRig.addAction(self.actionBuildAll)
        self.menuRig.addAction(self.actionUnbuildAll)
        self.menuRig.addAction(self.actionRebuildAll)
        self.menuJoint.addAction(self.actionCreateModule)
        self.menuJoint.addAction(self.actionAddSelectedInfluencesToModule)
        self.menuJoint.addAction(self.actionAddSelectedMeshesToModule)
        self.menuJoint.addAction(self.actionRemoveNodeFromModule)
        self.menuInfluences.addAction(self.actionMirrorJntsLToR)
        self.menuInfluences.addAction(self.actionMirrorJntsRToL)
        self.menuInfluences.addAction(self.actionMirrorSelection)
        self.menuSettings.addAction(self.actionShowPreferences)
        self.menuSettings.addAction(self.actionShowPluginManager)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuRig.menuAction())
        self.menubar.addAction(self.menuJoint.menuAction())
        self.menubar.addAction(self.menuInfluences.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(OpenRiggingToolkit)
        QtCore.QMetaObject.connectSlotsByName(OpenRiggingToolkit)

    def retranslateUi(self, OpenRiggingToolkit):
        OpenRiggingToolkit.setWindowTitle(
            QtCompat.translate("OpenRiggingToolkit", "Open Rigging Toolkit", None, -1)
        )
        self.label_modules.setText(
            QtCompat.translate("OpenRiggingToolkit", "Modules", None, -1)
        )
        self.label_jnts.setText(
            QtCompat.translate("OpenRiggingToolkit", "Influences", None, -1)
        )
        self.label.setText(QtCompat.translate("OpenRiggingToolkit", "Meshes", None, -1))
        self.menuFile.setTitle(
            QtCompat.translate("OpenRiggingToolkit", "File", None, -1)
        )
        self.menuRig.setTitle(QtCompat.translate("OpenRiggingToolkit", "Rig", None, -1))
        self.menuJoint.setTitle(
            QtCompat.translate("OpenRiggingToolkit", "Modules", None, -1)
        )
        self.menuInfluences.setTitle(
            QtCompat.translate("OpenRiggingToolkit", "Influences", None, -1)
        )
        self.menuSettings.setTitle(
            QtCompat.translate("OpenRiggingToolkit", "Settings", None, -1)
        )
        self.actionUpdate.setText(
            QtCompat.translate("OpenRiggingToolkit", "Update All", None, -1)
        )
        self.actionUpdate.setToolTip(
            QtCompat.translate("OpenRiggingToolkit", "Update", None, -1)
        )
        self.actionImport.setText(
            QtCompat.translate("OpenRiggingToolkit", "Import", None, -1)
        )
        self.actionExport.setText(
            QtCompat.translate("OpenRiggingToolkit", "Export", None, -1)
        )
        self.actionBuildAll.setText(
            QtCompat.translate("OpenRiggingToolkit", "Build All", None, -1)
        )
        self.actionUnbuildAll.setText(
            QtCompat.translate("OpenRiggingToolkit", "Unbuild All", None, -1)
        )
        self.actionRebuildAll.setText(
            QtCompat.translate("OpenRiggingToolkit", "Rebuild All", None, -1)
        )
        self.actionCreateModule.setText(
            QtCompat.translate("OpenRiggingToolkit", "Create Module", None, -1)
        )
        self.actionAddSelectedInfluencesToModule.setText(
            QtCompat.translate(
                "OpenRiggingToolkit", "Add Selected Influences to Module", None, -1
            )
        )
        self.actionRemoveNodeFromModule.setText(
            QtCompat.translate("OpenRiggingToolkit", "Remove Selection", None, -1)
        )
        self.actionMirrorJntsLToR.setText(
            QtCompat.translate("OpenRiggingToolkit", "Mirror L -> R", None, -1)
        )
        self.actionMirrorJntsRToL.setText(
            QtCompat.translate("OpenRiggingToolkit", "Mirror R -> L", None, -1)
        )
        self.actionMirrorSelection.setText(
            QtCompat.translate("OpenRiggingToolkit", "Mirror using Selection", None, -1)
        )
        self.actionShowPluginManager.setText(
            QtCompat.translate("OpenRiggingToolkit", "Plugin Manager", None, -1)
        )
        self.actionShowPreferences.setText(
            QtCompat.translate("OpenRiggingToolkit", "Preferences", None, -1)
        )
        self.actionAddSelectedMeshesToModule.setText(
            QtCompat.translate(
                "OpenRiggingToolkit", "Add Selected Meshes to Module", None, -1
            )
        )


from ..widget_logger import WidgetLogger
from ..widget_list_modules import WidgetListModules
from ..widget_list_meshes import WidgetListMeshes
from ..widget_list_influences import WidgetListInfluences
