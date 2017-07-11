from omtk.core import api
from omtk.core import preferences
from omtk.ui import widget_welcome
from omtk.vendor import libSerialization
from omtk.vendor.Qt import QtCore, QtWidgets

from . import model_rig_definitions
from . import model_rig_templates


class WidgetWelcome(QtWidgets.QWidget):
    onCreate = QtCore.Signal()

    def __init__(self, parent):
        super(WidgetWelcome, self).__init__(parent)
        self.ui = widget_welcome.Ui_Form()
        self.ui.setupUi(self)

        # Initialize rig definition view
        self.rig_def_view = self.ui.tableView_types_rig
        self.rig_def_model= model_rig_definitions.RigDefinitionsModel()
        self.rig_def_view.setModel(self.rig_def_model)

        # Initialize rig template view
        view = self.ui.tableView_types_template
        model = model_rig_templates.RigTemplatesModel()
        view.setModel(model)

        # Select default rig
        default_rig_def = preferences.preferences.get_default_rig_class()
        self.set_selected_rig_definition(default_rig_def)

        # Connect events
        self.ui.btn_create_rig_default.pressed.connect(self.on_create_rig)
        self.ui.btn_create_rig_template.pressed.connect(self.on_import_rig)

    def get_selected_rig_definition(self):
        row = next(iter(row.row() for row in self.rig_def_view.selectionModel().selectedRows()), None)
        if row:
            return self.rig_def_model.entries[row]

    def set_selected_rig_definition(self, rig_def):
        row = self.rig_def_model.entries.index(rig_def)
        self.rig_def_view.selectRow(row)

    def on_create_rig(self):
        rig_type = self.get_selected_rig_definition()

        # Initialize the scene
        rig = api.create(cls=rig_type)
        rig.build()
        libSerialization.export_network(rig)

        self.onCreate.emit()

    def on_import_rig(self):
        self.onCreate.emit()
