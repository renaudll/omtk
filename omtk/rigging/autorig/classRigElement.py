import collections

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