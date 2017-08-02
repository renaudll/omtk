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


class ComponentActionFlags:
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


class BuiltInComponentIds:
    """
    There Component ids are used internally and should never be used for something else.
    """
    Ik = '9458f1c5-8962-4338-a233-54808cc5f520'
    IkSoftSolver = 'e6259812-d64d-4509-a051-828e5ed36234'
    Fk = '3f8cba02-ca89-494e-aeba-e1e1dcf23f3d'
    Limb = '603683b2-bab1-4ac9-84a7-d091b14151eb'
    TwistExtractor = 'e0b775e1-1abd-4533-b5d5-ef03da434b93'


class PyFlowGraphMetadataKeys:
    """
    Metadata maya attributes that are created when using the node graph.
    """
    Position = 'omtkGraphPos'


COMPONENT_HUB_INN_NAME = 'inn'
COMPONENT_HUB_OUT_NAME = 'out'

COMPONENT_HUB_INN_ATTR_NAME = 'grp_inn'
COMPONENT_HUB_OUT_ATTR_NAME = 'grp_out'
