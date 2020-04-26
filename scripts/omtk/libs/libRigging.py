import logging
import math

import pymel.core as pymel
from maya import OpenMaya
from maya import cmds
from maya import mel

from omtk import constants
from omtk.libs import libPymel

_LOG = logging.getLogger(__name__)

__aBasicTypes = [int, float, bool, pymel.datatypes.Matrix, pymel.datatypes.Vector,
                 pymel.datatypes.Point]

_X_AXIS = pymel.datatypes.Vector.xAxis
_Y_AXIS = pymel.datatypes.Vector.yAxis
_Z_Axis = pymel.datatypes.Vector.zAxis


def is_basic_type(_val):
    global __aBasicTypes
    return type(_val) in __aBasicTypes


def connect_or_set_attr(_attr, _val):
    if isinstance(_val, (list, tuple)):
        # Note: List attribute and compound attribute don't have the same way of iterating.
        if _attr.isArray():
            for i, val in enumerate(_val):
                connect_or_set_attr(_attr.elementByLogicalIndex(i), val)
        elif _attr.isCompound():
            children = _attr.getChildren()
            for child, val in zip(children, _val):
                connect_or_set_attr(child, val)
        else:
            raise Exception(
                "Can't apply value {0} on attribute {1}, need an array or compound".format(
                    _val, _attr))

    else:
        if isinstance(_val, pymel.Attribute):
            pymel.connectAttr(_val, _attr, force=True)
        elif is_basic_type(_val):
            _attr.set(_val)
        else:
            raise TypeError(
                '[ConnectOrSetAttr] Invalid value for attribute {} of type {} and value {}'.format(
                    _attr.name(),
                    type(_val), _val))


def create_utility_node(_sClass, name=None, *args, **kwargs):
    uNode = pymel.createNode(_sClass, name=name) if name else pymel.createNode(_sClass)
    for sAttrName, pAttrValue in kwargs.items():
        if not uNode.hasAttr(sAttrName):
            raise Exception(
                '[CreateUtilityNode] UtilityNode {0} doesn\'t have an {1} attribute.'.format(
                    _sClass, sAttrName))
        else:
            connect_or_set_attr(uNode.attr(sAttrName), pAttrValue)
    return uNode


def connect_matrix_to_node(attr_tm, node, name=None):
    u = create_utility_node(
        'decomposeMatrix',
        name=name,
        inputMatrix=attr_tm
    )
    pymel.connectAttr(u.outputTranslate, node.translate, force=True)
    pymel.connectAttr(u.outputRotate, node.rotate, force=True)
    pymel.connectAttr(u.outputScale, node.scale, force=True)
    return u


#
# CtrlShapes Backup
#
def hold_ctrl_shapes(transform, parent=None):
    # Resolve each shape in it's most left position in the history.
    # This allow us to transform with multiples shapes and deformed shape.
    # If we encounter a deformed shape, we'll simple hold/fetch the Orig shape.

    # Resolve all shapes (pymel.nodetypes.CurveShape only for now)
    def is_shape(shape):
        return isinstance(shape,
                          pymel.nodetypes.CurveShape) and not shape.intermediateObject.get()

    all_shapes = filter(is_shape, transform.getShapes(noIntermediate=True))
    if not all_shapes:
        return

    # Resolve only orig shape

    def get_orig_shape(shape):
        def is_shape_history(hist):
            return is_shape(hist) and hist.getParent() == transform

        return next(reversed(filter(is_shape_history, shape.listHistory())))

    all_shapes = map(get_orig_shape, all_shapes)

    dst_transform = pymel.duplicate(transform, parentOnly=True, returnRootsOnly=True)[0]

    for src_shape in all_shapes:
        # We use the duplicate command to duplicate the shape.
        # However it has to be isolated in it's own transform so the duplicate method won't duplicate the other shapes.
        # Theorically it's possible to create a new nurbsCurve and connect/disconnect it's create attribute.
        # However without triggering a viewport refresh using the refresh command, the connect/disconnect trick don't work.

        tmp1 = pymel.createNode('transform')
        src_shape.setParent(tmp1, relative=True, shape=True)
        tmp2 = pymel.duplicate(tmp1)[0]
        dst_shape = tmp2.getShape()
        pymel.delete(tmp1)

        dst_shape.setParent(dst_transform, relative=True, shape=True)
        if dst_shape.intermediateObject.get():
            dst_shape.intermediateObject.set(False)
        pymel.delete(tmp2)

    '''
    dst_shapes = []
    for src_shape in all_shapes_orig:
        #src_type = src_shape.longName.type()
        dst_shape = pymel.createNode('nurbsCurve')
        tmp = dst_shape.getParent()
        pymel.nodeCast(src_shape, dst_shape)
        pymel.delete(tmp)
    '''

    '''
    snapshot = pymel.duplicate(transform, parentOnly=True, returnRootsOnly=True)[0]
    for shape in all_shapes_orig:
        shape.setParent(snapshot, s=True, r=True)
        if shape.intermediateObject.get():
            shape.intermediateObject.set(False)
    '''

    if parent:
        dst_transform.setParent(parent)
    else:
        dst_transform.setParent(world=True)

    new_name = '_{0}'.format(transform.name())
    cmds.rename(dst_transform.longName(),
                new_name)  # For strange reasons, using .rename don't always work.
    try:
        pymel.makeIdentity(dst_transform, scale=True, apply=True)
    except:
        pass
    dst_transform.template.set(True)

    return dst_transform


def fetch_ctrl_shapes(source, target):
    # Remove any previous shapes
    pymel.delete(
        filter(lambda x: isinstance(x, pymel.nodetypes.CurveShape), target.getShapes()))
    for source_shape in source.getShapes():
        source_shape.template.set(False)
        source_shape.setParent(target, r=True, s=True)
        source_shape.rename(target.name() + 'Shape')

    # TODO: Support AnnotationShapes
    pymel.delete(source)


def hold_all_ctrl_shapes(**kwargs):
    aCtrls = [o.getParent() for o in pymel.ls('anm_*', type='nurbsCurve')]
    return [hold_ctrl_shapes(oCtrl, **kwargs) for oCtrl in aCtrls]


def fetch_all_ctrl_shapes():
    ctrls = [o.getParent() for o in pymel.ls('_anm_*', type='nurbsCurve')]

    for ctrl in ctrls:
        target_name = ctrl.name()[1:]
        if pymel.objExists(target_name):
            target = pymel.PyNode(str(target_name))
            fetch_ctrl_shapes(ctrl, target)


def create_strech_attr_from_curve(curve_shape):
    curveLength = create_utility_node('curveInfo',
                                      inputCurve=curve_shape.worldSpace).arcLength
    return create_utility_node('multiplyDivide', operation=2, input1X=curveLength,
                               input2X=curveLength.get()).outputX


