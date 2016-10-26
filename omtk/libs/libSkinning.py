import pymel.core as pymel
from maya import OpenMaya
from omtk.libs import libPymel

def get_skin_cluster(obj):
    if isinstance(obj, pymel.nodetypes.SkinCluster):
        return obj
    for hist in pymel.listHistory(obj):
        if isinstance(hist, pymel.nodetypes.SkinCluster):
            return hist
    return None

#@decorators.profiler
def transfer_weights(obj, sources, target, add_missing_influences=False):
    """
    Transfer skin weights from multiples joints to a specific joint.
    Took 0.193 in Makino.
    :param obj: The skinned geometry or the Skin Cluster
    :param sources: An array of the joints to transfer from.
    :param target: The joint to transfer to.
    :return:
    """
    # TODO: automatically unlock influences?
    # TODO: add missing influences if necessary?

    # Validate obj type
    if not isinstance(obj, pymel.nodetypes.Mesh) and not isinstance(obj, pymel.nodetypes.SkinCluster):
        raise IOError("Unsupported geometry. Expected Mesh or SkinCluster, got {0}".format(type(obj)))

    # Resolve skinCluster
    skinCluster = get_skin_cluster(obj)
    if skinCluster is None:
        raise Exception("Can't find skinCluster on {0}".format(obj.__melobject__()))

    # Resolve influence indices
    influence_jnts = skinCluster.influenceObjects()

    # Add target if missing, otherwise thrown an error.
    if target not in influence_jnts:
        print("Can't find target {0} in skinCluster {1}".format(target.name(), skinCluster.name()))
        skinCluster.addInfluence(target, weight=0)
        influence_jnts.append(target)

    # Hack: Remove influences not present in skinCluster
    sources = filter(lambda jnt: jnt in influence_jnts, sources)

    if not sources:
        print "Abording transfering on {0}, nothing to transfer".format(obj.name())
        return

    num_jnts = len(influence_jnts)
    jnt_src_indices = [influence_jnts.index(source) for source in sources]
    jnt_dst_index = influence_jnts.index(target)
    influences = OpenMaya.MIntArray()
    for i in range(len(influence_jnts)):
        influences.append(i)

    # Ensure no provided joints are locked
    for source in sources:
        if source.lockInfluenceWeights.get():
            source.lockInfluenceWeights.set(False)
    if target.lockInfluenceWeights.get():
        target.lockInfluenceWeights.set(False)


    # Get weights
    old_weights = OpenMaya.MDoubleArray()
    mfnSkinCluster = skinCluster.__apimfn__()

    # Hack: If for any reasons a skinCluster was provided, use the first shape.
    if isinstance(obj, pymel.nodetypes.SkinCluster):
        new_obj = next(iter(obj.getOutputGeometry()), None)
        if new_obj is None:
            pymel.warning("Can't transfert weights. No geometry found affected by {0}.".format(obj))
            return
        obj = new_obj

    geometryDagPath = obj.__apimdagpath__()
    component = pymel.api.toComponentMObject(geometryDagPath)
    mfnSkinCluster.getWeights(geometryDagPath, component, influences, old_weights)

    # Compute new weights
    new_weights = OpenMaya.MDoubleArray()
    new_weights.copy(old_weights)
    num_vertices = len(obj.vtx)
    for v in range(num_vertices):
        total_weight = 0
        # Remove source weights
        for source_index in jnt_src_indices:
            i = source_index + (v * num_jnts)
            w = new_weights[i]
            if w:
                new_weights[i] = 0
                total_weight += w
        # Apply target weights if necessary
        if total_weight:
            i = jnt_dst_index + (v * num_jnts)
            new_weights[i] += total_weight

    mfnSkinCluster.setWeights(geometryDagPath, component, influences, new_weights, old_weights)

