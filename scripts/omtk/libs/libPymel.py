"""
Helpers that extend pymel capabilities.
"""
import logging
import pymel.core as pymel
from maya import OpenMaya
from maya import cmds
from pymel import core as pymel

_LOG = logging.getLogger(__name__)


def is_valid_PyNode(val):
    """
    Determine if a provided value is a valid pymel PyNode/Attribute by duck-typing.

    :param object val: A value to check
    :return: Is the object a valid PyNode?
    :rtype: bool
    """
    # In maya-2019, maya will crash when calling __melobject__ on an invalid PyNode/Attribute.
    # A workaround for now is to call __apimobject__() first.
    # Worst case it will raise a MayaAttributeError exception.
    try:
        val.__apimobject__()
    except Exception:
        return False

    try:
        mel = val.__melobject__()
    except Exception:
        return False

    return cmds.objExists(mel)


def distance_between_nodes(x, y):
    """
    Compute the distance between two nodes.

    :param x: A node
    :type x: pymel.PyNode
    :param y: Another node
    :type y: pymel.PyNode
    :return: The distance between two nodes.
    :rtype: float
    """
    ax, ay, az = x.getTranslation(space="world")
    bx, b, bz = y.getTranslation(space="world")
    return ((ax - bx) ** 2 + (ay - b) ** 2 + (az - bz) ** 2) ** 0.5


def distance_between_vectors(a, b):
    """
    Compute the distance between two vectors.
    src: http://darkvertex.com/wp/2010/06/05/python-distance-between-2-vectors/

    :param a: A vector
    :type a: pymel.datatypes.Vector
    :param b: Another vector
    :type b: pymel.datatypes.Vector
    :return: A distance
    :rtype: float
    """
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2) ** 0.5


def is_child_of(child, parent):
    """
    Check if a node is under another hierarchy.
    
    :param child: A node to check
    :param parent: A potential parent node
    :return: Is the node in the parent hierarchy?
    :rtype: bool
    """
    while child:
        if child == parent:
            return True
        child = child.getParent()
    return False


class PyNodeChain(list):
    """
    Array-like object for chain of PyNode.
    """

    # get the first pynode that have the attr
    def __getattr__(self, key):
        # _LOG.warning("Searching unknown attribute %s in %s", key, self)
        first_node = next(
            (node for node in self.__dict__["_list"] if hasattr(node, key)), None
        )
        if first_node is not None:
            return getattr(first_node, key)
        raise AttributeError

    # set all the pynodes that have the attr
    def __setattr__(self, key, value):
        for node in self:
            try:
                setattr(node, key, value)
            except Exception as e:
                _LOG.error(str(e))

    @property
    def start(self):
        """
        :return: The first node in the chain
        :rtype: pymel.PyNode or None
        """
        return next(iter(self), None)

    @property
    def end(self):
        """
        :return: The last node in the chain
        :rtype: pymel.PyNode or None
        """
        return self[-1] if len(self) > 0 else None

    @property
    def chain(self):
        return self

    def duplicate(self):
        new_chain = pymel.duplicate(list(self), renameChildren=True, parentOnly=True)
        return PyNodeChain(new_chain)

    def setParent(self, new_parent, **kwargs):
        for node in self:
            if node != new_parent and node.getParent() != new_parent:
                node.setParent(new_parent, **kwargs)

    # todo: convert to property?
    def length(self):
        """
        :return: The chain length
        :rtype: float
        """
        length = 0.0
        for i in range(len(self) - 1):
            head = self[i]
            tail = self[i + 1]
            length += distance_between_nodes(head, tail)
        return length


def duplicate_chain(chain):
    new_chain = pymel.duplicate(chain, renameChildren=True, parentOnly=True)
    return PyNodeChain(new_chain)


def get_num_parents(obj):
    num_parents = -1
    while obj is not None:
        obj = obj.getParent()
        num_parents += 1
    return num_parents


def get_chains_from_objs(objs):
    """
    Take an arbitraty collection of joints and sort them in hyerarchies.
    """
    chains = []
    objs = sorted(objs, key=get_num_parents)
    for obj in objs:
        parent = obj.getParent()
        if parent not in objs:
            chains.append([obj])
        else:
            for chain in chains:
                if parent in chain:
                    chain.append(obj)
    return [PyNodeChain(chain) for chain in chains]


def iter_parents(obj):
    while obj.getParent() is not None:
        obj = obj.getParent()
        yield obj


def get_parents(obj):
    return list(iter_parents(obj))


def get_common_parents(objs):
    """
    Return the first parent that all provided objects share.
    :param objs: A list of pymel.PyNode instances.
    :return: A pymel.PyNode instance.
    """
    parent_sets = set()
    for jnt in objs:
        parent_set = set(get_parents(jnt))
        if not parent_sets:
            parent_sets = parent_set
        else:
            parent_sets &= parent_set

    result = next(iter(reversed(sorted(parent_sets, key=get_num_parents))), None)
    if result and result in objs:
        result = result.getParent()
    return result