def create_arclengthdimension_for_nurbsplane(nurbs_shape, u=1.0, v=1.0):
    arcLengthDimension_shape = pymel.createNode('arcLengthDimension')
    arcLengthDimension_shape.uParamValue.set(u)
    arcLengthDimension_shape.vParamValue.set(v)
    pymel.connectAttr(nurbs_shape.worldSpace, arcLengthDimension_shape.nurbsGeometry)
    attr_length_u = arcLengthDimension_shape.arcLength
    attr_length_v = arcLengthDimension_shape.arcLengthInV
    return attr_length_u, attr_length_v, arcLengthDimension_shape


def get_surface_length(surface, u=1.0, v=1.0):
    attr_u, attr_v, util = create_arclengthdimension_for_nurbsplane(surface, u=u, v=v)
    length_u = attr_u.get()
    length_v = attr_v.get()
    pymel.delete(util.getParent())
    return length_u, length_v


def create_stretch_attr_from_nurbs_plane(nurbs_shape, u=1.0, v=1.0):
    """
    Compute the stretch applied on a pymel.nodetypes.NurbsSurface.
    :param nurbs_shape: The pymel.nodetypes.NurbsSurface node.
    :return: The stretch attribute and an arcLengthDimension that will need to be parented somewhere.
    """
    attr_length_u, attr_length_v, arcLengthDimension_shape = create_arclengthdimension_for_nurbsplane(
        nurbs_shape, u=u,
        v=v)
    attr_length_v = arcLengthDimension_shape.arcLengthInV
    multiply_node = create_utility_node('multiplyDivide', operation=2,
                                        input1X=attr_length_u,
                                        input2X=attr_length_u.get(),
                                        input1Y=attr_length_v,
                                        input2Y=attr_length_v.get()
                                        )
    attr_stretch_u = multiply_node.outputX
    attr_stretch_v = multiply_node.outputY
    return attr_stretch_u, attr_stretch_v, arcLengthDimension_shape


def create_stretch_node_between_2_bones(start, end, attr_scale=None):
    # Compute the Stretch
    start_world_trans_attr = create_utility_node('decomposeMatrix',
                                                 inputMatrix=start.worldMatrix
                                                 ).outputTranslate

    end_world_trans_attr = create_utility_node('decomposeMatrix',
                                               inputMatrix=end.worldMatrix
                                               ).outputTranslate

    distance_nonroll_attr = create_utility_node('distanceBetween',
                                                point1=start_world_trans_attr,
                                                point2=end_world_trans_attr
                                                ).distance

    # Adjust with a scale attribute if necessary
    scale_adjust_attr = distance_nonroll_attr.get()
    if attr_scale:
        scale_adjust_attr = create_utility_node('multiplyDivide',
                                                input1X=attr_scale,
                                                input2X=distance_nonroll_attr.get(),
                                                operation=1
                                                ).outputX

    stretch_factor = create_utility_node('multiplyDivide',
                                         input1X=distance_nonroll_attr,
                                         input2X=scale_adjust_attr,
                                         operation=2
                                         )

    return stretch_factor.outputX


def create_squash_attr_simple(attr_stretch):
    return create_utility_node('multiplyDivide', operation=2, input1X=1.0,
                               input2X=attr_stretch).outputX


def create_squash_attr(attr_stretch):
    # return next(iter(create_squash_atts(attr_stretch, 1)))
    attr_stretch_inv = create_utility_node('multiplyDivide', operation=2, input1X=1.0,
                                           input2X=attr_stretch).outputX
    return create_utility_node('multiplyDivide', operation=3, input1X=attr_stretch_inv,
                               input2X=2).outputX


def create_squash_atts(attr_stretch, samples):
    """
    Create attributes resolving a curve using the following formula.
    s^(e^(x^2)))
    see: http://www.wolframalpha.com/input/?i=%28x%5E2-1%29*-1
    :param attr_stretch: # The stretch attribute.
    :param samples: Number of samples to resolve.
    """
    if not isinstance(attr_stretch, pymel.Attribute):
        raise IOError("Expected pymel Attribute, got {0} ({1})".format(attr_stretch,
                                                                       type(
                                                                           attr_stretch)))

    attr_stretch_inv = create_utility_node('multiplyDivide', operation=2, input1X=1.0,
                                           input2X=attr_stretch).outputX

    return_vals = []
    for i in range(samples):
        pos = float(i) / (samples - 1) * 2.0 - 1.0

        # Blend between no squash and full squash using a bell curve.
        # 0 = Maximum Squash
        # 1 = No Squash
        # see see: http://www.wolframalpha.com/input/?i=%28x%5E2-1%29*-1
        blend = create_utility_node("multiplyDivide", operation=3, input1X=pos,
                                    input2X=2).outputX
        attr_squash = create_utility_node("blendTwoAttr", input=[attr_stretch_inv, 1],
                                          attributesBlender=blend)

        return_vals.append(attr_squash)
    return return_vals


def interp_linear(r, s, e):
    return (e - s) * r + s


def interp_linear_multiple(ratios, s, e):
    return [interp_linear(ratio, s, e) for ratio in ratios]


def interp_football(ratio):
    """
    https://www.wolframalpha.com/input/?i=cos(x%2B1*pi%2F2)%5E0.5
    """
    return math.cos(ratio / 2.0 * math.pi) ** 0.5