def transfer_weights_replace(source, target):
    """
    Quickly transfer weight for a source to a target by swapping the connection.
    Fast but only usefull when you are willing to lose the weights stored in target.
    """
    skinToReset = set()

    #TODO : Ensure that the transfered lockInfluenceWeight attr work correctly (The lock icon doesn't appear in the skinCluster)
    if source.hasAttr('lockInfluenceWeights'):
        attr_lockInfluenceWeights_src = source.lockInfluenceWeights
        #The target bone could possibly not have the attribute
        if target.hasAttr('lockInfluenceWeights'):
            attr_lockInfluenceWeights_dst = target.lockInfluenceWeights
        else:
            target.addAttr("lockInfluenceWeights", at="bool")
            attr_lockInfluenceWeights_dst = target.lockInfluenceWeights
            attr_lockInfluenceWeights_dst.set(attr_lockInfluenceWeights_src.get())
        for plug in attr_lockInfluenceWeights_src.outputs(plugs=True):
            if isinstance(plug.node(), pymel.nodetypes.SkinCluster):
                skinToReset.add(plug.node())
                pymel.disconnectAttr(attr_lockInfluenceWeights_src, plug)
                pymel.connectAttr(attr_lockInfluenceWeights_dst, plug)

    attr_objectColorRGB_src = source.attr('objectColorRGB')
    attr_objectColorRGB_dst = target.attr('objectColorRGB')
    for plug in attr_objectColorRGB_src.outputs(plugs=True):
        if isinstance(plug.node(), pymel.nodetypes.SkinCluster):
            pymel.disconnectAttr(attr_objectColorRGB_src, plug)
            pymel.connectAttr(attr_objectColorRGB_dst, plug)

    attr_worldMatrix_dst = target.worldMatrix
    for attr_worldMatrix_src in source.worldMatrix:
        for plug in attr_worldMatrix_src.outputs(plugs=True):
            if isinstance(plug.node(), pymel.nodetypes.SkinCluster):
                pymel.disconnectAttr(attr_worldMatrix_src, plug)
                pymel.connectAttr(attr_worldMatrix_dst, plug)

    #HACK : Evaluate back all skinCluster in which we changed connections
    pymel.dgdirty(skinToReset)

    '''
    skinClusters = set()
    for source in sources:
        for hist in source.listHistory(future=True):
            if isinstance(hist, pymel.nodetypes.SkinCluster):
                skinClusters.add(hist)

    for skinCluster in skinClusters:
        for geo in skinCluster.getGeometry():
            # Only mesh are supported for now
            if not isinstance(geo, pymel.nodetypes.Mesh):
                continue

            try:
                transfer_weights(geo, sources, target, **kwargs)
            except ValueError:  # jnt_dwn not in skinCluster
                pass
    '''

def interp_linear(r, s, e):
    return (e - s) * r + s

def interp_cubic(x):
    """
    src: http://stackoverflow.com/questions/1146281/cubic-curve-smooth-interpolation-in-c-sharp
    """
    return (x * x) * (3.0 - (2.0 * x))

def _get_point_weights_from_segments_weights(segments, segments_weights, pos):
    knot_index, ratio = segments.closest_segment_index(pos)
    knot_index_next = knot_index + 1 # TODO: Handle out of bound
    point_weights_inn = segments_weights[knot_index]
    point_weights_out = segments_weights[knot_index_next]
    point_weights = [(weight_out - weight_inn)*interp_cubic(ratio) + weight_inn for weight_inn, weight_out in zip(point_weights_inn, point_weights_out)]
    return point_weights

#@libPython.profiler
def transfer_weights_from_segments(obj, source, targets, dropoff=1.0, force_straight_line=False):
    """
    Automatically assign skin weights from source to destinations using the vertices position.
    """
    # Resolve the world position of the targets
    dst_positions = []
    for target in targets:
        dst_positions.append(target.getTranslation(space='world'))

    # Resolve skinCluster
    skinCluster = get_skin_cluster(obj)
    if skinCluster is None:
        raise Exception("Can't find skinCluster on {0}".format(obj.__melobject__()))

    # Resolve source indices
    influence_objects = skinCluster.influenceObjects()
    try:
        jnt_src_index = influence_objects.index(source)
    except ValueError:
        pymel.warning("Can't transfer weights from segments in {0}, source {1} is missing from skinCluster.".format(
            obj.__melobject__(),
            source.__melobject__()
        ))
        return False

    # Resolve targets indices
    targets = [target for target in targets if target in influence_objects]
    if not targets:
        pymel.warning("Can't transfer weights from segments in {0}, no targets found in skinCluster.".format(
            obj.__melobject__()
        ))
        return False
    jnt_dst_indexes = [influence_objects.index(target) for target in targets]

    # Store the affected joints only
    # This allow us to reference the index to navigate in the weights table.
    mint_influences = OpenMaya.MIntArray()
    mint_influences.append(jnt_src_index)
    for dst_index in jnt_dst_indexes:
        mint_influences.append(dst_index)
    chunk_size = mint_influences.length()

    # Resolve the positions to use for computing the segments.
    knot_positions = []
    for target in targets:
        # todo: document why we are using OpenMaya here
        mfn_transform = target.__apimfn__()
        pos = OpenMaya.MVector(mfn_transform.getTranslation(OpenMaya.MSpace.kWorld))
        knot_positions.append(pos)

    if force_straight_line:
        total_length = 0
        num_positions = len(knot_positions)
        # Resolve segment lengths
        segment_lengths = []
        for i in range(num_positions-1):
            pos_s = knot_positions[i]
            pos_e = knot_positions[i+1]
            length = (pos_s - pos_e).length()
            segment_lengths.append(length)
            total_length += length

        # Resolve segments ratios
        segment_ratios = [0.0]
        ratio_incr = 0
        for length in segment_lengths:
            ratio_incr += length / total_length
            segment_ratios.append(ratio_incr)

        # Compute new positions in a straight line.
        pos_s = knot_positions[0]
        pos_e = knot_positions[-1]
        knot_positions = []
        for ratio in segment_ratios:
            pos = (pos_e - pos_s) * ratio + pos_s
            knot_positions.append(pos)

    segments = libPymel.SegmentCollection.from_positions(knot_positions)

    # Get weights
    old_weights = OpenMaya.MDoubleArray()
    mfnSkinCluster = skinCluster.__apimfn__()
    geometryDagPath = obj.__apimdagpath__()
    component = pymel.api.toComponentMObject(geometryDagPath)
    mfnSkinCluster.getWeights(geometryDagPath, component, mint_influences, old_weights)

    # Compute new weights
    new_weights = OpenMaya.MDoubleArray()
    new_weights.copy(old_weights)

    knot_weights = segments.get_knot_weights(dropoff=dropoff)

    it_geometry= OpenMaya.MItGeometry(geometryDagPath)
    vert_index = 0
    while not it_geometry.isDone():
        memory_location = (chunk_size * vert_index)
        source_weight = old_weights[memory_location]
        if source_weight:
            # Get the current weights already assigned to the target weight
            target_memory_location = memory_location + 1
            cur_target_weights = [old_weights[i] for i in range(target_memory_location, target_memory_location + len(targets))]
            # Resolve weight using the vtx/cv position
            pos = OpenMaya.MVector(it_geometry.position(OpenMaya.MSpace.kWorld))  # MVector allow us to use .length()
            weights = _get_point_weights_from_segments_weights(segments, knot_weights, pos)

            # Ensure the total of the new weights match the source weights + current target weight
            total_weights = 0.0
            for weight in weights:
                total_weights += weight
            ratio = source_weight / total_weights
            weights = [(weight * ratio) + cur_target_weights[i] for i, weight in enumerate(weights)]

            # Write weights
            for i, weight in enumerate(weights):
                index = (vert_index * chunk_size) + i + 1
                new_weights[index] = weight
            new_weights[vert_index * chunk_size] = 0.0  # Remove original weight

        it_geometry.next()
        vert_index += 1

    mfnSkinCluster.setWeights(geometryDagPath, component, mint_influences, new_weights, old_weights)


