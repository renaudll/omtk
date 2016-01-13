import pymel.core as pymel
from maya import OpenMaya

from omtk.libs.libPymel import SegmentCollection


def get_skin_cluster(obj):
    for hist in pymel.listHistory(obj):
        if isinstance(hist, pymel.nodetypes.SkinCluster):
            return hist
    return None

#@decorators.profiler
def transfer_weights(obj, sources, target):
    """
    Transfer skin weights from multiples joints to a specific joint.
    Took 0.193 in Makino.
    :param obj: The skinned geometry.
    :param sources: An array of the joints to transfer from.
    :param target: The joint to transfer to.
    :return:
    """
    # TODO: automatically unlock influences?

    # Validate obj type
    if not isinstance(obj, pymel.nodetypes.Mesh):
        raise IOError("Unsupported geometry. Expected Mesh, got {0}".format(type(obj)))

    # Resolve skinCluster
    skinCluster = get_skin_cluster(obj)
    if skinCluster is None:
        raise Exception("Can't find skinCluster on {0}".format(obj.__melobject__()))

    # Ensure no provided joints are locked
    for source in sources:
        if source.lockInfluenceWeights.get():
            source.lockInfluenceWeights.set(False)
    if target.lockInfluenceWeights.get():
        target.lockInfluenceWeights.set(False)

    # Resolve influence indices
    influence_jnts = skinCluster.influenceObjects()
    num_jnts = len(influence_jnts)
    jnt_src_indices = [influence_jnts.index(source) for source in sources]
    jnt_dst_index = influence_jnts.index(target)
    influences = OpenMaya.MIntArray()
    for i in range(len(influence_jnts)):
        influences.append(i)
    # TODO: add only necessary influences

    # Get weights
    old_weights = OpenMaya.MDoubleArray()
    mfnSkinCluster = skinCluster.__apimfn__()
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

#@decorators.profiler
def transfer_weights_from_segments(obj, source, targets, dropoff=2):
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

    # Resolve influence indices
    influence_objects = skinCluster.influenceObjects()
    jnt_src_index = influence_objects.index(source)
    jnt_dst_indexes = [influence_objects.index(target) for target in targets]

    # Store the affected joints only
    # This allow us to reference the index to navigate in the weights table.
    mint_influences = OpenMaya.MIntArray()
    mint_influences.append(jnt_src_index)
    for dst_index in jnt_dst_indexes:
        mint_influences.append(dst_index)
    chunk_size = mint_influences.length()

    segments = SegmentCollection.from_transforms(targets)

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
        old_weight = old_weights[memory_location]
        if old_weight:
            # Resolve weight using the vtx/cv position
            pos = OpenMaya.MVector(it_geometry.position(OpenMaya.MSpace.kWorld))  # MVector allow us to use .length()
            weights = _get_point_weights_from_segments_weights(segments, knot_weights, pos)

            # Ensure the total of the new weights match the old weights
            total_weights = 0.0
            for weight in weights:
                total_weights += weight
            ratio = old_weight / total_weights
            weights= [weight * ratio for weight in weights]

            # Write weights
            for i, weight in enumerate(weights):
                index = (v * chunk_size) + i + 1
                new_weights[index] = weight

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
    segments = SegmentCollection.from_transforms(jnts)
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