def create_nurbs_plane_from_joints(jnts, degree=1, width=1):
    """
    Create a nurbsPlane following a provided joint chain.
    Note that the plane is oriented in the up axis (Y) of each joint.
    """

    # Create nurbsPlane
    num_patches_u = (len(jnts) - 1)
    plane = pymel.nurbsPlane(d=degree, u=num_patches_u)[0]

    # Note that the choosed offset is not arbitrary.
    # This will ensure that any follicle created on the resulting nurbsSurface
    # will share the same orientation.
    pos_upp_local = pymel.datatypes.Point(0, -width, 0)
    pos_dwn_local = pymel.datatypes.Point(0, width, 0)

    # Define how much in-between we need to compute.
    num_patches_v = 2
    num_inbetweens_outside = 0
    num_inbetweens_inside = 0
    add_inside_edges = True
    if degree == 1:  # Linear
        pass
    elif degree == 2:  # Quadratic
        num_inbetweens_outside = 1
        num_inbetweens_inside = 1
        add_inside_edges = False
        num_patches_v = 3
    elif degree == 3:  # Cubic
        num_inbetweens_outside = 1
        num_patches_v = 4
    else:
        # TODO: Support missing degrees!
        Exception("Unexpected value for parameter degree, got {0}.".format(degree))

    # Resolve ratios to compute v positions more easily.
    v_ratios = [v / float(num_patches_v - 1) for v in range(num_patches_v)]

    # Resolve positions for edges
    edges_positions_upp = []
    edges_positions_dwn = []
    for i, jnt in enumerate(jnts):
        jnt_tm_world = jnt.getMatrix(worldSpace=True)
        pos_upp = pos_upp_local * jnt_tm_world
        pos_dwn = pos_dwn_local * jnt_tm_world
        edges_positions_upp.append(pos_upp)
        edges_positions_dwn.append(pos_dwn)

    # Resolve all positions including in-between
    all_positions = []

    num_edges = len(edges_positions_upp)
    for i in range(num_edges - 1):
        pos_upp_inn = edges_positions_upp[i]
        pos_dwn_inn = edges_positions_dwn[i]
        is_first = i == 0
        is_before_last = i == num_edges - 2
        is_last = i == num_edges - 1

        # Add edge (note that we always add the first and last edge edge).
        if is_first or is_last or add_inside_edges:
            all_positions.append(
                interp_linear_multiple(v_ratios, pos_upp_inn, pos_dwn_inn))

        # Add in-betweens
        if is_last:  # For obvious reasons, we don't want to add any points after the last edge.
            continue

        num_inbetweens = num_inbetweens_outside if is_first or is_before_last else num_inbetweens_inside

        if num_inbetweens:
            pos_upp_out = edges_positions_upp[i + 1]
            pos_dwn_out = edges_positions_dwn[i + 1]
            for j in range(num_inbetweens_outside):
                ratio = float(j + 1) / (num_inbetweens_outside + 1)
                pos_upp = interp_linear(ratio, pos_upp_inn, pos_upp_out)
                pos_dwn = interp_linear(ratio, pos_dwn_inn, pos_dwn_out)
                all_positions.append(interp_linear_multiple(v_ratios, pos_upp, pos_dwn))

    # Add last edge
    all_positions.append(interp_linear_multiple(v_ratios, edges_positions_upp[-1],
                                                edges_positions_dwn[-1]))

    # Model the plane
    for u in range(len(all_positions)):
        for v in range(len(all_positions[u])):
            pos = all_positions[u][v]
            plane.setCV(u, v, pos)

    return plane


def create_nurbsCurve_from_joints(obj_s, obj_e, samples=2, num_cvs=3):
    pos_s = obj_s.getTranslation(worldSpace=True)
    pos_e = obj_e.getTranslation(worldSpace=True)
    coords = []
    for i in range(num_cvs):
        ratio = float(i) / (num_cvs - 1)
        oord = (pos_s + (ratio * (pos_e - pos_s)))
        coords.append(oord)

    nurbsCurve = pymel.curve(d=samples, p=coords)

    return nurbsCurve


def create_hyerarchy(_oObjs):
    for i in range(1, len(_oObjs)):
        _oObjs[i].setParent(_oObjs[i - 1])


def create_chain_between_objects(obj_s, obj_e, samples, parented=True):
    tm = obj_s.getMatrix(worldSpace=True)
    pos_s = obj_s.getTranslation(space='world')
    pos_e = obj_e.getTranslation(space='world')

    new_objs = []

    pymel.select(clear=True)
    for iCurJnt in range(0, samples):
        ratio = float(iCurJnt) / (samples - 1.00)
        pos = pos_s + (pos_e - pos_s) * ratio

        new_obj = pymel.duplicate(obj_s, parentOnly=True)[0]
        new_obj.setMatrix(tm, worldSpace=True)
        new_obj.setTranslation(pos, space='world')
        new_objs.append(new_obj)

    new_objs[0].setParent(world=True)
    if parented:
        create_hyerarchy(new_objs)
    else:
        for obj in new_objs[1:]:
            obj.setParent(world=True)

    return libPymel.PyNodeChain(new_objs)


'''
def reshape_ctrl(ctrl_shape, ref, multiplier=1.25):
    if not isinstance(ctrl_shape, pymel.nodetypes.NurbsCurve):
        raise Exception("Unexpected input, expected NurbsCurve, got {0}.".format(type(ctrl_shape)))

    geometries = libHistory.get_affected_shapes(ref)
    if not geometries:
        print "Cannot resize {0}, found no affected geometries!".format(ctrl_shape)
        return
    pos = ctrl_shape.getParent().getTranslation(space='world')
    pos = OpenMaya.MPoint(pos.x, pos.y, pos.z)

    results = OpenMaya.MPointArray()

    for i in range(ctrl_shape.numCVs()):
        cv_pos = ctrl_shape.cv[i].getPosition(space='world')
        length = None
        dir = cv_pos - pos
        dir.normalize()
        dir = OpenMaya.MVector(dir.x, dir.y, dir.z)

        # Resolve desired new length using raycast projection.
        for geometry in geometries:
            mfn_geometry = geometry.__apimfn__()
            if mfn_geometry.intersect(pos, dir, results, 1.0e-10, OpenMaya.MSpace.kWorld):
                cur_length = results[0].distanceTo(pos)
                if length is None or cur_length > length:
                    length = cur_length

        if length is None:
            continue

        cv_new_pos = pos + (dir * length * multiplier)
        ctrl_shape.cv[i].setPosition(cv_new_pos, space='world')
'''


# todo: check if memoized is really necessary?
# @libPython.memoized
def get_recommended_ctrl_size(obj, geometries=None, default_value=1.0, weight_x=0.0,
                              weight_neg_x=0.0, weight_y=1.0,
                              weight_neg_y=1.0, weight_z=0.0, weight_neg_z=0.0,
                              default_size=1.0):
    """
    Return the recommended size of a controller if it was created for this obj.
    :param obj: The object to analyze.
    """
    if geometries is None and isinstance(obj, pymel.nodetypes.Joint):
        skinClusters = set()
        for hist in obj.listHistory(future=True):
            if isinstance(hist, pymel.nodetypes.SkinCluster):
                skinClusters.add(hist)
        geometries = set()
        for skinCluster in skinClusters:
            geometries.update(skinCluster.getOutputGeometry())
        geometries = filter(lambda x: isinstance(x, pymel.nodetypes.Mesh),
                            geometries)  # Ensure we only deal with meshes

    if geometries is None:
        _LOG.warning("Cannot get recommended ctrl size. No geometries to do raycast on!")
        return default_size

    # Create a number of raycast for each geometry. Use the longuest distance.
    # Note that we are not using the negative Y axis, this give bettern result for example on shoulders.
    if isinstance(obj, pymel.nodetypes.Transform):
        ref_tm = obj.getMatrix(worldSpace=True)
    elif isinstance(obj, pymel.datatypes.Matrix):
        ref_tm = obj
    else:
        raise IOError("Unexpected type for reference object {0}".format(type(obj)))

    pos = ref_tm.translate
    pos = OpenMaya.MPoint(pos.x, pos.y, pos.z)

    dirs = []
    if weight_x:
        dirs.append(OpenMaya.MVector(ref_tm.a00, ref_tm.a01, ref_tm.a02))  # X Axis
    if weight_neg_x:
        dirs.append(OpenMaya.MVector(-ref_tm.a00, -ref_tm.a01, -ref_tm.a02))  # X Axis
    if weight_y:
        dirs.append(OpenMaya.MVector(ref_tm.a10, ref_tm.a11, ref_tm.a12))  # Y Axis
    if weight_neg_y:
        dirs.append(OpenMaya.MVector(-ref_tm.a10, -ref_tm.a11, -ref_tm.a12))  # Y Axis
    if weight_z:
        dirs.append(OpenMaya.MVector(ref_tm.a20, ref_tm.a21, ref_tm.a22))  # Z Axis
    if weight_neg_z:
        dirs.append(OpenMaya.MVector(-ref_tm.a20, -ref_tm.a21, -ref_tm.a22))  # Z Axis

    length = 0
    results = ray_cast(pos, dirs, geometries)
    if results:
        cur_lengh = min((result.distanceTo(pos) for result in results))
        if cur_lengh > length:
            length = cur_lengh

    if not length:
        if isinstance(obj, pymel.nodetypes.Joint):
            length = obj.radius.get()
        else:
            length = default_size
    return length