def assign_weights_from_segments(shape, jnts, dropoff=1.5):
    # Resolve skinCluster
    skinCluster = get_skin_cluster(shape)
    if skinCluster is None:
        raise Exception("Can't find skinCluster on {0}".format(shape.__melobject__()))

    # Resolve influence indices
    influence_objects = skinCluster.influenceObjects()
    jnt_indices = [influence_objects.index(jnt) for jnt in jnts]

    # Create the OpenMaya influence MIntArray
    mint_influences = OpenMaya.MIntArray()
    chunk_size = len(influence_objects)
    for i in range(chunk_size):
        mint_influences.append(i)

    # Resolve old weights (for undos)
    old_weights = OpenMaya.MDoubleArray()
    mfnSkinCluster = skinCluster.__apimfn__()
    geometryDagPath = shape.__apimdagpath__()
    component = pymel.api.toComponentMObject(geometryDagPath)
    mfnSkinCluster.getWeights(geometryDagPath, component, mint_influences, old_weights)

    # Resolve new weights
    # Note that we start with zero weight since we are re-skinning from scratch.
    segments = libPymel.SegmentCollection.from_transforms(jnts)
    knot_weights = segments.get_knot_weights(dropoff=dropoff)

    new_weights = OpenMaya.MDoubleArray(old_weights.length(), 0)

    # Iterate through all vtx/cvs
    it_geometry= OpenMaya.MItGeometry(geometryDagPath)
    vert_index = 0
    while not it_geometry.isDone():
        # Resolve weight using the vtx/cv position
        memory_location = (chunk_size * vert_index) + jnt_indices[0]
        pos = OpenMaya.MVector(it_geometry.position(OpenMaya.MSpace.kWorld))  # MVector allow us to use .length()
        weights = _get_point_weights_from_segments_weights(segments, knot_weights, pos)

        # Write weights
        for weight in weights:
            new_weights[memory_location] = weight
            memory_location += 1

        it_geometry.next()
        vert_index += 1


    mfnSkinCluster.setWeights(geometryDagPath, component, mint_influences, new_weights, old_weights)

#TODO : Reset the bind pose at the same time to prevent any problem
def reset_skin_cluster(skinCluster):
    influenceObjs = skinCluster.influenceObjects()
    pymel.skinCluster(skinCluster, e=True, unbindKeepHistory=True)
    for obj in skinCluster.getOutputGeometry():
        pymel.skinCluster(influenceObjs + [obj], tsb=True)

def reset_selection_skin_cluster():
    # Collect skinClusters
    skinClusters = set()
    for obj in pymel.selected():
        skinCluster = get_skin_cluster(obj)
        if skinCluster:
            skinClusters.add(skinCluster)

    for skinCluster in skinClusters:
        reset_skin_cluster(skinCluster)
