"""
Logic for the "WidgetListModules" class
"""
# TODO: Convert to a QStandardItemModel/QSortProxyModel combination
import functools
import inspect
import itertools
import logging
import re

import pymel.core as pymel

from omtk.core import constants
from omtk.core.module import Module
from omtk.core.rig import Rig
from omtk.core.exceptions import ValidationError
from omtk.libs import libQt
from omtk.widgets import _utils
from omtk.widgets.ui import widget_list_modules
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

_LOG = logging.getLogger("omtk")

_COLOR_INVALID = QtGui.QBrush(QtGui.QColor(255, 45, 45))
_COLOR_VALID = QtGui.QBrush(QtGui.QColor(45, 45, 45))
_COLOR_LOCKED = QtGui.QBrush(QtGui.QColor(125, 125, 125))
_COLOR_WARNING = QtGui.QBrush(QtGui.QColor(125, 125, 45))


class WidgetListModules(QtWidgets.QWidget):
    """
    A widget that list scene modules.
    """

    needExportNetwork = QtCore.Signal()
    needImportNetwork = QtCore.Signal()
    deletedRig = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(WidgetListModules, self).__init__(parent=parent)

        self._rig = None
        self._rigs = []
        self._is_modifying = False  # todo: document
        self._listen_events = True

        self.ui = widget_list_modules.Ui_Form()
        self.ui.setupUi(self)

        # Tweak gui
        self.ui.treeWidget.setStyleSheet(_utils.STYLE_SHEET)

        # Connect events
        self.ui.lineEdit_search.textChanged.connect(self.on_module_query_changed)
        self.ui.treeWidget.itemSelectionChanged.connect(
            self._on_module_selection_changed
        )
        self.ui.treeWidget.itemChanged.connect(self._on_module_changed)
        self.ui.treeWidget.itemDoubleClicked.connect(self._on_module_double_clicked)
        self.ui.treeWidget.focusInEvent = self._focus_in_module
        self.ui.treeWidget.customContextMenuRequested.connect(
            self._on_context_menu_request
        )
        self.ui.btn_update.pressed.connect(self.update)

    def set_rigs(self, rigs):
        """
        Set the displayed rigs

        :param rigs: The rigs to display
        :type rigs: omtk.core.Rig
        """
        self._rigs = rigs
        self._rig = next(iter(self._rigs), None)
        self.update()

    def get_selected_items(self):  # type: () -> List[QtWidgets.QTreeWidgetItem]
        return self.ui.treeWidget.selectedItems()

    def get_selected_networks(self):
        """
        Get the libSerialization networks for each selected modules.

        :return: The network objects
        :rtype list[pymel.nodetypes.Network]
        """
        return [item.net for item in self.get_selected_items() if hasattr(item, "net")]

    def get_selected_entries(self):
        """
        Return the metadata stored in each selected row.
        Whatever the metadata type (can be Rig or Module).

        :return: A list of object instances.
        :rtype: omtk.core.base.Buildable
        """
        return [item.metadata_data for item in self.get_selected_items()]

    def get_selected_modules(self):
        """
        Return the Module instances stored in each selected rows.

        :return: A list of Module instances.
        :rtype: list[omtk.core.module.Module]
        """
        return [
            item.metadata_data
            for item in self.get_selected_items()
            if item.metadata_type == _utils.MetadataType.Module
        ]

    def get_selected_rigs(self):
        """
        Return the Rig instances stored in each selected rows.

        :return: A list of Rig instances.
        :rtype: list[omtk.core.rig.Rig]
        """
        return [
            item.metadata_data
            for item in self.get_selected_items()
            if item.metadata_type == _utils.MetadataType.Rig
        ]

    def update(self):
        """
        Update the view items.
        """
        self.ui.treeWidget.clear()
        if not self._rigs:
            return

        for root in self._rigs:
            item = self._get_qtreewidgetitem(root)
            self.ui.treeWidget.addTopLevelItem(item)
            self.ui.treeWidget.expandItem(item)
        self._refresh_ui_modules_checked()
        self._refresh_ui_modules_visibility()

    def _refresh_ui_modules_checked(self):
        # Block the signal to make sure that the itemChanged event
        # is not called when adjusting the check state
        self.ui.treeWidget.blockSignals(True)
        for qt_item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            if hasattr(qt_item, "rig"):
                qt_item.setCheckState(
                    0,
                    QtCore.Qt.Checked
                    if qt_item.rig.is_built()
                    else QtCore.Qt.Unchecked,
                )
        self.ui.treeWidget.blockSignals(False)

    def _refresh_ui_modules_visibility(self, query_regex=None):
        # TODO: Replace with QSortFilterProxyModel
        if query_regex is None:
            query_raw = self.ui.lineEdit_search.text()
            query_regex = ".*%s.*" % query_raw if query_raw else ".*"

        def fn_can_show(item, query_regex):
            """
            :param item: The item to filter
            :type item: QtWidgets.QTreeWidgetItem
            :param str query_regex: The search regex
            :return: Can we show the regex?
            :rtype: bool
            """
            # Always shows non-module
            if not item.metadata_type == _utils.MetadataType.Module:
                return True

            module = item.metadata_data  # Retrieve monkey-patched data
            module_name = str(module)

            return not query_regex or re.match(query_regex, module_name, re.IGNORECASE)

        for qt_item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            can_show = fn_can_show(qt_item, query_regex)
            qt_item.setHidden(not can_show)

    # Block signals need to be called in a function because
    # if called in a signal, it will block it
    def _set_text_block(self, item, value):
        self.ui.treeWidget.blockSignals(True)
        if hasattr(item, "rig"):
            item.setText(0, value)
        self.ui.treeWidget.blockSignals(False)

    def _build_module(self, module):
        if module.locked:
            pymel.warning("Can't build locked module %s" % module)
            return

        self._rig.build([module])

        return True

    def _unbuild_module(self, module):
        if module.locked:
            pymel.warning("Can't unbuild locked module %s" % module)
            return

        module.unbuild()

        return True

    def _build(self, val, update=True):
        if val.is_built():
            pymel.warning("Can't build %s, already built." % val)
            return

        if isinstance(val, Module):
            self._build_module(val)
        elif isinstance(val, Rig):
            val.build()
        else:
            raise Exception("Unexpected datatype %s for %s" % (type(val), val))

        if update:
            self.update()

    def _unbuild(self, val, update=True):
        if not val.is_built():
            pymel.warning("Can't unbuild %s, already unbuilt." % val)
            return

        if isinstance(val, Module):
            self._unbuild_module(val)
        elif isinstance(val, Rig):
            val.unbuild()
        else:
            raise Exception("Unexpected datatype %s for %s" % (type(val), val))

        if update:
            self.update()

    def _update_qitem_module(self, item, module):
        label = str(module)

        # Add inputs namespace if any for clarity.
        module_namespace = module.get_inputs_namespace()
        if module_namespace:
            label = "%s:%s" % (module_namespace.strip(":"), label)

        if module.locked:
            item.setBackground(0, self._color_locked)
            label += " (locked)"

        else:
            # Set QTreeWidgetItem red if the module fail validation
            try:
                module.validate()
            except ValidationError as error:
                desired_color = _COLOR_INVALID
                msg = "Validation failed for %s: %s" % (module, error)
                _LOG.warning(msg)
                item.setToolTip(0, msg)
                item.setBackground(0, desired_color)

        item.setText(0, label)
        item._name = item.text(0)
        item._checked = module.is_built()

        flags = item.flags() | QtCore.Qt.ItemIsEditable
        item.setFlags(flags)
        item.setCheckState(
            0, QtCore.Qt.Checked if module.is_built() else QtCore.Qt.Unchecked
        )
        item.metadata_data = module
        item.metadata_type = _utils.MetadataType.Module

    def _update_qitem_rig(self, item, rig):
        label = str(rig)

        item.setText(0, label)
        item._name = item.text(0)
        item._checked = rig.is_built()

        flags = item.flags() | QtCore.Qt.ItemIsEditable
        item.setFlags(flags)
        item.setCheckState(
            0, QtCore.Qt.Checked if rig.is_built() else QtCore.Qt.Unchecked
        )

        item.metadata_type = _utils.MetadataType.Rig
        item.metadata_data = rig
        item.setIcon(0, QtGui.QIcon(":/out_character.png"))

    def _get_qtreewidgetitem(self, value):
        widget = QtWidgets.QTreeWidgetItem(0)
        if hasattr(value, "_network"):
            widget.net = value._network
        else:
            pymel.warning("%s have no _network attributes" % value)

        if isinstance(value, Module):
            self._update_qitem_module(widget, value)
        elif isinstance(value, Rig):
            self._update_qitem_rig(widget, value)
        self._rig_to_qtreewidgetitem(value, widget)

        return widget

    def _rig_to_qtreewidgetitem(self, rig, parent):
        """
        Convert a Rig object to a QTreeWidgetItem

        :param omtk.Rig rig: A module object
        :param parent: A QTreeWidgetItem object
        """
        known = set()
        sorted_modules = sorted(rig.children, key=lambda mod: mod.name)
        for module in sorted_modules:
            self._module_to_qtreewidget(module, parent, known)

    def _module_to_qtreewidget(self, module, parent, known):
        """
        Convert a Module object to a QTreeWidgetItem

        :param omtk.Module module: A module object
        :param parent: A QTreeWidgetItem
        :type parent: omtk.vendor.QtWidgets.QTreeWidgetItem
        """
        # Cyclic loop filter
        if module in known:
            return
        known.add(module)

        widget = self._get_qtreewidgetitem(module)
        widget.setIcon(0, QtGui.QIcon(":/out_objectSet.png"))

        # List inputs
        inputs = module.input
        if inputs:
            for input_ in inputs:
                item = QtWidgets.QTreeWidgetItem(0)
                item.setText(0, input_.name())
                item.metadata_type = _utils.MetadataType.Influence
                item.metadata_data = input_
                _utils.set_icon_from_type(input_, item)
                widget.addChild(item)
        parent.addChild(widget)

        # List sub modules
        # for submodule in module.iter_children():
        #     self._module_to_qtreewidget(submodule, widget, known)

    #
    # Events
    #
    def _on_build_selected(self):
        for val in self.get_selected_modules():
            self._build(val)
        _utils.update_network(self._rig)
        self.update()

    def _on_unbuild_selected(self):
        for qItem in self.ui.treeWidget.selectedItems():
            val = qItem.metadata_data
            self._unbuild(val)
            _utils.update_network(self._rig)
        self.update()

    def _on_rebuild_selected(self):
        for qItem in self.ui.treeWidget.selectedItems():
            val = qItem.metadata_data
            self._unbuild(val)
            self._build(val)
            _utils.update_network(self._rig)

    def _on_module_selection_changed(self):
        """
        Called when the module selection change.
        """
        # Filter deleted networks
        networks = [net for net in self.get_selected_networks() if net and net.exists()]
        pymel.select(networks)

    def _on_module_changed(self, item):
        """
        Called when an module item checked state change.

        :param item: The modified item
        :type item: QtWidgets.QTreeWidgetItem
        """
        if not self._listen_events:
            return

        # todo: handle exception
        # Check first if the checkbox have changed
        new_state = item.checkState(0) == QtCore.Qt.Checked
        new_text = item.text(0)
        module = item.metadata_data
        if item._checked != new_state:
            item._checked = new_state
            # Handle checkbox change
            if new_state:
                self._build(
                    module, update=False
                )  # note: setting update=True on maya-2017 can cause Qt to crash...
            else:
                self._unbuild(
                    module, update=False
                )  # note: setting update=True on maya-2017 can cause Qt to crash...
            _utils.update_network(self._rig, item=item)

        # Check if the name have changed
        if item._name != new_text:
            item._name = new_text
            module.name = new_text

            # Update directly the network value instead of re-exporting it
            if hasattr(item, "net"):
                name_attr = item.net.attr("name")
                name_attr.set(new_text)

    def on_module_query_changed(self, _):
        """
        Called when the module query text changed.

        :param str _: The query text
        """
        self._refresh_ui_modules_visibility()

    def _on_context_menu_request(self):
        """
        Called when the user right-click on the module view.
        """
        if self.ui.treeWidget.selectedItems():
            sel = self.ui.treeWidget.selectedItems()
            try:
                inst = sel[0].metadata_data
            except AttributeError:  # influence don't have a 'rig' attr
                return

            menu = QtWidgets.QMenu()
            action_build = menu.addAction("Build")
            action_build.triggered.connect(self._on_build_selected)
            action_unbuild = menu.addAction("Unbuild")
            action_unbuild.triggered.connect(self._on_unbuild_selected)
            action_rebuild = menu.addAction("Rebuild")
            action_rebuild.triggered.connect(self._on_rebuild_selected)
            menu.addSeparator()
            action_lock = menu.addAction("Lock")
            action_lock.triggered.connect(self._on_lock_selected)
            action_unlock = menu.addAction("Unlock")
            action_unlock.triggered.connect(self._on_unlock_selected)
            menu.addSeparator()
            if len(sel) == 1:
                action_rename = menu.addAction("Rename")
                action_rename.triggered.connect(
                    functools.partial(
                        self.ui.treeWidget.itemDoubleClicked.emit, sel[0], 0
                    )
                )
            action_remove = menu.addAction("Remove")
            action_remove.triggered.connect(functools.partial(self.on_remove))

            # Expose decorated functions

            def is_exposed(val):
                if not hasattr(val, "__can_show__"):
                    return False
                func = getattr(val, "__can_show__")
                if not func:
                    return False
                return val.__can_show__()

            functions = inspect.getmembers(inst, is_exposed)

            if functions:
                menu.addSeparator()
                for fn_name, _ in functions:
                    fn_nicename = fn_name.replace("_", " ").title()

                    func = functools.partial(self._execute_rcmenu_entry, fn_name)
                    action = menu.addAction(fn_nicename)
                    action.triggered.connect(func)

            menu.exec_(QtGui.QCursor.pos())

    def _execute_rcmenu_entry(self, fn_name):
        need_export_network = False
        for module in itertools.chain(
            self.get_selected_modules() + self.get_selected_rigs()
        ):
            # Resolve fn
            if not hasattr(module, fn_name):
                continue

            func = getattr(module, fn_name)
            if not inspect.ismethod(func):
                continue

            # Call fn
            _LOG.debug("Calling %s on %s", fn_name, module)
            func()
            if constants.UIExposeFlags.trigger_network_export in func._flags:
                need_export_network = True

        if need_export_network:
            self.needExportNetwork.emit()

    def _on_module_double_clicked(self, item):
        """
        Called when a module is double clicked.

        :param item: The active module
        :type item: QtWidgets.QTreeWidgetItem
        """
        if hasattr(item, "rig"):
            self._set_text_block(item, item.metadata_data.name)
            # Flag to know that we are currently modifying the name
            self._is_modifying = True
            self.ui.treeWidget.editItem(item, 0)

    def _focus_in_module(self, event):
        """
        :param event: The focus event
        :type event: QtGui.QFocusEvent
        """
        # Set back the text with the information about the module in it
        if self._is_modifying:
            sel = self.ui.treeWidget.selectedItems()
            if sel:
                self._listen_events = False
                selected_item = sel[0]
                if isinstance(selected_item.metadata_data, Module):
                    self._update_qitem_module(
                        selected_item, selected_item.metadata_data
                    )
                self._listen_events = True
            self._is_modifying = False
        self.focusInEvent(event)

    def _on_lock_selected(self):
        """
        Lock selected modules.
        """
        modules = [
            module for module in self.get_selected_modules() if not module.locked
        ]
        if not modules:
            return

        for module in modules:
            module.locked = True

        _utils.update_network(self._rig)
        self.update()

    def _on_unlock_selected(self):
        """
        Unlock selected modules.
        """
        modules = [module for module in self.get_selected_modules() if module.locked]
        if not modules:
            return

        for module in modules:
            module.locked = False

        _utils.update_network(self._rig)
        self.update()

    def on_remove(self):
        """
        Remove any selected modules and rigs.
        Removing module need the rig to be re-exported.
        """

        selected_rigs = self.get_selected_rigs()
        selected_modules = [
            module
            for module in self.get_selected_modules()
            if module.rig not in selected_rigs
        ]
        need_reexport = False

        # Remove all selected rigs second
        for rig in selected_rigs:
            if rig.is_built():
                rig.unbuild()

            # Manually delete network
            network = rig._network
            if network and network.exists():
                pymel.delete(network)

            self.deletedRig.emit(rig)

        # Remove all selected modules
        for module in selected_modules:
            if module.is_built():
                module.unbuild()
            module.rig.remove_module(module)
            need_reexport = True

        if need_reexport:
            self.needExportNetwork.emit()
