"""
Helper UI to create "Component".
Component are a concept of OMTK2 backported to OMTK1 for convinience.
"""

from ui import widget_create_component

reload(widget_create_component)
from omtk.vendor import libSerialization
from omtk.libs import libComponent

import pymel.core as pymel

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets


def create_offset_grp(obj, suffix='offset'):
    offset = pymel.createNode('transform', name=(obj.name() + '_' + suffix))
    offset.setMatrix(obj.getMatrix(worldSpace=True), worldSpace=True)
    offset.setParent(obj.getParent())
    obj.setParent(offset)
    return offset


# Step 1: Create the network
# w = ComponentWizard()
# 
# # Step 2: Expose the ctrls
# for obj in pymel.selected():
#     w.expose_ctrl(obj)
# 
# # Step 3: Export the influences
# for obj in pymel.selected():
#     w.expose_infl(obj)



class WidgetCreateComponent(QtWidgets.QMainWindow):
    def __init__(self):
        super(WidgetCreateComponent, self).__init__()

        self.ui = widget_create_component.Ui_MainWindow()
        self.ui.setupUi(self)

        self._wizard_network = None
        self._wizard = None
        wizard = self.import_()
        if not wizard:
            wizard = libComponent.ComponentWizard()
        self.set_wizard(wizard)

        self.export()

        self.ui.widget_view_ctrl.onNetworkChanged.connect(self.on_network_changed)
        self.ui.widget_view_infl.onNetworkChanged.connect(self.on_network_changed)
        self.ui.widget_view_guid.onNetworkChanged.connect(self.on_network_changed)

    def set_wizard(self, wizard):
        # type: (libComponent.ComponentWizard) -> None
        assert (isinstance(wizard, libComponent.ComponentWizard))
        self._wizard = wizard
        self.ui.widget_view_ctrl.set_entries(wizard, libComponent.ComponentPartCtrl, wizard.parts_ctrl)
        self.ui.widget_view_infl.set_entries(wizard, libComponent.ComponentPartInfluence, wizard.parts_influences)
        self.ui.widget_view_guid.set_entries(wizard, libComponent.ComponentPartGuide, wizard.parts_guides)

    def reset(self):
        self.model_ctrl.reset()
        self.model_guid.reset()
        self.model_infl.reset()

    def on_network_changed(self):
        self.export()

    def import_(self):
        networks = libSerialization.get_networks_from_class(libComponent.ComponentWizard.__name__)
        if not networks:
            return
        network = networks[0]
        self._wizard_network = network
        wizard = libSerialization.import_network(network)
        return wizard

    def export(self):
        if self._wizard_network:
            pymel.delete(self._wizard_network)
        self._wizard_network = libSerialization.export_network(self._wizard)


_gui = None


def show():
    global _gui
    _gui = WidgetCreateComponent()
    _gui.show()
