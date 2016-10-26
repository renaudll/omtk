import functools
import logging
import libSerialization
import pymel.core as pymel

def _get_module_networks_from_selection(module_name):
    """
    Search for specific module networks recursively, starting at selection.
    Note that to help with performances, we'll skip any Rig network we encounter.
    :param module_name: The name of the module to search for.
    :return: A list of pymel.nodetypes.Network.
    """
    def fn_skip(network):
        return libSerialization.is_network_from_class(network, 'Rig')
    def fn_key(network):
        return libSerialization.is_network_from_class(network, module_name)
    sel = pymel.selected()
    networks = libSerialization.get_connected_networks(sel, recursive=True, key=fn_key, key_skip=fn_skip)

    modules = [libSerialization.import_network(network, fn_skip=fn_skip) for network in networks]
    modules = filter(None, modules)  # Filter any invalid networks that libSerialization doesn't protect us from.
    return modules

def _call_on_networks_by_class(fn_name, module_name):
    modules = _get_module_networks_from_selection(module_name)
    for module in modules:
        # Resolve function
        if not hasattr(module, fn_name):
            logging.warning("Can't find attribute {0} in {1}".format(fn_name, module))
            continue
        fn = getattr(module, fn_name)
        if not hasattr(fn, '__call__'):
            logging.warning("Can't execute {0} in {1}, not callable!".format(fn_name, module))
            continue

        # Execute function
        try:
            fn()
        except Exception, e:
            logging.warning("Error excecuting {0} in {1}! {2}".format(fn_name, module, str(e)))

switchToIk = functools.partial(_call_on_networks_by_class, 'switch_to_ik', 'Limb')
switchToFk = functools.partial(_call_on_networks_by_class, 'switch_to_fk', 'Limb')
