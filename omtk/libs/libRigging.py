from maya import cmds
import pymel.core as pymel
import logging
import libPymel
import libPython

'''
This method facilitate the creation of utility nodes by connecting/settings automaticly attributes.
'''
__aBasicTypes = [int, float, bool, pymel.datatypes.Matrix, pymel.datatypes.Vector]


def is_basic_type(_val):
    global __aBasicTypes
    return type(_val) in __aBasicTypes


def connect_or_set_attr(_attr, _val):
    if isinstance(_val, list) or isinstance(_val, tuple):

        # Note: List attribute and compound attribute don't have the same way of iterating.
        if _attr.isArray():
            for i, val in enumerate(_val):
                connect_or_set_attr(_attr.elementByLogicalIndex(i), val)
        elif _attr.isCompound():
            children = _attr.getChildren()
            for child, val in zip(children, _val):
                connect_or_set_attr(child, val)
        else:
            raise Exception("Can't apply value {0} on attribute {1}, need an array or compound".format(_val, _attr))

        '''
        for i, pSubValue in enumerate(_val):
            ConnectOrSetAttr(_attr.elementByLogicalIndex(i), pSubValue)
        '''
    else:
        if isinstance(_val, pymel.Attribute):
            pymel.connectAttr(_val, _attr, force=True)
        elif is_basic_type(_val):
            _attr.set(_val)
        else:
            logging.error(
                '[ConnectOrSetAttr] Invalid value for attribute {0} of type {1} and value {2}'.format(_attr.name(),
                                                                                                      type(_val),
                                                                                                      _val))
            raise TypeError


def create_utility_node(_sClass, *args, **kwargs):
    uNode = pymel.shadingNode(_sClass, asUtility=True)
    for sAttrName, pAttrValue in kwargs.items():
        if not uNode.hasAttr(sAttrName):
            raise Exception(
                '[CreateUtilityNode] UtilityNode {0} doesn\'t have an {1} attribute. Skipping it.'.format(_sClass,
                                                                                                          sAttrName))
        else:
            connect_or_set_attr(uNode.attr(sAttrName), pAttrValue)
    return uNode


#
# CtrlShapes Backup
#
def hold_ctrl_shapes(transform, parent=None):
    shapes = filter(lambda x: isinstance(x, pymel.nodetypes.CurveShape), transform.getShapes())
    snapshot = pymel.duplicate(transform, parentOnly=True, returnRootsOnly=True)[0]
    for shape in shapes:
        shape.setParent(snapshot, s=True, r=True)
    if parent:
        snapshot.setParent(parent)
    else:
        snapshot.setParent(world=True)

    new_name = '_{0}'.format(transform.name())
    cmds.rename(snapshot.longName(), new_name)  # For strange reasons, using .rename don't always work.
    return snapshot


def fetch_ctrl_shapes(source, target):
    # Remove any previous shapes
    pymel.delete(filter(lambda x: isinstance(x, pymel.nodetypes.CurveShape), target.getShapes()))
    for source_shape in source.getShapes():
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
    curveLength = create_utility_node('curveInfo', inputCurve=curve_shape.worldSpace).arcLength
    return create_utility_node('multiplyDivide', operation=2, input1X=curveLength, input2X=curveLength.get()).outputX

def create_stretch_attr_from_nurbs_plane(nurbs_shape, u=1.0, v=1.0):
    """
    Compute the stretch applied on a pymel.nodetypes.NurbsSurface.
    :param nurbs_shape: The pymel.nodetypes.NurbsSurface node.
    :return: The stretch attribute and an arcLengthDimension that will need to be parented somewhere.
    """
    arcLengthDimension_shape = pymel.createNode('arcLengthDimension')
    arcLengthDimension_shape.uParamValue.set(u)
    arcLengthDimension_shape.vParamValue.set(v)
    pymel.connectAttr(nurbs_shape.worldSpace, arcLengthDimension_shape.nurbsGeometry)
    attr_length_u = arcLengthDimension_shape.arcLength
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

def create_squash_attr_simple(attr_stretch):
    return create_utility_node('multiplyDivide', operation=2, input1X=1.0, input2X=attr_stretch).outputX

