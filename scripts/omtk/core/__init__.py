from api import *
from omtk.core import plugin_manager

# Load plugins
plugin_manager.plugin_manager.get_plugins()  # force evaluating lazy singleton (todo: remove it?)
