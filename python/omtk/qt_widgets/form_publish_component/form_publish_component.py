"""
Helper UI to create "Component".
"""

import logging

from omtk.component import component_definition
from omtk.component import component_registry
from omtk.vendor.Qt import QtWidgets

from .ui import form_publish_component as ui_def

log = logging.getLogger(__name__)


class FormPublishComponent(QtWidgets.QMainWindow):
    def __init__(self, component):
        """

        :param omtk.Component component:
        """
        super(FormPublishComponent, self).__init__()

        self._component = component

        self.ui = ui_def.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_submit.pressed.connect(self.on_submit)

        self.load_component(component)

    def load_component(self, component):
        """

        :param omtk.Component component: The component to load.
        """
        component_def = component.get_definition()
        if component_def is None:
            log.warning("No definition associated with {0}. Creating an empty one.".format(component))
            component_def = component_definition.ComponentDefinition.empty()
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

        # todo: Ensure there's no component with the same uid and version in the REGISTRY_DEFAULT!

        self._component.set_definition(component_def)
        path = registry.get_path_from_component_def(component_def)
        log.info('Exporting component to {0}'.format(path))
        self._component.export(path)
        self.close()