class Tree(object):
    __slots__ = ("val", "children", "parent")

    def __init__(self, val):
        self.val = val
        self.children = []
        self.parent = None

    def append(self, tree):
        self.children.append(tree)
        tree.parent = self

    def __repr__(self):
        return "<Tree %s>" % self.val


def get_tree_from_objs(objs):
    """
    Sort all provided objects in a tree fashion.
    Support missing objects between hierarchy.
    Note that tree root value will always be None, representing the root node.
    """
    dagpaths = sorted([obj.fullPath() for obj in objs])

    root = Tree(None)

    def dag_is_child_of(dag_parent, dag_child):
        return dag_child.startswith(dag_parent + "|")

    last_knot = root
    for dagpath in dagpaths:
        knot = Tree(dagpath)

        # Resolve the new knot parent
        p = last_knot
        while not (p.val is None or dag_is_child_of(p.val, dagpath)):
            p = p.parent
        p.append(knot)

        # Save the last knot, since we are iterating in alphabetical order,
        # we can assume that the next knot parent can be found using this knot.
        last_knot = knot

    return root


def ls(*args, **kwargs):
    return PyNodeChain(pymel.ls(*args, **kwargs))


# Wrapper for pymel.ls that return only objects without parents.
def ls_root(*args, **kwargs):
    # TODO: Better finding of the root joint
    return PyNodeChain(
        filter(
            lambda x: x.getParent() is None or type(x.getParent()) != pymel.nt.Joint,
            iter(pymel.ls(*args, **kwargs)),
        )
    )


def ls_root_anms(pattern="anm*", **kwargs):
    return ls_root(pattern, type="transform", **kwargs)


def ls_root_geos(pattern="geo*", **kwargs):
    return ls_root(pattern, type="transform", **kwargs)


def ls_root_rigs(pattern="rig*", **kwargs):
    return ls_root(pattern, type="transform", **kwargs)


def ls_root_jnts(pattern="jnt*", **kwargs):
    return ls_root(pattern, type="transform", **kwargs)


# Class check for transform PyNodes
def isinstance_of_transform(obj, cls=pymel.nodetypes.Transform):
    return isinstance(obj, cls)


# Class check for shape PyNodes
def isinstance_of_shape(obj, cls=pymel.nodetypes.Shape):
    if isinstance(obj, pymel.nodetypes.Transform):
        return any((shape for shape in obj.getShapes() if isinstance(shape, cls)))
    elif isinstance(obj, pymel.nodetypes.Shape):
        return isinstance(obj, cls)


def create_zero_grp(obj):
    zero_grp = pymel.createNode("transform")
    new_name = obj.name() + "_" + "zero_grp"
    zero_grp.rename(new_name)

    # Note: Removed for performance
    zero_grp.setMatrix(obj.getMatrix(worldSpace=True))

    parent = obj.getParent()
    if parent:
        zero_grp.setParent(parent)

    obj.setParent(zero_grp)

    return zero_grp


def zero_out_objs(objs):
    for o in objs:
        create_zero_grp(o)


class Segment(object):
    """
    In Maya there's no class to represent a segment.
    This is the pymel.datatypes.Segment I've always wanted.
    """

    def __init__(self, pos_s, pos_e):
        self.pos_s = pos_s
        self.pos_e = pos_e

    def closest_point(self, p):
        """
        http://stackoverflow.com/questions/3120357/get-closest-point-to-a-line
        """
        a = self.pos_s
        b = self.pos_e
        a_to_p = p - a
        a_to_b = b - a
        ab_length = a_to_b.length()
        ap_length = a_to_p.length()
        a_to_p_norm = a_to_p.normal()
        a_to_b_norm = a_to_b.normal()
        atp_dot_atb = a_to_p_norm * (a_to_b_norm)  # dot product
        dist_norm = atp_dot_atb * ap_length / ab_length
        return pymel.datatypes.Vector(
            a.x + a_to_b.x * dist_norm,
            a.y + a_to_b.y * dist_norm,
            a.z + a_to_b.z * dist_norm,
        )

    def closest_point_normalized_distance(self, p, epsilon=0.001):
        """
        Same things as .closest_point but only return the distance relative from the length of a to b.
        Available for optimisation purpose.
        """
        a = self.pos_s
        b = self.pos_e
        a_to_p = p - a
        a_to_b = b - a
        ab_length = a_to_b.length()
        ap_length = a_to_p.length()
        a_to_p_norm = a_to_p.normal()
        a_to_b_norm = a_to_b.normal()
        atp_dot_atb = a_to_p_norm * a_to_b_norm

        return (
            abs(atp_dot_atb * ap_length / ab_length)
            if abs(ab_length) > epsilon
            else 0.0
        )


