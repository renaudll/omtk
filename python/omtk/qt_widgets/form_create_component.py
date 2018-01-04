import itertools
import os
import uuid
from collections import OrderedDict

import pymel.core as pymel
from omtk.core import component
from omtk.libs import libComponents
from omtk.libs import libComponent
from omtk.libs import libPython
from omtk.qt_widgets.ui.form_create_component import Ui_MainWindow as ui_def
from omtk.qt_widgets import main_window_extended
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets
from omtk.vendor import libSerialization

import logging

log_parent = logging.getLogger('omtk')
log = log_parent.getChild('create_component')


class AttributeMapModel(QtCore.QAbstractTableModel):
    def __init__(self, entries=None):
        super(AttributeMapModel, self).__init__()
        self._entries = [] if entries is None else entries

    def reset(self):
        """Backport of Qt4"""
        self.beginResetModel()
        self.endResetModel()

    def get_entries(self):
        return [v for k, v in self._entries]

    def set_entries(self, entries):
        self._entries = list(entries)
        self.reset()  # todo: fix for PySide2

        # todo: cleanup, ugly code

        self._map = OrderedDict()

        def _resolve1(attr):
            return attr.longName()

        def _resolve2(attr):
            return '{}{}'.format(attr.node().name(), attr.longName())

        all_attrs_names = set(_resolve1(attr) for attr in entries)
        all_attrs_nodenames = set()

        for attr in entries:
            # Always try to use the attribute name first
            guess = _resolve1(attr)
            if not guess in all_attrs_names:
                self._map[guess] = attr
                continue

            # Otherwise try to use the node name in the name
            guess = _resolve2(attr)
            if not guess in all_attrs_nodenames:
                self._map[guess] = attr
                all_attrs_nodenames.add(guess)
                continue

            # Otherwise, loop!
            for i in itertools.count():
                guess2 = guess + str(i)
                if guess2 not in self._map:
                    self._map[guess2] = attr
                    break

        self._entries = self._map.items()

    def rowCount(self, index):
        return len(self._entries)

    def columnCount(self, index):
        return 3  # Choosed Name, Attribute DagPath

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section == 0:
                return 'Name'
            if section == 1:
                return 'Node'
            if section == 2:
                return 'Attribute'

    _optimizable_attributes = (
        'translate', 'translateX', 'translateY', 'translateZ',
        'rotate', 'rotateX', 'rotateY', 'rotateZ',
        'scale', 'scaleX', 'scaleY', 'scaleZ',
        'rotatePivot', 'scalePivot', 'rotateOrder'
    )

    def data(self, index, role):
        row = index.row()
        col = index.column()
        if role == QtCore.Qt.DisplayRole:
            if col == 0:
                return self._entries[row][0]
            if col == 1:
                return self._entries[row][1].node().name()
            if col == 2:
                return self._entries[row][1].longName()
        if role == QtCore.Qt.BackgroundRole:
            if self._entries[row][1].longName() in self._optimizable_attributes:
                return QtGui.QColor(128, 128, 0)


