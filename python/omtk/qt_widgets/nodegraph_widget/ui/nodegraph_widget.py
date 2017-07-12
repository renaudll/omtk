# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/nodegraph_widget/ui/nodegraph_widget.ui'
#
# Created: Wed Jul 12 12:34:42 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(966, 424)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_add = QtGui.QPushButton(Form)
        self.pushButton_add.setObjectName("pushButton_add")
        self.horizontalLayout.addWidget(self.pushButton_add)
        self.pushButton_del = QtGui.QPushButton(Form)
        self.pushButton_del.setObjectName("pushButton_del")
        self.horizontalLayout.addWidget(self.pushButton_del)
        self.pushButton_clear = QtGui.QPushButton(Form)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.horizontalLayout.addWidget(self.pushButton_clear)
        self.pushButton_expand = QtGui.QPushButton(Form)
        self.pushButton_expand.setObjectName("pushButton_expand")
        self.horizontalLayout.addWidget(self.pushButton_expand)
        self.pushButton_collapse = QtGui.QPushButton(Form)
        self.pushButton_collapse.setObjectName("pushButton_collapse")
        self.horizontalLayout.addWidget(self.pushButton_collapse)
        self.pushButton_down = QtGui.QPushButton(Form)
        self.pushButton_down.setObjectName("pushButton_down")
        self.horizontalLayout.addWidget(self.pushButton_down)
        self.pushButton_up = QtGui.QPushButton(Form)
        self.pushButton_up.setObjectName("pushButton_up")
        self.horizontalLayout.addWidget(self.pushButton_up)
        self.pushButton_arrange_upstream = QtGui.QPushButton(Form)
        self.pushButton_arrange_upstream.setObjectName("pushButton_arrange_upstream")
        self.horizontalLayout.addWidget(self.pushButton_arrange_upstream)
        self.pushButton_arrange_downstream = QtGui.QPushButton(Form)
        self.pushButton_arrange_downstream.setObjectName("pushButton_arrange_downstream")
        self.horizontalLayout.addWidget(self.pushButton_arrange_downstream)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget_breadcrumb = WidgetBreadcrumb(Form)
        self.widget_breadcrumb.setObjectName("widget_breadcrumb")
        self.verticalLayout.addWidget(self.widget_breadcrumb)
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_add.setText(QtGui.QApplication.translate("Form", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_del.setText(QtGui.QApplication.translate("Form", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_clear.setText(QtGui.QApplication.translate("Form", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_expand.setText(QtGui.QApplication.translate("Form", "Expand", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_collapse.setText(QtGui.QApplication.translate("Form", "Collapse", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_down.setText(QtGui.QApplication.translate("Form", "Go Down", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_up.setText(QtGui.QApplication.translate("Form", "Go Up", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_arrange_upstream.setText(QtGui.QApplication.translate("Form", "Arrange Uppstream", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_arrange_downstream.setText(QtGui.QApplication.translate("Form", "Arrange Downstrea", None, QtGui.QApplication.UnicodeUTF8))

from ...widget_breadcrumb import WidgetBreadcrumb
