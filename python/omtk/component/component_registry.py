"""
Handle scanning and handling of saved _known_definitions.
"""
import logging
import os

from omtk import decorators
from omtk.component import component_definition
from omtk.exceptions import MultipleComponentDefinitionError

if False:  # for type hinting
    from typing import List, Generator, Union
    from omtk.component import Component
    from omtk.component.component_definition import ComponentDefinition

log = logging.getLogger(__name__)

def get_default_components_dir():
    """Return the directory to save component to."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'components'))


class ComponentRegistry(object):
    def __init__(self, paths=None):
        self.paths = paths if paths else [get_default_components_dir()]

        # Determine where new _known_definitions will be registered.
        self.primary_path = next(iter(self.paths), None)

        self._known_definitions = []

        self.scan()

    def scan(self):
        self._known_definitions = [c for c in self._scan()]

    def _scan(self):
        known = set()

        for path_dir in self.paths:
            log.info('Searching component in {0}'.format(path_dir))
            if not os.path.exists(path_dir):
                continue

            for filename in os.listdir(path_dir):
                basename, ext = os.path.splitext(filename)
                if ext != '.ma':
                    continue
                path = os.path.join(path_dir, filename)

                log.debug('Creating ComponentDefinition from {0}'.format(path))
                component_def = component_definition.ComponentDefinition.from_file(path)
                if not component_def:
                    continue

                key = hash((component_def.uid, component_def.version))
                if key in known:
                    raise MultipleComponentDefinitionError(
                        "Found more than two component with the same uid and version: {0}".format(
                            component_def
                        )
                    )
                known.add(key)

                log.debug('Registering {0} from {1}'.format(component_def, path))
                yield component_def

        from omtk.core import plugin_manager
        pm = plugin_manager.plugin_manager

        log.info("Scanning for ComponentScripted")
        for plugin in pm.get_loaded_plugins_by_type(plugin_manager.ComponentScriptedType.type_name):
            component_def = plugin.cls.get_definition()
            log.debug('Registering {0} from {1}'.format(component_def, plugin))
            yield component_def

        # log.info("Searching modules")
        # for plugin in pm.get_loaded_plugins_by_type(plugin_manager.ModulePluginType.type_name):
        #     try:
        #         component_def = plugin.cls.get_definition()
        #     except AttributeError, e:
        #         log.warning("Error obtaining plugin class definition for {0}: {1}".format(plugin, e))
        #         continue
        #     log.debug('Registering {0} from {1}'.format(component_def, plugin))
        #     yield component_def

    def get_path_from_component_def(self, inst_def):
        dirname = self.primary_path
        filename = '{0}-{1}.ma'.format(inst_def.name, inst_def.version)
        path = os.path.join(dirname, filename)
        return path

    def register(self, inst, inst_def):
        # type: (Component, ComponentDefinition) -> str
        path = self.get_path_from_component_def(inst_def)
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            raise Exception("Can't register component. Destination directory does not exist. {0}".format(dirname))
        if os.path.exists(path):
            raise Exception("Can't register component. File already exist. {0}".format(path))

        inst_def.path = path  # hack?
        inst.set_definition(inst_def)  # Ensure the definition is set
        inst.export(path)
        self._known_definitions.append(inst_def)
        return path

    def _iter_component_versions(self, search_def):
        # type: (ComponentDefinition) -> Generator[ComponentDefinition]
        """Resolve all the available versions for a specific component."""
        for component_def in self._known_definitions:
            if component_def.uid == search_def.uid:
                yield component_def

    def get_component_versions(self, search_def):
        # type: (ComponentDefinition) -> List[ComponentDefinition]
        """Resolve all the available versions for a specific component. Values are in decreasing version order."""
        return list(reversed(sorted(self._iter_component_versions(search_def), key=lambda x: x.version)))

    def get_latest_component_version(self, search_def):
        # type: (ComponentDefinition) -> ComponentDefinition
        return next(iter(self.get_component_versions(search_def)), None)

    def is_latest_component_version(self, search_def):
        # type: (ComponentDefinition) -> bool
        """Check if a component need to be updated. Return True if an update is needed, False otherwise."""
        # todo: check timestamp instead of version number?
        latest_def = self.get_latest_component_version(search_def)
        return latest_def is not None and search_def == latest_def

    def get_latest_component_definition_by_name(self, name):
        # type: (str) -> Union[ComponentDefinition,None]
        """
        Return the latest component matching the provided name.
        :param name: The name to match.
        :return: A ComponentDefinition.
        """
        latest_version = None
        latest_definition = None
        for cur_def in self._known_definitions:
            if cur_def.name == name and (latest_version is None or latest_version < cur_def.version):
                latest_version = cur_def.version
                latest_definition = cur_def
        return latest_definition

    def get_component_definitions(self):
        return self._known_definitions


@decorators.memoized
def get_registry():
    return ComponentRegistry()
