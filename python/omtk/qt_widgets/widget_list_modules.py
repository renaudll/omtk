import logging
import re
import traceback

import pymel.core as pymel
from omtk import factory_tree_widget_item, factory_rc_menu
from omtk import ui_shared
from omtk.core import classModule
from omtk.core import classRig
from omtk.core.classEntity import Entity
from omtk.core.classNode import Node
from omtk.libs import libQt
from omtk.qt_widgets.ui import widget_list_modules
from omtk.vendor.Qt import QtCore, QtWidgets

log = logging.getLogger('omtk')


class WidgetListModules(QtWidgets.QWidget):
    needExportNetwork = QtCore.Signal()
    needImportNetwork = QtCore.Signal()
    deletedRig = QtCore.Signal(object)
    actionRequested = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(WidgetListModules, self).__init__(parent=parent)

        self._rig = None
        self._rigs = []
        self._is_modifying = False  # todo: document
        self._listen_events = True  # todo: replace by blockSignal calls?

        # Used to prevent cyclic dependencies
        # todo: use a solver class?
        self._known_data_ids = set()

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
        self.ui.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.on_context_menu_request)
        self.ui.btn_update.pressed.connect(self.update)

    def set_rigs(self, rigs, update=True):
        self._rigs = rigs
        self._rig = next(iter(self._rigs), None)
        if update:
            self.update()

    def get_selected_items(self):
        return self.ui.treeWidget.selectedItems()

    def get_selected_objects(self):
        """
        Get the Maya objects associated with the selection.
        :return: A list of pymel.PyNode instances.
        """
        result = []
        for item in self.get_selected_items():
            if not hasattr(item, 'metadata'):
                continue
            metadata = item._meta_data

            if isinstance(metadata, Node):
                result.append(metadata)
            elif hasattr(metadata, '_network'):
                result.append(metadata._network)
            elif hasattr(metadata, '__melobject__'):
                result.append(metadata)
            else:
                print("Unexpected metadata type: {0}".format(metadata))
        return result

    def get_selected_entries(self):
        """
        Return the metadata stored in each selected row. Whatever the metadata type (can be Rig or Module).
        :return: A list of object instances.
        """
        return [item._meta_data for item in self.get_selected_items()]

    def get_selected_modules(self):
        """
        Return the Module instances stored in each selected rows.
        :return: A list of Module instances.
        """
        return [item._meta_data for item in self.get_selected_items() if item._meta_type == ui_shared.MimeTypes.Module]

    def get_selected_rigs(self):
        """
        Return the Rig instances stored in each selected rows.
        :return: A list of Rig instances.
        """
        return [item._meta_data for item in self.get_selected_items() if item._meta_type == ui_shared.MimeTypes.Rig]

    def get_selected_components(self):
        """
        Return the Component instance stored in each selected rows.
        :return: A list of Component instances.
        """
        return [item._meta_data for item in self.get_selected_items() if isinstance(item._meta_data, Entity)]

    def update(self, *args, **kwargs):
        self.ui.treeWidget.clear()
        if not self._rigs:
            return

        # self._known_data_ids = set()

        for root in self._rigs:
            # self._known_data_ids.add(id(root))
            # item = self._create_tree_widget_item_from_component(root)
            item = factory_tree_widget_item.get(root)
            # qItem = self._rig_to_tree_widget(root)
            self.ui.treeWidget.addTopLevelItem(item)
            self.ui.treeWidget.expandItem(item)

        # from omtk.vendor import libSerialization
        # networks = libSerialization.get_networks_from_class(Component.__name__)
        # for network in networks:
        #     module = libSerialization.import_network(network)
        #     item = factory_tree_widget_item.get_tree_item(module)
        #     self.ui.treeWidget.addTopLevelItem(item)
        #     self.ui.treeWidget.expandItem(item)

        self.refresh_ui()

    def refresh_ui(self):
        self._refresh_ui_modules_checked()
        self._refresh_ui_modules_visibility()

    def _refresh_ui_modules_checked(self):
        # Block the signal to make sure that the itemChanged event is not called when adjusting the check state
        self.ui.treeWidget.blockSignals(True)
        for qt_item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            if hasattr(qt_item, "rig"):
                qt_item.setCheckState(0, QtCore.Qt.Checked if qt_item._meta_data.is_built else QtCore.Qt.Unchecked)
        self.ui.treeWidget.blockSignals(False)

    def _refresh_ui_modules_visibility(self, query_regex=None):
        if query_regex is None:
            query_raw = self.ui.lineEdit_search.text()
            query_regex = ".*{0}.*".format(query_raw) if query_raw else ".*"

        def fn_can_show(qItem, query_regex):
            # Always shows non-module
            if not hasattr(qItem, 'rig'):
                return True
            if not isinstance(qItem._meta_data, classModule.Module):
                return True

            module = qItem._meta_data  # Retrieve monkey-patched data
            module_name = str(module)

            return not query_regex or re.match(query_regex, module_name, re.IGNORECASE)

        # unselectableBrush = QtGui.QBrush(QtCore.Qt.darkGray)
        # selectableBrush = QtGui.QBrush(QtCore.Qt.white)
        for qt_item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            can_show = fn_can_show(qt_item, query_regex)
            qt_item.setHidden(not can_show)

    def _refresh_ui_enabled(self, val):
        """
        Used for drag and drop operation, this will change the 'enabled' value for all QTreeWidgetItem that can accept the new value.
        :param val:
        :return:
        """
        for item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            if item._meta_type == ui_shared.MimeTypes.Attribute:
                component_attr = item._meta_data
                if component_attr.validate(val):
                    flags = item.flags()
                    flags &= ~QtCore.Qt.ItemIsEnabled
                    item.setFlags(flags)

    def _reset_ui_enabled(self):
        for item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            flags = item.flags()
            flags |= QtCore.Qt.ItemIsEnabled
            item.setFlags(flags)

    # Block signals need to be called in a function because if called in a signal, it will block it
    def _set_text_block(self, item, str):
        self.ui.treeWidget.blockSignals(True)
        if hasattr(item, "rig"):
            item.setText(0, str)
        self.ui.treeWidget.blockSignals(False)

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
        if val.is_built:
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
        if not val.is_built:
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
            val = qItem._meta_data
            self._unbuild(val)
            ui_shared._update_network(self._rig)
        self.update()

    def on_rebuild_selected(self):
        for qItem in self.ui.treeWidget.selectedItems():
            val = qItem._meta_data
            self._unbuild(val)
            self._build(val)
            ui_shared._update_network(self._rig)

    def on_module_selection_changed(self):
        # Filter deleted networks
        networks = [net for net in self.get_selected_objects() if net and net.exists()]
        pymel.select(networks)

    def on_module_changed(self, item):
        if not self._listen_events:
            return

        # todo: handle exception
        # Check first if the checkbox have changed
        need_update = False
        new_state = item.checkState(0) == QtCore.Qt.Checked
        new_text = item.text(0)

        # debug
        if not hasattr(item, 'metadata'):
            print '???', item.text(0)
            return

        module = item._meta_data
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

    # def _iter_components_recursive(self, entity):
    #     """Recursively return all modules and submodules starting with provided entity."""
    #     # todo: replace by Component.iter_sub_components_recursive?
    #     yield entity
    #     for sub_entity in entity.iter_sub_components():
    #         for sub_sub_entity in self._iter_components_recursive(sub_entity):
    #             yield sub_sub_entity
    #
    # def _get_actions(self, entities):
    #     """Recursively scan for actions stored inside entities."""
    #     result = collections.defaultdict(list)
    #     for entity in entities:
    #         for component in self._iter_components_recursive(entity):
    #             for action in component.iter_actions():
    #                 action_name = action.get_name()
    #                 result[action_name].append(action)
    #     return result

    def on_context_menu_request(self):
        selected_items = self.ui.treeWidget.selectedItems()
        selected_components = [item._meta_data for item in selected_items if isinstance(item._meta_data, Entity)]
        if selected_components:
            factory_rc_menu.get_menu(selected_components, self.actionRequested.emit)
            # menu.exec_(QtGui.QCursor.pos())
            # if self.ui.treeWidget.selectedItems():
            #     sel = self.ui.treeWidget.selectedItems()
            #
            #     # We don't support actions on non-component entities (for now)
            #     if not any(True for item in sel if isinstance(item._meta_data, Component)):
            #         return
            #
            #     menu = QtWidgets.QMenu()
            #     actionBuild = menu.addAction("Build")
            #     actionBuild.triggered.connect(self.on_build_selected)
            #     actionUnbuild = menu.addAction("Unbuild")
            #     actionUnbuild.triggered.connect(self.on_unbuild_selected)
            #     actionRebuild = menu.addAction("Rebuild")
            #     actionRebuild.triggered.connect(self.on_rebuild_selected)
            #     menu.addSeparator()
            #     actionLock = menu.addAction("Lock")
            #     actionLock.triggered.connect(self.on_lock_selected)
            #     action_unlock = menu.addAction("Unlock")
            #     action_unlock.triggered.connect(self.on_unlock_selected)
            #     menu.addSeparator()
            #     if len(sel) == 1:
            #         actionRemove = menu.addAction("Rename")
            #         # actionRemove.triggered.connect(functools.partial(self.ui.treeWidget.editItem, sel[0], 0))
            #         actionRemove.triggered.connect(functools.partial(self.ui.treeWidget.itemDoubleClicked.emit, sel[0], 0))
            #     actionRemove = menu.addAction("Remove")
            #     actionRemove.triggered.connect(functools.partial(self.on_remove))
            #
            #     # Expose decorated functions
            #     # todo: group actions by class name?
            #     components = self.get_selected_components()
            #     # actions_map = self._get_actions(components)
            #
            #     actions_data = []
            #     cache_component_class_level = {}
            #     for entity in components:
            #         for component in self._iter_components_recursive(entity):
            #             component_cls = component.__class__
            #             component_level = cache_component_class_level.get(component_cls)
            #             if component_level is None:
            #                 component_level = libPython.get_class_parent_level(component_cls)
            #                 cache_component_class_level[component_cls] = component_level
            #             for action in component.iter_actions():
            #                 action_name = action.get_name()
            #                 # actions_map[(component_level, component_cls.__name__, action_name)].append(action)
            #                 actions_data.append(
            #                     (component_level, component_cls.__name__, action_name, action)
            #                 )
            #
            #     if actions_data:
            #         for cls_level, entries in itertools.groupby(actions_data, operator.itemgetter(0)):
            #             print cls_level
            #             for cls_name, entries in itertools.groupby(entries, operator.itemgetter(1)):
            #                 menu.addSeparator()
            #                 menu.addAction(str(cls_name)).setEnabled(False)
            #                 for fn_name, entries in itertools.groupby(entries, operator.itemgetter(2)):
            #                     action = menu.addAction(fn_name)
            #                     action.triggered.connect(functools.partial(self._execute_rcmenu_entry, fn_name))
            #
            #     menu.exec_(QtGui.QCursor.pos())

    # def _execute_rcmenu_entry(self, fn_name):
    #     need_export_network = False
    #     entities = self.get_selected_components()
    #     action_map = self._get_actions(entities)
    #     for action in action_map[fn_name]:
    #         action.execute()
    #         if constants.ComponentActionFlags.trigger_network_export in action.iter_flags():
    #             need_export_network = True
    #
    #     if need_export_network:
    #         self.needExportNetwork.emit()

    def on_module_double_clicked(self, item):
        if hasattr(item, "rig"):
            self._set_text_block(item, item._meta_data.name)
            self._is_modifying = True  # Flag to know that we are currently modifying the name
            self.ui.treeWidget.editItem(item, 0)

    def focus_in_module(self, event):
        # Set back the text with the information about the module in it
        if self._is_modifying:
            sel = self.ui.treeWidget.selectedItems()
            if sel:
                self._listen_events = False
                selected_item = sel[0]
                if isinstance(selected_item._meta_data, classModule.Module):
                    selected_item._update()
                self._listen_events = True
            self._is_modifying = False
        self.focusInEvent(event)

    def on_lock_selected(self):
        need_update = False
        for item in self.ui.treeWidget.selectedItems():
            val = item._meta_data
            if isinstance(val, classModule.Module) and not val.locked:
                need_update = True
                val.locked = True
        if need_update:
            ui_shared._update_network(self._rig)
            self.update()

    def on_unlock_selected(self):
        need_update = False
        for item in self.ui.treeWidget.selectedItems():
            val = item._meta_data
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
                if rig.is_built:
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
                if module.is_built:
                    module.unbuild()
                module.rig.remove_module(module)
                need_reexport = True
            except Exception, e:
                log.error("Error removing {0}. Received {1}. {2}".format(module, type(e).__name__, str(e).strip()))
                traceback.print_exc()

        if need_reexport:
            self.needExportNetwork.emit()
