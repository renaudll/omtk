import os
import copy
import sys
import importlib
import pkgutil
import logging
import inspect

log = logging.getLogger('omtk')
from omtk.libs import libPython

class PluginStatus:
    Loaded = 'Loaded'
    Unloaded = 'Unloaded'
    Failed = 'Failed'

class Plugin(object):
    root_package_name = 'omtk'

    def __init__(self, module_name, type_name):
        self.name = module_name
        self.module_name = module_name
        self.type_name = type_name
        self.module = None
        self.cls = None
        self.status = PluginStatus.Unloaded
        self.description = None

        self.load()

    def load(self, force=False):
        """
        Load the plugin, note that loading twice as no effect unless the force flag is used.
        :param force: If True, the plugin module will be reloaded.
        :return:
        """
        self.cls = None
        self.module = None
        self.description = None

        # Resolve full module path
        module_path = '{0}.{1}.{2}'.format(self.root_package_name, self.type_name, self.module_name)

        try:
            # Load module using import_module before using pkgutil
            # src: https://bugs.python.org/issue25372
            importlib.import_module(module_path)

            self.module = sys.modules.get(module_path, None)
            if self.module is None or force:
                if force:
                    log.debug("Reloading module {0}".format(module_path))
                else:
                    log.debug("Loading module {0}".format(module_path))

                self.module = pkgutil.get_loader(module_path).load_module(module_path)

            # Ensure there is a register_plugin function
            if not hasattr(self.module, 'register_plugin') or not hasattr(self.module.register_plugin, '__call__'):
                raise Exception("Cannot register plugin {0}. No register_plugin function found!".format(
                    self.module_name
                ))

            # Get module class
            self.cls = self.module.register_plugin()
            self.name = self.cls.__name__
            self.description = self.cls.__doc__
            if self.description:
                self.description = next(iter(filter(None, self.description.split('\n'))), None)
            self.status = PluginStatus.Loaded
        except Exception, e:
            self.status = PluginStatus.Failed
            self.description = str(e)
            log.warning("Plugin {0} failed to load! {0}".format(self.module_name, self.description))

    @classmethod
    def from_module(cls, name, type_name):
        plugin = Plugin(name, type_name=type_name)
        return plugin

    def __contains__(self, item):  # arm, fk
        """
        Return True if item is used in this module.
        Mainly used for efficient reloading.
        """
        if isinstance(item, Plugin):
            item_module = item.module
        elif inspect.ismodule(item):
            item_module = item
        else:
            raise NotImplementedError("Unexpected type {0} for value {1}.".format(type(item), item))

        # If there's no associated module, we deduct that it cannot be contained.
        if item.module is None:
            return False

        item_module_name = item_module.__name__

        # Check for module import
        # ex: import my_module
        for module_name, module in inspect.getmembers(self.module, inspect.ismodule):
            if module == item_module:
                return True

        # Check class in case of indirect module import
        # ex: from my_module import my_class
        for class_name, cls in inspect.getmembers(self.module, inspect.isclass):
            if cls.__module__ == item_module_name:
                return True

        return False

    def __cmp__(self, other):
        """
        Ensure we can sort plugins by their names.
        """
        return cmp(self.module_name, other.name)

    def __repr__(self):
        return '<Plugin "{0}">'.format(self.module_name)

class PluginType(object):
    type_name = None

    def __init__(self):
        self._plugins = []
        self.load_plugins()

    def load_plugins(self):
        # Ensure we are not dealing directly with the abstract class.
        if not self.type_name:
            raise Exception("Please subclass Plugin before loading.")

        root_package_name = 'omtk'
        package_name = root_package_name + '.' + self.type_name
        #log.debug("Checking {0}".format(package_name))

        # Prevent reloading (for now)
        package = sys.modules.get(package_name, None)
        if package is None:
            package = pkgutil.get_loader(package_name).load_module(package_name)

        for loader, modname, ispkg in pkgutil.walk_packages(package.__path__):
            #log.debug("Found plugin {0}".format(modname))
            plugin = Plugin.from_module(modname, self.type_name)
            self._plugins.append(plugin)

