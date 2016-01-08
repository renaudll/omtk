import logging, collections
import pymel.core as pymel


#
# A PyNodeChain is a special pymel-related object that act exactly like a standard array.
# However it allow us to have more bells and whistles.
#

def is_valid_PyNode(val):
    return (val and hasattr(val, 'exists') and val.exists()) if val else None


def distance(x, y):
    """
    Return the distance between two pynodes.
    """
    ax, ay, az = x.getTranslation(space="world")
    bx, b, bz = y.getTranslation(space="world")
    return ((ax - bx) ** 2 + (ay - b) ** 2 + (az - bz) ** 2) ** 0.5


def is_child_of(node, potential_parent):
    while node:
        if node == potential_parent:
            return True
        node = node.getParent()
    return False


class PyNodeChain(collections.MutableSequence):
    """A container for manipulating lists of hosts"""

    def __init__(self, _list=None):
        self.__dict__['_list'] = _list if _list else []

    def __len__(self):
        return len(self._list)

    def __getitem__(self, ii):
        return self._list[ii]

    def __delitem__(self, ii):
        del self._list[ii]

    def __setitem__(self, ii, val):
        return self._list[ii]

    def __str__(self):
        return str(self._list)

    @property
    def start(self):
        return next(iter(self._list), None)

    @property
    def end(self):
        return self._list[-1] if len(self._list) > 0 else None

    @property
    def chain(self):
        return self._list

    def insert(self, ii, val):
        self._list.insert(ii, val)

    def setParent(self, new_parent, **kwargs):
        for node in self._list:
            if node != new_parent and node.getParent() != new_parent:
                node.setParent(new_parent, **kwargs)

    # todo: convert to property?
    def length(self):
        length = 0
        for i in range(len(self._list) - 1):
            head = self._list[i]
            tail = self._list[i + 1]
            length += distance(head, tail)
        return length

    # get the first pynode that have the attr
    def __getattr__(self, key):
        logging.warning("Searching unknow attribute {key} in {self}", key=key, self=self)
        first_node = next((node for node in self.__dict__['_list'] if hasattr(node, key)), None)
        if first_node is not None:
            return getattr(first_node, key)
        raise AttributeError

    # set all the pynodes that have the attr
    def __setattr__(self, key, value):
        for node in self:
            try:
                setattr(node, key, value)
            except Exception, e:
                logging.error(str(e))


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
    chains = []
    sorted(objs, key=get_num_parents)
    for obj in objs:
        parent = obj.getParent()
        if parent not in objs:
            chains.append([obj])
        else:
            for chain in chains:
                if parent in chain:
                    chain.append(obj)
    return [PyNodeChain(chain) for chain in chains]


#
# ls() reimplementations
#

def ls_ex(*args, **kwargs):
    return PyNodeChain(pymel.ls(*args, **kwargs))


# Wrapper for pymel.ls that return only objects without parents.
def ls_root(*args, **kwargs):
    return PyNodeChain(filter(lambda x: x.getParent() is None, iter(pymel.ls(*args, **kwargs))))


def ls_root_anms(**kwargs):
    return ls_root('anm*', type='transform', **kwargs)


def ls_root_geos(**kwargs):
    return ls_root('geo*', type='transform', **kwargs)


def ls_root_rigs(**kwargs):
    return ls_root('rig*', type='transform', **kwargs)


def ls_root_jnts(**kwargs):
    return ls_root('jnt*', type='transform', **kwargs)


#
# isinstance() reimplementation
#

# Class check for transform PyNodes
def isinstance_of_transform(obj, cls=pymel.nodetypes.Transform):
    return isinstance(obj, cls)


# Class check for shape PyNodes
def isinstance_of_shape(obj, cls=pymel.nodetypes.Shape):
    if isinstance(obj, pymel.nodetypes.Transform):
        return any((shape for shape in obj.getShapes() if isinstance(shape, cls)))
