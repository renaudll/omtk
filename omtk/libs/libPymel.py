import logging
import pymel.core as pymel
#
# A PyNodeChain is a special pymel-related object that act exactly like a standard array.
# However it allow us to have more bells and whistles.
#
import collections
class PyNodeChain(collections.MutableSequence):
    """A container for manipulating lists of hosts"""
    def __init__(self, _list=[]):
        self._list = _list

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

    def insert(self, ii, val):
        self._list.insert(ii, val)

    def append(self, val):
        self.insert(len(self._list), val)

    ###

    def __getattr__(self, key):
        first_node = next((node for node in self if hasattr(node)), None)
        if first_node is not None:
            return getattr(first_node, key)
        raise AttributeError

    def __setattr__(self, key, value):
        for node in self:
            try:
                setattr(node, key, value)
            except Exception, e:
                logging.error(str(e))

#
# ls() reimplementations
#

def ls_ex(*args, **kwargs):
    return PyNodeChain(pymel.ls(*args, **kwargs))

# Wrapper for pymel.ls that return only objects without parents.
def ls_root(*args, **kwargs):
    return filter(lambda x:x.getParent() is None, iter(pymel.ls_ex(*args, **kwargs)))

def ls_root_geos(*args, **kwargs):
    return ls_root('geo*', *args, **kwargs)

def ls_root_rigs(*args, **kwargs):
    return ls_root('rig*', *args, **kwargs)

def ls_root_jnts(*args, **kwargs):
    return ls_root('jnt*', *args, **kwargs)

def ls_root_geos(*args, **kwargs):
    return ls_root('geo*', *args, **kwargs)