def ray_cast(pos, dirs, geometries, debug=False, tolerance=1.0e-5):
    """
    Simple pymel wrapper for the MFnGeometry intersect method.
    Note: Default tolerance is 1.0e-5. With the default MFnMesh.intersect valut of 1.0e10, sometime
    the raycase might misfire. Still doesn't know why.
    :param pos: Any OpenMaya.MPoint compatible type (ex: pymel.datatypes.Point)
    :param dirs: Any OpenMaya.MVector compatible type (ex: pymel.datatypes.Vector) or list.
    :param geometries: The geometries to intersect.
    :param debug: If True, spaceLocators will be created at intersection points.
    :return: pymel.datatypes.Point list containing the intersection points.
    """
    # Cast pos to OpenMaya.MPoint if necessary.
    if type(pos) != OpenMaya.MPoint:
        pos = OpenMaya.MPoint(pos.x, pos.y, pos.z)

    # Cast dir to list
    if not isinstance(dirs, (list, tuple)):
        dirs = [dirs]

    # Cast dir to OpenMaya.MVector if necessary.
    for i, dir in enumerate(dirs):
        if not type(dir) == OpenMaya.MVector:
            dirs[i] = OpenMaya.MVector(dir.x, dir.y, dir.z)

    results = []

    buffer_results = OpenMaya.MPointArray()
    for geometry in geometries:
        # Resolve the MFnMesh, note that in some case (ex: a mesh with zero vertices), pymel will return a MFnDagNode.
        # If this happen we'll want to ignore the mesh.
        # todo: use a generic function?
        mfn_geo = geometry.__apimfn__()

        if isinstance(mfn_geo, OpenMaya.MFnMesh):
            for dir in dirs:
                mfn_geo.intersect(pos, dir, buffer_results, tolerance,
                                  OpenMaya.MSpace.kWorld)
        elif isinstance(mfn_geo, OpenMaya.MFnNurbsSurface):
            uArray = OpenMaya.MDoubleArray()
            vArray = OpenMaya.MDoubleArray()
            for dir in dirs:
                mfn_geo.intersect(pos, dir, uArray, vArray, buffer_results, tolerance,
                                  OpenMaya.MSpace.kWorld)
        else:
            pymel.warning("Can't proceed with raycast, mesh is invalid: {0}".format(
                geometry.__melobject__()))
            continue

        for i in range(buffer_results.length()):
            results.append(pymel.datatypes.Point(buffer_results[i]))

    if debug:
        for result in results:
            loc = pymel.spaceLocator()
            loc.setTranslation(result)

    return results


def ray_cast_nearest(pos, *args, **kwargs):
    results = ray_cast(pos, *args, **kwargs)
    results = sorted(results, key=lambda x: libPymel.distance_between_vectors(pos, x))
    return next(iter(results), None)


def ray_cast_farthest(pos, *args, **kwargs):
    results = ray_cast(pos, *args, **kwargs)
    results = sorted(results, key=lambda x: libPymel.distance_between_vectors(pos, x))
    return next(iter(reversed(results)), None)


# TODO: Benchmark performances
def snap(obj_dst, obj_src):
    obj_dst.setMatrix(obj_src.getMatrix(worldSpace=True), worldSpace=True)


#
# Boxes proxy setup
# This is usefull for building a rig without any geometry.
#

def create_boxes():
    boxes = []
    for jnt in pymel.ls(type='joint'):
        joint_data = JointData(jnt)
        if joint_data.is_valid():
            length = joint_data.length
            transform, make = pymel.polyCube(height=length, width=length * 0.33,
                                             depth=length * 0.33)
            r_offset = pymel.datatypes.Matrix(0, -1.0, -0.0, 0.0, 1.0, 0, 0.0, 0.0, 0.0,
                                              -0.0, 1.0, 0.0,
                                              joint_data.dir[0] * length * 0.5,
                                              joint_data.dir[1] * length * 0.5,
                                              joint_data.dir[2] * length * 0.5,
                                              1.0)
            cylinder_tm = r_offset
            transform.setParent(jnt)
            transform.setMatrix(cylinder_tm)
            boxes.append(transform)
    return boxes


def collect_proxy_boxes():
    return_values = []
    for obj in pymel.ls(type='transform'):
        if any((hist for hist in obj.listHistory() if
                isinstance(hist, pymel.nodetypes.PolyCube))):
            if isinstance(obj.getParent(), pymel.nodetypes.Joint):
                return_values.append(obj)
    return return_values


def finalize_boxes():
    # collect weights
    boxes = collect_proxy_boxes()
    jnts = [box.getParent() for box in boxes]
    weights = []
    for i, box in enumerate(boxes):
        weights.extend([i] * len(box.vtx))

    # mergeboxes
    polyUnite = pymel.createNode('polyUnite')
    itt = 0
    for box in boxes:
        for shape in box.getShapes():
            pymel.connectAttr(shape.worldMatrix, polyUnite.inputMat[itt])
            pymel.connectAttr(shape.outMesh, polyUnite.inputPoly[itt])
            itt += 1
    outputMesh = pymel.createNode('mesh')
    pymel.connectAttr(polyUnite.output, outputMesh.inMesh)
    # pymel.delete(boxes)

    # set skin weights
    pymel.skinCluster(jnts, outputMesh.getParent(), toSelectedBones=True)
    skinCluster = next((hist for hist in outputMesh.listHistory() if
                        isinstance(hist, pymel.nodetypes.SkinCluster)),
                       None)
    for vtx, inf in zip(iter(outputMesh.vtx), weights):
        skinCluster.setWeights(vtx, [inf], [1])


'''
# src: http://tech-artists.org/forum/showthread.php?4384-Vector-math-and-Maya
from pymel.core.datatypes import Vector, Matrix, Point
def matrix_from_normal(up_vect, front_vect):
    # normalize first!
    up_vect.normalize()
    front_vect.normalize()

    #get the third axis with the cross vector
    side_vect = Vector.cross(up_vect, front_vect)
    #recross in case up and front were not originally orthoganl:
    front_vect = Vector.cross(side_vect, up_vect )

    #the new matrix is
    return Matrix (
        side_vect.x, side_vect.y, side_vect.z, 0,
        up_vect.x, up_vect.y, up_vect.z, 0,
        front_vect.x, front_vect.y, front_vect.z, 0,
        0,0,0,1)
'''


