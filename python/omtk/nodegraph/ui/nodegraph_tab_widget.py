# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/nodegraph/ui/nodegraph_tab_widget.ui'
#
# Created: Sat Sep 29 16:35:03 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(747, 698)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_breadcrumb = WidgetBreadcrumb(Form)
        self.widget_breadcrumb.setObjectName("widget_breadcrumb")
        self.verticalLayout.addWidget(self.widget_breadcrumb)
        self.widget_nodegraph = NodeGraphView(Form)
        self.widget_nodegraph.setObjectName("widget_nodegraph")
        self.verticalLayout.addWidget(self.widget_nodegraph)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))

from ...widget_breadcrumb import WidgetBreadcrumb
from ..nodegraph_view import NodeGraphView
