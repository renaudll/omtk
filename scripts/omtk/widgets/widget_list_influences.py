"""
Logic for WidgetListInfluences
"""
import re
import pymel.core as pymel
from omtk.widgets.ui import widget_list_influences

from omtk.libs import libQt
from omtk.libs import libPymel
from omtk.widgets import _utils
from omtk.vendor import libSerialization
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets


class WidgetListInfluences(QtWidgets.QWidget):
    """
    Qt Widget that list influences.
    """

    onRightClick = QtCore.Signal()

    def __init__(self, parent=None):
        super(WidgetListInfluences, self).__init__(parent=parent)

        self._rig = None

        self.ui = widget_list_influences.Ui_Form()
        self.ui.setupUi(self)

        # Tweak gui
        self.ui.treeWidget.setStyleSheet(_utils.STYLE_SHEET)

        # Connect signals
        self.ui.treeWidget.customContextMenuRequested.connect(self.onRightClick)

        # Connect events
        self.ui.treeWidget.itemSelectionChanged.connect(
            self.on_influence_selection_changed
        )
        self.ui.lineEdit_search.textChanged.connect(self.on_query_changed)
        self.ui.checkBox_hideAssigned.stateChanged.connect(self.on_query_changed)
        self.ui.btn_update.pressed.connect(self.update)

    def set_rig(self, rig, update=True):
        self._rig = rig
        if update:
            self.update()

    def update(self):
        self.ui.treeWidget.clear()

        if self._rig is None:
            return

        all_potential_influences = self._rig.get_potential_influences()

        if all_potential_influences:
            data = libPymel.get_tree_from_objs(all_potential_influences)

            self._fill_widget_influences(self.ui.treeWidget.invisibleRootItem(), data)
            self.ui.treeWidget.sortItems(0, QtCore.Qt.AscendingOrder)

        self.update_list_visibility()

    def _fill_widget_influences(self, qt_parent, data):
        obj = pymel.PyNode(data.val) if data.val else None
        if obj:
            obj_name = obj.name()

            def _is_module(network):
                return libSerialization.is_network_from_class(network, "Module")

            networks = libSerialization.get_connected_networks(
                obj, key=_is_module, recursive=False
            )

            brush = QtGui.QBrush(QtCore.Qt.white)

            if self._is_influence(obj):  # todo: listen to the Rig class
                item = QtWidgets.QTreeWidgetItem(0)
                item.obj = obj

                # Monkey-patch mesh QWidget
                item.metadata_type = _utils.MetadataType.Influence
                item.metadata_data = obj

                item.networks = networks
                item.setText(0, obj_name)
                item.setForeground(0, brush)
                _utils.set_icon_from_type(obj, item)
                item.setCheckState(
                    0, QtCore.Qt.Checked if networks else QtCore.Qt.Unchecked
                )
                if item.flags() & QtCore.Qt.ItemIsUserCheckable:
                    item.setFlags(item.flags() ^ QtCore.Qt.ItemIsUserCheckable)
                qt_parent.addChild(item)
                qt_parent = item

        for child_data in data.children:
            self._fill_widget_influences(qt_parent, child_data)

    def _is_influence(self, obj):
        """
        Supported influences are joints and nurbsSurface.

        :param obj: An object to check
        :type obj: pymel.PyNode
        :return: Is the object an influence?
        :rtype: bool
        """
        return libPymel.isinstance_of_transform(
            obj, pymel.nodetypes.Joint
        ) or libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)

    def update_list_visibility(self, query_regex=None):
        if query_regex is None:
            query_raw = self.ui.lineEdit_search.text()
            query_regex = ".*%s.*" % query_raw if query_raw else ".*"

        brush_selectable = QtGui.QBrush(QtCore.Qt.white)
        brush_unselectable = QtGui.QBrush(QtCore.Qt.darkGray)
        for item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            can_show = self._can_show_QTreeWidgetItem(item, query_regex)
            item.setHidden(not can_show)
            if can_show:
                item.setForeground(0, brush_selectable)
                flags = item.flags()
                if not flags & QtCore.Qt.ItemIsSelectable:  # Make selectable
                    flags ^= QtCore.Qt.ItemIsSelectable
                    item.setFlags(flags)
                self._show_parent_recursive(item.parent())
            else:
                item.setForeground(0, brush_unselectable)
                flags = item.flags()
                if flags & QtCore.Qt.ItemIsSelectable:  # Make selectable
                    flags ^= QtCore.Qt.ItemIsSelectable
                    item.setFlags(flags)

        self.ui.treeWidget.expandAll()

    def _can_show_QTreeWidgetItem(self, qItem, query_regex):
        obj = qItem.obj  # Retrieve monkey-patched data
        obj_name = obj.name()
        # print obj_name

        if not re.match(query_regex, obj_name, re.IGNORECASE):
            return False

        if self.ui.checkBox_hideAssigned.isChecked():
            if qItem.networks:
                return False

        return True

    def _show_parent_recursive(self, qt_parent_item):
        if qt_parent_item is not None:
            if qt_parent_item.isHidden:
                qt_parent_item.setHidden(False)
            self._show_parent_recursive(qt_parent_item.parent())

    def get_selection(self):
        result = []
        for item in self.ui.treeWidget.selectedItems():
            if item.obj.exists():
                result.append(item.obj)
        return result

    #
    # Events
    #

    def on_influence_selection_changed(self):
        pymel.select(self.get_selection())

    def on_query_changed(self):
        self.update_list_visibility()
