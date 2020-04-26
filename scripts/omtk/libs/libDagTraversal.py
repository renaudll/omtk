"""
Functions that traverse the DAG tree in search of specific networks/serialized objects.
"""
from omtk.vendor import libSerialization


def get_avar_network_by_name(avar_name):
    """Find a serialized avar with a provided name in the scene."""
    for network in libSerialization.iter_networks_from_class("AbstractAvar"):
        if network.hasAttr("name") and network.attr("name").get() == avar_name:
            return network


def get_avar_by_name(avar_name):
    """Find an avar with a provided name in the scene."""
    network = get_avar_network_by_name(avar_name)
    if network:
        avar = libSerialization.import_network(network)
        if avar:
            return avar
