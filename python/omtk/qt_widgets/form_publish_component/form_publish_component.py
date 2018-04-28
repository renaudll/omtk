"""
Helper UI to create "Component".
"""

from .ui import form_publish_component as ui_def
import pymel.core as pymel
from omtk.vendor.Qt import QtWidgets
from omtk.libs import libAttr
from omtk.core import component_definition
from omtk.core import component_registry
from omtk import log

if False:  # for type hinting
    from omtk.core.component import Component


class FormPublishComponent(QtWidgets.QMainWindow):
    def __init__(self, component):
        super(FormPublishComponent, self).__init__()

        self._component = component

        self.ui = ui_def.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_submit.pressed.connect(self.on_submit)

        self.load_component(component)

    def load_component(self, component):
        # type: (Component) -> None
        component_def = component.get_definition()
        self.ui.lineEdit_name.setText(component_def.name)
        self.ui.lineEdit_author.setText(component_def.author)
        self.ui.lineEdit_version.setText(component_def.version)
        self.ui.lineEdit_uid.setText(component_def.uid)

    def get_new_definition(self):
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

    def on_submit(self):
        registry = component_registry.get_registry()
        component_def = self.get_new_definition()
        self._component.set_definition(component_def)
        path = registry.get_path_from_component_def(component_def)
        log.info('Exporting component to {0}'.format(path))
        self._component.export(path)
        self.close()