class SegmentCollection(object):
    """
    A collection of single segments. Used for math computations.
    """

    def __init__(self, segments=None):
        """
        :param segments: A list of segments
        :type segments: list of Segment
        """
        self.segments = segments or []
        self.knots = [segment.pos_s for segment in self.segments]
        self.knots.append(self.segments[-1].pos_e)

    def closest_segment(self, pos):
        """
        Return the closest segment to a provided point.

        :param pos: A point vector
        :type pos: pymel.datatypes.Vector
        :return: The segment closest to the point
        :rtype: Segment
        """
        bound_min = -0.000000000001  # Damn float imprecision
        bound_max = 1.0000000000001  # Damn float imprecision
        num_segments = len(self.segments)
        for i, segment in enumerate(self.segments):
            distance_normalized = segment.closest_point_normalized_distance(pos)
            if bound_min <= distance_normalized <= bound_max:
                return segment, distance_normalized
            if i == 0 and distance_normalized < bound_min:  # Handle out-of-bound
                return segment, 0.0
            # Handle out-of-bound
            if i == (num_segments - 1) and distance_normalized > bound_max:
                return segment, 1.0
        raise Exception("Can't resolve segment for %s" % pos)

    def closest_segment_index(self, pos):
        closest_segment, ratio = self.closest_segment(pos)
        index = self.segments.index(closest_segment)
        return index, ratio

    def get_knot_weights(self, dropoff=1.0):
        num_knots = len(self.knots)
        knots_weights = []
        for i, knot in enumerate(self.knots):
            if i == 0:
                weights = [0] * num_knots
                weights[0] = 1.0
            elif i == (num_knots - 1):
                weights = [0] * num_knots
                weights[-1] = 1.0
            else:
                weights = []
                total_weight = 0.0
                for j in range(num_knots):
                    distance = abs(j - i)
                    weight = max(0, 1.0 - (distance / dropoff))
                    total_weight += weight
                    weights.append(weight)
                weights = [weight / total_weight for weight in weights]
            knots_weights.append(weights)
        return knots_weights

    @classmethod
    def from_transforms(cls, objs):
        segments = []
        num_objs = len(objs)
        for i in range(num_objs - 1):
            obj_s = objs[i]
            obj_e = objs[i + 1]
            mfn_transform_s = obj_s.__apimfn__()
            mfn_transform_e = obj_e.__apimfn__()
            pos_s = OpenMaya.MVector(
                mfn_transform_s.getTranslation(OpenMaya.MSpace.kWorld)
            )
            pos_e = OpenMaya.MVector(
                mfn_transform_e.getTranslation(OpenMaya.MSpace.kWorld)
            )
            segment = Segment(pos_s, pos_e)
            segments.append(segment)
        return cls(segments)

    @classmethod
    def from_positions(cls, positions):
        segments = []
        num_positions = len(positions)
        for i in range(num_positions - 1):
            pos_s = positions[i]
            pos_e = positions[i + 1]
            segment = Segment(pos_s, pos_e)
            segments.append(segment)
        return cls(segments)


def get_rotation_from_matrix(tm):
    """
    Bypass pymel bug
    see https://github.com/LumaPictures/pymel/issues/355
    """
    return pymel.datatypes.TransformationMatrix(tm).rotate


def makeIdentity_safe(
    obj, translate=False, rotate=False, scale=False, apply=False, **kwargs
):
    """
    Extended pymel.makeIdentity method that won't crash for idiotic reasons.
    """
    from . import libAttr

    affected_attrs = []

    # Ensure the shape don't have any extra transformation.
    if apply:
        if translate:
            libAttr.unlock_translation(obj)
            affected_attrs.extend(
                [obj.translate, obj.translateX, obj.translateY, obj.translateZ]
            )
        if rotate:
            libAttr.unlock_rotation(obj)
            affected_attrs.extend([obj.rotate, obj.rotateX, obj.rotateY, obj.rotateZ])
        if scale:
            libAttr.unlock_scale(obj)
            affected_attrs.extend([obj.scale, obj.scaleX, obj.scaleY, obj.scaleZ])

    # Make identify will fail if attributes are connected...
    with libAttr.context_disconnected_attrs(
        affected_attrs, hold_inputs=True, hold_outputs=False
    ):
        pymel.makeIdentity(
            obj, apply=apply, translate=translate, rotate=rotate, scale=scale, **kwargs
        )


def conform_to_pynode(value):
    """
    :param value: A value to conform
    :type value: str or pymel.PyNode
    :return:
    :rtype: pymel.PyNode
    """
    return pymel.PyNode(value) if isinstance(value, basestring) else value
    # return value if isinstance(value, pymel.PyNode) else pymel.PyNode(value)


def conform_to_pynode_list(value):
    """
    :param value:
    :type value: None or list[str] or list[pymel.PyNode]
    :return:
    :rtype: list[pymel.PyNode]
    """
    if value and not isinstance(value, list):
        raise IOError(
            "Unexpected type for argument input. Expected list, got %s. %s"
            % (type(value), value)
        )
    return [conform_to_pynode(entry) for entry in value] if value else []