def create_squash_attr(attr_stretch):
    #return next(iter(create_squash_atts(attr_stretch, 1)))
    attr_stretch_inv = create_utility_node('multiplyDivide', operation=2, input1X=1.0, input2X=attr_stretch).outputX
    return create_utility_node('multiplyDivide', operation=3, input1X=attr_stretch_inv, input2X=2).outputX

def create_squash_atts(attr_stretch, samples):
    """
    Create attributes resolving a curve using the following formula.
    s^(e^(x^2)))
    see: http://www.wolframalpha.com/input/?i=%28x%5E2-1%29*-1
    :param attr_stretch: # The stretch attribute.
    :param samples: Number of samples to resolve.
    """
    import libFormula
    if not isinstance(attr_stretch, pymel.Attribute):
        raise IOError("Expected pymel Attribute, got {0} ({1})".format(attr_stretch, type(attr_stretch)))

    attr_stretch_inv = create_utility_node('multiplyDivide', operation=2, input1X=1.0, input2X=attr_stretch).outputX

    return_vals = []
    for i in range(samples):
        pos = float(i) / (samples - 1) * 2.0 - 1.0

        # Blend between no squash and full squash using a bell curve.
        # 0 = Maximum Squash
        # 1 = No Squash
        # see see: http://www.wolframalpha.com/input/?i=%28x%5E2-1%29*-1
        blend = libFormula.parse("x^2", x=pos)

        attr_squash = libFormula.parse("((max-min)*blend)+min",
            min=attr_stretch_inv,
            max=1,
            blend=blend
        )

        return_vals.append(attr_squash)
    return return_vals

def interp_linear(r, s, e):
    return (e - s) * r + s

def interp_linear_multiple(ratios, s, e):
    return [interp_linear(ratio, s, e) for ratio in ratios]

def create_nurbs_plane_from_joints(jnts, degree=1, width=1):
    """
    Create a nurbsPlane following a provided joint chain.
    Note that the plane is oriented in the up axis (Y) of each joint.
    """

    # Create nurbsPlane
    num_patches_u = (len(jnts)-1)
    plane = pymel.nurbsPlane(d=degree, u=num_patches_u)[0]

    pos_upp_local = pymel.datatypes.Point(0,0,width)
    pos_dwn_local = pymel.datatypes.Point(0,0,-width)

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
    v_ratios = [v / float(num_patches_v-1) for v in range(num_patches_v)]

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
    for i in range(num_edges-1):
        pos_upp_inn = edges_positions_upp[i]
        pos_dwn_inn = edges_positions_dwn[i]
        is_first = i == 0
        is_before_last = i == num_edges - 2
        is_last  = i == num_edges - 1

        # Add edge (note that we always add the first and last edge edge).
        if is_first or is_last or add_inside_edges:
            all_positions.append(interp_linear_multiple(v_ratios, pos_upp_inn, pos_dwn_inn))

        # Add in-betweens
        if is_last:  # For obvious reasons, we don't want to add any points after the last edge.
            continue

        num_inbetweens = num_inbetweens_outside if is_first or is_before_last else num_inbetweens_inside

        if num_inbetweens:
            pos_upp_out = edges_positions_upp[i+1]
            pos_dwn_out = edges_positions_dwn[i+1]
            for j in range(num_inbetweens_outside):
                ratio = float(j+1)/(num_inbetweens_outside+1)
                pos_upp = interp_linear(ratio, pos_upp_inn, pos_upp_out)
                pos_dwn = interp_linear(ratio, pos_dwn_inn, pos_dwn_out)
                all_positions.append(interp_linear_multiple(v_ratios, pos_upp, pos_dwn))

    # Add last edge
    all_positions.append(interp_linear_multiple(v_ratios, edges_positions_upp[-1], edges_positions_dwn[-1]))


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
        _oObjs[i].setParent(_oObjs[i-1])


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
        new_obj.setMatrix(tm)
        new_obj.setTranslation(pos, space='world')
        new_objs.append(new_obj)

    new_objs[0].setParent(world=True)
    if parented:
        create_hyerarchy(new_objs)

    return libPymel.PyNodeChain(new_objs)
