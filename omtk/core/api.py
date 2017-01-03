import os
import re
import contextlib
import logging

import libSerialization
import pymel.core as pymel
from omtk.libs import libPymel
from omtk.libs import libPython

log = logging.getLogger('omtk')
log.setLevel(logging.DEBUG)

__all__ = (
    'get_version',
    'create',
    'find',
    'find_one',
    'build_all',
    'unbuild_all',
    'build_selected',
    'unbuild_selected',
    'calibrate_selected'
)

@libPython.memoized
def get_version():
    """
    Read the REZ package associated with the project and return the current version.
    This is used to analyze old rigs and recommend specific scripts to correct them if needed.
    :return:
    """
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'package.py'))
    if not os.path.exists(package_path):
        raise Exception("Cannot find package file! {}".format(package_path))
    regex_getversion = re.compile('^version *= [\'|"]*([0-9\.]*)[\'|"]$')
    with open(package_path, 'r') as fp:
        for line in fp:
            line = line.strip('\n')
            result = regex_getversion.match(line)
            if result:
                result = next(iter(result.groups()))
                return result

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
    rigs = find()
    for rig in rigs:
        network = rig._network  # monkey-patched by libSerialization
        if rig.build(strict=strict):
            pymel.delete(network)
            libSerialization.export_network(rig)


# @libPython.profiler
@libPython.log_execution_time('unbuild_all')
def unbuild_all(strict=False):
    rigs = find()
    for rig in rigs:
        network = rig._network  # monkey-patched by libSerialization
        if rig.unbuild(strict=strict):
            pymel.delete(network)
            network = libSerialization.export_network(rig)


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

    def fn_skip(network):
        return libSerialization.is_network_from_class(network, 'Rig')

    if sel is None:
        sel = pymel.selected()

    # Resolve the rig network from the selection

    module_networks = libSerialization.get_connected_networks(sel, key=is_module_child_of_rig, key_skip=fn_skip)
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

        def can_build_module(module):
            if module.is_built():
               return False

            try:
                module.validate()
                return True
            except Exception, e:
                pymel.warning("Can't build {0}: {1}".format(module.name, str(e)))
                return False

        modules = [module for module in modules if can_build_module(module)]
        if not modules:
            return

        # Build selected modules
        rig.pre_build()
        for module in modules:
            if can_build_module(module):
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

        # Build selected modules
        modules = [module for module in modules if module.is_built()]
        if not modules:
            return

        for module in modules:
            module.unbuild()

        # Re-export network
        if hasattr(rig, '_network'):
            pymel.delete(rig._network)
        libSerialization.export_network(rig)


# def rebuild_selection():
#     with with_preserve_selection():
#         rig, modules = _get_modules_from_selection()
#         if not rig or not modules:
#             return
#
#         for module in modules:
#             if module.is_built():
#                 module.unbuild()
#             module.build()
#
#         if hasattr(rig, '_network'):
#             pymel.delete(rig._network)
#         libSerialization.export_network(rig)


def calibrate_selected(sel=None):
    rig, modules = _get_modules_from_selection()
    # Build selected modules
    for module in modules:
        if hasattr(module, 'calibrate') and hasattr(module.calibrate, '__call__'):
            module.calibrate()