class CreateComponentForm(main_window_extended.MainWindowExtended):
    def __init__(self):
        super(CreateComponentForm, self).__init__()
        self.ui = ui_def()
        self.ui.setupUi(self)

        # Initialize cache
        self._components = self.get_scene_components()
        self._component = next(iter(self._components), None)

        # Connect models
        # self._model_attr_inn = AttributeMapModel()
        # self._model_attr_out = AttributeMapModel()

        self._wizard_network = None
        self._wizard = None
        wizard, wizard_network = self.import_()
        if not wizard:
            wizard = libComponent.ComponentWizard()
            wizard.initialize()

        self.set_wizard(wizard, wizard_network)

        self.export()

        self.ui.widget_view_ctrl.onNetworkChanged.connect(self.on_network_changed)
        self.ui.widget_view_infl.onNetworkChanged.connect(self.on_network_changed)
        self.ui.widget_view_guid.onNetworkChanged.connect(self.on_network_changed)

        # Connect events
        self.ui.pushButton_submit.pressed.connect(self.on_user_submit)
        self.ui.lineEdit_id.textChanged.connect(self.update_enabled)
        self.ui.lineEdit_author.textChanged.connect(self.update_enabled)
        self.ui.lineEdit_name.textChanged.connect(self.update_enabled)
        self.ui.lineEdit_version.textChanged.connect(self.update_enabled)
        self.ui.pushButton_select.pressed.connect(self.on_select)
        self.ui.pushButton_create.pressed.connect(self.on_create_new)

        self.ui.lineEdit_id.setText(str(uuid.uuid4()))

        self.update_component_list()
        self.update_enabled()

        # Hack: Ensure events are connected on the new statusBar
        self.set_logger(log)

    # --- new ---

    def set_wizard(self, wizard, wizard_network=None):
        # type: (libComponent.ComponentWizard) -> None
        assert (isinstance(wizard, libComponent.ComponentWizard))
        self._wizard = wizard
        self._wizard_network = wizard_network
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
            return None, None
        network = networks[0]
        wizard = libSerialization.import_network(network)
        return wizard, network

    def export(self):
        if self._wizard_network:
            pymel.delete(self._wizard_network)
        self._wizard_network = libSerialization.export_network(self._wizard)

    # --- legacy ---

    def update_component_list(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems([str(c) for c in self._components])
        if self._component:
            try:
                index = self._components.index(self._component)
                self.ui.comboBox.setCurrentIndex(index)
            except ValueError:
                pass

    def iter_scene_components(self):
        for network in libSerialization.iter_networks_from_class(component.Component.__name__):
            inst = libSerialization.import_network(network)
            if inst:
                yield inst

    def get_scene_components(self):
        return list(self.iter_scene_components())

    def update_enabled(self):
        have_component = bool(self._component)
        have_name = bool(self.ui.lineEdit_name.text())
        have_author = bool(self.ui.lineEdit_author.text())
        have_version = bool(self.ui.lineEdit_version.text())
        have_uid = bool(self.ui.lineEdit_id.text())
        self.ui.lineEdit_name.setEnabled(have_component)
        self.ui.lineEdit_author.setEnabled(have_component)
        self.ui.lineEdit_version.setEnabled(have_component)
        self.ui.lineEdit_id.setEnabled(have_component)
        self.ui.pushButton_select.setEnabled(have_component)
        self.ui.pushButton_submit.setEnabled(have_component and have_name and have_author and have_version and have_uid)
        self.ui.widget_view_ctrl.setEnabled(have_component)
        self.ui.widget_view_infl.setEnabled(have_component)
        self.ui.widget_view_guid.setEnabled(have_component)

    def on_create_new(self):
        inst = component.Component()
        inst.build_interface()
        self.component = inst
        self._components.append(inst)
        self.update_component_list()

    def on_select(self):
        grp_inn = self._component.grp_inn
        grp_out = self._component.grp_out
        grp_dag = self._component.grp_dag
        objs_to_select = []
        if grp_inn and grp_inn.exists():
            objs_to_select.append(grp_inn)
        if grp_out and grp_inn.exists():
            objs_to_select.append(grp_out)
        if grp_dag and grp_inn.exists():
            objs_to_select.append(grp_dag)
            objs_to_select.extend(
                pymel.listRelatives(grp_dag, allDescendents=True)
            )
        pymel.select(objs_to_select)

    def on_user_submit(self):
        uid = self.ui.lineEdit_id.text()
        name = self.ui.lineEdit_name.text()
        author = self.ui.lineEdit_author.text()
        version = self.ui.lineEdit_version.text()

        # Resolve output file
        dir = libComponents.get_component_dir()
        path_out = os.path.join(dir, '{0}.ma'.format(name))
        print("Exporting to {0}".format(path_out))

        # Prevent any collisions
        # if os.path.exists(path_out):
        #     raise Exception("Cannot save component over already existing component!")

        # Create component definition
        # todo: maybe set data in component instance?
        inst = self._component
        inst.uid = uid
        inst.name = name
        inst.author = author
        inst.version = version

        # Save component to file
        inst.export(path_out)


@libPython.memoized
def get():
    return CreateComponentForm()


def show():
    gui = get()
    gui.show()
