import contextlib
import functools
import inspect
import json
import logging
import os

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
    networks = libSerialization.getNetworksByClass('Rig')
    return [libSerialization.import_network(network, module='omtk') for network in networks]


def find_one(*args, **kwargs):
    return next(iter(find(*args, **kwargs)), None)


# @libPython.profiler
@libPython.log_execution_time('build_all')
def build_all(strict=False):
    """
    Build all the rigs embedded in the current maya scene.
    """
    networks = libSerialization.getNetworksByClass('Rig')
    for network in networks:
        rigroot = libSerialization.import_network(network)
        if rigroot.build(strict=strict):
            pymel.delete(network)
            libSerialization.export_network(rigroot)


# @libPython.profiler
@libPython.log_execution_time('unbuild_all')
def unbuild_all(strict=False):
    networks = libSerialization.getNetworksByClass('Rig')
    for network in networks:
        rigroot = libSerialization.import_network(network)
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
            if libSerialization.isNetworkInstanceOfClass(plug_node, 'Rig'):
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
    module_networks = libSerialization.getConnectedNetworks(sel, key=is_module_child_of_rig)
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


def patch_spaceswitch_data_into_network(sel=None):
    if sel is None:
        sel = pymel.selected()

    networks = libSerialization.getConnectedNetworks(sel, key=lambda
        net: libSerialization.isNetworkInstanceOfClass(net, 'BaseCtrl'))

    for net in networks:
        ctrl_instance = libSerialization.import_network(net)
        data = ctrl_instance.get_spaceswitch_enum_targets()

        if data:
            # Create missing attributes if needed
            if not net.hasAttr('targets_indexes'):
                log.info('targets_indexes attribute is missing on network {0}. It will be created'.format(net))
                pymel.addAttr(net, longName='targets_indexes', at='long', multi=True)
            if not net.hasAttr('targets'):
                log.info('targets attribute is missing on network {0}. It will be created'.format(net))
                pymel.addAttr(net, longName='targets', at='message', multi=True)
            if not net.hasAttr('local_index'):
                log.info('targets_indexes attribute is missing on network {0}. It will be created'.format(net))
                pymel.addAttr(net, longName='local_index', at='long')

            # Add data if needed
            for index, (name, obj) in data.items():
                target_data = net.targets.get()
                indexes_data = net.targets_indexes.get()
                if obj not in target_data:
                    if index not in indexes_data:
                        if obj is not None:
                            log.info('Patching network {0} space switch data named {1} - Index {2} on object {3}'
                                     .format(net.name(), name, index, obj))
                            pymel.connectAttr(obj.message, net.targets[len(target_data)])
                            net.targets_indexes[len(target_data)].set(index)
                        elif name == 'Local':
                            log.info('Patching network {0} space switch data named {1} - Index {2} as local index'
                                     .format(net.name(), name, index))
                            net.local_index.set(index)
                    else:
                        if obj is not None:
                            log.warning('Object {0} have not been found in attribute targets but index {1} yes.'
                                        'This object will not be patched to prevent any index conflict. '
                                        'Look at your data to understand'.format(obj, index))
                else:
                    log.info('Space Switch object {0} is already included in the targets attributes'.format(obj))


def patch_spaceswitch_object_into_network():
    """
    This function is not clean, but it can be used to generate spaceswitch object for certain module and after look at
    all space switch target information to replace to space switch object target that could used a ctrl to the new space
    switch object that will not be removed after an unbuild
    """
    import omtk  # Import omtk to be able to do isinstance os certain module

    # Get the rig instance in the scene (Now support only the first one found
    rig_net = libSerialization.getNetworksByClass('Rig')[0]
    rig_instance = libSerialization.import_network(rig_net)

    # Get all the module that we could need to patch
    to_patch = [module for module in rig_instance.modules if isinstance(module, omtk.modules.rigDpSpine.DpSpine) or
                isinstance(module, omtk.modules.rigLimb.Limb)]
    # Get through all the modules to patch and replace space switch connection from the ctrl to the space switch object
    for module in to_patch:
        module_to_patch = module
        # If we have a limb, we want to patch the ik system
        if isinstance(module, omtk.modules.rigLimb.Limb):
            module_to_patch = module.sysIK
        # Generate the space switch objects first if needed
        module_to_patch.setup_spaceswitch_objects(rig_instance)

    pymel.delete(rig_net)
    libSerialization.export_network(rig_instance)

    for module in to_patch:
        module_to_patch = module
        # If we got an ik, we need to check if the ik ctrl is used as a space switch target somewhere
        if isinstance(module_to_patch, omtk.modules.rigIK.IK):
            # Find all connection that have from the ctrl ik and replace it
            connected_to_ik = module_to_patch.ctrl_ik.node.message.outputs(s=False, d=True, p=True)
            for connection in connected_to_ik:
                attr_name = connection.shortName()
                if attr_name.find('targets') >= 0:  # Not sexy, but it work
                    log.info('Reconnecting {0} from {1} to space switch node {2}'
                             .format(connection, module_to_patch.ctrl_ik, module_to_patch.ctrl_ik_sw))
                    connection.disconnect()
                    pymel.connectAttr(module_to_patch.ctrl_ik_sw.message, connection, force=True)
        elif isinstance(module_to_patch, omtk.modules.rigDpSpine.DpSpine):
            # Find all connection that have from the ctrl fk upp (chest) and replace it
            same_connections = []
            connected_to_fk_upp = module_to_patch.ctrl_fk_upp.node.message.outputs(s=False, d=True, p=True)
            for connection in connected_to_fk_upp:
                attr_name = connection.shortName()
                if attr_name.find('targets') >= 0:
                    log.info('Reconnecting {0} from {1} to space switch node {2}'
                             .format(connection, module_to_patch.ctrl_fk_upp, module_to_patch.ctrl_fk_upp_sw))
                    connection.disconnect()
                    pymel.connectAttr(module_to_patch.ctrl_fk_upp_sw.message, connection, force=True)
            # Find all connection that have from the ctrl ik down (COG) and replace it
            connected_to_ik_dwn = module_to_patch.ctrl_ik_dwn.node.message.outputs(s=False, d=True, p=True)
            connected_to_fk_dwn = module_to_patch.ctrl_fk_dwn.node.message.outputs(s=False, d=True, p=True)
            all_connections = []
            all_connections.extend(connected_to_ik_dwn)
            for con in connected_to_fk_dwn:
                if con not in all_connections:
                    all_connections.append(con)
            for connection in all_connections:
                attr_name = connection.shortName()
                if attr_name.find('targets') >= 0:
                    log.info('Reconnecting {0} from {1} to space switch node {2}'
                             .format(connection, module_to_patch.ctrl_ik_dwn_sw, module_to_patch.ctrl_ik_dwn_sw))
                    connection.disconnect()
                    pymel.connectAttr(module_to_patch.ctrl_ik_dwn_sw.message, connection, force=True)

                    # pymel.delete(rig_net)
                    # libSerialization.export_network(rig_instance)


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
