from maya import OpenMaya


def enumerate_MNodeMessage_signals(msg):
    if msg & OpenMaya.MNodeMessage.kConnectionMade:
        yield 'kConnectionMade'
    if msg & OpenMaya.MNodeMessage.kConnectionBroken:
        yield 'kConnectionBroken'
    if msg & OpenMaya.MNodeMessage.kAttributeEval:
        yield 'kAttributeEval'
    if msg & OpenMaya.MNodeMessage.kAttributeSet:
        yield 'kAttributeSet'
    if msg & OpenMaya.MNodeMessage.kAttributeLocked:
        yield 'kAttributeLocked'
    if msg & OpenMaya.MNodeMessage.kAttributeUnlocked:
        yield 'kAttributeUnlocked'
    if msg & OpenMaya.MNodeMessage.kAttributeAdded:
        yield 'kAttributeAdded'
    if msg & OpenMaya.MNodeMessage.kAttributeRemoved:
        yield 'kAttributeRemoved'
    if msg & OpenMaya.MNodeMessage.kAttributeRenamed:
        yield 'kAttributeRenamed'
    if msg & OpenMaya.MNodeMessage.kAttributeKeyable:
        yield 'kAttributeKeyable'
    if msg & OpenMaya.MNodeMessage.kAttributeUnkeyable:
        yield 'kAttributeUnkeyable'
    if msg & OpenMaya.MNodeMessage.kIncomingDirection:
        yield 'kIncomingDirection'
    if msg & OpenMaya.MNodeMessage.kAttributeArrayAdded:
        yield 'kAttributeArrayAdded'
    if msg & OpenMaya.MNodeMessage.kAttributeArrayRemoved:
        yield 'kAttributeArrayRemoved'
    if msg & OpenMaya.MNodeMessage.kOtherPlugSet:
        yield 'kOtherPlugSet'


def debug_MNodeMessage_callback(msg):
    return ', '.join(list(enumerate_MNodeMessage_signals(msg)))



from omtk.vendor.enum34 import Enum


class enumMFnDataType(Enum):
    kInvalid = 0  # Invalid value.
    kNumeric = 1  # Numeric, use MFnNumericData extract the node data.
    kPlugin = 2  # Plugin Blind Data, use MFnPluginData to extract the node data.
    kPluginGeometry = 3  # Plugin Geometry, use MFnGeometryData to extract the node data.
    kString = 4  # String, use MFnStringData to extract the node data.
    kMatrix = 5  # Matrix, use MFnMatrixData to extract the node data.
    kStringArray = 6  # String Array, use MFnStringArrayData to extract the node data.
    kDoubleArray = 7  # Double Array, use MFnDoubleArrayData to extract the node data.
    kIntArray = 8  # Int Array, use MFnIntArrayData to extract the node data.
    kPointArray = 9  # Point Array, use MFnPointArrayData to extract the node data.
    kVectorArray = 10  # Vector Array, use MFnVectorArrayData to extract the node data.
    kComponentList = 11  # Component List, use MFnComponentListData to extract the node data.
    kMesh = 12  # Mesh, use MFnMeshData to extract the node data.
    kLattice = 13  # Lattice, use MFnLatticeData to extract the node data.
    kNurbsCurve = 14  # Nurbs Curve, use MFnNurbsCurveData to extract the node data.
    kNurbsSurface = 15  # Nurbs Surface, use MFnNurbsSurfaceData to extract the node data.
    kSphere = 16  # Sphere, use MFnSphereData to extract the node data.
    kDynArrayAttrs = 17  # ArrayAttrs, use MFnArrayAttrsData to extract the node data.
    kDynSweptGeometry = 18  # SweptGeometry, use MFnDynSweptGeometryData to extract the node data. This data node is in OpenMayaFX which must be linked to.
    kSubdSurface = 19  # Subdivision Surface, use MFnSubdData to extract the node data.
    kNObject = 20  # nObject data, use MFnNObjectData to extract node data
    kNId = 21  # nId data, use MFnNIdData to extract node data
    kLast = 22  # Last value. It does not represent real data, but can be used to loop on all possible types
