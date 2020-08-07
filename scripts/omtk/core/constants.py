"""
Public constants
"""
import os
import re

from omtk import decorators
from omtk.vendor.enum34 import Enum


COMPONENT_HUB_INN_NAME = "inn"  # todo: change to 'in', 'inn' mean bed and breakfest...
COMPONENT_HUB_OUT_NAME = "out"
COMPONENT_HUB_DAG_NAME = "dag"
COMPONENT_METANETWORK_NAME = "metadata"

COMPONENT_HUB_INN_ATTR_NAME = "grp_inn"
COMPONENT_HUB_OUT_ATTR_NAME = "grp_out"


class PyFlowGraphMetadataKeys:
    """Metadata maya attributes that are created when using the node graph."""

    Position = "_graphpos"


BLACKLISTED_PORT_NAMES = (
    PyFlowGraphMetadataKeys.Position,
    PyFlowGraphMetadataKeys.Position + "X",
    PyFlowGraphMetadataKeys.Position + "Y",
    PyFlowGraphMetadataKeys.Position + "Z",
)


class Axis:  # pylint: disable=no-init
    """
    Available axis for a 3 dimensional vector.
    """

    x = "X"
    y = "Y"
    z = "Z"


class SpaceSwitchReservedIndex:  # pylint: disable=no-init
    """
    Reserved index for space swiching.
    """

    world = -3
    local = -2
    root = -1


class UIExposeFlags:  # pylint: disable=no-init
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


class SpaceSwitchReservedInde(Enum):
    """Fake enum as class with constant variable to represent the reserved index in controller space switch."""

    world = -3
    local = -2
    root = -1


class ComponentActionFlag(Enum):
    """Flags used when exposing Rig or Module functionality in the ui."""

    trigger_network_export = 1


class BuiltInComponentIds(Enum):
    """There Component ids are used internally and should never be used for something else."""

    Ik = "9458f1c5-8962-4338-a233-54808cc5f520"
    IkSoftSolver = "e6259812-d64d-4509-a051-828e5ed36234"
    Fk = "3f8cba02-ca89-494e-aeba-e1e1dcf23f3d"
    Limb = "603683b2-bab1-4ac9-84a7-d091b14151eb"
    TwistExtractor = "e0b775e1-1abd-4533-b5d5-ef03da434b93"
    GradientFloat = "6f6e9c48-6c3a-4678-82a5-a7a94107e69d"


@decorators.memoized
def get_version():  # TODO: Why is this here?
    """
    Read the REZ package associated with the project and return the current version.
    This is used to analyze old rigs and recommend specific scripts to correct them if needed.

    :return: The fully qualified version as a str instance.
    :rtype: str
    """
    package_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "package.py")
    )
    if not os.path.exists(package_path):
        raise Exception("Cannot find package file! {}".format(package_path))
    regex_getversion = re.compile("^version *= ['|\"]*(.*)['|\"]$")
    with open(package_path, "r") as fp:
        for line in fp:
            line = line.strip("\n")
            result = regex_getversion.match(line)
            if result:
                result = next(iter(result.groups()))
                return result


class EnumAttrTypes(Enum):
    """
    # src: http://download.autodesk.com/us/maya/2010help/CommandsPython/addAttr.html
    """

    bool = "bool"
    long = "long"
    short = "short"
    byte = "byte"
    char = "char"
    enum = "enum"
    float = "float"
    double = "double"
    doubleAngle = "doubleAngle"
    doubleLinear = "doubleLinear"
    string = "string"
    stringArray = "stringArray"
    compound = "compound"
    message = "message"
    time = "time"
    matrix = "matrix"
    fltMatrix = "fltMatrix"
    reflectanceRGB = "reflectanceRGB"
    reflectance = "reflectance"
    spectrumRGB = "spectrumRGB"
    spectrum = "spectrum"
    float2 = "float2"
    float3 = "float3"
    double2 = "double2"
    double3 = "double3"
    long2 = "long2"
    long3 = "long3"
    short2 = "short2"
    short3 = "short3"
    doubleArray = "doubleArray"
    Int32Array = "Int32Array"
    vectorArray = "vectorArray"
    nurbsCurve = "nurbsCurve"
    nurbsSurface = "nurbsSurface"
    mesh = "mesh"
    lattice = "lattice"
    pointArray = "pointArray"
