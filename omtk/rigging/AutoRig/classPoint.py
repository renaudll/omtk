import pymel.core as pymel
from classRigNode import RigNode
from rigFK import FK

'''
This class is a pymel.PyNode wrapper that extent it's functionnality.
Note: We can't directly inherit from pymel.PyNode.
'''

def enum(**enums):
    return type('Enum', (), enums)

class BaseHelper(RigNode):
    def __deleteNode__(self):
        pymel.delete(self.node)

    def __build__(self):
        raise NotImplementedError

    def __update__(self):
        self.__deleteNode__()
        self.__createNode__()
        self.rig = self.__build__()

class HelperPoint(BaseHelper):
    def __createNode__(self, *args, **kwargs):
        return pymel.joint(*args, **kwargs)

    def __build__(self):
        rig = FK([self.node])
        rig.Build()
        return rig

class HelperDeformer(BaseHelper):
    def __init__(self, _numJnts, *args, **kwargs):
        self.setNumJnts(_numJnts)

    def __createNode__(self, *args, **kwargs):
        offset = pymel.datatypes.Vector(0, 1, 0)
        return [pymel.joint(pos=offset * i) for i in self.numJnts]

    def __build__(self):
        rig = FK(self.node)
        rig.Build()
        return rig

    def setNumJnts(self, _numJnts, *args, **kwargs):
        self.numJnts = _numJnts
        self.__update__()

