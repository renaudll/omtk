"""
Registry of constant values
"""
from omtk.vendor.enum34 import Enum

# These name are reserved and cannot be used as-is.
# Thanks hypothesis for helping me find them!
BLACKLISTED_NODE_NAMES = (
    # mel keywords:
    "break",
    "case",
    "default",
    "do",
    "else",
    "false",
    "float",
    "global",
    "for",
    "if",
    "in",
    "int",
    "matrix",
    "no",
    "proc",
    "string",
    "switch",
    "true",
    "vector",
    "while",
    "yes",
)


# Theses types will always have a transform as their parent.
# Theses classification type can be obtained using cmds.getClassification().
SHAPE_CLASS = (
    "drawdb.light",  # include ambientLight, areaLight, directionalLight, pointLight, etc
    "mesh",
    "nurbsSurface",
    "nurbsCurve",
    "locator",
    "volume",
)


# When creating an individual shape, the name of the parent will be determined from this map.
DEFAULT_PREFIX_BY_SHAPE_TYPE = {
    "mesh": "polySurface",
    "nurbsSurface": "surface",
    "nurbsCurve": "curve",
}


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
    double4 = "double4"
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

    # The types bellow are returned when generating a MockedSessionSchema
    # We don't know why they exist and don't really want them.
    typed = "typed"
    generic = "generic"
    lightData = "lightData"
    addr = "addr"
    floatLinear = "floatLinear"
    polyFaces = "polyFaces"


# Determine which type combination create unitConversion node
# and what is the conversionFactor value.
# If a type is not here it won't create any unitConversion.
CONVERSION_FACTOR_BY_TYPE = {
    (EnumAttrTypes.double, EnumAttrTypes.doubleAngle): 0.017453292519943295,
    (EnumAttrTypes.bool, EnumAttrTypes.doubleAngle): 0.017453292519943295,
}

# Connection ports that cannot be connected together.
IMPOSSIBLE_CONNECTIONS = {
    (EnumAttrTypes.char, EnumAttrTypes.string),
}

# Ensure that we have combination in reverse orders
CONVERSION_FACTOR_BY_TYPE = {
    CONVERSION_FACTOR_BY_TYPE[key]: 1.0 / val for key, val in CONVERSION_FACTOR_BY_TYPE.items()
}
