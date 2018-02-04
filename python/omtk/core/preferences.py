"""
Provide a Preference class to store the user preferences of the local installation.
"""
import os
import inspect
import json
import logging
from omtk.libs import libPython

log = logging.getLogger('omtk')

from omtk import constants

CONFIG_FILENAME = 'config.json'

@libPython.memoized
def _get_path_config_dir():
    current_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
    config_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
    return config_dir

@libPython.memoized
def get_path_preferences():
    """
    :return: The search path of the configuration file.
    """
    config_dir = _get_path_config_dir()
    config_path = os.path.join(config_dir, CONFIG_FILENAME)
    log.info('Preference path is {0}'.format(config_path))
    return config_path


class Preferences(object):
    def __init__(self):
        self.default_rig = None
        self.hide_welcome_screen = True

    def save(self, path=None):
        if path is None:
            path = get_path_preferences()

        data = self.__dict__
        with open(path, 'w') as fp:
            json.dump(data, fp)

    def load(self, path=None):
        if path is None:
            path = get_path_preferences()

        if not path or not os.path.exists(path):
            log.warning("Can't find config file. Using default config.")
            return

        with open(path, 'r') as fp:
            data = json.load(fp)
            self.__dict__.update(data)

    @libPython.memoized
    def _get_config_nodegraph_raw(self):
        # todo: refactor preference class to better handle categories?
        try:
            dirname = _get_path_config_dir()
            path = os.path.abspath(os.path.join(dirname, '..', 'python', 'config_nodegraph.json'))
            if not os.path.exists(path):
                raise Exception("Configure file does not exist. {0}".format(path))
            with open(path, 'r') as fp:
                return json.load(fp)
        except Exception, e:
            log.error('Error loading nodegraph configuration files: {0}'.format(e))
            return {}

    def get_nodegraph_default_attr_map(self):
        return self._get_config_nodegraph_raw().get('interesting_attributes', {})

    def get_nodegraph_blacklisted_nodetypes(self):
        return self._get_config_nodegraph_raw().get('blacklisted_nodetypes', [])

    def get_default_rig_class(self):
        from omtk.core import plugin_manager

        # Listen to an environment variable to drive the default rig for specific projects.
        default_rig = self.default_rig if self.default_rig else 'RigStandard'

        default_rig_override = os.environ.get(constants.EnvironmentVariables.OMTK_DEFAULT_RIG, None)
        if default_rig_override:
            default_rig = default_rig_override

        if default_rig:
            for plugin in plugin_manager.plugin_manager.iter_loaded_plugins_by_type('rigs'):
                if plugin.cls.__name__ == default_rig:
                    return plugin.cls
            log.warning("Can't find default rig type {0}.".format(default_rig))

        raise Exception("No Rig definition found!")




# todo: remove any other references to get_preferences() than in session
@libPython.memoized
def get_preferences():
    preferences = Preferences()
    preferences.load()
    return preferences
