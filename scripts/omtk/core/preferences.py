"""
Provide a Preference class to store the user preferences of the local installation.
"""
import os
import inspect
import json
import logging

from omtk.core import constants

log = logging.getLogger("omtk")

CONFIG_FILENAME = "config.json"


def get_path_preferences():
    """
    :return: The search path of the configuration file.
    """
    current_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
    config_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
    config_path = os.path.join(config_dir, CONFIG_FILENAME)
    return config_path


class Preferences(object):
    def __init__(self):
        self.default_rig = None
        self.hide_welcome_screen = True

    def save(self, path=None):
        if path is None:
            path = get_path_preferences()

        data = self.__dict__
        with open(path, "w") as fp:
            json.dump(data, fp)

    def load(self, path=None):
        if path is None:
            path = get_path_preferences()

        if not path or not os.path.exists(path):
            log.warning("Can't find config file. Using default config.")
            return

        with open(path, "r") as fp:
            data = json.load(fp)
            self.__dict__.update(data)

    def get_default_rig_class(self):
        try:
            from maya import cmds
        except ImportError:
            return None

        from omtk.core import plugin_manager

        # Listen to an environment variable to drive the default rig for specific projects.
        default_rig = self.default_rig

        default_rig_override = os.environ.get(constants.EnvironmentVariables.OMTK_DEFAULT_RIG, None)
        if default_rig_override:
            default_rig = default_rig_override

        if default_rig:
            for plugin in plugin_manager.plugin_manager.iter_loaded_plugins_by_type("rigs"):
                if plugin.cls.__name__ == default_rig:
                    return plugin.cls
            log.warning("Can't find default rig type %s.", default_rig)

        # If no match is found, return the base implementation
        from omtk.core import rig

        return rig.Rig

    def _get_config_nodegraph_raw(self):
        # todo: refactor preference class to better handle categories?
        try:
            dirname = get_path_preferences()
            path = os.path.abspath(os.path.join(dirname, "..", "python", "config_nodegraph.json"))
            if not os.path.exists(path):
                raise Exception("Configure file does not exist. {0}".format(path))
            with open(path, "r") as fp:
                return json.load(fp)
        except Exception as e:
            log.error("Error loading nodegraph_unit_tests configuration files: {0}".format(e))
            return {}

    def get_nodegraph_default_attr_map(self):
        return self._get_config_nodegraph_raw().get("interesting_attributes", {})

    def get_nodegraph_blacklisted_nodetypes(self):
        return self._get_config_nodegraph_raw().get("_blacklisted_node_types", [])

    def get_nodegraph_blacklisted_node_names(self):
        return self._get_config_nodegraph_raw().get("_blacklisted_node_names", [])

    def get_nodegraph_blacklisted_port_names(self):
        data = self._get_config_nodegraph_raw()
        return set(data.get("_blacklisted_port_names", [])) | set(constants.BLACKLISTED_PORT_NAMES)

    # def get_default_rig_class(self):
    #     from omtk.core import plugin_manager
    #
    #     # Listen to an environment variable to drive the default rig for specific projects.
    #     default_rig = self.default_rig if self.default_rig else 'RigStandard'
    #
    #     default_rig_override = os.environ.get(constants.EnvironmentVariables.OMTK_DEFAULT_RIG, None)
    #     if default_rig_override:
    #         default_rig = default_rig_override
    #
    #     if default_rig:
    #         for plugin in plugin_manager.plugin_manager.iter_loaded_plugins_by_type('rigs'):
    #             if plugin.cls.__name__ == default_rig:
    #                 return plugin.cls
    #         log.warning("Can't find default rig type {0}.".format(default_rig))
    #
    #     raise Exception("No Rig definition found!")


preferences = Preferences()
preferences.load()
