import itertools
import os
import uuid
from collections import OrderedDict

import pymel.core as pymel
from omtk.core import classComponent
from omtk.libs import libComponents
from omtk.libs import libPython
from omtk.qt_widgets.ui.form_create_component import Ui_MainWindow as ui_def
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets


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


class CreateComponentForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CreateComponentForm, self).__init__(parent=parent)
        self.ui = ui_def()
        self.ui.setupUi(self)

        # Connect models
        self._model_attr_inn = AttributeMapModel()
        self._model_attr_out = AttributeMapModel()
        proxy_model_inn = QtCore.QSortFilterProxyModel()
        proxy_model_inn.setSourceModel(self._model_attr_inn)
        proxy_model_out = QtCore.QSortFilterProxyModel()
        proxy_model_out.setSourceModel(self._model_attr_out)
        self.ui.tableView_attrs_inn.setModel(proxy_model_inn)
        self.ui.tableView_attrs_out.setModel(proxy_model_out)

        # Connect events
        self.ui.pushButton_resolve.pressed.connect(self.on_user_resolve_input)
        self.ui.pushButton_submit.pressed.connect(self.on_user_submit)
        self.ui.lineEdit_id.textChanged.connect(self.update_enabled)
        self.ui.lineEdit_author.textChanged.connect(self.update_enabled)
        self.ui.lineEdit_name.textChanged.connect(self.update_enabled)

        # Resolve on opening
        self.on_user_resolve_input()

        self.ui.lineEdit_id.setText(str(uuid.uuid4()))

        self.update_enabled()

    def update_enabled(self):
        self.ui.pushButton_submit.setEnabled(
            bool(self._model_attr_inn.get_entries()) &
            bool(self._model_attr_out.get_entries()) &
            bool(self.ui.lineEdit_author.text()) &
            bool(self.ui.lineEdit_id.text()) &
            bool(self.ui.lineEdit_name.text())
        )

    def on_user_resolve_input(self):
        sel = pymel.selected()
        input_attrs, output_attrs = libComponents.identify_network_io_ports(sel)
        self._model_attr_inn.set_entries(input_attrs)
        self._model_attr_out.set_entries(output_attrs)

        self.update_enabled()

    def on_user_submit(self):
        uid = self.ui.lineEdit_id.text()
        name = self.ui.lineEdit_name.text()
        author = self.ui.lineEdit_author.text()
        version = self.ui.lineEdit_version.text()

        # Resolve output file
        dir = libComponents.get_component_dir()
        path_out = os.path.join(dir, '{0}.ma'.format(name))

        # Prevent any collisions
        # if os.path.exists(path_out):
        #     raise Exception("Cannot save component over already existing component!")

        # Create component
        input_attrs = self._model_attr_inn.get_entries()
        output_attrs = self._model_attr_out.get_entries()
        inst = classComponent.Component.from_attributes(input_attrs, output_attrs)

        # Create component definition
        # todo: maybe set data in component instance?
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