# todo: move to libPymel
def get_matrix_axis_x(tm):
    return pymel.datatypes.Vector(
        tm.a00, tm.a01, tm.a02
    )


# todo: move to libPymel
def get_matrix_axis_y(tm):
    return pymel.datatypes.Vector(
        tm.a10, tm.a11, tm.a12
    )


# todo: move to libPymel
def get_matrix_axis_z(tm):
    return pymel.datatypes.Vector(
        tm.a20, tm.a21, tm.a22
    )


# todo: move to libPymel
def get_matrix_axis(tm, axis):
    fn = None
    if axis == constants.Axis.x:
        fn = get_matrix_axis_x
    elif axis == constants.Axis.y:
        fn = get_matrix_axis_y
    elif axis == constants.Axis.z:
        fn = get_matrix_axis_z
    else:
        raise IOError("Unexpected axis. Got {}".format(
            axis
        ))

    return fn(tm)


# todo: move to libPymel
def get_matrix_from_direction(look_vec, upp_vec,
                              look_axis=pymel.datatypes.Vector.xAxis,
                              upp_axis=pymel.datatypes.Vector.zAxis):
    # print look_axis, look_vec
    # print upp_axis, upp_vec
    # Ensure we deal with normalized vectors
    look_vec.normalize()
    upp_vec.normalize()

    side_vec = pymel.datatypes.Vector.cross(look_vec, upp_vec)
    side_vec.normalize()

    # recross in case up and front were not originally orthogonal:
    upp_vec = pymel.datatypes.Vector.cross(side_vec, look_vec)

    #
    # Build resulting matrix
    #

    tm = pymel.datatypes.Matrix(
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 1
    )

    # Add look component
    axis = look_axis
    vec = look_vec
    tm += pymel.datatypes.Matrix(
        axis.x * vec.x, axis.x * vec.y, axis.x * vec.z, 0,
        axis.y * vec.x, axis.y * vec.y, axis.y * vec.z, 0,
        axis.z * vec.x, axis.z * vec.y, axis.z * vec.z, 0,
        0, 0, 0, 0
    )

    # Add upp component
    axis = upp_axis
    vec = upp_vec
    tm += pymel.datatypes.Matrix(
        axis.x * vec.x, axis.x * vec.y, axis.x * vec.z, 0,
        axis.y * vec.x, axis.y * vec.y, axis.y * vec.z, 0,
        axis.z * vec.x, axis.z * vec.y, axis.z * vec.z, 0,
        0, 0, 0, 0
    )

    # Add side component
    axis = look_axis.cross(upp_axis)
    vec = side_vec
    tm += pymel.datatypes.Matrix(
        axis.x * vec.x, axis.x * vec.y, axis.x * vec.z, 0,
        axis.y * vec.x, axis.y * vec.y, axis.y * vec.z, 0,
        axis.z * vec.x, axis.z * vec.y, axis.z * vec.z, 0,
        0, 0, 0, 0
    )

    return tm


def align_joints_to_view(
        joints, cam, affect_pos=True, look_axis=_X_AXIS, upp_axis=_Z_Axis
):
    """
    Align the up axis of selected joints to the look axis of a camera.
    """
    pos_start = joints[0].getTranslation(space='world')

    # Get camera direction
    cam_pos = cam.getTranslation(space='world')
    direction = cam_pos - pos_start

    align_joints_to_dir(
        joints, direction, affect_pos=affect_pos, look_axis=look_axis, upp_axis=upp_axis
    )


def align_joints_to_direction(
        joints, direction, affect_pos=True, look_axis=_X_AXIS, upp_axis=_Z_Axis
):
    """
    Align the up axis of selected joints to a direction vector.

    :param joints:
    :param direction:
    :param affect_pos:
    :param look_axis:
    :param upp_axis:
    :return:
    """
    pos_start = joints[0].getTranslation(space='world')

    # Conform direction to Vector
    direction = pymel.datatypes.Vector(direction)
    direction.normalize()  # TODO: Do no modify by reference

    # Store original positions
    positions_orig = [joint.getTranslation(space='world') for joint in joints]

    # Compute positions that respect the plane
    positions = []
    if affect_pos:

        pos_inn = positions_orig[0]
        pos_out = positions_orig[-1]
        dir = pos_out - pos_inn
        ref_tm = get_matrix_from_direction(dir, direction)
        ref_tm.translate = pos_inn
        ref_tm_inv = ref_tm.inverse()

        for i in range(len(joints)):
            joint_pos = positions_orig[i]
            if i == 0:
                positions.append(joint_pos)
            else:
                joint_local_pos = (joint_pos - pos_start) * ref_tm_inv

                # Remove any translate out of the 2D plane
                multiplier = look_axis + upp_axis
                # joint_local_pos.z = 0
                joint_local_pos.x *= multiplier.x
                joint_local_pos.y *= multiplier.y
                joint_local_pos.z *= multiplier.z

                new_joint_pos = (joint_local_pos * ref_tm) + pos_start
                positions.append(new_joint_pos)
    else:
        for joint in joints:
            positions.append(joint.getTranslation(space='world'))

    # Compute transforms
    transforms = []
    num_positions = len(positions)
    for i in range(num_positions):
        pos_inn = positions[i]

        # Compute rotation-only matrix
        if i < num_positions - 1:
            pos_out = positions[i + 1]
            # Compute look axis
            x_axis = pos_out - pos_inn
            x_axis.normalize()

            # Compute side axis
            z_axis = pymel.datatypes.Vector(x_axis).cross(direction)

            # Compute up axis (corrected)
            y_axis = z_axis.cross(x_axis)

            # Next ref_y_axis will use parent correct up axis to prevent flipping
            direction = y_axis

            tm = get_matrix_from_direction(x_axis, y_axis, look_axis=look_axis,
                                           upp_axis=upp_axis)
        else:
            tm = transforms[
                i - 1].copy()  # Last joint share the same rotation as it's parent

        # Add translation
        if affect_pos:
            tm.translate = pos_inn
        else:
            tm.translate = positions_orig[i]

        transforms.append(tm)

    # Apply transforms
    for transform, node in zip(transforms, joints):
        node.setMatrix(transform, worldSpace=True)


