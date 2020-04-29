import re
import functools
import inspect
import traceback
import logging
import itertools

import pymel.core as pymel
from omtk.widgets.ui import widget_list_modules

from omtk import constants
from omtk.widgets import ui_shared
from omtk.libs import libQt
from omtk.core import classModule
from omtk.core import classRig

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

log = logging.getLogger("omtk")


class CustomTreeWidget(QtWidgets.QTreeWidgetItem):
    pass


class WidgetListModules(QtWidgets.QWidget):
    needExportNetwork = QtCore.Signal()
    needImportNetwork = QtCore.Signal()
    deletedRig = QtCore.Signal(object)

    _color_invalid = QtGui.QBrush(QtGui.QColor(255, 45, 45))
    _color_valid = QtGui.QBrush(QtGui.QColor(45, 45, 45))
    _color_locked = QtGui.QBrush(QtGui.QColor(125, 125, 125))
    _color_warning = QtGui.QBrush(QtGui.QColor(125, 125, 45))

    def __init__(self, parent=None):
        super(WidgetListModules, self).__init__(parent=parent)

        self._rig = None
        self._rigs = []
        self._is_modifying = False  # todo: document
        self._listen_events = True

        self.ui = widget_list_modules.Ui_Form()
        self.ui.setupUi(self)

        # Tweak gui
        self.ui.treeWidget.setStyleSheet(ui_shared._STYLE_SHEET)

        # Connect signal

        # Connect events
        self.ui.lineEdit_search.textChanged.connect(self.on_module_query_changed)
        self.ui.treeWidget.itemSelectionChanged.connect(
            self.on_module_selection_changed
        )
        self.ui.treeWidget.itemChanged.connect(self.on_module_changed)
        self.ui.treeWidget.itemDoubleClicked.connect(self.on_module_double_clicked)
        self.ui.treeWidget.focusInEvent = self.focus_in_module
        self.ui.treeWidget.customContextMenuRequested.connect(
            self.on_context_menu_request
        )
        self.ui.btn_update.pressed.connect(self.update)

    def set_rigs(self, rig, update=True):
        self._rigs = rig
        self._rig = next(iter(self._rigs), None)
        if update:
            self.update()

    def get_selected_items(self):
        return self.ui.treeWidget.selectedItems()

    def get_selected_networks(self):
        return [item.net for item in self.get_selected_items() if hasattr(item, "net")]

    def get_selected_entries(self):
        """
        Return the metadata stored in each selected row. Whatever the metadata type (can be Rig or Module).
        :return: A list of object instances.
        """
        return [item.metadata_data for item in self.get_selected_items()]

    def get_selected_modules(self):
        """
        Return the Module instances stored in each selected rows.
        :return: A list of Module instances.
        """
        return [
            item.metadata_data
            for item in self.get_selected_items()
            if item.metadata_type == ui_shared.MetadataType.Module
        ]

    def get_selected_rigs(self):
        """
        Return the Rig instances stored in each selected rows.
        :return: A list of Rig instances.
        """
        return [
            item.metadata_data
            for item in self.get_selected_items()
            if item.metadata_type == ui_shared.MetadataType.Rig
        ]

    def update(self, *args, **kwargs):
        self.ui.treeWidget.clear()
        if not self._rigs:
            return

        for root in self._rigs:
            qItem = self._get_qtreewidgetitem(root)
            self.ui.treeWidget.addTopLevelItem(qItem)
            self.ui.treeWidget.expandItem(qItem)
        self.refresh_ui()

    def refresh_ui(self):
        self._refresh_ui_modules_checked()
        self._refresh_ui_modules_visibility()

    def _refresh_ui_modules_checked(self):
        # Block the signal to make sure that the itemChanged event is not called when adjusting the check state
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
        if query_regex is None:
            query_raw = self.ui.lineEdit_search.text()
            query_regex = ".*%s.*" % query_raw if query_raw else ".*"

        def fn_can_show(qItem, query_regex):
            # Always shows non-module
            if not qItem.metadata_type == ui_shared.MetadataType.Module:
                return True

            module = qItem.metadata_data  # Retrieve monkey-patched data
            module_name = str(module)

            return not query_regex or re.match(query_regex, module_name, re.IGNORECASE)

        for qt_item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            can_show = fn_can_show(qt_item, query_regex)
            qt_item.setHidden(not can_show)

    # Block signals need to be called in a function because if called in a signal, it will block it
    def _set_text_block(self, item, str):
        self.ui.treeWidget.blockSignals(True)
        if hasattr(item, "rig"):
            item.setText(0, str)
        self.ui.treeWidget.blockSignals(False)

    def _can_build(self, data, verbose=True):
        validate_message = None
        try:
            if isinstance(data, classRig.Rig):
                data.validate()
            elif isinstance(data, classModule.Module):
                data.validate()
            else:
                raise Exception("Unexpected datatype %s for %s" % (type(data), data))
        except Exception, e:
            if verbose:
                validate_message = str(e)
                pymel.warning("%s failed validation: %s" % (data, str(e)))
            return False, validate_message
        return True, validate_message

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

        try:
            if isinstance(val, classModule.Module):
                self._build_module(val)
            elif isinstance(val, classRig.Rig):
                val.build()
            else:
                raise Exception("Unexpected datatype %s for %s" % (type(val), val))
        except Exception, e:
            log.error(
                "Error building %s. Received %s. %s",
                val,
                type(e).__name__,
                str(e).strip(),
            )
            traceback.print_exc()

        if update:
            self.update()

    def _unbuild(self, val, update=True):
        if not val.is_built():
            pymel.warning("Can't unbuild %s, already unbuilt." % val)
            return

        try:
            if isinstance(val, classModule.Module):
                self._unbuild_module(val)
            elif isinstance(val, classRig.Rig):
                val.unbuild()
            else:
                raise Exception("Unexpected datatype %s for %s" % (type(val), val))
        except Exception, e:
            log.error(
                "Error building %s. Received %s. %s",
                val,
                type(e).__name__,
                str(e).strip(),
            )
            traceback.print_exc()

        if update:
            self.update()

    def _update_qitem_module(self, qitem, module):
        label = str(module)

        # Add inputs namespace if any for clarity.
        module_namespace = module.get_inputs_namespace()
        if module_namespace:
            label = "%s:%s" % (module_namespace.strip(":"), label)

        if module.locked:
            qitem.setBackground(0, self._color_locked)
            label += " (locked)"
        elif module.is_built():
            # Add a warning on outdated versions
            version_major, version_minor, version_patch = module.get_version()
            if (
                version_major is not None
                and version_minor is not None
                and version_patch is not None
            ):
                warning_msg = ""
                try:
                    module.validate_version(version_major, version_minor, version_patch)
                except Exception, e:
                    warning_msg = (
                        "v%s.%s.%s is known to have issues and need to be updated: %s"
                        % (version_major, version_minor, version_patch, str(e))
                    )

                if warning_msg:
                    desired_color = self._color_warning
                    qitem.setToolTip(0, warning_msg)
                    qitem.setBackground(0, desired_color)
                    label += " (problematic)"
                    module.warning(warning_msg)
        else:
            # Set QTreeWidgetItem red if the module fail validation
            can_build, validation_message = self._can_build(module, verbose=True)
            if not can_build:
                desired_color = self._color_invalid
                msg = "Validation failed for %s: %s" % (module, validation_message)
                log.warning(msg)
                qitem.setToolTip(0, msg)
                qitem.setBackground(0, desired_color)

        qitem.setText(0, label)
        qitem._name = qitem.text(0)
        qitem._checked = module.is_built()

        flags = qitem.flags() | QtCore.Qt.ItemIsEditable
        qitem.setFlags(flags)
        qitem.setCheckState(
            0, QtCore.Qt.Checked if module.is_built() else QtCore.Qt.Unchecked
        )
        qitem.metadata_data = module
        qitem.metadata_type = ui_shared.MetadataType.Module

    def _update_qitem_rig(self, qitem, rig):
        label = str(rig)

        qitem.setText(0, label)
        qitem._name = qitem.text(0)
        qitem._checked = rig.is_built()

        flags = qitem.flags() | QtCore.Qt.ItemIsEditable
        qitem.setFlags(flags)
        qitem.setCheckState(
            0, QtCore.Qt.Checked if rig.is_built() else QtCore.Qt.Unchecked
        )

        qitem.metadata_type = ui_shared.MetadataType.Rig
        qitem.metadata_data = rig
        qitem.setIcon(0, QtGui.QIcon(":/out_character.png"))

    def _get_qtreewidgetitem(self, value):
        widget = CustomTreeWidget(0)
        if hasattr(value, "_network"):
            widget.net = value._network
        else:
            pymel.warning("%s have no _network attributes" % value)

        if isinstance(value, classModule.Module):
            self._update_qitem_module(widget, value)
        elif isinstance(value, classRig.Rig):
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
        sorted_modules = sorted(rig, key=lambda mod: mod.name)
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
            for input in inputs:
                qInputItem = CustomTreeWidget(0)
                qInputItem.setText(0, input.name())
                qInputItem.metadata_type = (
                    ui_shared.MetadataType.Influence
                )  # todo: support mesh metadata?
                qInputItem.metadata_data = input
                ui_shared.set_icon_from_type(input, qInputItem)
                widget.addChild(qInputItem)
        parent.addChild(widget)

        # List sub modules
        for attrname in dir(module):
            if attrname.startswith("_"):  # ignore private attr
                continue

            attr = getattr(module, attrname)

            if isinstance(attr, (tuple, list, set)):
                for subattr in attr:
                    if isinstance(subattr, classModule.Module):
                        self._module_to_qtreewidget(subattr, widget, known)

            if isinstance(attr, classModule.Module):
                self._module_to_qtreewidget(attr, widget, known)

    #
    # Events
    #
    def on_build_selected(self):
        for val in self.get_selected_modules():
            self._build(val)
        ui_shared._update_network(self._rig)
        self.update()

    def on_unbuild_selected(self):
        for qItem in self.ui.treeWidget.selectedItems():
            val = qItem.metadata_data
            self._unbuild(val)
            ui_shared._update_network(self._rig)
        self.update()

    def on_rebuild_selected(self):
        for qItem in self.ui.treeWidget.selectedItems():
            val = qItem.metadata_data
            self._unbuild(val)
            self._build(val)
            ui_shared._update_network(self._rig)

    def on_module_selection_changed(self):
        # Filter deleted networks
        networks = [net for net in self.get_selected_networks() if net and net.exists()]
        pymel.select(networks)

    def on_module_changed(self, item):
        if not self._listen_events:
            return

        # todo: handle exception
        # Check first if the checkbox have changed
        need_update = False
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
            ui_shared._update_network(self._rig, item=item)

        # Check if the name have changed
        if item._name != new_text:
            item._name = new_text
            module.name = new_text

            # Update directly the network value instead of re-exporting it
            if hasattr(item, "net"):
                name_attr = item.net.attr("name")
                name_attr.set(new_text)

    def on_module_query_changed(self, *args, **kwargs):
        self._refresh_ui_modules_visibility()

    def on_context_menu_request(self):
        if self.ui.treeWidget.selectedItems():
            sel = self.ui.treeWidget.selectedItems()
            try:
                inst = sel[0].metadata_data
            except AttributeError:  # influence don't have a 'rig' attr
                return

            menu = QtWidgets.QMenu()
            actionBuild = menu.addAction("Build")
            actionBuild.triggered.connect(self.on_build_selected)
            actionUnbuild = menu.addAction("Unbuild")
            actionUnbuild.triggered.connect(self.on_unbuild_selected)
            actionRebuild = menu.addAction("Rebuild")
            actionRebuild.triggered.connect(self.on_rebuild_selected)
            menu.addSeparator()
            actionLock = menu.addAction("Lock")
            actionLock.triggered.connect(self.on_lock_selected)
            action_unlock = menu.addAction("Unlock")
            action_unlock.triggered.connect(self.on_unlock_selected)
            menu.addSeparator()
            if len(sel) == 1:
                actionRemove = menu.addAction("Rename")
                # actionRemove.triggered.connect(functools.partial(self.ui.treeWidget.editItem, sel[0], 0))
                actionRemove.triggered.connect(
                    functools.partial(
                        self.ui.treeWidget.itemDoubleClicked.emit, sel[0], 0
                    )
                )
            actionRemove = menu.addAction("Remove")
            actionRemove.triggered.connect(functools.partial(self.on_remove))

            # Expose decorated functions

            def is_exposed(val):
                if not hasattr(val, "__can_show__"):
                    return False
                fn = getattr(val, "__can_show__")
                if fn is None:
                    return False
                # if not inspect.ismethod(fn):
                #    return False
                return val.__can_show__()

            functions = inspect.getmembers(inst, is_exposed)

            if functions:
                menu.addSeparator()
                for fn_name, fn in functions:
                    fn_nicename = fn_name.replace("_", " ").title()

                    fn = functools.partial(self._execute_rcmenu_entry, fn_name)
                    action = menu.addAction(fn_nicename)
                    action.triggered.connect(fn)

            menu.exec_(QtGui.QCursor.pos())

    def _execute_rcmenu_entry(self, fn_name):
        need_export_network = False
        for module in itertools.chain(
            self.get_selected_modules() + self.get_selected_rigs()
        ):
            # Resolve fn
            if not hasattr(module, fn_name):
                continue

            fn = getattr(module, fn_name)
            if not inspect.ismethod(fn):
                continue

            # Call fn
            log.debug("Calling %s on %s", fn_name, module)
            fn()
            if constants.UIExposeFlags.trigger_network_export in fn._flags:
                need_export_network = True

        if need_export_network:
            self.needExportNetwork.emit()

    def on_module_double_clicked(self, item):
        if hasattr(item, "rig"):
            self._set_text_block(item, item.metadata_data.name)
            self._is_modifying = (
                True  # Flag to know that we are currently modifying the name
            )
            self.ui.treeWidget.editItem(item, 0)

    def focus_in_module(self, event):
        # Set back the text with the information about the module in it
        if self._is_modifying:
            sel = self.ui.treeWidget.selectedItems()
            if sel:
                self._listen_events = False
                selected_item = sel[0]
                if isinstance(selected_item.metadata_data, classModule.Module):
                    self._update_qitem_module(
                        selected_item, selected_item.metadata_data
                    )
                self._listen_events = True
            self._is_modifying = False
        self.focusInEvent(event)

    def on_lock_selected(self):
        need_update = False
        for item in self.ui.treeWidget.selectedItems():
            val = item.metadata_data
            if isinstance(val, classModule.Module) and not val.locked:
                need_update = True
                val.locked = True
        if need_update:
            ui_shared._update_network(self._rig)
            self.update()

    def on_unlock_selected(self):
        need_update = False
        for item in self.ui.treeWidget.selectedItems():
            val = item.metadata_data
            if isinstance(val, classModule.Module) and val.locked:
                need_update = True
                val.locked = False
        if need_update:
            ui_shared._update_network(self._rig)
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
            try:
                if rig.is_built():
                    rig.unbuild()

                # Manually delete network
                network = rig._network
                if network and network.exists():
                    pymel.delete(network)

                self.deletedRig.emit(rig)

            except Exception, e:
                log.error(
                    "Error removing %s. Received %s. %s",
                    rig,
                    type(e).__name__,
                    str(e).strip(),
                )
                traceback.print_exc()

        # Remove all selected modules
        for module in selected_modules:
            try:
                if module.is_built():
                    module.unbuild()
                module.rig.remove_module(module)
                need_reexport = True
            except Exception, e:
                log.error(
                    "Error removing %s. Received %s. %s",
                    module,
                    type(e).__name__,
                    str(e).strip(),
                )
                traceback.print_exc()

        if need_reexport:
            self.needExportNetwork.emit()
