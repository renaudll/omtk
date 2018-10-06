# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/python/omtk/python/omtk/qt_widgets/ui/preferences_window.ui'
#
# Created: Sun Sep 30 19:03:56 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(379, 278)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox_logLevel = QtWidgets.QComboBox(Dialog)
        self.comboBox_logLevel.setObjectName("comboBox_logLevel")
        self.comboBox_logLevel.addItem("")
        self.comboBox_logLevel.addItem("")
        self.comboBox_logLevel.addItem("")
        self.comboBox_logLevel.addItem("")
        self.gridLayout.addWidget(self.comboBox_logLevel, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "OMTK - Preferences", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Default Rig Class", None, -1))
        self.comboBox_logLevel.setItemText(0, QtWidgets.QApplication.translate("Dialog", "DEBUG", None, -1))
        self.comboBox_logLevel.setItemText(1, QtWidgets.QApplication.translate("Dialog", "INFO", None, -1))
        self.comboBox_logLevel.setItemText(2, QtWidgets.QApplication.translate("Dialog", "WARNING", None, -1))
        self.comboBox_logLevel.setItemText(3, QtWidgets.QApplication.translate("Dialog", "ERROR", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Default Log Level", None, -1))
        self.checkBox.setText(QtWidgets.QApplication.translate("Dialog", "Hide Welcome Screen", None, -1))

