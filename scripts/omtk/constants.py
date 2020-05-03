"""
Public constants
"""
# TODO: Use real enum or convert to scalar


class Axis:  # pylint: disable=old-style-class, no-init
    """
    Available axis for a 3 dimensional vector.
    """

    x = "X"
    y = "Y"
    z = "Z"


class SpaceSwitchReservedIndex:  # pylint: disable=old-style-class, no-init
    """
    Reserved index for space swiching.
    """

    world = -3
    local = -2
    root = -1


class UIExposeFlags:  # pylint: disable=old-style-class, no-init
    """
    Flags used when exposing Rig or Module functionality in the ui.
    """

    trigger_network_export = 1


class EnvironmentVariables:
    """
    Customize the behavior of OMTK by defining environment variables.
    """

    # Force a specific rig type as default.
    # Usefull for project-specific configurations.
    OMTK_DEFAULT_RIG = "OMTK_DEFAULT_RIG"

    # Define additional location on disk to search for plugins.
    OMTK_PLUGINS = "OMTK_PLUGINS"
