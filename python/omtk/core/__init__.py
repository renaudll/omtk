import inspect
import json
import logging
import os

from . import plugin_manager

log = logging.getLogger(__name__)
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