from maya import OpenMaya

def get_affected_geometries(obj):
    """
    :param obj: A reference object, generally a pymel.nodetypes.Join.
    :return: The geometries affected by the object.
    """
    geometries = set()

    if isinstance(obj, pymel.nodetypes.Joint):
        # Collect all geometries affected by the joint.
        skinClusters = set()
        for hist in obj.listHistory(future=True):
            if isinstance(hist, pymel.nodetypes.SkinCluster):
                skinClusters.add(hist)

        for skinCluster in skinClusters:
            geometries.update(skinCluster.getOutputGeometry())

    return geometries


def reshape_ctrl(ctrl_shape, ref, multiplier=1.25):
    if not isinstance(ctrl_shape, pymel.nodetypes.NurbsCurve):
        raise Exception("Unexpected input, expected NurbsCurve, got {0}.".format(type(ctrl_shape)))

    geometries = get_affected_geometries(ref)
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


@libPython.memoized
def get_recommended_ctrl_size(obj, default_value=1.0, weight_x=0.0, weight_neg_x=0.0, weight_y=1.0,
                              weight_neg_y=1.0, weight_z=0.0, weight_neg_z=0.0):
    """
    Return the recommended size of a controller if it was created for this obj.
    :param obj: The object to analyze.
    """
    # TODO: Move to a cleaner location?
    if isinstance(obj, pymel.nodetypes.Joint):

        # Collect all geometries affected by the joint.
        skinClusters = set()
        for hist in obj.listHistory(future=True):
            if isinstance(hist, pymel.nodetypes.SkinCluster):
                skinClusters.add(hist)
        geometries = set()
        for skinCluster in skinClusters:
            geometries.update(skinCluster.getOutputGeometry())

        # Create a number of raycast for each geometry. Use the longuest distance.
        # Note that we are not using the negative Y axis, this give bettern result for example on shoulders.
        ref_tm = obj.getMatrix(worldSpace=True)
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
        results = OpenMaya.MPointArray()
        for geometry in geometries:
            mfn_geo = geometry.__apimfn__()
            for dir in dirs:
                if mfn_geo.intersect(pos, dir, results, 1.0e-10, OpenMaya.MSpace.kWorld):
                    cur_length = min((results[0].distanceTo(pos) for i in range(results.length())))
                    if cur_length > length:
                        length = cur_length
        if not length:
            length = obj.radius.get()
        return length

    print "Cannot get recommended size for {0}, return default value of {1}".format(
        obj.name(), default_value
    )
    return default_value

def ray_cast(pos, dir, geometries, debug=False):
    """
    Simple pymel wrapper for the MFnGeometry intersect method.
    :param pos: Any OpenMaya.MPoint compatible type (ex: pymel.datatypes.Point)
    :param dir: Any OpenMaya.MVector compatible type (ex: pymel.datatypes.Vector)
    :param geometries: The geometries to intersect.
    :param debug: If True, spaceLocators will be created at intersection points.
    :return: pymel.datatypes.Point list containing the intersection points.
    """
    # Cast pos to OpenMaya.MPoint if necessary.
    if type(pos) != OpenMaya.MPoint:
        pos = OpenMaya.MPoint(pos.x, pos.y, pos.z)

    # Cast dir to OpenMaya.MVector if necessary.
    if type(dir) != OpenMaya.MVector:
        dir = OpenMaya.MVector(dir.x, dir.y, dir.z)

    results = []

    buffer_results = OpenMaya.MPointArray()
    for geometry in geometries:
        mfn_geo = geometry.__apimfn__()
        if mfn_geo.intersect(pos, dir, buffer_results, 1.0e-10, OpenMaya.MSpace.kWorld):
            for i in range(buffer_results.length()):
                results.append(pymel.datatypes.Point(buffer_results[i]))

    if debug:
        for result in results:
            loc = pymel.spaceLocator()
            loc.setTranslation(result)

    return results


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
            print jnt, joint_data
            transform, make = pymel.polyCube(height=length, width=length*0.33, depth=length*0.33)
            r_offset = pymel.datatypes.Matrix(0, -1.0, -0.0, 0.0, 1.0, 0, 0.0, 0.0, 0.0, -0.0, 1.0, 0.0,
                                              joint_data.dir[0]*length*0.5,
                                              joint_data.dir[1]*length*0.5,
                                              joint_data.dir[2]*length*0.5,
                                              1.0)
            cylinder_tm = r_offset
            transform.setParent(jnt)
            transform.setMatrix(cylinder_tm)
            boxes.append(transform)
    return boxes

