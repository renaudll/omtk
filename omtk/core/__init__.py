import contextlib
import functools
import inspect
import json
import logging
import os

import utils
import constants
import classCtrl
import classModule
import className
import classNode
import classRig
import libSerialization
import pymel.core as pymel
from omtk.libs import libPymel
from omtk.libs import libPython
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
    reload(constants)
    reload(utils)
    reload(className)
    reload(classNode)
    reload(classCtrl)
    reload(classModule)
    reload(classRig)

    import plugin_manager
    reload(plugin_manager)
    plugin_manager.plugin_manager.reload_all()

    import preferences
    reload(preferences)


def create(*args, **kwargs):
    from omtk.core import preferences
    cls = preferences.preferences.get_default_rig_class()
    return cls(*args, **kwargs)


def find():
    """
    :return: All the rigs embedded in the current maya scene.
    """
    # TODO: Find why when a scene is open for a long time, this function is slower
    networks = libSerialization.get_networks_from_class('Rig')
    results = [libSerialization.import_network(network, module='omtk') for network in networks]
    results = filter(None, results)  # Prevent un-serializable networks from passing through.
    return results


def find_one():
    """
    :return: The first rig embedded in the current maya scene.
    """
    return next(iter(find()), None)


# @libPython.profiler
@libPython.log_execution_time('build_all')
def build_all(strict=False):
    """
    Build all the rigs embedded in the current maya scene.
    """
    networks = libSerialization.get_networks_from_class('Rig')
    for network in networks:
        rigroot = libSerialization.import_network(network)
        if not rigroot:
            log.warning("Error importing rig network {0}".format(network))
            continue
        if rigroot.build(strict=strict):
            pymel.delete(network)
            libSerialization.export_network(rigroot)


# @libPython.profiler
@libPython.log_execution_time('unbuild_all')
def unbuild_all(strict=False):
    networks = libSerialization.get_networks_from_class('Rig')
    for network in networks:
        rigroot = libSerialization.import_network(network)
        if not rigroot:
            log.warning("Error importing rig network {0}".format(network))
            continue
        rigroot.unbuild(strict=strict)
        pymel.delete(network)
        # Write changes to scene
        network = libSerialization.export_network(rigroot)
        pymel.select(network)


def _get_modules_from_selection(sel=None):
    def get_rig_network_from_module(network):
        for plug in network.message.outputs(plugs=True):
            plug_node = plug.node()
            if not isinstance(plug_node, pymel.nodetypes.Network):
                continue
            if libSerialization.is_network_from_class(plug_node, 'Rig'):
                return plug_node
        return None

    def is_module_child_of_rig(network):
        """
        Allow us to recognize module directly connected to a 'Rig' network.
        This way we can ignore 'sub-modules' (ex: individual avars)
        :param network: The network to analyse.
        :return: True if the network is directly connected to a 'Rig' network.
        """
        return get_rig_network_from_module(network) is not None

    if sel is None:
        sel = pymel.selected()

    # Resolve the rig network from the selection
    module_networks = libSerialization.get_connected_networks(sel, key=is_module_child_of_rig)
    if not module_networks:
        pymel.warning("Found no module related to selection.")
        return None, None

    # Resolve rig
    rig_networks = set()
    for module in module_networks:
        rig_network = get_rig_network_from_module(module)
        rig_networks.add(rig_network)
    rig_network = next(iter(rig_networks), None)
    if not rig_network:
        pymel.warning("Found no rig related to selection.")
        return None, None

    # Deserialize the rig and find the associated networks
    rig = libSerialization.import_network(rig_network)
    modules = []
    for module in rig.modules:
        if module._network in module_networks:
            modules.append(module)

    return rig, modules

@contextlib.contextmanager
def with_preserve_selection():
    sel = pymel.selected()
    yield True
    sel = filter(libPymel.is_valid_PyNode, sel)
    if sel:
        pymel.select(sel)
    else:
        pymel.select(clear=True)


def build_selected(sel=None):
    with with_preserve_selection():
        rig, modules = _get_modules_from_selection()
        if not rig or not modules:
            return

        is_module_unbuilt = lambda x: not x.is_built()
        modules = filter(is_module_unbuilt, modules)

        def can_build_module(module):
            try:
                module.validate()
                return True
            except Exception, e:
                pymel.warning("Can't build {0}: {1}".format(module.name, str(e)))
                return False

        modules = filter(can_build_module, modules)

        if not modules:
            return

        # Build selected modules
        rig.pre_build()
        for module in modules:
            module.build()
            rig.post_build_module(module)

        # Re-export network
        if hasattr(rig, '_network'):
            pymel.delete(rig._network)
        libSerialization.export_network(rig)


def unbuild_selected(sel=None):
    with with_preserve_selection():
        rig, modules = _get_modules_from_selection()
        if not rig or not modules:
            return

        is_module_built = lambda x: x.is_built()
        modules = filter(is_module_built, modules)

        # Build selected modules
        for module in modules:
            module.unbuild()

        # Re-export network
        if hasattr(rig, '_network'):
            pymel.delete(rig._network)
        libSerialization.export_network(rig)


def calibrate_selected(sel=None):
    rig, modules = _get_modules_from_selection()
    # Build selected modules
    for module in modules:
        if hasattr(module, 'calibrate') and hasattr(module.calibrate, '__call__'):
            module.calibrate()