def get_active_camera():
    """
    Return the active camera.
    Thanks to Nohra Seif for the snippet!
    """
    # seems that $gMainPane contain the name of the main window pane layout holding the panels.
    main_pane = mel.eval('string $test = $gMainPane;')
    if main_pane != "":
        # get the layout's immediate children
        main_pane_ctrls = pymel.paneLayout(main_pane, q=True, childArray=True)
        for i in range(len(main_pane_ctrls)):
            # panel containing the specified control
            panel_name = pymel.getPanel(containing=main_pane_ctrls[i])
            if "" != panel_name:
                # Return the type of the specified panel.
                if ("modelPanel" == pymel.getPanel(typeOf=panel_name)):
                    # Return whether the control can actually be seen by the user, isObscured for invisible
                    if not (pymel.control(main_pane_ctrls[i], q=True, isObscured=True)):
                        model_editor = pymel.modelPanel(panel_name, q=True,
                                                        modelEditor=True)
                        if model_editor:
                            # If this view is already active, let's continue to use it.
                            if pymel.modelEditor(model_editor, q=True, activeView=True):
                                # get the camera in the current modelPanel
                                return pymel.PyNode(
                                    pymel.modelPanel(model_editor, q=True, camera=True))


def align_selected_joints_to_active_view(default_cam='persp'):
    sel = pymel.selected()
    cam = get_active_camera()
    if not cam:
        pymel.warning("Can't find active camera, will use {0}.".format(default_cam))
        cam = pymel.PyNode(default_cam)
    align_joints_to_view(sel, cam)


def align_selected_joints_to_persp():
    # TODO: Deprecated, remove me after 2016-05-01
    sel = pymel.selected()
    cam = pymel.PyNode('persp')
    align_joints_to_view(sel, cam)


def _filter_shape(obj, key):
    if not isinstance(obj, pymel.nodetypes.SurfaceShape):
        return False

    if obj.intermediateObject.get():
        return False

    if key is not None and not key(obj):
        return False

    return True


def get_nearest_affected_mesh(jnt, key=None):
    """
    Return the immediate mesh affected by provided object in the geometry stack.
    """
    affected_meshes = [hist for hist in jnt.listHistory(future=True) if
                       _filter_shape(hist, key)]

    return next(iter(affected_meshes), None)


def get_farest_affected_mesh(jnt, key=None):
    """
    Return the last mesh affected by provided object in the geometry stack.
    Usefull to identify which mesh to use in the 'doritos' setup.
    """
    affected_meshes = [hist for hist in jnt.listHistory(future=True) if
                       _filter_shape(hist, key)]

    return next(iter(reversed(affected_meshes)), None)


def get_multi_attr_available_slot(attr_multi):
    # "Safe" way to get available attribute child of an attribute.
    i = 0
    while attr_multi[i].isDestination():
        i += 1
    return attr_multi[i]


def get_closest_point_on_mesh(mesh, pos):
    """
    Return informations about the closest intersection between a point and a mesh polygons.
    :param mesh: A pymel.nodetypes.Mesh to analyze.
    :param pos: A pymel.datatypes.Vector world-space position.
    :return: A 3-sized tuple containing:
    - A pymel.datatypes.Vector representing the closest intersection between the mesh and the provided position.
    - The u coordinate of the resulting position.
    - The v coordinate of the resulting position.
    If nothing is found, a 3-sized tuple containing all None values are returned.
    """
    if isinstance(mesh, pymel.nodetypes.Transform):
        mesh = mesh.getShape()

    if not isinstance(mesh, pymel.nodetypes.Mesh):
        raise IOError("Unexpected datatype. Expected Mesh, got {0}".format(type(mesh)))

    # closestPointOnMesh ignores polymesh transforms
    util_transformGeometry = create_utility_node('transformGeometry',
                                                 inputGeometry=mesh.outMesh,
                                                 transform=mesh.worldMatrix
                                                 )

    # TODO: maybe support multiple uv sets?
    util_cpom = create_utility_node('closestPointOnMesh',
                                    inPosition=pos,
                                    inMesh=util_transformGeometry.outputGeometry
                                    )

    pos = util_cpom.position.get()
    u = util_cpom.parameterU.get()
    v = util_cpom.parameterV.get()

    pymel.delete(util_transformGeometry)
    pymel.delete(util_cpom)

    return pos, u, v


def get_closest_point_on_surface(nurbsSurface, pos):
    if isinstance(nurbsSurface, pymel.nodetypes.Transform):
        nurbsSurface = nurbsSurface.getShape(noIntermediate=True)

    if not isinstance(nurbsSurface, pymel.nodetypes.NurbsSurface):
        raise IOError("Unexpected datatype. Expected NurbsSurface, got {0}".format(
            type(nurbsSurface)))

    # closestPointOnSurface don't listen to transform so we'll need to duplicate the shape.
    util_cpos = create_utility_node('closestPointOnSurface',
                                    inPosition=pos,
                                    inputSurface=nurbsSurface.worldSpace
                                    )

    pos = util_cpos.position.get()
    u = util_cpos.parameterU.get()
    v = util_cpos.parameterV.get()

    # follicles use normalized uv's when attaching to nurbs so we need to know the uv min max values
    surface_min_u, surface_max_u = nurbsSurface.minMaxRangeU.get()
    surface_min_v, surface_max_v = nurbsSurface.minMaxRangeV.get()
    u = abs((u - surface_min_u) / (surface_max_u - surface_min_u))
    v = abs((v - surface_min_v) / (surface_max_v - surface_min_v))

    pymel.delete(util_cpos)

    return pos, u, v


def get_closest_point_on_shape(shape, pos):
    if isinstance(shape, pymel.nodetypes.Transform):
        shape = shape.getShape(noIntermediate=True)

    if isinstance(shape, pymel.nodetypes.Mesh):
        return get_closest_point_on_mesh(shape, pos)
    elif isinstance(shape, pymel.nodetypes.NurbsSurface):
        return get_closest_point_on_surface(shape, pos)
    raise NotImplementedError(
        "Unexpected data type. Expected Mesh or NurbsSurface, got {0}({1})".format(
            shape, type(shape)))


def get_closest_point_on_shapes(meshes, pos):
    """
    Return informations about the closest intersection between a point and multiple mesh polygons.
    :param mesh: A pymel.nodetypes.Mesh to analyze.
    :param pos: A pymel.datatypes.Vector world-space position.
    :return: A 4-sized tuple containing:
    - A pymel.nodetypes.Mesh instance representing the closest mesh.
    - A pymel.datatypes.Vector representing the closest intersection between the mesh and the provided position.
    - The u coordinate of the resulting position.
    - The v coordinate of the resulting position.
    If nothing is found, a 4-sized tuple containing all None values are returned.
    """
    shortest_delta = None
    return_val = (None, None, None, None)
    for mesh in meshes:
        closest_pos, closest_u, closest_v = get_closest_point_on_shape(mesh, pos)
        delta = libPymel.distance_between_vectors(pos, closest_pos)
        if shortest_delta is None or delta < shortest_delta:
            shortest_delta = delta
            return_val = (mesh, closest_pos, closest_u, closest_v)
    return return_val


