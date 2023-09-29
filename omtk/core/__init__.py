import inspect
import json
import logging
import os

from . import utils
from . import classCtrl
from . import classCtrlModel
from . import classModule
from . import classModuleMap
from . import classModuleCompound
from . import className
from . import classNode
from . import classRig
from .api import *
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