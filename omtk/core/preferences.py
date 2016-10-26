"""
Provide a Preference class to store the user preferences of the local installation.
"""
import os
import inspect
import json
import logging
log = logging.getLogger('omtk')

CONFIG_FILENAME = 'config.json'

def get_path_preferences():
    """
    :return: The search path of the configuration file.
    """
    current_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
    config_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
    config_path = os.path.join(config_dir, CONFIG_FILENAME)
    return config_path

class Preferences(object):
    def __init__(self):
        self.default_rig = None

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

    def get_default_rig_class(self):
        from omtk.core import plugin_manager
        if self.default_rig:
            for plugin in plugin_manager.plugin_manager.iter_loaded_plugins_by_type('rigs'):
                if plugin.cls.__name__ == self.default_rig:
                    return plugin.cls
            log.warning("Can't find default rig type {0}.".format(self.default_rig))

        # If no match is found, return the base implementation
        from omtk.core import classRig
        return classRig.Rig

preferences = Preferences()
preferences.load()
