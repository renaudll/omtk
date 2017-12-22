# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/widget_component_wizard/ui/widget_create_component.ui'
#
# Created: Wed Dec 20 20:39:32 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(819, 416)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_ctrl = QtWidgets.QLabel(self.centralwidget)
        self.label_ctrl.setObjectName("label_ctrl")
        self.verticalLayout.addWidget(self.label_ctrl)
        self.widget_view_ctrl = WidgetCreateComponentWizardParts(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_view_ctrl.sizePolicy().hasHeightForWidth())
        self.widget_view_ctrl.setSizePolicy(sizePolicy)
        self.widget_view_ctrl.setObjectName("widget_view_ctrl")
        self.verticalLayout.addWidget(self.widget_view_ctrl)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_infl = QtWidgets.QLabel(self.centralwidget)
        self.label_infl.setObjectName("label_infl")
        self.verticalLayout_2.addWidget(self.label_infl)
        self.widget_view_infl = WidgetCreateComponentWizardParts(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_view_infl.sizePolicy().hasHeightForWidth())
        self.widget_view_infl.setSizePolicy(sizePolicy)
        self.widget_view_infl.setObjectName("widget_view_infl")
        self.verticalLayout_2.addWidget(self.widget_view_infl)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_guid = QtWidgets.QLabel(self.centralwidget)
        self.label_guid.setObjectName("label_guid")
        self.verticalLayout_3.addWidget(self.label_guid)
        self.widget_view_guid = WidgetCreateComponentWizardParts(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_view_guid.sizePolicy().hasHeightForWidth())
        self.widget_view_guid.setSizePolicy(sizePolicy)
        self.widget_view_guid.setObjectName("widget_view_guid")
        self.verticalLayout_3.addWidget(self.widget_view_guid)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 819, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Component Creation Wizard"))
        self.label_ctrl.setText(QtWidgets.QApplication.translate("MainWindow", "Ctrls:"))
        self.label_infl.setText(QtWidgets.QApplication.translate("MainWindow", "Influences:"))
        self.label_guid.setText(QtWidgets.QApplication.translate("MainWindow", "Guides:"))

from ..widget_create_component_wizard_parts import WidgetCreateComponentWizardParts
