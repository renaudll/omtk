class Axis:
    """
    Fake enum as class with constant variable to represent the axis value that could change
    """
    x = 'X'
    y = 'Y'
    z = 'Z'


class SpaceSwitchReservedIndex:
    """
    Fake enum as class with constant variable to represent the reserved index in controller space switch
    """
    world = -3
    local = -2
    root = -1


class UIExposeFlags:
    """
    Flags used when exposing Rig or Module functionality in the ui.
    """
    trigger_network_export = 1


class EnvironmentVariables:
    """
    Customize the behavior of OMTK by defining thoses environment variables.
    """
    # Force a specific rig type as default.
    # Usefull for project-specific configurations.
    OMTK_DEFAULT_RIG = 'OMTK_DEFAULT_RIG'

    # Define additional location on disk to search for plugins.
    OMTK_PLUGINS = 'OMTK_PLUGINS'
