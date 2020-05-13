"""
Toogle selection between the facial animation layer and the rigging layer.
"""
import pymel.core as pymel
from omtk.vendor import libSerialization
from omtk.core import macros


def get_avars_networks_from_selection(objs):
    """
    Return all avars associated with the current selection.
    :param objs: A list of pymel.PyNode. If nothing is provided the selection is used.
    :return: A list of Avar instances.
    """

    def fn_skip(network):
        return libSerialization.is_network_from_class(network, "Rig")

    def fn_filter(network):
        return libSerialization.is_network_from_class(network, "AbstractAvar")

    if objs is None:
        objs = pymel.selected()

    networks = libSerialization.get_connected_networks(
        objs, key=fn_filter, key_skip=fn_skip
    )

    return networks


def iter_connected_ctrl_models_networks(objs):
    def fn_skip(network):
        return libSerialization.is_network_from_class(
            network, "Module"
        ) and not libSerialization.is_network_from_class(network, "BaseCtrlModel")

    def fn_filter(network):
        return libSerialization.is_network_from_class(network, "BaseCtrlModel")

    if objs is None:
        objs = pymel.selected()

    for network in libSerialization.iter_connected_networks(
        objs, key=fn_filter, key_skip=fn_skip
    ):
        yield network


def get_connected_ctrl_models_networks(objs):
    return list(iter_connected_ctrl_models_networks(objs))


def iter_connected_ctrl_models(objs):
    for network in iter_connected_ctrl_models_networks(objs):
        ctrl_model = libSerialization.import_network(network)
        if ctrl_model:
            yield ctrl_model


def get_connected_ctrl_models(objs):
    return list(iter_connected_ctrl_models(objs))


class ToogleAvarSelection(macros.BaseMacro):
    def run(self):
        sel = pymel.selected()

        avar_networks = get_avars_networks_from_selection(sel)
        if not avar_networks:
            pymel.warning("Please select an avar controller or grp.")
            return

        # Determine which "mode" where are in.
        # Check if we are currently in 'animation' mode or 'rigging' mode.
        # If there's any controllers selected,
        # we are in animation mode and want to select avar_grp.
        # If there aren't any controllers selected,
        # we are in rigging mode and want to select avar ctrls.
        is_animation_mode = bool(get_connected_ctrl_models_networks(sel))

        if is_animation_mode:
            self._select_rig_objs(avar_networks)
        else:
            self._select_ctrl_objs(avar_networks)

    def _select_ctrl_objs(self, avar_networks):
        result = set()

        def fn_filter(network):
            return isinstance(
                network, pymel.nodetypes.Network
            ) and libSerialization.is_network_from_class(network, "BaseCtrl")

        for avar_network in avar_networks:
            if avar_network.hasAttr("ctrl"):
                for hist in avar_network.attr("ctrl").listHistory():
                    if fn_filter(hist):
                        ctrl = (
                            next(iter(hist.attr("node").inputs()), None)
                            if hist.hasAttr("node")
                            else None
                        )
                        if ctrl:
                            result.add(ctrl)
        pymel.select(result)

    def _select_rig_objs(self, avar_networks):
        result = set()
        for network in avar_networks:
            if network.hasAttr("grp_rig"):
                grp_rig = next(iter(network.attr("grp_rig").inputs()), None)
                # HACK: Duck type avars by checking the UD avar
                # Fix this
                if grp_rig and grp_rig.hasAttr("avar_ud"):
                    result.add(grp_rig)
        pymel.select(result)


def register_plugin():
    return ToogleAvarSelection
