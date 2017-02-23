import re
import functools
import inspect
import traceback
import logging
import itertools

import pymel.core as pymel
from ui import widget_list_modules

from omtk import constants
from omtk import ui_shared
from omtk.libs import libQt
from omtk.core import classModule
from omtk.core import classRig

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

log = logging.getLogger('omtk')


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

        self.ui = widget_list_modules.Ui_Form()
        self.ui.setupUi(self)

        # Tweak gui
        self.ui.treeWidget.setStyleSheet(ui_shared._STYLE_SHEET)

        # Connect signal

        # Connect events
        self.ui.lineEdit_search.textChanged.connect(self.on_module_query_changed)
        self.ui.treeWidget.itemSelectionChanged.connect(self.on_module_selection_changed)
        self.ui.treeWidget.itemChanged.connect(self.on_module_changed)
        self.ui.treeWidget.itemDoubleClicked.connect(self.on_module_double_clicked)
        self.ui.treeWidget.focusInEvent = self.focus_in_module
        self.ui.treeWidget.customContextMenuRequested.connect(self.on_context_menu_request)
        self.ui.btn_update.pressed.connect(self.update)


    def set_rigs(self, rig, update=True):
        self._rigs = rig
        self._rig = next(iter(self._rigs), None)
        if update:
            self.update()

    def get_selected_items(self):
        return self.ui.treeWidget.selectedItems()

    def get_selected_networks(self):
        return [item.net for item in self.get_selected_items() if hasattr(item, 'net')]

    def get_selected_entries(self):
        """
        Return the metadata stored in each selected row. Whatever the metadata type (can be Rig or Module).
        :return: A list of object instances.
        """
        return [item.rig for item in self.get_selected_items()]

    def get_selected_modules(self):
        """
        Return the Module instances stored in each selected rows.
        :return: A list of Module instances.
        """
        return [item.rig for item in self.get_selected_items() if item._meta_type == ui_shared.MetadataType.Module]

    def get_selected_rigs(self):
        """
        Return the Rig instances stored in each selected rows.
        :return: A list of Rig instances.
        """
        return [item.rig for item in self.get_selected_items() if item._meta_type == ui_shared.MetadataType.Rig]

    def update(self, *args, **kwargs):
        self.ui.treeWidget.clear()
        if not self._rigs:
            return

        for root in self._rigs:
            qItem = self._rig_to_tree_widget(root)
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
                qt_item.setCheckState(0, QtCore.Qt.Checked if qt_item.rig.is_built() else QtCore.Qt.Unchecked)
        self.ui.treeWidget.blockSignals(False)

    def _refresh_ui_modules_visibility(self, query_regex=None):
        if query_regex is None:
            query_raw = self.ui.lineEdit_search.text()
            query_regex = ".*{0}.*".format(query_raw) if query_raw else ".*"

        def fn_can_show(qItem, query_regex):
            # Always shows non-module
            if not hasattr(qItem, 'rig'):
                return True
            if not isinstance(qItem.rig, classModule.Module):
                return True

            module = qItem.rig  # Retrieve monkey-patched data
            module_name = str(module)

            return not query_regex or re.match(query_regex, module_name, re.IGNORECASE)

        # unselectableBrush = QtGui.QBrush(QtCore.Qt.darkGray)
        # selectableBrush = QtGui.QBrush(QtCore.Qt.white)
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
                raise Exception("Unexpected datatype {0} for {1}".format(type(data), data))
        except Exception, e:
            if verbose:
                validate_message  = str(e)
                pymel.warning("{0} failed validation: {1}".format(data, str(e)))
            return False, validate_message
        return True, validate_message

    def _build_module(self, module):
        if module.locked:
            pymel.warning("Can't build locked module {0}".format(module))
            return

        self._rig.build([module])

        return True

    def _unbuild_module(self, module):
        if module.locked:
            pymel.warning("Can't unbuild locked module {0}".format(module))
            return

        module.unbuild()

        return True

    def _build(self, val, update=True):
        if val.is_built():
            pymel.warning("Can't build {0}, already built.".format(val))
            return

        try:
            if isinstance(val, classModule.Module):
                self._build_module(val)
            elif isinstance(val, classRig.Rig):
                val.build()
            else:
                raise Exception("Unexpected datatype {0} for {1}".format(type(val), val))
        except Exception, e:
            log.error("Error building {0}. Received {1}. {2}".format(val, type(e).__name__, str(e).strip()))
            traceback.print_exc()

        if update:
            self.update()

    def _unbuild(self, val, update=True):
        if not val.is_built():
            pymel.warning("Can't unbuild {0}, already unbuilt.".format(val))
            return

        try:
            if isinstance(val, classModule.Module):
                self._unbuild_module(val)
            elif isinstance(val, classRig.Rig):
                val.unbuild()
            else:
                raise Exception("Unexpected datatype {0} for {1}".format(type(val), val))
        except Exception, e:
            log.error("Error building {0}. Received {1}. {2}".format(val, type(e).__name__, str(e).strip()))
            traceback.print_exc()

        if update:
            self.update()

    def _rig_to_tree_widget(self, module):
        qItem = QtWidgets.QTreeWidgetItem(0)
        if hasattr(module, '_network'):
            qItem.net = module._network
        else:
            pymel.warning("{0} have no _network attributes".format(module))
        qItem.rig = module
        label = str(module)

        # HACK: bypass the stylecheet
        # see: http://forum.qt.io/topic/22219/item-view-stylesheet-bgcolor/12
        # style_sheet_invalid = """
        # QTreeView::item
        # {
        #   background-color: rgb(45,45,45);
        # }"""

        # Set QTreeWidgetItem gray if the module fail validation
        if isinstance(module, classModule.Module):
            if module.locked:
                qItem.setBackground(0, self._color_locked)
                label += ' (locked)'
            elif module.is_built():
                version_major, version_minor, version_patch = module.get_version()
                if version_major is not None and version_minor is not None and version_patch is not None:
                    warning_msg = ''
                    try:
                        module.validate_version(version_major, version_minor, version_patch)
                    except Exception, e:
                        warning_msg = 'v{}.{}.{} is known to have issues and need to be updated: {}'.format(
                            version_major, version_minor, version_patch,
                            str(e)
                        )

                    if warning_msg:
                        desired_color = self._color_warning
                        qItem.setToolTip(0, warning_msg)
                        qItem.setBackground(0, desired_color)
                        label += ' (problematic)'
            else:
                # Set QTreeWidgetItem red if the module fail validation
                can_build, validation_message = self._can_build(module, verbose=True)
                if not can_build:
                    desired_color = self._color_invalid
                    msg = 'Validation failed for {0}: {1}'.format(module, validation_message)
                    log.warning(msg)
                    qItem.setToolTip(0, msg)
                    qItem.setBackground(0, desired_color)

        qItem.setText(0, label)
        qItem._name = qItem.text(0)
        qItem._checked = module.is_built()

        flags = qItem.flags() | QtCore.Qt.ItemIsEditable
        qItem.setFlags(flags)
        qItem.setCheckState(0, QtCore.Qt.Checked if module.is_built() else QtCore.Qt.Unchecked)

        if isinstance(module, classRig.Rig):
            qItem._meta_type = ui_shared.MetadataType.Rig
            qItem.setIcon(0, QtGui.QIcon(":/out_character.png"))
            sorted_modules = sorted(module, key=lambda mod: mod.name)
            for child in sorted_modules:
                qSubItem = self._rig_to_tree_widget(child)
                qSubItem.setIcon(0, QtGui.QIcon(":/out_objectSet.png"))
                for input in child.input:
                    qInputItem = QtWidgets.QTreeWidgetItem(0)
                    qInputItem.setText(0, input.name())
                    ui_shared._set_icon_from_type(input, qInputItem)
                    qInputItem.setFlags(flags)
                    qSubItem.addChild(qInputItem)
                qItem.addChild(qSubItem)
        elif isinstance(module, classModule.Module):
            qItem._meta_type = ui_shared.MetadataType.Module
        return qItem

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
            val = qItem.rig
            self._unbuild(val)
            ui_shared._update_network(self._rig)
        self.update()

    def on_rebuild_selected(self):
        for qItem in self.ui.treeWidget.selectedItems():
            val = qItem.rig
            self._unbuild(val)
            self._build(val)
            ui_shared._update_network(self._rig)

    def on_module_selection_changed(self):
        # Filter deleted networks
        networks = [net for net in self.get_selected_networks() if net and net.exists()]
        pymel.select(networks)

    def on_module_changed(self, item):
        # todo: handle exception
        # Check first if the checkbox have changed
        need_update = False
        new_state = item.checkState(0) == QtCore.Qt.Checked
        new_text = item.text(0)
        module = item.rig
        if item._checked != new_state:
            item._checked = new_state
            # Handle checkbox change
            if new_state:
                self._build(module, update=False)  # note: setting update=True on maya-2017 can cause Qt to crash...
            else:
                self._unbuild(module, update=False)  # note: setting update=True on maya-2017 can cause Qt to crash...
            # need_update = True
            ui_shared._update_network(self._rig, item=item)

        # Check if the name have changed
        if (item._name != new_text):
            item._name = new_text
            module.name = new_text

            # Update directly the network value instead of re-exporting it
            if hasattr(item, "net"):
                name_attr = item.net.attr("name")
                name_attr.set(new_text)

        # Ensure to only refresh the UI and not recreate all
        # if need_update:
        #     self.refresh_ui()

    def on_module_query_changed(self, *args, **kwargs):
        self._refresh_ui_modules_visibility()

    def on_context_menu_request(self):
        if self.ui.treeWidget.selectedItems():
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
            sel = self.ui.treeWidget.selectedItems()
            if len(sel) == 1:
                actionRemove = menu.addAction("Rename")
                # actionRemove.triggered.connect(functools.partial(self.ui.treeWidget.editItem, sel[0], 0))
                actionRemove.triggered.connect(functools.partial(self.ui.treeWidget.itemDoubleClicked.emit, sel[0], 0))
            actionRemove = menu.addAction("Remove")
            actionRemove.triggered.connect(functools.partial(self.on_remove))

            # Expose decorated functions
            inst = sel[0].rig

            def is_exposed(val):
                if not hasattr(val, '__can_show__'):
                    return False
                fn = getattr(val, '__can_show__')
                if fn is None:
                    return False
                # if not inspect.ismethod(fn):
                #    return False
                return val.__can_show__()

            functions = inspect.getmembers(inst, is_exposed)

            if functions:
                menu.addSeparator()
                for fn_name, fn in functions:
                    fn_nicename = fn_name.replace('_', ' ').title()

                    fn = functools.partial(self._execute_rcmenu_entry, fn_name)
                    action = menu.addAction(fn_nicename)
                    action.triggered.connect(fn)

            menu.exec_(QtGui.QCursor.pos())

    def _execute_rcmenu_entry(self, fn_name):
        need_export_network = False
        for module in itertools.chain(self.get_selected_modules() + self.get_selected_rigs()):
            # Resolve fn
            if not hasattr(module, fn_name):
                continue

            fn = getattr(module, fn_name)
            if not inspect.ismethod(fn):
                continue

            # Call fn
            log.debug("Calling {0} on {1}".format(fn_name, module))
            fn()
            if constants.UIExposeFlags.trigger_network_export in fn._flags:
                need_export_network = True

        if need_export_network:
            self.needExportNetwork.emit()

    def on_module_double_clicked(self, item):
        if hasattr(item, "rig"):
            self._set_text_block(item, item.rig.name)
            self._is_modifying = True  # Flag to know that we are currently modifying the name
            self.ui.treeWidget.editItem(item, 0)

    def focus_in_module(self, event):
        # Set back the text with the information about the module in it
        if self._is_modifying:
            sel = self.ui.treeWidget.selectedItems()
            if sel:
                self._set_text_block(sel[0], str(sel[0].rig))
                # sel[0].setText(0, str(sel[0].rig))
            self._is_modifying = False
        self.focusInEvent(event)

    def on_lock_selected(self):
        need_update = False
        for item in self.ui.treeWidget.selectedItems():
            val = item.rig
            if isinstance(val, classModule.Module) and not val.locked:
                need_update = True
                val.locked = True
        if need_update:
            ui_shared._update_network(self._rig)
            self.update()

    def on_unlock_selected(self):
        need_update = False
        for item in self.ui.treeWidget.selectedItems():
            val = item.rig
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
        selected_modules = [module for module in self.get_selected_modules() if module.rig not in selected_rigs]
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
                log.error("Error removing {0}. Received {1}. {2}".format(rig, type(e).__name__, str(e).strip()))
                traceback.print_exc()

        # Remove all selected modules
        for module in selected_modules:
            try:
                if module.is_built():
                    module.unbuild()
                module.rig.remove_module(module)
                need_reexport = True
            except Exception, e:
                log.error("Error removing {0}. Received {1}. {2}".format(module, type(e).__name__, str(e).strip()))
                traceback.print_exc()

        if need_reexport:
            self.needExportNetwork.emit()
