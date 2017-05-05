import re
import functools
import traceback
import logging
import collections

import pymel.core as pymel
from ui import widget_list_modules

from omtk import constants
from omtk import ui_shared
from omtk.libs import libQt
from omtk.core.classNode import Node
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classComponent import Component
from omtk.core import classModule
from omtk.core import classRig

from omtk.vendor.Qt import QtCore, QtGui, QtWidgets

log = logging.getLogger('omtk')


class AttributeType:
    Basic = 0
    Iterable = 1
    Dictionary = 2
    Node = 3
    Ctrl = 4
    Attribute = 5
    Component = 6


def get_component_attribute_type(val):
    if val is None or isinstance(val, (
            bool,
            int,
            float,
            long,
            basestring,
            type,
            pymel.util.enum.EnumValue,
            pymel.datatypes.Vector,
            pymel.datatypes.Point,
            pymel.datatypes.Matrix
    )):
        return AttributeType.Basic
    if isinstance(val, (list, set, tuple)):
        return AttributeType.Iterable
    if isinstance(val, (dict, collections.defaultdict)):
        return AttributeType.Dictionary
    if isinstance(val, BaseCtrl):
        return AttributeType.Ctrl
    if isinstance(val, (pymel.PyNode, Node)):
        return AttributeType.Node
    if isinstance(val, pymel.Attribute):
        return AttributeType.Attribute
    if isinstance(val, Component):
        return AttributeType.Component
    raise Exception("Cannot resolve Component attribute type for {0} {1}".format(type(val), val))





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
        self.ui.treeWidget.customContextMenuRequested.connect(self.on_context_menu_request)
        self.ui.btn_update.pressed.connect(self.update)

    def set_rigs(self, rig, update=True):
        self._rigs = rig
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
            metadata = item.metadata

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
        return [item.metadata for item in self.get_selected_items()]

    def get_selected_modules(self):
        """
        Return the Module instances stored in each selected rows.
        :return: A list of Module instances.
        """
        return [item.metadata for item in self.get_selected_items() if item._meta_type == ui_shared.MetadataType.Module]

    def get_selected_rigs(self):
        """
        Return the Rig instances stored in each selected rows.
        :return: A list of Rig instances.
        """
        return [item.metadata for item in self.get_selected_items() if item._meta_type == ui_shared.MetadataType.Rig]

    def get_selected_components(self):
        """
        Return the Component instance stored in each selected rows.
        :return: A list of Component instances.
        """
        return [item.metadata for item in self.get_selected_items() if isinstance(item.metadata, Component)]

    def update(self, *args, **kwargs):
        self.ui.treeWidget.clear()
        if not self._rigs:
            return

        self._known_data_ids = set()
        for root in self._rigs:
            self._known_data_ids.add(id(root))
            item = self._create_tree_widget_item_from_component(root)
            # qItem = self._rig_to_tree_widget(root)
            self.ui.treeWidget.addTopLevelItem(item)
            self.ui.treeWidget.expandItem(item)
        self.refresh_ui()

    def refresh_ui(self):
        self._refresh_ui_modules_checked()
        self._refresh_ui_modules_visibility()

    def _refresh_ui_modules_checked(self):
        # Block the signal to make sure that the itemChanged event is not called when adjusting the check state
        self.ui.treeWidget.blockSignals(True)
        for qt_item in libQt.get_all_QTreeWidgetItem(self.ui.treeWidget):
            if hasattr(qt_item, "rig"):
                qt_item.setCheckState(0, QtCore.Qt.Checked if qt_item.metadata.is_built() else QtCore.Qt.Unchecked)
        self.ui.treeWidget.blockSignals(False)

    def _refresh_ui_modules_visibility(self, query_regex=None):
        if query_regex is None:
            query_raw = self.ui.lineEdit_search.text()
            query_regex = ".*{0}.*".format(query_raw) if query_raw else ".*"

        def fn_can_show(qItem, query_regex):
            # Always shows non-module
            if not hasattr(qItem, 'rig'):
                return True
            if not isinstance(qItem.metadata, classModule.Module):
                return True

            module = qItem.metadata  # Retrieve monkey-patched data
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
                validate_message = str(e)
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

    def _update_qitem_module(self, qitem, module):
        label = str(module)

        # Add inputs namespace if any for clarity.
        module_namespace = module.get_inputs_namespace()
        if module_namespace:
            label = '{0}:{1}'.format(module_namespace.strip(':'), label)

        if module.locked:
            qitem.setBackground(0, self._color_locked)
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
                    qitem.setToolTip(0, warning_msg)
                    qitem.setBackground(0, desired_color)
                    label += ' (problematic)'
                    module.warning(warning_msg)
        else:
            # Set QTreeWidgetItem red if the module fail validation
            can_build, validation_message = self._can_build(module, verbose=True)
            if not can_build:
                desired_color = self._color_invalid
                msg = 'Validation failed for {0}: {1}'.format(module, validation_message)
                log.warning(msg)
                qitem.setToolTip(0, msg)
                qitem.setBackground(0, desired_color)

        qitem.setText(0, label)
        qitem._name = qitem.text(0)
        qitem._checked = module.is_built()

        flags = qitem.flags() | QtCore.Qt.ItemIsEditable
        qitem.setFlags(flags)
        qitem.setCheckState(0, QtCore.Qt.Checked if module.is_built() else QtCore.Qt.Unchecked)
        qitem._meta_type = ui_shared.MetadataType.Module

    def _update_qitem_rig(self, qitem, rig):
        label = str(rig)

        qitem.setText(0, label)
        qitem._name = qitem.text(0)
        qitem._checked = rig.is_built()

        flags = qitem.flags() | QtCore.Qt.ItemIsEditable
        qitem.setFlags(flags)
        qitem.setCheckState(0, QtCore.Qt.Checked if rig.is_built() else QtCore.Qt.Unchecked)

        qitem._meta_type = ui_shared.MetadataType.Rig
        qitem.setIcon(0, QtGui.QIcon(":/out_character.png"))

    # def _create_tree_widget_item(self, val):
    #     item = QtWidgets.QTreeWidgetItem(0)
    #     if isinstance(val, Component):
    #         item.setIcon(0, QtGui.QIcon(":/out_objectSet.png"))
    #
    #         # todo: validate this is necessary?
    #         if hasattr(val, '_network'):
    #             item.net = module._network

    def can_show_component_attribute(self, attr_name, attr_value):
        # Hack: Blacklist some attr name (for now)
        if attr_name in ('grp_anm', 'grp_rig'):
            return False

        # Validate name (private attribute should not be visible)
        if next(iter(attr_name), None) == '_':
            return False

        # Validate type
        attr_type = get_component_attribute_type(attr_value)
        if not attr_type in (
                AttributeType.Iterable,
                AttributeType.Node,
                AttributeType.Attribute,
                AttributeType.Component
        ):
            return False

        # Do not show non-dagnodes.
        if isinstance(attr_value, pymel.PyNode) and not isinstance(attr_value, pymel.nodetypes.DagNode):
            return False

        # Ignore empty collections
        if attr_type == AttributeType.Iterable and not attr_value:
            return False

        # Prevent cyclic dependency, we only show something the first time we encounter it.
        data_id = id(attr_value)
        if data_id in self._known_data_ids:
            return False
        self._known_data_ids.add(data_id)

        return True

    def _create_tree_widget_item_from_value(self, value):
        value_type = get_component_attribute_type(value)
        if value_type == AttributeType.Component:
            return self._create_tree_widget_item_from_component(value)
        if value_type == AttributeType.Node or value_type == AttributeType.Ctrl:
            return self._create_tree_widget_item_from_pynode(value)
        raise Exception("Unsupported value type {0} for {1}".format(value_type, value))

    def _create_tree_widget_item_from_component(self, component):
        item = QtWidgets.QTreeWidgetItem(0)
        item.setIcon(0, QtGui.QIcon(":/out_objectSet.png"))

        # Store the source network in metadata
        if hasattr(component, '_network'):
            item.net = component._network
        else:
            log.warning("{0} have no _network attributes".format(component))

        # Store the component in metadata
        item.metadata = component

        # todo: cleanup
        if isinstance(component, classModule.Module):
            self._update_qitem_module(item, component)
        elif isinstance(component, classRig.Rig):
            self._update_qitem_rig(item, component)
            # sorted_modules = sorted(module, key=lambda mod: mod.name)
            # for child in sorted_modules:
            #     qSubItem = self._create_tree_widget_module(child)
            #     qItem.addChild(qSubItem)

        keys = sorted(component.__dict__.keys())  # prevent error if dictionary change during iteration
        for attr_name in keys:
            attr = getattr(component, attr_name)
            attr_type = get_component_attribute_type(attr)
            if not self.can_show_component_attribute(attr_name, attr):
                continue

            item_attr = QtWidgets.QTreeWidgetItem(0)
            item_attr.setText(0, "{0}:".format(attr_name))
            item.addChild(item_attr)

            if attr_type == AttributeType.Iterable:
                for sub_attr in attr:
                    item_child = self._create_tree_widget_item_from_value(sub_attr)
                    item_attr.addChild(item_child)
            else:
                item_child = self._create_tree_widget_item_from_value(attr)
                item_attr.addChild(item_child)

            # Hack: Force expand 'modules' attribute. todo: rename with children.
            if attr_name == 'modules':
                self.ui.treeWidget.expandItem(item_attr)

        return item

    def _create_tree_widget_item_from_pynode(self, pynode):
        item = QtWidgets.QTreeWidgetItem(0)
        item.setText(0, pynode.name())
        item.metadata = pynode
        ui_shared._set_icon_from_type(pynode, item)
        return item

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
            val = qItem.metadata
            self._unbuild(val)
            ui_shared._update_network(self._rig)
        self.update()

    def on_rebuild_selected(self):
        for qItem in self.ui.treeWidget.selectedItems():
            val = qItem.metadata
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
        module = item.metadata
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

    def _iter_components_recursive(self, entity):
        """Recursively return all modules and submodules starting with provided entity."""
        yield entity
        for sub_entity in entity.iter_sub_components():
            for sub_sub_entity in self._iter_components_recursive(sub_entity):
                yield sub_sub_entity

    def _get_actions(self, entities):
        """Recursively scan for actions stored inside entities."""
        result = collections.defaultdict(list)
        for entity in entities:
            for component in self._iter_components_recursive(entity):
                for action in component.iter_actions():
                    action_name = action.get_name()
                    result[action_name].append(action)
        return result

    def on_context_menu_request(self):
        if self.ui.treeWidget.selectedItems():
            sel = self.ui.treeWidget.selectedItems()

            # We don't support actions on non-component entities (for now)
            if not any(True for item in sel if isinstance(item.metadata, Component)):
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
                actionRemove.triggered.connect(functools.partial(self.ui.treeWidget.itemDoubleClicked.emit, sel[0], 0))
            actionRemove = menu.addAction("Remove")
            actionRemove.triggered.connect(functools.partial(self.on_remove))

            # Expose decorated functions
            components = self.get_selected_components()
            actions_map = self._get_actions(components)
            if actions_map:
                menu.addSeparator()
                for fn_name in sorted(actions_map.keys()):
                    fn_nicename = fn_name.replace('_', ' ').title()

                    fn_ = functools.partial(self._execute_rcmenu_entry, fn_name)
                    action = menu.addAction(fn_nicename)
                    action.triggered.connect(fn_)

            menu.exec_(QtGui.QCursor.pos())

    def _execute_rcmenu_entry(self, fn_name):
        need_export_network = False
        entities = self.get_selected_components()
        action_map = self._get_actions(entities)
        for action in action_map[fn_name]:
            action.execute()
            if constants.ComponentActionFlags.trigger_network_export in action.iter_flags():
                need_export_network = True

        if need_export_network:
            self.needExportNetwork.emit()

    def on_module_double_clicked(self, item):
        if hasattr(item, "rig"):
            self._set_text_block(item, item.metadata.name)
            self._is_modifying = True  # Flag to know that we are currently modifying the name
            self.ui.treeWidget.editItem(item, 0)

    def focus_in_module(self, event):
        # Set back the text with the information about the module in it
        if self._is_modifying:
            sel = self.ui.treeWidget.selectedItems()
            if sel:
                self._listen_events = False
                selected_item = sel[0]
                if isinstance(selected_item.metadata, classModule.Module):
                    self._update_qitem_module(selected_item, selected_item.metadata)
                self._listen_events = True
            self._is_modifying = False
        self.focusInEvent(event)

    def on_lock_selected(self):
        need_update = False
        for item in self.ui.treeWidget.selectedItems():
            val = item.metadata
            if isinstance(val, classModule.Module) and not val.locked:
                need_update = True
                val.locked = True
        if need_update:
            ui_shared._update_network(self._rig)
            self.update()

    def on_unlock_selected(self):
        need_update = False
        for item in self.ui.treeWidget.selectedItems():
            val = item.metadata
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