def get_point_on_surface_from_uv(shape, u, v):
    follicle_shape = pymel.createNode('follicle')
    follicle_shape.parameterU.set(u)
    follicle_shape.parameterV.set(v)

    if isinstance(shape, pymel.nodetypes.Transform):
        shape = shape.getShape(noIntermediate=True)

    if isinstance(shape, pymel.nodetypes.NurbsSurface):
        pymel.connectAttr(shape.worldSpace, follicle_shape.inputSurface)
    elif isinstance(shape, pymel.nodetypes.Mesh):
        pymel.connectAttr(shape.outMesh, follicle_shape.inputMesh)
    else:
        raise Exception(
            "Unexpected shape type. Expected nurbsSurface or mesh, got {0}. {1}".format(
                type(shape), shape))

    pos = follicle_shape.outTranslate.get()
    follicle_transform = follicle_shape.getParent()
    pymel.delete(follicle_transform)

    return pos


# TODO: write an alternative method that work when the mesh have no UVs using pointOnMesh constraint.
def create_follicle2(shape, u=0, v=0, connect_transform=True):
    """
    Alternative to djRivet when you already know the u and v values.
    :param shape: The nurbsSurface to attach the follicle.
    :param u: The value of the follicle parameterU. Default to 0.
    :param v: The value of the follicle parameterV. Default to 0.
    :param connect_transform: If True, the output position and rotation will affect the follicle transform. Set the False if you wish to delete the transform afterward.
    :return: The created follicle shape.
    """
    follicle_shape = pymel.createNode('follicle')
    if isinstance(u, pymel.Attribute):
        pymel.connectAttr(u, follicle_shape.parameterU)
    else:
        follicle_shape.parameterU.set(u)
    if isinstance(v, pymel.Attribute):
        pymel.connectAttr(v, follicle_shape.parameterV)
    else:
        follicle_shape.parameterV.set(v)

    # HACK: If a transform was provided, use the first surface.
    if isinstance(shape, pymel.nodetypes.Transform):
        shape = shape.getShape(noIntermediate=True)

    if isinstance(shape, pymel.nodetypes.NurbsSurface):
        pymel.connectAttr(shape.worldSpace, follicle_shape.inputSurface)
    elif isinstance(shape, pymel.nodetypes.Mesh):
        '''
        # closestPointOnMesh ignores polymesh transforms
        util_transformGeometry = create_utility_node('transformGeometry',
                                                     inputGeometry=shape.outMesh,
                                                     transform=shape.worldMatrix
                                                     )
        '''

        pymel.connectAttr(shape.outMesh, follicle_shape.inputMesh)
    else:
        raise Exception(
            "Unexpected shape type. Expected nurbsSurface or mesh, got {0}. {1}".format(
                shape.type(), shape))

    if connect_transform:
        follicle_transform = follicle_shape.getParent()
        pymel.connectAttr(follicle_shape.outTranslate, follicle_transform.translate)
        pymel.connectAttr(follicle_shape.outRotate, follicle_transform.rotate)

    return follicle_shape


def get_average_pos_between_vectors(jnts):
    pos = pymel.datatypes.Vector()
    for jnt in jnts:
        pos += jnt.getTranslation(space='world')
    return pos / len(jnts)


def get_average_pos_between_nodes(jnts):
    nearest_jnt = None
    nearest_distance = None

    middle = get_average_pos_between_vectors(jnts)
    middle.y = 0
    middle.z = 0

    for jnt in jnts:
        jnt_pos = jnt.getTranslation(space='world')
        jnt_pos.y = 0
        jnt_pos.z = 0
        distance = libPymel.distance_between_vectors(jnt_pos, middle)
        # distance = abs(.x)
        if nearest_jnt is None or distance < nearest_distance:
            nearest_jnt = jnt
            nearest_distance = distance
    return nearest_jnt


#
# Driven Keys Methods
#

def create_animCurveU(type, kt, kv, kit=None, kot=None, kix=None, kiy=None, kox=None,
                      koy=None, pre=0, pst=0):
    """
    :param type:
    :param keys: A tuple containing the following values: key time, key value
    :param pre:
    :param post:
    :return:
    """
    # Use a temporary node to create the curve
    tmp = pymel.createNode('transform')

    # Resolve the attributes we'll want to "connect"
    att_src = tmp.sx
    att_dst = None
    if type == 'animCurveUU':
        att_dst = tmp.sy
    elif type == 'animCurveUL':
        att_dst = tmp.tx
    elif type == 'animCurveUA':
        att_dst = tmp.rx
    else:
        raise NotImplemented("Unexpected animCurve type. Got {0}.".format(type))

    # Create keys
    for key_time, key_val in zip(kt, kv):
        att_src.set(key_time)
        att_dst.set(key_val)
        pymel.setDrivenKeyframe(att_dst, cd=att_src)

    # Get curve and delete tmp object
    curve = next(iter(att_dst.inputs()))
    pymel.disconnectAttr(curve.output, att_dst)
    pymel.disconnectAttr(att_src, curve.input)
    pymel.delete(tmp)

    curve.setPreInfinityType(pre)
    curve.setPostInfinityType(pst)

    num_keys = len(kt)
    if kit:
        for i, ti in zip(range(num_keys), kit):
            curve.setInTangentType(i, ti)
    if kot:
        for i, to in zip(range(num_keys), kot):
            curve.setOutTangentType(i, to)
    if kix and kiy:
        for i, tix, tiy in zip(range(num_keys), kix, kiy):
            curve.setTangent(i, tix, tiy, True)
    if kox and koy:
        for i, tox, toy in zip(range(num_keys), kox, koy):
            curve.setTangent(i, tox, toy, False)

    return curve


def connectAttr_withBlendWeighted(attr_src, attr_dst, multiplier=None, **kwargs):
    # Check on which attribute @attr_dst is connected to (if applicable).
    attr_dst_input = next(iter(attr_dst.inputs(plugs=True, skipConversionNodes=True)),
                          None)

    # If the animCurve is not connected to a BlendWeighted node, we'll need to create one.
    if attr_dst_input is None or not isinstance(attr_dst_input.node(),
                                                pymel.nodetypes.BlendWeighted):
        util_blend = pymel.createNode('blendWeighted')

        if attr_dst_input is not None:
            next_available = util_blend.input.numElements()

            pymel.connectAttr(attr_dst_input, util_blend.input[next_available])

    else:
        util_blend = attr_dst_input.node()

    # todo: use blendWeighted for the multiplier?
    if multiplier:
        attr_src = create_utility_node('multiplyDivide', input1X=attr_src,
                                       input2X=multiplier).outputX

    next_input = get_multi_attr_available_slot(util_blend.input)
    pymel.connectAttr(attr_src, next_input)

    if not attr_dst.isDestination():
        pymel.connectAttr(util_blend.output, attr_dst, force=True, **kwargs)

    return util_blend


