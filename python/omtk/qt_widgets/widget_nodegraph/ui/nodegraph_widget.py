# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/widget_nodegraph/ui/widget_nodegraph.ui'
#
# Created: Thu Nov 16 21:56:04 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1301, 525)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_add = QtWidgets.QPushButton(Form)
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout.addWidget(self.pushButton_add)
        self.pushButton_del = QtWidgets.QPushButton(Form)
        self.pushButton_del.setObjectName("pushButton_del")
        self.horizontalLayout.addWidget(self.pushButton_del)
        self.pushButton_clear = QtWidgets.QPushButton(Form)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.horizontalLayout.addWidget(self.pushButton_clear)
        self.pushButton_expand = QtWidgets.QPushButton(Form)
        self.pushButton_expand.setObjectName("pushButton_expand")
        self.horizontalLayout.addWidget(self.pushButton_expand)
        self.pushButton_collapse = QtWidgets.QPushButton(Form)
        self.pushButton_collapse.setObjectName("pushButton_collapse")
        self.horizontalLayout.addWidget(self.pushButton_collapse)
        self.pushButton_down = QtWidgets.QPushButton(Form)
        self.pushButton_down.setObjectName("pushButton_down")
        self.horizontalLayout.addWidget(self.pushButton_down)
        self.pushButton_up = QtWidgets.QPushButton(Form)
        self.pushButton_up.setObjectName("pushButton_up")
        self.horizontalLayout.addWidget(self.pushButton_up)
        self.pushButton_group = QtWidgets.QPushButton(Form)
        self.pushButton_group.setObjectName("pushButton_group")
        self.horizontalLayout.addWidget(self.pushButton_group)
        self.pushButton_ungroup = QtWidgets.QPushButton(Form)
        self.pushButton_ungroup.setObjectName("pushButton_ungroup")
        self.horizontalLayout.addWidget(self.pushButton_ungroup)
        self.pushButton_arrange_upstream = QtWidgets.QPushButton(Form)
        self.pushButton_arrange_upstream.setObjectName("pushButton_arrange_upstream")
        self.horizontalLayout.addWidget(self.pushButton_arrange_upstream)
        self.pushButton_arrange_downstream = QtWidgets.QPushButton(Form)
        self.pushButton_arrange_downstream.setObjectName("pushButton_arrange_downstream")
        self.horizontalLayout.addWidget(self.pushButton_arrange_downstream)
        self.pushButton_arrange_spring = QtWidgets.QPushButton(Form)
        self.pushButton_arrange_spring.setObjectName("pushButton_arrange_spring")
        self.horizontalLayout.addWidget(self.pushButton_arrange_spring)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget_breadcrumb = WidgetBreadcrumb(Form)
        self.widget_breadcrumb.setObjectName("widget_breadcrumb")
        self.verticalLayout.addWidget(self.widget_breadcrumb)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.pushButton_add.setText(QtWidgets.QApplication.translate("Form", "Add", None, -1))
        self.pushButton_del.setText(QtWidgets.QApplication.translate("Form", "Remove", None, -1))
        self.pushButton_clear.setText(QtWidgets.QApplication.translate("Form", "Clear", None, -1))
        self.pushButton_expand.setText(QtWidgets.QApplication.translate("Form", "Expand", None, -1))
        self.pushButton_collapse.setText(QtWidgets.QApplication.translate("Form", "Collapse", None, -1))
        self.pushButton_down.setText(QtWidgets.QApplication.translate("Form", "Go Down", None, -1))
        self.pushButton_up.setText(QtWidgets.QApplication.translate("Form", "Go Up", None, -1))
        self.pushButton_group.setText(QtWidgets.QApplication.translate("Form", "Group", None, -1))
        self.pushButton_ungroup.setText(QtWidgets.QApplication.translate("Form", "Ungroup", None, -1))
        self.pushButton_arrange_upstream.setText(QtWidgets.QApplication.translate("Form", "Arrange Uppstream", None, -1))
        self.pushButton_arrange_downstream.setText(QtWidgets.QApplication.translate("Form", "Arrange Downstrea", None, -1))
        self.pushButton_arrange_spring.setText(QtWidgets.QApplication.translate("Form", "Arrange Spring", None, -1))

from ...widget_breadcrumb import WidgetBreadcrumb
