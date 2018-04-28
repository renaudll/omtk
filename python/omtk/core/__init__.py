import inspect
import json
import logging
import os

from . import plugin_manager

log = logging.getLogger('omtk')
log.setLevel(logging.INFO)

# Load configuration file
# Currently this only allow the default rig class from being used.
config = {}
config_dir = os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), '..'))
config_path = os.path.join(config_dir, 'config.json')
if os.path.exists(config_path):
    with open(config_path) as fp:
        config = json.load(fp)

# Load plugins
plugin_manager.plugin_manager.get_plugins()  # force evaluating lazy singleton (todo: remove it?)


def reload_():
    import entity
    import entity_action
    import entity_attribute
    import component_definition
    import component
    import component_scripted
    import component_registry
    import ctrl
    import module
    import module_logic_avar
    import module_logic_ctrl
    import module_map
    import nomenclature
    import node
    import rig

    reload(nomenclature)
    reload(entity)
    reload(entity_action)
    reload(entity_attribute)
    reload(component_definition)
    reload(component)
    reload(component_scripted)
    reload(component_registry)
    reload(node)
    reload(ctrl)
    reload(module)
    reload(module_logic_avar)
    reload(module_logic_ctrl)
    reload(module_map)
    reload(rig)

    import plugin_manager
    reload(plugin_manager)
    plugin_manager.plugin_manager.reload_all()

    import preferences
    reload(preferences)
