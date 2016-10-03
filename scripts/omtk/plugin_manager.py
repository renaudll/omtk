import os
import sys
import importlib
import pkgutil
import logging
log = logging.getLogger('omtk')
from omtk.libs import libPython

class PluginStatus:
    Loaded = 'Loaded'
    Unloaded = 'Unloaded'
    Failed = 'Failed'

class Plugin(object):
    root_package_name = 'omtk'

    def __init__(self, name, type_name):
        self.name = name
        self.type_name = type_name
        self.module = None
        self.cls = None
        self.status = PluginStatus.Unloaded
        self.description = None

        self.load()

    def load(self):
        self.cls = None
        self.module = None
        self.description = None

        # Resolve full module path
        module_path = '{0}.{1}.{2}'.format(self.root_package_name, self.type_name, self.name)

        try:
            # Load/Reload module
            log.debug("Loading module {0}".format(module_path))
            self.module = pkgutil.get_loader(module_path).load_module(module_path)

            # Ensure there is a register_plugin function
            if not hasattr(self.module, 'register_plugin') or not hasattr(self.module.register_plugin, '__call__'):
                raise Exception("Cannot register plugin {0}. No register_plugin function found!".format(
                    self.name
                ))

            # Get module class
            self.cls = self.module.register_plugin()
            self.description = self.cls.__doc__
            self.status = PluginStatus.Loaded
        except Exception, e:
            self.status = PluginStatus.Failed
            self.description = str(e)
            log.warning("Plugin {0} failed to load! {0}".format(self.name, self.description))

    @classmethod
    def from_module(cls, name, type_name):
        plugin = Plugin(name, type_name=type_name)
        return plugin

    def __repr__(self):
        return '<Plugin "{0}">'.format(self.name)

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
        log.debug("Checking {0}".format(package_name))
        #package = importlib.import_module(package_name)
        package = pkgutil.get_loader(package_name).load_module(package_name)
        for loader, modname, ispkg in pkgutil.walk_packages(package.__path__):
            log.debug("Found plugin {0}".format(modname))
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

    def iter_plugins(self):
        for plugin_type in self._plugin_types.values():
            for plugin in plugin_type()._plugins:
                yield plugin

    def get_plugins(self):
        return list(self.iter_plugins())

    def reload_all(self):
        for plugin in self.iter_plugins():
            plugin.load()

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


class ModulePlugin(PluginType):
    type_name = 'modules'

class RigPlugin(PluginType):
    type_name = 'rigs'

# Ensure paths in OMTK_PLUGINS is in the sys.path so they will get loaded.
for path in os.environ.get('OMTK_PLUGINS', '').split(os.pathsep):
    if not path in sys.path:
        log.info("Adding to sys.path {0}".format(path))
        sys.path.append(path)

plugin_manager = PluginManager()
plugin_manager.register_plugin_type(ModulePlugin)
plugin_manager.register_plugin_type(RigPlugin)
