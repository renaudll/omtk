import inspect
import json
import logging
import os

from api import *
from . import plugin_manager

log = logging.getLogger('omtk')
log.setLevel(logging.DEBUG)

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


def _reload():
    import classComponent
    import classComponentAction
    import classComponentAttribute
    import classCtrl
    import classModule
    import classModuleAvarLogic
    import classModuleCtrlLogic
    import classModuleMap
    import classNomenclature
    import classNode
    import classRig

    reload(api)  # this won't reload functions imported in the main module. Use api directly if you are debugging it.
    reload(classNomenclature)
    reload(classComponent)
    reload(classComponentAction)
    reload(classComponentAttribute)
    reload(classNode)
    reload(classCtrl)
    reload(classModule)
    reload(classModuleAvarLogic)
    reload(classModuleCtrlLogic)
    reload(classModuleMap)
    reload(classRig)

    import plugin_manager
    reload(plugin_manager)
    plugin_manager.plugin_manager.reload_all()

    import preferences
    reload(preferences)
