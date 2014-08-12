import collections
import pymel.core as pymel
from omtk.libs import libPymel

class RigElement(collections.MutableSequence):
    def __init__(self):
        self.children = []
	#
    # collections.MutableSequence overrides
    #
    def __getitem__(self, item):
        self.children.__getitem__(item)

    def __setitem__(self, index, value):
        self.children.__setitem__(index, value)

    def __delitem__(self, index):
        self.children.__delitem__(index)

    def __len__(self):
        return self.children.__len__()

    def insert(self, index, value):
        self.children.insert(index, value)
        value._parent = self # Store the parent for optimized network serialization (see libs.libSerialization)

    def __iter__(self):
        return iter(self.children)

    #
    #
    #

    def isBuilt(self):
        for child in self:
            if child.isBuilt():
                return True
        return False

    def _clean_invalid_pynodes(self):
        fnCanDelete = lambda x: (isinstance(x, (pymel.PyNode, pymel.Attribute)) and not libPymel.is_valid_PyNode(x))
        for key, val in self.__dict__.iteritems():
            if fnCanDelete(val):
                setattr(self, key, None)
            elif isinstance(val, (list, set, tuple)):
                for i in reversed(range(len(val))):
                    if fnCanDelete(val[i]):
                        val.pop(i)
                if len(val) == 0:
                    setattr(self, key, None)

    def unbuild(self):
        # Remove any references to missing pynodes
        self._clean_invalid_pynodes()

