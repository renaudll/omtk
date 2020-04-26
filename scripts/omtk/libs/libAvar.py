"""
Library for dealing with AVARs (animation variables).
For more information about AVARs, read "The Art of Moving Points" by Brian Tindall.
https://books.apple.com/us/book/the-art-of-moving-points/id639498241
"""
# TODO: This is not used anywhere, can we delete this?
import re

from pymel import core as pymel

from omtk.vendor import libSerialization


def connect_t_to_avar():
    """
    Will always call connect_to_avar with the specific needed dict

    :param ctrl: The ctrl we want that will control the fb, ud and lr avar
    :param avar_node: The node on which we can find the avar we want to control
    """

    ctrl = pymel.selected()[0]
    avar_node = pymel.selected()[1]

    avar_info = {"avar_ud": "ty", "avar_fb": "tz", "avar_lr": "tx"}
    connect_to_avar(ctrl, avar_node, avar_info)


def connect_r_to_avar():
    """
    Will always call connect_to_avar with the specific needed dict

    :param ctrl: The ctrl we want that will control the fb, ud and lr avar
    :param avar_node: The node on which we can find the avar we want to control
    """

    ctrl = pymel.selected()[0]
    avar_node = pymel.selected()[1]

    avar_info = {"avar_yw": "ry", "avar_rl": "rz", "avar_pt": "rx"}
    connect_to_avar(ctrl, avar_node, avar_info)


def connect_to_avar(ctrl, avar_node, mapping_dict):
    """
    Connect the translate attribute of a controller
    on the specific avar of the avar_node.
    Take into consideration that the calibration should
    be done done to match 1 at the maximum displacement

    :param ctrl: The ctrl we want that will control the fb, ud and lr avar
    :param avar_node: The node on which we can find the avar we want to control
    :param mapping_dict: Dictionary in which the key represent the avar attribute name
                         and the value the ctrl attribute that will drive this avar
    """
    regex_input_idx = r"^input[[]{1}(\d)[]]{1}$"

    # First get the weightBlended from the needed avar
    for avar_name, ctrl_attr_name in mapping_dict.iteritems():
        bw_list = avar_node.attr(avar_name).listConnections(
            c=False, d=False, t="blendWeighted"
        )
        if len(bw_list) != 1:
            raise (
                "Could not connect ctrl {0} translation in avar node {1}".format(
                    ctrl, avar_node
                )
            )
        match = re.search(regex_input_idx, bw_list[0].input.elements()[-1])
        input_idx = int(match.group(1)) + 1
        pymel.connectAttr(ctrl.attr(ctrl_attr_name), bw_list[0].input[input_idx])

    pymel.select(ctrl)


def get_avar_network_by_name(avar_name):
    """
    Find a serialized avar with a provided name in the scene.
    """
    for network in libSerialization.iter_networks_from_class("AbstractAvar"):
        if network.hasAttr("name") and network.attr("name").get() == avar_name:
            return network


def get_avar_by_name(avar_name):
    """
    Find an avar with a provided name in the scene.
    """
    network = get_avar_network_by_name(avar_name)
    if network:
        avar = libSerialization.import_network(network)
        if avar:
            return avar
