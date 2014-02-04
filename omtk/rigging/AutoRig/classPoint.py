import pymel.core as pymel
from classRigNode import RigNode
from rigFK import FK
from omtk.libs import libRigging

'''
This class is a pymel.PyNode wrapper that extent it's functionnality.
Note: We can't directly inherit from pymel.PyNode.
'''

def enum(**enums):
    return type('Enum', (), enums)

def BackupAttr(_att):
    attInput = next(iter(_att.inputs(plugs=True)), None)
    if attInput is not None:
        return attInput
    else:
        return _att.get()

def RestoreAttr(_attOld, _attNew):
    if isinstance(_attOld, pymel.general.Attribute):
        return _attOld
    else:
        return _attNew


'''
HelperPoint represent the smallest unit of deformation in a rig.
'''
class HelperPoint(RigNode):
    def __createNode__(self, *args, **kwargs):
        return pymel.joint(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(HelperPoint, self).__init__(*args, **kwargs)

    def __deleteNode__(self):
        # Backup keyable attributes connections
        for att in self.node.listAttr(keyable=True):
            setattr(self, att.shortName(), BackupAttr(att))

'''
class NurbsPlane(RigNode):
    def __createNode__(self, **kwargs):
        return next(iter(pymel.nurbsPlane(**kwargs)), None)
'''

'''
A follice is constrained to the surface of a nurbsSurface. (see NurbsPlane class)
'''
class Follicle(RigNode):
    def __init__(self, _parent, *args, **kwargs):
        assert(isinstance(_parent, pymel.nodetypes.NurbsSurface))

        super(Follicle, self).__init__(*args, **kwargs)

        # Get uvInit
        u = libRigging.CreateUtilityNode('closestPointOnSurface',
            inPosition=self.node.getTranslation(space='world'),
            inputSurface=_parent.worldSpace)
        uInit = u.parameterU.get()
        vInit = u.parameterV.get()
        pymel.delete(u)
        
        # Normalize uvInit
        oPlaneShape = _parent.getShape()
        assert(isinstance(oPlaneShape, pymel.nodetypes.NurbsSurface))
        fMinU, fMaxU = oPlaneShape.minMaxURange()
        fMinV, fMaxV = oPlaneShape.minMaxVRange()
        uInit = (uInit - fMinU) / (fMaxU - fMaxV)
        vInit = (vInit - fMinV) / (fMaxV - fMaxV)

    def __createNode__(self, *args, **kwargs):
        return pymel.createNode('follicleShape')

######

class BaseHelper(RigNode):
    def __deleteNode__(self):
        pymel.delete(self.node)

    def __build__(self):
        raise NotImplementedError

    def __update__(self):
        self.__deleteNode__()
        self.__createNode__()
        self.rig = self.__build__()

class ChainDeformer(BaseHelper):
    def __init__(self, _numJnts, *args, **kwargs):
        self.setNumJnts(_numJnts)
        super(ChainDeformer, self).__init__(*args, **kwargs)

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

