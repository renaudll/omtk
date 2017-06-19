"""
Factory method to generate a QTreeWidgetItem from any value, preferably starting from a Component.
"""
import logging

import pymel.core as pymel

from omtk import ui_shared
from omtk.core.classModule import Module
from omtk.core.classRig import Rig
from omtk import factory_datatypes
from omtk.factory_datatypes import AttributeType, get_component_attribute_type
from omtk.vendor.Qt import QtCore, QtWidgets, QtGui

log = logging.getLogger('omtk')


_color_invalid = QtGui.QBrush(QtGui.QColor(255, 45, 45))
_color_valid = QtGui.QBrush(QtGui.QColor(45, 45, 45))
_color_locked = QtGui.QBrush(QtGui.QColor(125, 125, 125))
_color_warning = QtGui.QBrush(QtGui.QColor(125, 125, 45))

class TreeWidgetItemEx(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, meta_type, meta_data):
        super(TreeWidgetItemEx, self).__init__(parent)

        self._meta_type = meta_type
        self._meta_data = meta_data

        self.update_()

    def update_(self):
        icon = factory_datatypes.get_icon_from_datatype(self._meta_type)
        if icon:
            self.setIcon(0, icon)

        if hasattr(self._meta_data, '_network'):
            self.net = self._meta_data._network
        else:
            log.warning("{0} have no _network attributes".format(self._meta_data))


class TreeWidgetItemComponent(TreeWidgetItemEx):
    def update_(self):
        super(TreeWidgetItemComponent, self).update_()

        component = self._meta_data
        label = str(component) + str(component.get_version())
        self.setText(0, label)


class TreeWidgetItemRig(TreeWidgetItemComponent):
    def __init__(self, parent, meta_data):
        super(TreeWidgetItemRig, self).__init__(parent, factory_datatypes.AttributeType.Rig, meta_data)

    def update_(self):
        super(TreeWidgetItemRig, self).update_()

        rig = self._meta_data
        label = str(rig)

        self.setText(0, label)
        self._name = self.text(0)
        self._checked = rig.is_built

        flags = self.flags() | QtCore.Qt.ItemIsEditable
        self.setFlags(flags)
        self.setCheckState(0, QtCore.Qt.Checked if rig.is_built else QtCore.Qt.Unchecked)

        self._meta_type = ui_shared.MimeTypes.Rig


class TreeWidgetItemModule(TreeWidgetItemComponent):
    def __init__(self, parent, meta_data):
        super(TreeWidgetItemModule, self).__init__(parent, factory_datatypes.AttributeType.Module, meta_data)

    def update_(self):
        super(TreeWidgetItemModule, self).update_()

        module = self._meta_data
        label = str(module)
        # Add inputs namespace if any for clarity.
        module_namespace = module.get_inputs_namespace()
        if module_namespace:
            label = '{0}:{1}'.format(module_namespace.strip(':'), label)

        if module.locked:
            self.setBackground(0, _color_locked)
            label += ' (locked)'
        elif module.is_built:
            version_major, version_minor, version_patch = module.get_version()
            if version_major is not None and version_minor is not None and version_patch is not None:
                warning_msg = ''
                try:
                    module.validate_version(version_major, version_minor, version_patch)
                except Exception, e:
                    warning_msg = 'v{}.{}.{} is known_data_id to have issues and need to be updated: {}'.format(
                        version_major, version_minor, version_patch,
                        str(e)
                    )

                if warning_msg:
                    desired_color = _color_warning
                    self.setToolTip(0, warning_msg)
                    self.setBackground(0, desired_color)
                    label += ' (problematic)'
                    module.warning(warning_msg)
        else:
            # Set QTreeWidgetItem red if the module fail validation
            try:
                module.validate()
            except Exception, e:
                msg = 'Validation failed for {0}: {1}'.format(module, e)
                log.warning(msg)
                self.setToolTip(0, msg)
                self.setBackground(0, _color_invalid)

        self.setText(0, label)
        self._name = self.text(0)
        self._checked = module.is_built

        flags = self.flags() | QtCore.Qt.ItemIsEditable
        self.setFlags(flags)
        self.setCheckState(0, QtCore.Qt.Checked if module.is_built else QtCore.Qt.Unchecked)


def get_tree_item(value, known_data_id=None):
    value_type = get_component_attribute_type(value)
    if value_type in (
            AttributeType.Component,
            AttributeType.Module,
            AttributeType.Rig
    ):
        return _get_item_from_component(value, known_data_id=known_data_id)
    if value_type == AttributeType.Node or value_type == AttributeType.Ctrl:
        return _create_tree_widget_item_from_pynode(value)
    raise Exception("Unsupported value type {0} for {1}".format(value_type, value))


def _get_item_from_component(component, known_data_id=None):
    # Prevent cyclic dependency by not showing two component twice.
    if known_data_id is None:
        known_data_id = set()

    meta_type = factory_datatypes.get_component_attribute_type(component)
    if meta_type == factory_datatypes.AttributeType.Module:
        item = TreeWidgetItemModule(0, component)
    elif meta_type == factory_datatypes.AttributeType.Rig:
        item = TreeWidgetItemRig(0, component)
    elif meta_type == factory_datatypes.AttributeType.Component:
        item = TreeWidgetItemComponent(0, meta_type, component)
    else:
        item = QtWidgets.QTreeWidgetItem(0)

    keys = list(component.iter_attributes())

    # keys = sorted(component.__dict__.keys())  # prevent error if dictionary change during iteration
    for attr in keys:
        attr_name = attr.name
        attr_val = attr.get()  # getattr(component, attr_name)
        attr_type = get_component_attribute_type(attr_val)
        if not can_show_component_attribute(attr_name, attr_val, known_data_id=known_data_id):
            continue

        item_attr = QtWidgets.QTreeWidgetItem(0)
        item_attr._meta_data = attr
        item_attr._meta_type = ui_shared.MimeTypes.Attribute
        item_attr.setText(0, "{0}:".format(attr_name))
        item.addChild(item_attr)

        if attr_type == AttributeType.Iterable:
            for sub_attr in attr_val:
                item_child = get_tree_item(sub_attr)
                item_attr.addChild(item_child)
        else:
            item_child = get_tree_item(attr_val)
            item_attr.addChild(item_child)

            # Hack: Force expand 'modules' attribute. todo: rename with children.
            # if attr_name == 'modules':
            #     self.ui.treeWidget.expandItem(item_attr)

    return item


def can_show_component_attribute(attr_name, attr_value, known_data_id):
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
            AttributeType.Component,
            AttributeType.Module,
            AttributeType.Rig
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
    if data_id in known_data_id:
        return False
    known_data_id.add(data_id)

    return True


def _create_tree_widget_item_from_pynode(pynode):
    item = QtWidgets.QTreeWidgetItem(0)
    item.setText(0, pynode.name())
    item._meta_data = pynode
    item._meta_type = ui_shared.MimeTypes.Influence  # todo: is this the correct type?
    ui_shared._set_icon_from_type(pynode, item)
    return item
