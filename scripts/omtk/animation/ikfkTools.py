import functools
import logging
import libSerialization
import pymel.core as pymel


def CallFnOnNetworkByClass(_sFn, _sCls):
    fnFilter = lambda x: libSerialization.is_network_from_class(x, _sCls)
    networks = libSerialization.get_connected_networks(pymel.selected(), key=fnFilter)
    for network in networks:
        rigPart = libSerialization.import_network(network)

        if not hasattr(rigPart, _sFn):
            logging.warning("Can't find attribute {0} in {1}".format(_sFn, network)); continue

        try:
            getattr(rigPart, _sFn)()
        except Exception as e:
            print(str(e))

switchToIk = functools.partial(CallFnOnNetworkByClass, 'switch_to_ik', 'Limb')
switchToFk = functools.partial(CallFnOnNetworkByClass, 'switch_to_fk', 'Limb')
