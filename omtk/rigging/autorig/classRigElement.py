import collections

class RigElement(collections.MutableSequence):
    def __init__(self):
        self.aChildrens = []
	#
    # collections.MutableSequence overrides
    #
    def __getitem__(self, item):
        self.aChildrens.__getitem__(item)

    def __setitem__(self, index, value):
        self.aChildrens.__setitem__(index, value)

    def __delitem__(self, index):
        self.aChildrens.__delitem__(index)

    def __len__(self):
        return self.aChildrens.__len__()

    def insert(self, index, value):
        self.aChildrens.insert(index, value)
        value._parent = self # Store the parent for optimized network serialization (see libs.libSerialization)

    def __iter__(self):
        return iter(self.aChildrens)

    #
    #
    #

    def isBuilt(self):
        if any(o for o in self if o.isBuilt()):
            return True