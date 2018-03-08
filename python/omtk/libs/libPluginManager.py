from pymel.util.enum import Enum
from omtk.core import plugin_manager

NONE_PLUGIN_TYPE = 'None'  # Enum value that represent the absence of any plugin


def create_pymel_enum_from_plugin_type(plugin_type_name, add_null=False):
    pm = plugin_manager.plugin_manager
    plugins = pm.get_loaded_plugins_by_type(plugin_type_name)
    choices = []
    if add_null:
        choices.append(NONE_PLUGIN_TYPE)  # todo: don't hardcode?
    choices.extend([plugin.cls.name for plugin in plugins])
    enum = Enum(plugin_type_name, choices)
    return enum


def get_plugin_by_class_name(plugin_type_name, plugin_name):
    pm = plugin_manager.plugin_manager
    for plugin in pm.iter_loaded_plugins_by_type(plugin_type_name):
        if plugin.cls.name == plugin_name:
            return plugin.cls