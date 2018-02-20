"""
Helper UI to create "Component".
"""

from .ui import form_add_attribute as ui_def
import pymel.core as pymel
from omtk.vendor.Qt import QtWidgets
from omtk.libs import libAttr


# maya known attr type names
TYPE_FLOAT = 'float'
TYPE_INT = 'byte'  # 8 bit integer
TYPE_STR = 'string'
TYPE_BOOL = 'bool'
TYPE_MATRIX = 'matrix'
TYPE_MESSAGE = 'message'


class FormCreateAttribute(QtWidgets.QMainWindow):
    def __init__(self):
        super(FormCreateAttribute, self).__init__()

        self.ui = ui_def.Ui_MainWindow()
        self.ui.setupUi(self)

        # Set default radio button
        self.ui.rb_float.setChecked(True)

        self.ui.pushButton.pressed.connect(self.on_submit)

    def get_attr_type(self):
        if self.ui.rb_float.isChecked():
            return TYPE_FLOAT
        if self.ui.rb_integer.isChecked():
            return TYPE_INT
        if self.ui.rb_string.isChecked():
            return TYPE_STR
        if self.ui.rb_boolean.isChecked():
            return TYPE_BOOL
        if self.ui.rb_matrix.isChecked():
            return TYPE_MATRIX
        if self.ui.rb_message.isChecked():
            return TYPE_MESSAGE
        raise Exception("No attribute type provided")

    def add_attribute(self, obj, name, type, value):
        kwargs = libAttr._g_addAttr_kwargs_map[type]  # todo: create method?
        return libAttr.addAttr(obj, name, **kwargs)

    def on_submit(self):
        name = self.ui.lineEdit_name.text()
        type_ = self.get_attr_type()
        value = self.ui.lineEdit_value.text()

        for obj in pymel.selected():
            self.add_attribute(obj, name, type_, value)
