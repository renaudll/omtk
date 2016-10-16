import pymel.core as pymel
import libSerialization
import omtk
from omtk.modules import rigDpSpine
from omtk.modules import rigLimb
from omtk.modules import rigIK
import logging
log = logging.getLogger('omtk')

def patch_spaceswitch_data_into_network(sel=None):
    if sel is None:
        sel = pymel.selected()

    networks = libSerialization.get_connected_networks(sel, key=lambda
        net: libSerialization.is_network_from_class(net, 'BaseCtrl'))

    for net in networks:
        print net
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
    rig_net = libSerialization.get_networks_from_class('Rig')[0]
    rig_instance = libSerialization.import_network(rig_net)

    # Get all the module that we could need to patch
    to_patch = [module for module in rig_instance.modules if isinstance(module, rigDpSpine.DpSpine) or
                isinstance(module, rigLimb.Limb)]
    # Get through all the modules to patch and replace space switch connection from the ctrl to the space switch object
    for module in to_patch:
        module_to_patch = module
        # If we have a limb, we want to patch the ik system
        if isinstance(module, rigLimb.Limb):
            module_to_patch = module.sysIK
        # Generate the space switch objects first if needed
        module_to_patch.setup_spaceswitch_objects()

    pymel.delete(rig_net)
    libSerialization.export_network(rig_instance)

    for module in to_patch:
        module_to_patch = module
        # If we got an ik, we need to check if the ik ctrl is used as a space switch target somewhere
        if isinstance(module_to_patch, rigIK.IK):
            # Find all connection that have from the ctrl ik and replace it
            connected_to_ik = module_to_patch.ctrl_ik.node.message.outputs(s=False, d=True, p=True)
            for connection in connected_to_ik:
                attr_name = connection.shortName()
                if attr_name.find('targets') >= 0:  # Not sexy, but it work
                    log.info('Reconnecting {0} from {1} to space switch node {2}'
                             .format(connection, module_to_patch.ctrl_ik, module_to_patch.ctrl_ik_sw))
                    connection.disconnect()
                    pymel.connectAttr(module_to_patch.ctrl_ik_sw.message, connection, force=True)
        elif isinstance(module_to_patch, rigDpSpine.DpSpine):
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
