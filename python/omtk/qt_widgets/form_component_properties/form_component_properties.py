from .ui import form_component_properties as ui_def
from omtk.vendor.Qt import QtWidgets
from omtk.core import component_definition
from omtk import log

if False:  # for type hinting
    from omtk.core.component import Component


class ComponentPropertyWidget(QtWidgets.QMainWindow):
    """
    Widget that display and allow the user to change the metadata associated with a component.
    """
    def __init__(self, component):
        super(ComponentPropertyWidget, self).__init__()

        self._component = component

        self.ui = ui_def.Ui_MainWindow()
        self.ui.setupUi(self)

        self.load_component(component)

        self.ui.pushButton_save.pressed.connect(self.on_save)

    def load_component(self, component):
        # type: (Component) -> None
        component_def = component.get_definition()
        if component_def is None:
            log.warning("No definition associated with {0}. Creating an empty one.".format(component))
            component_def = component_definition.ComponentDefinition.empty()
        self.ui.lineEdit_name.setText(component_def.name)
        self.ui.lineEdit_author.setText(component_def.author)
        self.ui.lineEdit_version.setText(component_def.version)
        self.ui.lineEdit_uid.setText(component_def.uid)

    def get_definition(self):
        name = self.ui.lineEdit_name.text()
        author = self.ui.lineEdit_author.text()
        version = self.ui.lineEdit_version.text()
        uid = self.ui.lineEdit_uid.text()
        return component_definition.ComponentDefinition(
            name=name,
            author=author,
            version=version,
            uid=uid
        )

    def on_save(self):
        new_def = self.get_definition()
        self._component.set_definition(new_def)

