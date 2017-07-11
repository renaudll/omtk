# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/nodegraph_widget/ui/nodegraph_widget.ui'
#
# Created: Tue Jul  4 23:27:10 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(760, 424)
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
        self.pushButton_arrange_upstream = QtWidgets.QPushButton(Form)
        self.pushButton_arrange_upstream.setObjectName("pushButton_arrange_upstream")
        self.horizontalLayout.addWidget(self.pushButton_arrange_upstream)
        self.pushButton_arrange_downstream = QtWidgets.QPushButton(Form)
        self.pushButton_arrange_downstream.setObjectName("pushButton_arrange_downstream")
        self.horizontalLayout.addWidget(self.pushButton_arrange_downstream)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget_breadcrumb = WidgetBreadcrumb(Form)
        self.widget_breadcrumb.setObjectName("widget_breadcrumb")
        self.verticalLayout.addWidget(self.widget_breadcrumb)
        self.widget_view = NodeGraphView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_view.sizePolicy().hasHeightForWidth())
        self.widget_view.setSizePolicy(sizePolicy)
        self.widget_view.setObjectName("widget_view")
        self.verticalLayout.addWidget(self.widget_view)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None))
        self.pushButton_add.setText(QtWidgets.QApplication.translate("Form", "Add", None))
        self.pushButton_del.setText(QtWidgets.QApplication.translate("Form", "Remove", None))
        self.pushButton_clear.setText(QtWidgets.QApplication.translate("Form", "Clear", None))
        self.pushButton_expand.setText(QtWidgets.QApplication.translate("Form", "Expand", None))
        self.pushButton_collapse.setText(QtWidgets.QApplication.translate("Form", "Collapse", None))
        self.pushButton_down.setText(QtWidgets.QApplication.translate("Form", "Go Down", None))
        self.pushButton_up.setText(QtWidgets.QApplication.translate("Form", "Go Up", None))
        self.pushButton_arrange_upstream.setText(QtWidgets.QApplication.translate("Form", "Arrange Uppstream", None))
        self.pushButton_arrange_downstream.setText(QtWidgets.QApplication.translate("Form", "Arrange Downstrea", None))

from ..nodegraph_view import NodeGraphView
from omtk.qt_widgets.widget_breadcrumb import WidgetBreadcrumb