class PluginManager(object):
    def __init__(self):
        self._plugins = []
        self._plugin_types = {}

    def register_plugin_type(self, plugin_type):
        self._plugin_types[plugin_type.type_name] = libPython.LazySingleton(plugin_type)

    def unregister_plugin_type(self, plugin_type):
        self._plugin_types.pop(plugin_type.type_name, None)

    def iter_plugins(self, key=None):
        for plugin_type in self._plugin_types.values():
            for plugin in plugin_type()._plugins:
                if key is None or key(plugin):
                    yield plugin

    def get_plugins(self, key=None):
        return list(self.iter_plugins(key=None))

    def iter_loaded_plugins_by_type(self, type_name):
        def fn_filter(plugin):
            return plugin.status == PluginStatus.Loaded and plugin.type_name == type_name
        for plugin in self.iter_plugins(key=fn_filter):
            yield plugin

    def get_loaded_plugins_by_type(self, type_name):
        return list(self.iter_loaded_plugins_by_type(type_name))

    def iter_plugins_by_status(self, status):
        def fn_filter(plugin):
            return plugin.status == status
        for plugin in self.iter_plugins(key=fn_filter):
            yield plugin

    def get_failed_plugins(self):
        return list(self.iter_plugins_by_status(PluginStatus.Failed))

    def reload_all(self, force=True):
        for plugin in self.get_plugins_sorted():
            plugin.load(force=force)

    def _iter_dependent_plugins(self, plugin):
        for cur_plugin in self.get_plugins():
            # Ignore self
            if cur_plugin is plugin:
                continue
            if cur_plugin in plugin:
                yield(cur_plugin)

    def _get_dependent_plugins(self, plugin):
        return list(self._iter_dependent_plugins(plugin))

    def get_plugins_sorted(self):
        """
        Sorting plugins is hard since their dependencies are tree-like and using
        recursively to traverse this tree can cause performance issues.
        For this reason, implementing __cmp__ in the Plugin type is not enough, we need to be aware
        of all the other plugins to correctly sort them.
        IK ->            -> Arm
             \          /
              -> Limb ->
             /          \
        FK ->            -> Leg
        :return:
        """
        plugins = self.get_plugins()
        dirty_plugins = copy.copy(plugins)
        result = []

        def is_leaf(plugin):
            for p in dirty_plugins:
                # Ignore self
                if p is plugin:
                    continue
                # If the plugin is used somewhere, it is not a leaf.
                if plugin in p:
                    return False
            return True

        while dirty_plugins:
            # Find any plugins that have no dependencies.
            for i in reversed(range(len(dirty_plugins))):
                plugin = dirty_plugins[i]
                if is_leaf(plugin):
                    result.append(dirty_plugins.pop(i))

        return list(reversed(result))

    # def _extend_dependent_plugins(self, src_plugins):
    #     other_plugins = [plugin for plugin in self.iter_plugins() if not plugin in src_plugins]
    #
    #     result = copy.copy(src_plugins)
    #     for plugin in src_plugins:
    #         for other_plugin in other_plugins:
    #             if plugin in other_plugin:
    #                 result.append(other_plugin)
    #     return sorted(result)

    def get_summary(self):
        header_row = ('TYPE', 'NAME', 'DESC', 'STATUS')

        # Build rows
        rows = []
        for plugin in self.get_plugins():
            rows.append(
                (plugin.type_name, plugin.name, plugin.description or '', plugin.status)
            )
        rows = sorted(rows)

        # Resolve column_widths
        column_widths = []
        for i, header_cell in enumerate(header_row):
            width = max(len(row[i]) for row in rows)
            width = max(len(header_cell), width)
            column_widths.append(width)

        # Print rows
        format_str = '| {0} |'.format(' | '.join('{{{0}:{1}}}'.format(i, width) for i, width in enumerate(column_widths)))
        print(format_str.format(*header_row))
        for row in rows:
            print(format_str.format(*row))


class ModulePluginType(PluginType):
    type_name = 'modules'

class RigPluginType(PluginType):
    type_name = 'rigs'

# class UnitTestPluginType(PluginType):
#     type_name = 'tests'

def initialize():
    # Ensure paths in OMTK_PLUGINS is in the sys.path so they will get loaded.
    plugin_dirs = os.environ.get('OMTK_PLUGINS', '').split(os.pathsep)
    plugin_dirs = filter(None, plugin_dirs)
    for path in plugin_dirs:
        if not path in sys.path:
            log.info("Adding to sys.path {0}".format(path))
            sys.path.append(path)

    pm = PluginManager()
    pm.register_plugin_type(ModulePluginType)
    pm.register_plugin_type(RigPluginType)
    #pm.register_plugin_type(UnitTestPluginType)
    return pm

plugin_manager = initialize()