def collect_proxy_boxes():
    return_values = []
    for obj in pymel.ls(type='transform'):
        if any((hist for hist in obj.listHistory() if isinstance(hist, pymel.nodetypes.PolyCube))):
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
    #pymel.delete(boxes)

    # set skin weights
    pymel.skinCluster(jnts, outputMesh.getParent(), toSelectedBones=True)
    skinCluster = next((hist for hist in outputMesh.listHistory() if isinstance(hist, pymel.nodetypes.SkinCluster)), None)
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

def get_matrix_from_direction(look_vec, upp_vec):
    # Ensure we deal with normalized vectors
    look_vec.normalize()
    upp_vec.normalize()

    side_vec = pymel.datatypes.Vector.cross(look_vec, upp_vec)
    #recross in case up and front were not originally orthogonal:
    upp_vec = pymel.datatypes.Vector.cross(side_vec, look_vec)

    #the new matrix is
    return pymel.datatypes.Matrix (
        look_vec.x, look_vec.y, look_vec.z, 0,
        upp_vec.x, upp_vec.y, upp_vec.z, 0,
        side_vec.x, side_vec.y, side_vec.z, 0,
        0, 0, 0, 1)

'''
def debug_pos(pos):
    l = pymel.spaceLocator()
    l.setTranslation(pos)

def debug_tm(tm):
    l = pymel.spaceLocator()
    l.setMatrix(tm)
    l.s.set(10,10,10)
'''

def align_joints_to_view(joints, cam, affect_pos=True):
    """
    Align the up axis of selected joints to the look axis of a camera.
    Similar to an existing functionnality in blender.
    """

    pos_start = joints[0].getTranslation(space='world')

    # Get camera direction
    cam_tm = cam.getMatrix(worldSpace=True)
    cam_pos = cam.getTranslation(space='world')
    cam_upp = cam_pos - pos_start
    cam_upp.normalize()

    # Store original positions
    positions_orig = [joint.getTranslation(space='world') for joint in joints]

    # Compute positions that respect the plane
    positions = []
    if affect_pos:

        pos_inn = positions_orig[0]
        pos_out = positions_orig[-1]
        look_axis = pos_out - pos_inn
        ref_tm = get_matrix_from_direction(look_axis, cam_upp)
        ref_tm.translate = pos_inn
        ref_tm_inv = ref_tm.inverse()

        for i in range(len(joints)):
            joint = joints[i]
            joint_pos = positions_orig[i]
            if i == 0:
                positions.append(joint_pos)
            else:
                joint_local_pos = (joint_pos - pos_start) * ref_tm_inv
                joint_local_pos.z = 0
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
        if i < num_positions-1:
            pos_out = positions[i+1]
            # Compute look axis
            x_axis = pos_out - pos_inn
            x_axis.normalize()

            # Compute side axis
            z_axis = pymel.datatypes.Vector(x_axis).cross(cam_upp)

            # Compute up axis (corrected)
            y_axis = z_axis.cross(x_axis)

            # Next ref_y_axis will use parent correct up axis to prevent flipping
            cam_upp = y_axis

            tm = get_matrix_from_direction(x_axis, y_axis)
        else:
            tm = transforms[i-1].copy() # Last joint share the same rotation as it's parent

        # Add translation
        if affect_pos:
            tm.translate = pos_inn
        else:
            tm.translate = positions_orig[i]

        transforms.append(tm)

    # Apply transforms
    for transform, node in zip(transforms, joints):
        node.setMatrix(transform, worldSpace=True)



def align_selected_joints_to_persp ():
    sel = pymel.selected()
    cam = pymel.PyNode('persp')
    align_joints_to_view(sel, cam)