import os
import re
import contextlib
import logging

import pymel.core as pymel
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.vendor import libSerialization

_PACKAGE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),  # /script/omtk/core/
        "..",  # /script/omtk
        "..",  # /script/
        "..",  # /
        "package.py",  # /package.py
    )
)

log = logging.getLogger("omtk")
log.setLevel(logging.DEBUG)

__all__ = (
    "get_version",
    "create",
    "find",
    "find_one",
    "build_all",
    "unbuild_all",
    "build_selected",
    "unbuild_selected",
    "calibrate_selected",
    "build_modules_by_type",
    "unbuild_modules_by_type",
    "rebuild_modules_by_type",
    "run_macro",
)


def get_version():
    """
    Return the current omtk version.
    This is used to analyze old rigs and
    recommend specific scripts to correct them if needed.
    :return: A PEP0396 compliant version string
    :rtype: str
    """
    import omtk

    return omtk.__version__


def create(*args, **kwargs):
    from omtk.core import preferences

    cls = preferences.preferences.get_default_rig_class()
    return cls(*args, **kwargs)


def find():
    """
    :return: All the rigs embedded in the current maya scene.
    """
    from omtk.vendor import libSerialization

    # TODO: Find why when a scene is open for a long time, this function is slower
    networks = libSerialization.get_networks_from_class("Rig")
    results = [
        libSerialization.import_network(network, module="omtk") for network in networks
    ]
    results = filter(
        None, results
    )  # Prevent un-serializable networks from passing through.
    return results


def find_one():
    """
    :return: The first rig embedded in the current maya scene.
    """
    return next(iter(find()), None)


# @libPython.profiler
@libPython.log_execution_time("build_all")
def build_all(strict=False):
    """
    Build all the rigs embedded in the current maya scene.
    """
    from omtk.vendor import libSerialization

    rigs = find()
    for rig in rigs:
        network = rig._network  # monkey-patched by libSerialization
        if rig.build(strict=strict):
            pymel.delete(network)
            libSerialization.export_network(rig)


# @libPython.profiler
@libPython.log_execution_time("unbuild_all")
def unbuild_all(strict=False):
    from omtk.vendor import libSerialization

    rigs = find()
    for rig in rigs:
        network = rig._network  # monkey-patched by libSerialization
        if rig.unbuild(strict=strict):
            pymel.delete(network)
            libSerialization.export_network(rig)


def _iter_modules_by_type(module_type):
    """
    Yield all modules in the scene having a specific type.
    :param module_type: A type (ex: Module.FaceJaw)
    :yield: Module instances
    """
    rigs = find()
    for rig in rigs:
        yield rig, _iter_rig_modules_by_type(rig, module_type)


def _iter_rig_modules_by_type(rig, module_type):
    """
    Yield all modules in a provided rig having a specific type.
    :param rig: The rig to analyse.
    :param module_type: A type (ex: Module.FaceJaw)
    :yield: Module instances
    """
    for module in rig.modules:
        if isinstance(module, module_type):
            yield module


def _get_modules_from_selection(sel=None):
    from omtk.vendor import libSerialization

    def get_rig_network_from_module(network):
        for plug in network.message.outputs(plugs=True):
            plug_node = plug.node()
            if not isinstance(plug_node, pymel.nodetypes.Network):
                continue
            if libSerialization.is_network_from_class(plug_node, "Rig"):
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
        return libSerialization.is_network_from_class(network, "Rig")

    if sel is None:
        sel = pymel.selected()

    # Resolve the rig network from the selection

    module_networks = libSerialization.get_connected_networks(
        sel, key=is_module_child_of_rig, key_skip=fn_skip
    )
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


def build_selected():
    """
    Resolve modules related to the selection and build them.
    """
    with with_preserve_selection():
        rig, modules = _get_modules_from_selection()
        if not rig or not modules:
            return

        modules = [module for module in modules if not module.is_built()]
        if not modules:
            return

        rig.build(modules=modules)

        # Re-export network
        if hasattr(rig, "_network"):
            pymel.delete(rig._network)
        libSerialization.export_network(rig)


def build_modules_by_type(module_type):
    for rig, modules in _iter_modules_by_type(module_type):
        modules = [module for module in modules if not module.is_built()]
        if not modules:
            continue

        rig.build(modules=modules)

        # Re-export network
        if hasattr(rig, "_network"):
            pymel.delete(rig._network)
        libSerialization.export_network(rig)


def unbuild_modules_by_type(module_type):
    for rig, modules in _iter_modules_by_type(module_type):
        modules = [module for module in modules if module.is_built()]
        if not modules:
            continue

        for module in modules:
            module.unbuild()

        # Re-export network
        if hasattr(rig, "_network"):
            pymel.delete(rig._network)
        libSerialization.export_network(rig)


def rebuild_modules_by_type(module_type):
    for rig, modules in _iter_modules_by_type(module_type):
        modules = list(modules)
        if not modules:
            continue

        for module in modules:
            if module.is_built():
                module.unbuild()

        rig.build(modules=modules)

        # Re-export network
        if hasattr(rig, "_network"):
            pymel.delete(rig._network)
        libSerialization.export_network(rig)


def unbuild_selected(sel=None):
    from omtk.vendor import libSerialization

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
        if hasattr(rig, "_network"):
            pymel.delete(rig._network)
        libSerialization.export_network(rig)


def calibrate_selected(sel=None):
    rig, modules = _get_modules_from_selection()
    # Build selected modules
    for module in modules:
        if hasattr(module, "calibrate") and hasattr(module.calibrate, "__call__"):
            module.calibrate()


def _get_macro_by_name(macro_name):
    from omtk.core import plugin_manager

    pm = plugin_manager.plugin_manager

    for macro in pm.iter_loaded_plugins_by_type(
        plugin_manager.MacroPluginType.type_name
    ):
        if macro.module_name == macro_name:
            return macro.cls()


def run_macro(macro_name):
    macro = _get_macro_by_name(macro_name)
    if not macro:
        pymel.warning("Cannot find macro with name %s" % macro_name)
        return
    macro.run()