def _get_or_create_blendweighted_for_attr(attr):
    """
    Ensure that an attribute is connected to a blendWeighted node.
    If the attribute is already connected, inject an intermediate blendWeighted node.
    :param attr: An attribute to connect to
    :type attr: pymel.Attribute
    :return: A blendWeighted node
    :rtype: pymel.nodetypes.BlendWeighted
    """
    src_attr = next(iter(attr.inputs(plugs=True, skipConversionNodes=True)), None)
    src_node = src_attr.node() if src_attr else None

    if isinstance(src_node, pymel.nodetypes.BlendWeighted):
        return src_node

    blend = pymel.createNode('blendWeighted')

    if src_attr:
        next_available = blend.input.numElements()
        pymel.connectAttr(src_attr, blend.input[next_available])

    return blend


def connectAttrs_withBlendWeighted(srcs, dst, weights=None):
    """
    Connect multiples source attributes to a destination attribute
    with a blendWeighted node. For optimisation purpose, if the destination attribute
    is already connected to a blendWeighted node, it will be re-used.

    :param srcs: The source attributes
    :type srcs: list of pymel.Attribute
    :param dst: The destination attributes
    :type dst: pymel.Attribute
    :param weights: An optional list of weights to use
    :type weight: list[float] or list[pymel.Attribute]
    :return: The used blendWeighted node
    :rtype: pymel.nodetypes.BlendWeighted
    """
    util_blend = _get_or_create_blendweighted_for_attr(dst)
    if not dst.isDestination():
        pymel.connectAttr(util_blend.output, dst, force=True)

    if weights is None:
        weights = [None] * len(srcs)
    for src, weight in zip(srcs, weights):
        dst = get_multi_attr_available_slot(util_blend.input)
        pymel.connectAttr(src, dst)
        if weight:
            index_dst = dst.index()
            attr_weight = util_blend.weight[index_dst]
            if isinstance(weight, pymel.Attribute):
                pymel.connectAttr(weight, attr_weight)
            else:
                attr_weight.set(weight)


def getAttrOutput(attr, plugs=True, skipBlendWeighted=False, **kwargs):
    """
    Extend the capabilities of pymel.Attribute.outputs() by provided additional skip.
    :param attr:
    :param plugs:
    :param skipBlendWeighted:
    :param kwargs:
    :return:
    """
    attr_outs = attr.outputs(plugs=True, **kwargs)

    # Skip BlendWeighted
    if skipBlendWeighted:
        attr_outs_filtered = []
        for attr_out in attr_outs:
            attr_out_node = attr_out.node()
            if isinstance(attr_out_node, pymel.nodetypes.BlendWeighted):
                for attr_out in attr_out_node.output.outputs(plugs=True, **kwargs):
                    attr_outs_filtered.append(attr_out)
            else:
                attr_outs_filtered.append(attr_out)
        attr_outs = attr_outs_filtered

    if plugs:
        return attr_outs
    else:
        return [attr.node() for attr in attr_outs]


def connectAttr_withLinearDrivenKeys(attr_src, attr_dst, type='animCurveUU', force=True,
                                     kt=(-1.0, 0.0, 1.0),
                                     kv=(-1.0, 0.0, 1.0), kit=(4, 2, 4), kot=(4, 2, 4),
                                     pre='linear', pst='linear'):
    # Skip if a connection already exist
    for node in getAttrOutput(attr_src, plugs=False, skipBlendWeighted=True):
        if 'animCurveU' in node.type():
            drivenkey_outplugs = getAttrOutput(node.output, plugs=True,
                                               skipBlendWeighted=True)
            for drivenkey_outplug in drivenkey_outplugs:
                if drivenkey_outplug == attr_dst:
                    if force:
                        pymel.disconnectAttr(node.input)
                        pymel.disconnectAttr(node.output)
                        pymel.delete(node)
                    else:
                        print(
                        "Can't connect. Attribute {0} is already connected to {1} via {2}".format(
                            attr_src.longName(),
                            attr_dst.longName(),
                            drivenkey_outplug.node().longName()
                        ))
                        return

    animCurve = create_animCurveU('animCurveUU',
                                  kt=kt,
                                  kv=kv,
                                  kit=kit,  # Spline/Linear/Spline
                                  kot=kot,  # Spline/Linear/Spline
                                  pre=pre,
                                  pst=pst
                                  )
    animCurve.rename('{0}_{1}'.format(attr_src.node().name(), attr_src.longName()))
    pymel.connectAttr(attr_src, animCurve.input)
    return connectAttr_withBlendWeighted(animCurve.output, attr_dst)


def calibrate_attr_using_translation(attr, ref, step_size=0.1, epsilon=0.01,
                                     default=1.0):
    """
    Return the distance that @ref move when @attr is changed.
    This is used to automatically tweak the ctrl sensibility so the doritos have a more pleasant feel.
    Note that to compensate non-linear movement, a small value (@step_size) is used.
    """
    attr.set(0)
    pos_s = ref.getTranslation(space='world')
    attr.set(step_size)
    pos_e = ref.getTranslation(space='world')
    attr.set(0)
    distance = libPymel.distance_between_vectors(pos_s, pos_e) / abs(step_size)

    if distance > epsilon:
        return distance

    _LOG.warning("Can't detect sensibility for %s", attr)
    return default


def debug_matrix_attr(attr):
    util_decompose = create_utility_node(
        'decomposeMatrix',
        inputMatrix=attr
    )
    loc = pymel.spaceLocator()
    pymel.connectAttr(util_decompose.outputTranslate, loc.translate)
    pymel.connectAttr(util_decompose.outputRotate, loc.rotate)
    pymel.connectAttr(util_decompose.outputScale, loc.scale)
    return loc


def create_safe_division(attr_numerator, attr_denominator, nomenclature, suffix):
    """
    Create a utility node setup that prevent Maya from throwing a warning in case of division by zero.
    Maya is stupid when trying to handle division by zero in nodes.
    We can't use a condition after the multiplyDivide to deactivate it if the denominator is zero since
    the multiplyDivide will still get evaluated and throw a warning.
    For this reason we'll create TWO conditions, the second one will change the denominator to a non-zero value.
    :param attr_inn: A numerical value or pymel.Attribute instance representing the numerator.
    :param attr_out: A numerical value or pymel.Attribute instance representing the denominator.
    :return: A pymel.Attribute containing the result of the operation.
    """
    # Create a condition that force the denominator to have a non-zero value.
    attr_numerator_fake = create_utility_node(
        'condition',
        name=nomenclature.resolve('{}SafePre'.format(suffix)),
        firstTerm=attr_denominator,
        colorIfFalseR=attr_denominator,
        colorIfTrueR=0.01,
    ).outColorR
    attr_result = create_utility_node(
        'multiplyDivide',
        name=nomenclature.resolve(suffix),
        operation=2,  # division,
        input1X=attr_numerator,
        input2X=attr_numerator_fake
    ).outputX
    attr_result_safe = create_utility_node(
        'condition',
        name=nomenclature.resolve('{}SafePost'.format(suffix)),
        firstTerm=attr_denominator,
        colorIfFalseR=attr_result,
        colorIfTrueR=0.0
    ).outColorR
    return attr_result_safe
